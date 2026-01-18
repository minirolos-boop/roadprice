# monitor.py
# Collector + KPIs + persistance SQLite (auto-migration de schéma)
# + Récupération des TOURS (départs par date)
# + DOUBLE CHECK: Récupération du détail d'un tour par destination pour "whatsIncluded" (Lits partagés)
# + Extraction du MoneyPot, MaxPax corrigé, Private Room Free.

import os
import re
import json
import time
import html as ihtml
import sqlite3
import argparse
import logging
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

API_TRAVELS       = "https://api-catalog.weroad.fr/travels"
API_TOURS         = "https://api-catalog.weroad.fr/travels/{slug}/tours"
API_TOUR_DETAIL   = "https://api-catalog.weroad.fr/travels/{slug}/tours/{tour_id}" # NOUVEAU ENDPOINT
API_TRAVEL_DETAIL = "https://api-catalog.weroad.fr/travels/{slug}"

DEFAULT_TIMEOUT = 45
DEFAULT_RETRIES = 4
DEFAULT_BACKOFF = 0.8  # seconds, exponential


# -------------------- Utils --------------------
def g(d, path, default=None):
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def num(x):
    return x if isinstance(x, (int, float)) else None


def to_month(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").strftime("%Y-%m")
    except Exception:
        try:
            return pd.to_datetime(s).strftime("%Y-%m")
        except Exception:
            return None


def _session():
    s = requests.Session()
    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "weroad-monitor/1.1 (+analytics)",
        "accept-language": "fr-FR,fr;q=0.9,en;q=0.8",
        "connection": "keep-alive",
    }
    token = os.getenv("WEROAD_TOKEN")
    if token:
        headers["authorization"] = f"Bearer {token}"
    s.headers.update(headers)
    return s


def _get_json(url: str, params: Optional[Dict[str, Any]] = None,
              timeout: int = DEFAULT_TIMEOUT,
              retries: int = DEFAULT_RETRIES) -> Any:
    last_exc = None
    with _session() as s:
        for attempt in range(retries + 1):
            try:
                r = s.get(url, params=params, timeout=timeout)
                if r.status_code in (429, 500, 502, 503, 504):
                    raise requests.HTTPError(f"{r.status_code} {r.reason}")
                r.raise_for_status()
                return r.json()
            except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as e:
                last_exc = e
                sleep = (DEFAULT_BACKOFF * (2 ** attempt))
                logging.warning("GET %s failed (attempt %d/%d): %s; retrying in %.2fs",
                                url, attempt + 1, retries + 1, e, sleep)
                time.sleep(sleep)
    raise last_exc  # type: ignore[misc]


# -------------------- MoneyPot extraction --------------------
_MONEYPOT_NUM_RE = re.compile(
    r"""
    (?P<a>\d{1,3}(?:[ . \u00A0]\d{3})*(?:[,.]\d+)?)     # premier nombre
    (?:\s*(?:-|–|à|a|to|en|aux|and|et)\s* (?P<b>\d{1,3}(?:[ . \u00A0]\d{3})*(?:[,.]\d+)?)
    )?
    \s*(?:€|eur(?:o|os)?)                               # € / euro(s)
    """,
    re.IGNORECASE | re.VERBOSE,
)

def _to_float_eur(s: str) -> Optional[float]:
    if s is None:
        return None
    s = s.replace("\u00A0", " ")
    s = s.replace(".", "")
    s = s.replace(" ", "")
    s = s.replace(",", ".")
    try:
        return float(s)
    except Exception:
        return None

def parse_money_pot(description_html: str) -> Tuple[Optional[float], Optional[float], str]:
    if not description_html:
        return None, None, ""
    txt = ihtml.unescape(description_html)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()

    m = _MONEYPOT_NUM_RE.search(txt)
    if not m:
        alt = re.search(r"(\d[\d . \u00A0,]*)\s*(?:€|eur(?:o|os)?)", txt, flags=re.IGNORECASE)
        if not alt:
            if "pot commun" in txt.lower():
                alt2 = re.search(r"(\d{2,5})(?!\s?%)", txt)
                if alt2:
                    a2 = _to_float_eur(alt2.group(1))
                    return a2, a2, txt
            return None, None, txt
        a = _to_float_eur(alt.group(1))
        return a, a, txt

    a = _to_float_eur(m.group("a"))
    b = _to_float_eur(m.group("b")) if m.group("b") else None
    if a is not None and b is not None:
        lo, hi = (min(a, b), max(a, b))
    elif a is not None:
        lo = hi = a
    else:
        lo = hi = None
    return lo, hi, txt

def _deep_find_money_pot(node):
    stack = [node]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            if "moneyPot" in cur and isinstance(cur["moneyPot"], dict):
                return cur["moneyPot"]
            for k, v in cur.items():
                if k == "description" and isinstance(v, str) and re.search(r"(€|eur(?:o|os)?)", v, re.I):
                    return {"description": v}
                stack.append(v)
        elif isinstance(cur, list):
            stack.extend(cur)
    return None

def _collect_descriptions(node) -> list[str]:
    out = []
    stack = [node]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            for k, v in cur.items():
                if isinstance(v, str) and k.lower() in ("description", "money_pot_description", "content", "body", "info"):
                    out.append(v)
                stack.append(v)
        elif isinstance(cur, list):
            stack.extend(cur)
    return out

def extract_money_pot_from_travel_json(payload: dict) -> tuple[float | None, float | None, str]:
    root = payload if isinstance(payload, dict) else {}
    try:
        travel = root.get("data", {}).get("travel", {})
        mp = travel.get("moneyPot")
        if isinstance(mp, dict):
            desc = mp.get("description")
            if isinstance(desc, str) and desc.strip():
                mn, mx, raw = parse_money_pot(desc)
                return mn, mx, raw
    except Exception:
        pass
    mp2 = _deep_find_money_pot(root)
    if isinstance(mp2, dict) and isinstance(mp2.get("description"), str):
        mn, mx, raw = parse_money_pot(mp2["description"])
        return mn, mx, raw
    for cand in _collect_descriptions(root):
        if re.search(r"(€|eur(?:o|os)?)", cand, re.I) or "pot commun" in cand.lower():
            mn, mx, raw = parse_money_pot(cand)
            return mn, mx, raw
    return None, None, ""

def fetch_travel_detail(slug: str) -> dict:
    base = API_TRAVEL_DETAIL.format(slug=slug)
    candidates = [base, base + "?market=FR", base + "?lang=fr-FR"]
    for url in candidates:
        try:
            data = _get_json(url)
            if isinstance(data, dict) and data:
                return data
        except Exception as e:
            logging.debug("fetch_travel_detail: %s failed: %s", url, e)
    return {}


def enrich_with_money_pot(df_travels: pd.DataFrame, max_workers: int = 12) -> pd.DataFrame:
    out = df_travels.copy()
    for c in ("money_pot_min_eur", "money_pot_max_eur", "money_pot_raw", "money_pot_med_eur", "total_price_eur"):
        if c not in out.columns:
            out[c] = None

    if out.empty or "slug" not in out.columns:
        return out

    slugs = out["slug"].dropna().astype(str).unique().tolist()
    if not slugs:
        return out

    def _job(slug: str):
        try:
            data = fetch_travel_detail(slug)
            mn, mx, raw = extract_money_pot_from_travel_json(data)
            return slug, mn, mx, raw
        except Exception as e:
            return slug, None, None, None

    results: Dict[str, Tuple[Optional[float], Optional[float], Optional[str]]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(_job, slug): slug for slug in slugs}
        for fut in as_completed(futs):
            slug, mn, mx, raw = fut.result()
            results[slug] = (mn, mx, raw)

    out["money_pot_min_eur"] = out["slug"].map(lambda s: results.get(s, (None, None, None))[0])
    out["money_pot_max_eur"] = out["slug"].map(lambda s: results.get(s, (None, None, None))[1])
    out["money_pot_raw"]     = out["slug"].map(lambda s: results.get(s, (None, None, None))[2] or "")
    out["money_pot_med_eur"] = out[["money_pot_min_eur", "money_pot_max_eur"]].mean(axis=1, skipna=True)
    out["total_price_eur"]   = out["price_eur"].astype(float).fillna(0) + out["money_pot_med_eur"].astype(float).fillna(0)

    found = int(out["money_pot_min_eur"].notna().sum())
    total = int(out["slug"].notna().sum())
    logging.info("MoneyPot détecté pour %d/%d voyages (%.1f%%)", found, total, 100.0 * found / max(total, 1))

    return out


# -------------------- Fetch + normalize --------------------
def fetch_travels():
    data = _get_json(API_TRAVELS)
    items = data.get("data", data) or []
    return items if isinstance(items, list) else []


def normalize_travels(travels):
    rows = []
    for t in travels:
        bt = t.get("bestTour") or {}
        price = num(g(bt, ["price", "EUR"]))
        base  = num(g(bt, ["basePrice", "EUR"]))

        disc_val = disc_pct = None
        if price is not None and base is not None and base > price:
            disc_val = base - price
            disc_pct = round((base - price) / base * 100, 1)

        if price is None and base is None:
            min_p = max_p = None
        elif price is None:
            min_p = max_p = base
        elif base is None:
            min_p = max_p = price
        else:
            min_p = min(price, base)
            max_p = max(price, base)

        slug = t.get("slug")
        dest_url = f"https://www.weroad.fr/destinations/{slug}" if slug else None

        rows.append(
            {
                "id": t.get("id"),
                "slug": slug,
                "url": dest_url,
                "title": t.get("title") or t.get("destinationLabel") or slug,
                "destination_label": t.get("destinationLabel"),
                "country_name": g(t, ["primaryDestination", "name"]),
                "continent": g(t, ["primaryDestination", "primaryContinent", "name"]),
                "status": t.get("status"),
                "isBookable": t.get("isBookable"),
                "days": t.get("numberOfDays"),
                "style": g(t, ["travelStyle", "displayName"]),
                "types": ", ".join([x.get("displayName") for x in t.get("travelTypes", []) if x.get("displayName")]),
                "price_eur": price,
                "base_price_eur": base,
                "discount_value_eur": disc_val,
                "discount_pct": disc_pct,
                "sales_status": g(bt, ["salesStatus"]),
                "seatsToConfirm": g(bt, ["seatsToConfirm"]),
                "maxPax": g(bt, ["maxPax"]),
                "weroadersCount": g(bt, ["groupInfo", "weroadersCount"]),
                "min_price_eur": min_p,
                "max_price_eur": max_p,
                "best_starting_date": g(bt, ["startingDate"]),
                "best_ending_date": g(bt, ["endingDate"]),
                "rating": g(t, ["userRating", "rating"]),
                "rating_count": g(t, ["userRating", "count"]),
            }
        )

    df = pd.DataFrame(rows)
    df["month"] = df["best_starting_date"].map(to_month)
    if not df.empty and "sales_status" in df.columns:
        df = df[df["sales_status"].astype(str).str.strip().ne("")]
        df = df.dropna(subset=["sales_status"])
    return df


def fetch_tours_for_slug(slug: str) -> list[dict]:
    url = API_TOURS.format(slug=slug)
    data = _get_json(url)
    items = data.get("data", data) or []
    return items if isinstance(items, list) else []


def normalize_tours(travels: list[dict], max_workers: int = 12) -> pd.DataFrame:
    """
    Récupère /travels/{slug}/tours en parallèle.
    Enrichi avec :
    - Private Room Free (Booking Pillars)
    - Shared Bed detection (VIA UN APPEL DÉTAILLÉ SUPPLEMENTAIRE PAR SLUG)
    - Correction MaxPax
    """
    slugs = [t.get("slug") for t in travels if t.get("slug")]
    slugs = list(dict.fromkeys(slugs))  # uniques

    rows = []

    # Mots-clés pour détection lits partagés
    # On reste large pour attraper "chambre quadruple" ou "lits doubles"
    BED_KEYWORDS = [
        "à partager",
        "queen size",
        "queen-size",
        "chambre quadruple",
        "2 lits doubles",
        "lits doubles"
    ]

    def _fetch_slug_with_detail(slug: str):
        """
        Récupère la liste des tours, PUIS récupère le détail du PREMIER tour
        pour analyser 'whatsIncluded' (lits partagés), car cette info
        n'est PAS dans la liste.
        """
        try:
            # 1. Liste des tours
            tours = fetch_tours_for_slug(slug)
            
            # 2. Analyse détaillée (Shared Bed) sur le premier tour disponible
            shared_bed_detected = 0
            if tours:
                # On prend le premier tour comme échantillon pour la destination
                sample_id = tours[0].get("id")
                if sample_id:
                    try:
                        detail_url = API_TOUR_DETAIL.format(slug=slug, tour_id=sample_id)
                        detail_data = _get_json(detail_url)
                        
                        # Analyse whatsIncluded dans le détail
                        whats_included = detail_data.get("data", detail_data).get("whatsIncluded") or []
                        for item in whats_included:
                            raw_desc = item.get("description")
                            if isinstance(raw_desc, str):
                                # NETTOYAGE HTML IMPORTANT ICI
                                clean_txt = ihtml.unescape(raw_desc)
                                clean_txt = re.sub(r"<[^>]+>", " ", clean_txt) # Enleve les balises
                                clean_txt = re.sub(r"\s+", " ", clean_txt).strip().lower()
                                
                                for kw in BED_KEYWORDS:
                                    if kw in clean_txt:
                                        shared_bed_detected = 1
                                        logging.info(f"🚨 LIT PARTAGÉ [{slug}] via détail : '{kw}' trouvé dans '{clean_txt[:30]}...'")
                                        break
                                if shared_bed_detected: break
                    except Exception as e:
                        logging.warning(f"Detail fetch failed for {slug}/{sample_id}: {e}")

            return slug, tours, shared_bed_detected
        except Exception as e:
            logging.warning("fetch_tours_for_slug(%s) failed: %s", slug, e)
            return slug, [], 0

    if not slugs:
        return pd.DataFrame()

    results: Dict[str, Tuple[list[dict], int]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(_fetch_slug_with_detail, slug): slug for slug in slugs}
        for fut in as_completed(futs):
            slug, tours, shared_flag = fut.result()
            results[slug] = (tours, shared_flag)

    for t in travels:
        slug = t.get("slug")
        if not slug:
            continue
        
        tours, shared_bed_flag = results.get(slug, ([], 0))
        
        for tour in tours:
            tour_id = tour.get("id")
            price   = num(g(tour, ["price", "EUR"]))
            base    = num(g(tour, ["basePrice", "EUR"]))

            disc_val = disc_pct = None
            if price is not None and base is not None and base > price:
                disc_val = base - price
                disc_pct = round((base - price) / base * 100, 1)

            url_dest    = f"https://www.weroad.fr/destinations/{slug}"
            url_precise = f"{url_dest}/{tour_id}" if tour_id else url_dest

            # Info groupe
            max_pax = g(tour, ["maxPax"]) or g(tour, ["groupInfo", "expectedGroupSizeCount"])

            rows.append(
                {
                    "tour_id": tour_id,
                    "slug": slug,
                    "title": t.get("title") or t.get("destinationLabel") or slug,
                    "destination_label": t.get("destinationLabel"),
                    "country_name": g(t, ["primaryDestination", "name"]),
                    "starting_date": g(tour, ["startingDate"]),
                    "ending_date": g(tour, ["endingDate"]),
                    "price_eur": price,
                    "base_price_eur": base,
                    "discount_value_eur": disc_val,
                    "discount_pct": disc_pct,
                    "sales_status": g(tour, ["salesStatus"]),
                    "seatsToConfirm": g(tour, ["seatsToConfirm"]),
                    "maxPax": max_pax,
                    "weroadersCount": g(tour, ["groupInfo", "weroadersCount"]),
                    
                    # NOUVEAUX CHAMPS
                    "private_room_free": g(tour, ["bookingPillars", "privateRoomForFree"]),
                    # On applique le flag détecté sur le détail du premier tour à tous les tours
                    "shared_bed": shared_bed_flag,
                    
                    "url": url_dest,
                    "url_precise": url_precise,
                }
            )

    df = pd.DataFrame(rows)
    if not df.empty and "sales_status" in df.columns:
        df = df[df["sales_status"].astype(str).str.strip().ne("")]
        df = df.dropna(subset=["sales_status"])
    if "tour_id" in df.columns:
        df = df.drop_duplicates(subset=["tour_id"])
    return df


# -------------------- Analyses --------------------
def weekly_kpis(df: pd.DataFrame) -> dict:
    out = {}
    for c in ["price_eur", "base_price_eur", "discount_value_eur", "discount_pct", "total_price_eur"]:
        series = df[c] if c in df else pd.Series(dtype=float)
        series = series.dropna()
        out[f"{c}_min"] = float(series.min()) if not series.empty else None
        out[f"{c}_max"] = float(series.max()) if not series.empty else None
        out[f"{c}_avg"] = float(series.mean()) if not series.empty else None
        out[f"{c}_med"] = float(series.median()) if not series.empty else None

    out["count_total"] = int(len(df))
    out["count_promos"] = int(df["discount_pct"].notna().sum()) if "discount_pct" in df.columns else 0
    out["promo_share_pct"] = round(100 * out["count_promos"] / out["count_total"], 1) if out["count_total"] else 0.0

    s = df["month"].dropna() if "month" in df.columns else pd.Series([], dtype=object)
    depart_by_month = s.value_counts().sort_index().to_dict()
    out["depart_by_month"] = json.dumps(depart_by_month, ensure_ascii=False)
    return out


def cheapest_by_destination(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=["destination_label", "price_eur"]).copy()
    if base.empty:
        idx = pd.Index([], name="destination_label")
        return pd.DataFrame(columns=["title", "country_name", "price_eur", "url"]).set_index(idx)
    idxmin = base.groupby("destination_label")["price_eur"].idxmin()
    return (
        base.loc[idxmin, ["destination_label", "title", "country_name", "price_eur", "url"]]
        .set_index("destination_label")
    )


def weekly_diff(df_curr: pd.DataFrame, df_prev: pd.DataFrame | None) -> pd.DataFrame:
    L = cheapest_by_destination(df_curr)
    R = cheapest_by_destination(df_prev) if df_prev is not None and not df_prev.empty else L.iloc[0:0]
    diff = L.join(R, how="left", lsuffix="_curr", rsuffix="_prev")

    diff["delta_abs"] = diff["price_eur_curr"] - diff["price_eur_prev"]
    den = diff["price_eur_prev"].replace({0: np.nan})
    diff["delta_pct"] = diff["delta_abs"] / den
    diff.replace([np.inf, -np.inf], np.nan, inplace=True)

    diff["movement"] = diff["delta_abs"].apply(
        lambda v: "↓" if (pd.notna(v) and v < 0) else ("↑" if (pd.notna(v) and v > 0) else "=")
    )

    out = diff.reset_index()
    if "url_curr" in out.columns:
        out["url"] = out["url_curr"]
    elif "url_prev" in out.columns:
        out["url"] = out["url_prev"]
    keep = [
        "destination_label", "title_curr", "country_name_curr",
        "price_eur_prev", "price_eur_curr", "delta_abs", "delta_pct",
        "movement", "url"
    ]
    cols = [c for c in keep if c in out.columns]
    return out[cols].copy()


def same_date_diff(df_tours_curr: pd.DataFrame, df_tours_prev: pd.DataFrame, money_map: pd.DataFrame) -> pd.DataFrame:
    if df_tours_curr.empty or df_tours_prev.empty:
        return pd.DataFrame()

    L = df_tours_curr.set_index("tour_id")
    R = df_tours_prev.set_index("tour_id")

    common_ids = L.index.intersection(R.index)
    if common_ids.empty:
        return pd.DataFrame()

    left  = L.loc[common_ids]
    right = R.loc[common_ids]

    out = pd.DataFrame({
        "tour_id": common_ids,
        "slug": left.get("slug"),
        "destination_label": left.get("destination_label"),
        "title": left.get("title"),
        "starting_date": left.get("starting_date"),
        "url_precise": left.get("url_precise"),
        "price_eur_prev": right.get("price_eur"),
        "price_eur_curr": left.get("price_eur"),
    }).reset_index(drop=True)

    # inject money pot median per slug
    mp = money_map[["slug", "money_pot_med_eur"]].drop_duplicates()
    out = out.merge(mp, on="slug", how="left", suffixes=("", "_mp"))
    out.rename(columns={"money_pot_med_eur": "money_pot_med_eur_slug"}, inplace=True)

    out["total_price_prev"] = out["price_eur_prev"].astype(float).fillna(0) + out["money_pot_med_eur_slug"].astype(float).fillna(0)
    out["total_price_curr"] = out["price_eur_curr"].astype(float).fillna(0) + out["money_pot_med_eur_slug"].astype(float).fillna(0)

    out["delta_abs"] = out["price_eur_curr"] - out["price_eur_prev"]
    den = out["price_eur_prev"].replace({0: np.nan})
    out["delta_pct"] = out["delta_abs"] / den
    out.replace([np.inf, -np.inf], np.nan, inplace=True)
    out["movement"] = out["delta_abs"].apply(
        lambda v: "↓" if (pd.notna(v) and v < 0) else ("↑" if (pd.notna(v) and v > 0) else "=")
    )
    return out


# -------------------- Export --------------------
def _to_excel_sorted(df: pd.DataFrame, writer, sheet_name: str, by=None, ascending=None):
    out = df.copy()
    try:
        if by:
            cols = by if isinstance(by, (list, tuple)) else [by]
            if all(c in out.columns for c in cols):
                out = out.sort_values(by=cols, ascending=ascending if ascending is not None else True)
    except Exception:
        pass
    out.to_excel(writer, index=False, sheet_name=sheet_name)


def export_excel(
    df_curr: pd.DataFrame,
    wk_kpis: dict,
    wk_diff: pd.DataFrame,
    mo_kpis: pd.DataFrame,
    mo_diff: pd.DataFrame,
    alerts: pd.DataFrame,
    df_tours: pd.DataFrame,
    same_d: pd.DataFrame,
    out="weekly_report.xlsx",
):
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        df_curr.to_excel(w, index=False, sheet_name="Voyages_Week")
        pd.DataFrame([wk_kpis]).to_excel(w, index=False, sheet_name="Weekly_KPIs")
        _to_excel_sorted(wk_diff, w, "Weekly_Diff", by=["delta_pct", "delta_abs"], ascending=[False, False])
        alerts.to_excel(w, index=False, sheet_name="Alerts")
        mo_kpis.to_excel(w, index=False, sheet_name="Monthly_KPIs")
        mo_diff.to_excel(w, index=False, sheet_name="Monthly_Diff")
        df_tours.to_excel(w, index=False, sheet_name="Tours")
        _to_excel_sorted(same_d, w, "Same_Date_Diff", by=["delta_pct", "delta_abs"], ascending=[False, False])
    logging.info("Exporté: %s", out)


# ---------- SQLite helpers: creation + migration ----------
def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    cur = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1", (name,)
    )
    return cur.fetchone() is not None

def add_missing_columns(conn: sqlite3.Connection, table: str, columns_sql: Dict[str, str]):
    if not table_exists(conn, table):
        return
    cur = conn.execute(f'PRAGMA table_info("{table}")')
    existing = {row[1] for row in cur.fetchall()}
    for col, typ in columns_sql.items():
        if col not in existing:
            conn.execute(f'ALTER TABLE "{table}" ADD COLUMN "{col}" {typ}')
    conn.commit()

def ensure_all_tables(conn: sqlite3.Connection):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS snapshots (
      run_ts TEXT, id TEXT, slug TEXT, url TEXT, title TEXT, destination_label TEXT,
      country_name TEXT, continent TEXT, status TEXT, isBookable INTEGER, days INTEGER,
      style TEXT, types TEXT, price_eur REAL, base_price_eur REAL, discount_value_eur REAL,
      discount_pct REAL, sales_status TEXT, seatsToConfirm INTEGER, maxPax INTEGER,
      weroadersCount INTEGER, min_price_eur REAL, max_price_eur REAL, best_starting_date TEXT,
      best_ending_date TEXT, rating REAL, rating_count INTEGER, month TEXT,
      money_pot_min_eur REAL, money_pot_max_eur REAL, money_pot_med_eur REAL,
      total_price_eur REAL, money_pot_raw TEXT
    );
    CREATE TABLE IF NOT EXISTS weekly_kpis (
      run_ts TEXT, price_eur_min REAL, price_eur_max REAL, price_eur_avg REAL, price_eur_med REAL,
      base_price_eur_min REAL, base_price_eur_max REAL, base_price_eur_avg REAL, base_price_eur_med REAL,
      discount_value_eur_min REAL, discount_value_eur_max REAL, discount_value_eur_avg REAL, discount_value_eur_med REAL,
      discount_pct_min REAL, discount_pct_max REAL, discount_pct_avg REAL, discount_pct_med REAL,
      total_price_eur_min REAL, total_price_eur_max REAL, total_price_eur_avg REAL, total_price_eur_med REAL,
      count_total INTEGER, count_promos INTEGER, promo_share_pct REAL, depart_by_month TEXT
    );
    CREATE TABLE IF NOT EXISTS weekly_diff (
      run_ts TEXT, destination_label TEXT, title_curr TEXT, country_name_curr TEXT,
      price_eur_prev REAL, price_eur_curr REAL, delta_abs REAL, delta_pct REAL,
      movement TEXT, url TEXT, flag INTEGER
    );
    CREATE TABLE IF NOT EXISTS monthly_kpis (
      run_ts TEXT, month TEXT, destination_label TEXT, prix_min REAL, prix_avg REAL, nb_depart INTEGER,
      prix_min_prev REAL, prix_avg_prev REAL, nb_depart_prev REAL, delta_prix_min REAL,
      delta_prix_avg REAL, delta_nb_depart REAL, delta_prix_min_pct REAL, delta_prix_avg_pct REAL
    );
    CREATE TABLE IF NOT EXISTS monthly_diff (
      run_ts TEXT, month TEXT, destination_label TEXT, prix_min REAL, prix_avg REAL, nb_depart INTEGER,
      prix_min_prev REAL, prix_avg_prev REAL, nb_depart_prev REAL, delta_prix_min REAL,
      delta_prix_avg REAL, delta_nb_depart REAL, delta_prix_min_pct REAL, delta_prix_avg_pct REAL
    );
    CREATE TABLE IF NOT EXISTS alerts (
      run_ts TEXT, destination_label TEXT, title_curr TEXT, country_name_curr TEXT,
      price_eur_prev REAL, price_eur_curr REAL, delta_abs REAL, delta_pct REAL,
      movement TEXT, url TEXT, flag INTEGER
    );
    CREATE TABLE IF NOT EXISTS tours (
      run_ts TEXT, tour_id TEXT, slug TEXT, title TEXT, destination_label TEXT, country_name TEXT,
      starting_date TEXT, ending_date TEXT, price_eur REAL, base_price_eur REAL,
      discount_value_eur REAL, discount_pct REAL, sales_status TEXT, seatsToConfirm INTEGER,
      maxPax INTEGER, weroadersCount INTEGER, private_room_free INTEGER, shared_bed INTEGER,
      url TEXT, url_precise TEXT
    );
    CREATE TABLE IF NOT EXISTS same_date_diff (
      run_ts TEXT, tour_id TEXT, slug TEXT, destination_label TEXT, title TEXT, starting_date TEXT,
      url_precise TEXT, price_eur_prev REAL, price_eur_curr REAL, money_pot_med_eur_slug REAL,
      total_price_prev REAL, total_price_curr REAL, delta_abs REAL, delta_pct REAL, movement TEXT
    );
    """)
    conn.commit()

    try:
        conn.execute("CREATE INDEX IF NOT EXISTS idx_snapshots_run_ts ON snapshots(run_ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_snapshots_dest ON snapshots(destination_label)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_snapshots_dest_run ON snapshots(destination_label, run_ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_weekly_diff_run_ts ON weekly_diff(run_ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_weekly_diff_dest ON weekly_diff(destination_label)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_weekly_kpis_run_ts ON weekly_kpis(run_ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_monthly_kpis_run_ts ON monthly_kpis(run_ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_monthly_diff_run_ts ON monthly_diff(run_ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_alerts_run_ts ON alerts(run_ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_tours_run_ts ON tours(run_ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_tours_tour_id ON tours(tour_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_tours_slug_start ON tours(slug, starting_date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_same_date_diff_run_ts ON same_date_diff(run_ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_same_date_diff_tour_id ON same_date_diff(tour_id)")
        conn.commit()
    except Exception as e:
        logging.warning("ensure indexes: %s", e)


def persist_sqlite(
    df_curr: pd.DataFrame,
    wk_kpis: dict,
    wk_diff: pd.DataFrame,
    mo_kpis: pd.DataFrame,
    mo_diff: pd.DataFrame,
    alerts: pd.DataFrame,
    df_tours: pd.DataFrame,
    same_d: pd.DataFrame,
    db_path: str,
    run_ts: str,
):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        try:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute("PRAGMA foreign_keys=ON;")
        except Exception:
            pass

        ensure_all_tables(conn)

        df_snap = df_curr.copy()
        df_snap["run_ts"] = run_ts
        df_snap.to_sql("snapshots", conn, if_exists="append", index=False)

        wk_k_df = pd.DataFrame([{**wk_kpis, "run_ts": run_ts}])
        wk_k_df.to_sql("weekly_kpis", conn, if_exists="append", index=False)

        wk_diff2 = wk_diff.copy()
        wk_diff2["run_ts"] = run_ts
        add_missing_columns(conn, "weekly_diff", {"flag": "INTEGER"})
        wk_diff2.to_sql("weekly_diff", conn, if_exists="append", index=False)

        mo_k_df = mo_kpis.copy()
        mo_k_df["run_ts"] = run_ts
        mo_k_df.to_sql("monthly_kpis", conn, if_exists="append", index=False)

        mo_diff2 = mo_diff.copy()
        mo_diff2["run_ts"] = run_ts
        mo_diff2.to_sql("monthly_diff", conn, if_exists="append", index=False)

        alerts2 = alerts.copy()
        alerts2["run_ts"] = run_ts
        add_missing_columns(conn, "alerts", {"flag": "INTEGER"})
        alerts2.to_sql("alerts", conn, if_exists="append", index=False)

        tours2 = df_tours.copy()
        tours2["run_ts"] = run_ts
        add_missing_columns(conn, "tours", {
            "private_room_free": "INTEGER", 
            "shared_bed": "INTEGER"
        })
        tours2.to_sql("tours", conn, if_exists="append", index=False)

        sdd2 = same_d.copy()
        sdd2["run_ts"] = run_ts
        sdd_cols = {
            "money_pot_med_eur_slug": "REAL",
            "total_price_prev": "REAL",
            "total_price_curr": "REAL",
        }
        add_missing_columns(conn, "same_date_diff", sdd_cols)
        sdd2.to_sql("same_date_diff", conn, if_exists="append", index=False)

    finally:
        conn.close()
    logging.info("Persisté SQLite: %s", db_path)


# -------------------- Main --------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="weekly_report.xlsx", help="Chemin du rapport Excel")
    ap.add_argument("--sqlite", default="data/weroad.db", help="Chemin de la base SQLite (ou vide pour désactiver)")
    ap.add_argument("--alert-pct", type=float, default=float(os.getenv("ALERT_PCT", 0.10)), help="Seuil variation % (0.10=10%)")
    ap.add_argument("--alert-eur", type=float, default=float(os.getenv("ALERT_EUR", 150.0)), help="Seuil variation absolue €")
    ap.add_argument("--workers", type=int, default=int(os.getenv("WORKERS", 12)),
                    help="Nombre de threads pour récupérer les tours")
    ap.add_argument("--skip-tours", action="store_true",
                    help="Désactiver la récupération des TOURS (plus rapide)")
    ap.add_argument("--money-pot", action="store_true",
                    help="Active l'extraction du moneypot par voyage")
    ap.add_argument("--money-pot-workers", type=int, default=int(os.getenv("MONEYPOT_WORKERS", 12)),
                    help="Nombre de threads pour récupérer le moneypot")
    args = ap.parse_args()

    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    logging.info("Run timestamp (UTC): %s", run_ts)
    logging.info("Fetching travels list… (workers=%s; money-pot-workers=%s)", args.workers, args.money_pot_workers)

    travels = fetch_travels()
    df_curr  = normalize_travels(travels)

    if args.money_pot:
        df_curr = enrich_with_money_pot(df_curr, max_workers=args.money_pot_workers)
    else:
        for c in ("money_pot_min_eur","money_pot_max_eur","money_pot_raw","money_pot_med_eur","total_price_eur"):
            if c not in df_curr.columns:
                df_curr[c] = None
        if df_curr["total_price_eur"].isna().all():
            df_curr["total_price_eur"] = df_curr["price_eur"].astype(float).fillna(0)

    if args.skip_tours:
        df_tours_curr = pd.DataFrame(columns=[
            "tour_id","slug","title","destination_label","country_name",
            "starting_date","ending_date","price_eur","base_price_eur",
            "discount_value_eur","discount_pct","sales_status","seatsToConfirm",
            "maxPax","weroadersCount","private_room_free","shared_bed","url","url_precise"
        ])
    else:
        df_tours_curr = normalize_tours(travels, max_workers=args.workers)

    df_prev = pd.DataFrame()
    df_tours_prev = pd.DataFrame()
    if args.sqlite and Path(args.sqlite).exists():
        conn = sqlite3.connect(args.sqlite)
        try:
            runs = pd.read_sql_query("SELECT DISTINCT run_ts FROM snapshots ORDER BY run_ts", conn)
            if not runs.empty:
                last_ts = runs["run_ts"].iloc[-1]
                df_prev = pd.read_sql_query("SELECT * FROM snapshots WHERE run_ts = ?", conn, params=(last_ts,))
            try:
                runs_tours = pd.read_sql_query("SELECT DISTINCT run_ts FROM tours ORDER BY run_ts", conn)
                if not runs_tours.empty:
                    last_tours_ts = runs_tours["run_ts"].iloc[-1]
                    df_tours_prev = pd.read_sql_query("SELECT * FROM tours WHERE run_ts = ?", conn, params=(last_tours_ts,))
            except Exception:
                pass
        finally:
            conn.close()

    wk_k  = weekly_kpis(df_curr)
    wk_d  = weekly_diff(df_curr, df_prev)

    if not df_curr.empty:
        mo_k = df_curr.dropna(subset=["month"]).groupby(["month","destination_label"]).agg(
            prix_min=("price_eur","min"),
            prix_avg=("price_eur","mean"),
            nb_depart=("best_starting_date","count"),
        ).reset_index()
        mo_k = mo_k.sort_values(["destination_label","month"])
        mo_k["prix_min_prev"] = mo_k.groupby("destination_label")["prix_min"].shift(1)
        mo_k["prix_avg_prev"] = mo_k.groupby("destination_label")["prix_avg"].shift(1)
        mo_k["nb_depart_prev"] = mo_k.groupby("destination_label")["nb_depart"].shift(1)
        mo_k["delta_prix_min"] = mo_k["prix_min"] - mo_k["prix_min_prev"]
        mo_k["delta_prix_avg"] = mo_k["prix_avg"] - mo_k["prix_avg_prev"]
        mo_k["delta_nb_depart"] = mo_k["nb_depart"] - mo_k["nb_depart_prev"]
        mo_k["delta_prix_min_pct"] = mo_k["delta_prix_min"] / mo_k["prix_min_prev"].replace({0: np.nan})
        mo_k["delta_prix_avg_pct"] = mo_k["delta_prix_avg"] / mo_k["prix_avg_prev"].replace({0: np.nan})
        mo_k.replace([np.inf, -np.inf], np.nan, inplace=True)
        mo_d = mo_k.copy()
    else:
        mo_k = pd.DataFrame(columns=["month","destination_label","prix_min","prix_avg","nb_depart"])
        mo_d = pd.DataFrame()

    alert_pct = args.alert_pct
    alert_eur = args.alert_eur
    if not wk_d.empty:
        wk_d["flag"] = (wk_d.get("delta_pct", 0).abs() > alert_pct) | (wk_d.get("delta_abs", 0).abs() > alert_eur)
        alerts = wk_d[wk_d["flag"]].copy()
    else:
        alerts = pd.DataFrame()

    money_map = df_curr[["slug", "money_pot_med_eur"]].drop_duplicates()
    sdd = same_date_diff(df_tours_curr, df_tours_prev, money_map)

    export_excel(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, df_tours_curr, sdd, out=args.out)

    if args.sqlite:
        persist_sqlite(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, df_tours_curr, sdd, db_path=args.sqlite, run_ts=run_ts)


if __name__ == "__main__":
    main()
