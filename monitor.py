# monitor.py
# Collector + KPIs + persistance SQLite (création de TOUTES les tables au 1er run)
# + Récupération des TOURS (départs par date) et comparaison même-date
# + Extraction du MoneyPot (min/max + texte brut) depuis data.travel.moneyPot.description

import os
import re
import json
import time
import logging
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Optional, Tuple, List

import numpy as np
import pandas as pd
import requests
import html as ihtml

# --- Endpoints ---
API_TRAVELS       = "https://api-catalog.weroad.fr/travels"
API_TOURS         = "https://api-catalog.weroad.fr/travels/{slug}/tours"
API_TRAVEL_DETAIL = "https://api-catalog.weroad.fr/travels/{slug}"

DEFAULT_TIMEOUT = 45
DEFAULT_RETRIES = 4
DEFAULT_BACKOFF = 0.8  # seconds, exponential backoff

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

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
        "user-agent": "weroad-monitor/1.0 (+analytics)",
        "accept-language": "fr-FR,fr;q=0.9,en;q=0.8",
        "connection": "keep-alive",
    }
    token = os.getenv("WEROAD_TOKEN")
    if token:
        headers["authorization"] = f"Bearer {token}"
    s.headers.update(headers)
    return s

def _get_json(url: str, params: Optional[Dict[str, Any]] = None,
              timeout: int = DEFAULT_TIMEOUT, retries: int = DEFAULT_RETRIES) -> Any:
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
                sleep = DEFAULT_BACKOFF * (2 ** attempt)
                logging.warning("GET %s failed (%s) attempt %d/%d; retry in %.2fs",
                                url, e, attempt + 1, retries + 1, sleep)
                time.sleep(sleep)
    raise last_exc  # type: ignore[misc]

# -------------------- MoneyPot extraction --------------------
_MONEYPOT_NUM_RE = re.compile(
    r"""
    (?P<a>\d{1,3}(?:[ . \u00A0]\d{3})*(?:[,.]\d+)?)     # premier nombre (1 200, 1.200, 200,50)
    (?:\s*(?:-|–|à|a|to|en|aux|and|et)\s*
       (?P<b>\d{1,3}(?:[ . \u00A0]\d{3})*(?:[,.]\d+)?)
    )?
    \s*(?:€|eur(?:o|os)?)                               # € / euro(s)
    """,
    re.IGNORECASE | re.VERBOSE,
)

def _to_float_eur(s: str) -> Optional[float]:
    if s is None:
        return None
    s = s.replace("\u00A0", " ")
    s = s.replace(".", "")     # 1.200 -> 1200
    s = s.replace(" ", "")     # 1 200 -> 1200
    s = s.replace(",", ".")    # 200,50 -> 200.50
    try:
        return float(s)
    except Exception:
        return None

def parse_money_pot(description_html: str) -> Tuple[Optional[float], Optional[float], str]:
    """Retourne (min_eur, max_eur, raw_text)."""
    if not description_html:
        return None, None, ""
    txt = ihtml.unescape(description_html)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()

    m = _MONEYPOT_NUM_RE.search(txt)
    if not m:
        alt = re.search(r"(\d[\d . \u00A0,]*)\s*(?:€|eur(?:o|os)?)", txt, flags=re.IGNORECASE)
        if not alt:
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
    """Parcours récursif pour trouver un dict moneyPot ou une description contenant €."""
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

def _collect_descriptions(node) -> List[str]:
    out: List[str] = []
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

def extract_money_pot_from_travel_json(payload: dict) -> Tuple[Optional[float], Optional[float], str]:
    # 1) data.travel.moneyPot.description
    root = payload if isinstance(payload, dict) else {}
    travel = root.get("data", {}).get("travel", {})
    if isinstance(travel, dict):
        mp = travel.get("moneyPot")
        if isinstance(mp, dict):
            desc = mp.get("description")
            if isinstance(desc, str) and desc.strip():
                return parse_money_pot(desc)

    # 2) recherche profonde
    mp2 = _deep_find_money_pot(root)
    if isinstance(mp2, dict) and isinstance(mp2.get("description"), str):
        return parse_money_pot(mp2["description"])

    # 3) fallback : 1ère description qui mentionne €
    for cand in _collect_descriptions(root):
        if re.search(r"(€|eur(?:o|os)?)", cand, re.I):
            return parse_money_pot(cand)

    return None, None, ""

def fetch_travel_detail(slug: str) -> dict:
    base = API_TRAVEL_DETAIL.format(slug=slug)
    candidates = [base, base + "?market=FR", base + "?lang=fr-FR", base + "?market=FR&lang=fr-FR"]
    for url in candidates:
        try:
            data = _get_json(url)
            if isinstance(data, dict) and data:
                return data
        except Exception:
            pass
    return {}

def enrich_with_money_pot(df_travels: pd.DataFrame, max_workers: int = 12) -> pd.DataFrame:
    out = df_travels.copy()
    for c in ("money_pot_min_eur", "money_pot_max_eur", "money_pot_raw"):
        if c not in out.columns:
            out[c] = None

    slugs = out["slug"].dropna().astype(str).unique().tolist() if "slug" in out.columns else []
    if not slugs:
        out["money_pot_med_eur"] = np.nan
        out["total_price_eur"] = out.get("price_eur", pd.Series(dtype=float))
        return out

    def _job(slug: str):
        try:
            data = fetch_travel_detail(slug)
            mn, mx, raw = extract_money_pot_from_travel_json(data)
            return slug, mn, mx, raw
        except Exception as e:
            logging.warning("moneyPot fetch failed for %s: %s", slug, e)
            return slug, None, None, ""

    results: Dict[str, Tuple[Optional[float], Optional[float], str]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(_job, slug): slug for slug in slugs}
        for fut in as_completed(futs):
            slug, mn, mx, raw = fut.result()
            results[slug] = (mn, mx, raw)

    out["money_pot_min_eur"] = out["slug"].map(lambda s: results.get(s, (None, None, ""))[0])
    out["money_pot_max_eur"] = out["slug"].map(lambda s: results.get(s, (None, None, ""))[1])
    out["money_pot_raw"]     = out["slug"].map(lambda s: results.get(s, (None, None, ""))[2])

    out["money_pot_med_eur"] = out[["money_pot_min_eur", "money_pot_max_eur"]].mean(axis=1, skipna=True)
    # Prix total = meilleur prix (price_eur) + médiane moneypot
    out["total_price_eur"] = out.get("price_eur", pd.Series(dtype=float)).fillna(0) + out["money_pot_med_eur"].fillna(0)

    found = int(pd.notna(out["money_pot_min_eur"]).sum())
    total = int(len(out))
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
    slugs = [t.get("slug") for t in travels if t.get("slug")]
    slugs = list(dict.fromkeys(slugs))
    rows = []

    def _fetch(slug: str):
        try:
            return slug, fetch_tours_for_slug(slug)
        except Exception as e:
            logging.warning("fetch_tours_for_slug(%s) failed: %s", slug, e)
            return slug, []

    if not slugs:
        return pd.DataFrame()

    results: Dict[str, list[dict]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(_fetch, slug): slug for slug in slugs}
        for fut in as_completed(futs):
            slug, tours = fut.result()
            results[slug] = tours

    for t in travels:
        slug = t.get("slug")
        if not slug:
            continue
        for tour in results.get(slug, []):
            tour_id = tour.get("id")
            price   = num(g(tour, ["price", "EUR"]))
            base    = num(g(tour, ["basePrice", "EUR"]))

            disc_val = disc_pct = None
            if price is not None and base is not None and base > price:
                disc_val = base - price
                disc_pct = round((base - price) / base * 100, 1)

            url_dest    = f"https://www.weroad.fr/destinations/{slug}"
            url_precise = f"{url_dest}/{tour_id}" if tour_id else url_dest

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
                    "maxPax": g(tour, ["maxPax"]),
                    "weroadersCount": g(tour, ["groupInfo", "weroadersCount"]),
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
    for c in ["price_eur", "base_price_eur", "discount_value_eur", "discount_pct"]:
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

def same_date_diff(df_tours_curr: pd.DataFrame, df_tours_prev: pd.DataFrame) -> pd.DataFrame:
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

    out["delta_abs"] = out["price_eur_curr"] - out["price_eur_prev"]
    den = out["price_eur_prev"].replace({0: np.nan})
    out["delta_pct"] = out["delta_abs"] / den
    out.replace([np.inf, -np.inf], np.nan, inplace=True)
    out["movement"] = out["delta_abs"].apply(
        lambda v: "↓" if (pd.notna(v) and v < 0) else ("↑" if (pd.notna(v) and v > 0) else "=")
    )
    return out

# -------------------- Export Excel (optionnel) --------------------
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
    logging.info("Exporté Excel: %s", out)

# -------------------- SQLite: création des tables AU 1er RUN --------------------
def ensure_all_tables(conn: sqlite3.Connection):
    conn.executescript("""
    -- Snapshots (vue voyages + MoneyPot)
    CREATE TABLE IF NOT EXISTS snapshots (
      run_ts TEXT,
      id TEXT,
      slug TEXT,
      url TEXT,
      title TEXT,
      destination_label TEXT,
      country_name TEXT,
      continent TEXT,
      status TEXT,
      isBookable INTEGER,
      days INTEGER,
      style TEXT,
      types TEXT,
      price_eur REAL,
      base_price_eur REAL,
      discount_value_eur REAL,
      discount_pct REAL,
      sales_status TEXT,
      seatsToConfirm INTEGER,
      maxPax INTEGER,
      weroadersCount INTEGER,
      min_price_eur REAL,
      max_price_eur REAL,
      best_starting_date TEXT,
      best_ending_date TEXT,
      rating REAL,
      rating_count INTEGER,
      month TEXT,
      money_pot_min_eur REAL,
      money_pot_max_eur REAL,
      money_pot_med_eur REAL,
      total_price_eur REAL,
      money_pot_raw TEXT
    );

    -- KPIs hebdo
    CREATE TABLE IF NOT EXISTS weekly_kpis (
      run_ts TEXT,
      price_eur_min REAL,
      price_eur_max REAL,
      price_eur_avg REAL,
      price_eur_med REAL,
      base_price_eur_min REAL,
      base_price_eur_max REAL,
      base_price_eur_avg REAL,
      base_price_eur_med REAL,
      discount_value_eur_min REAL,
      discount_value_eur_max REAL,
      discount_value_eur_avg REAL,
      discount_value_eur_med REAL,
      discount_pct_min REAL,
      discount_pct_max REAL,
      discount_pct_avg REAL,
      discount_pct_med REAL,
      count_total INTEGER,
      count_promos INTEGER,
      promo_share_pct REAL,
      depart_by_month TEXT
    );

    -- Diff hebdo (meilleur prix par destination)
    CREATE TABLE IF NOT EXISTS weekly_diff (
      run_ts TEXT,
      destination_label TEXT,
      title_curr TEXT,
      country_name_curr TEXT,
      price_eur_prev REAL,
      price_eur_curr REAL,
      delta_abs REAL,
      delta_pct REAL,
      movement TEXT,
      url TEXT,
      flag INTEGER
    );

    -- KPIs mensuels (vue étalée)
    CREATE TABLE IF NOT EXISTS monthly_kpis (
      run_ts TEXT,
      month TEXT,
      destination_label TEXT,
      prix_min REAL,
      prix_avg REAL,
      nb_depart INTEGER,
      prix_min_prev REAL,
      prix_avg_prev REAL,
      nb_depart_prev REAL,
      delta_prix_min REAL,
      delta_prix_avg REAL,
      delta_nb_depart REAL,
      delta_prix_min_pct REAL,
      delta_prix_avg_pct REAL
    );

    -- Copie des deltas mensuels (on stocke mo_k enrichi)
    CREATE TABLE IF NOT EXISTS monthly_diff AS
      SELECT '' AS run_ts, '' AS month, '' AS destination_label,
             0.0 AS prix_min, 0.0 AS prix_avg, 0 AS nb_depart,
             0.0 AS prix_min_prev, 0.0 AS prix_avg_prev, 0 AS nb_depart_prev,
             0.0 AS delta_prix_min, 0.0 AS delta_prix_avg, 0.0 AS delta_nb_depart,
             0.0 AS delta_prix_min_pct, 0.0 AS delta_prix_avg_pct
      WHERE 0;

    -- Alerts (seuils Δ)
    CREATE TABLE IF NOT EXISTS alerts (
      run_ts TEXT,
      destination_label TEXT,
      title_curr TEXT,
      country_name_curr TEXT,
      price_eur_prev REAL,
      price_eur_curr REAL,
      delta_abs REAL,
      delta_pct REAL,
      movement TEXT,
      url TEXT,
      flag INTEGER
    );

    -- TOURS (départs)
    CREATE TABLE IF NOT EXISTS tours (
      run_ts TEXT,
      tour_id TEXT,
      slug TEXT,
      title TEXT,
      destination_label TEXT,
      country_name TEXT,
      starting_date TEXT,
      ending_date TEXT,
      price_eur REAL,
      base_price_eur REAL,
      discount_value_eur REAL,
      discount_pct REAL,
      sales_status TEXT,
      seatsToConfirm INTEGER,
      maxPax INTEGER,
      weroadersCount INTEGER,
      url TEXT,
      url_precise TEXT
    );

    -- Diff sur mêmes départs (même tour_id)
    CREATE TABLE IF NOT EXISTS same_date_diff (
      run_ts TEXT,
      tour_id TEXT,
      slug TEXT,
      destination_label TEXT,
      title TEXT,
      starting_date TEXT,
      url_precise TEXT,
      price_eur_prev REAL,
      price_eur_curr REAL,
      delta_abs REAL,
      delta_pct REAL,
      movement TEXT
    );
    """)
    # Indexes
    try:
        conn.executescript("""
        CREATE INDEX IF NOT EXISTS idx_snapshots_run_ts ON snapshots(run_ts);
        CREATE INDEX IF NOT EXISTS idx_snapshots_dest ON snapshots(destination_label);
        CREATE INDEX IF NOT EXISTS idx_snapshots_dest_run ON snapshots(destination_label, run_ts);

        CREATE INDEX IF NOT EXISTS idx_weekly_kpis_run_ts ON weekly_kpis(run_ts);
        CREATE INDEX IF NOT EXISTS idx_weekly_diff_run_ts ON weekly_diff(run_ts);
        CREATE INDEX IF NOT EXISTS idx_weekly_diff_dest ON weekly_diff(destination_label);

        CREATE INDEX IF NOT EXISTS idx_monthly_kpis_run_ts ON monthly_kpis(run_ts);
        CREATE INDEX IF NOT EXISTS idx_monthly_diff_run_ts ON monthly_diff(run_ts);

        CREATE INDEX IF NOT EXISTS idx_alerts_run_ts ON alerts(run_ts);

        CREATE INDEX IF NOT EXISTS idx_tours_run_ts ON tours(run_ts);
        CREATE INDEX IF NOT EXISTS idx_tours_tour_id ON tours(tour_id);
        CREATE INDEX IF NOT EXISTS idx_tours_slug_start ON tours(slug, starting_date);

        CREATE INDEX IF NOT EXISTS idx_same_date_diff_run_ts ON same_date_diff(run_ts);
        CREATE INDEX IF NOT EXISTS idx_same_date_diff_tour_id ON same_date_diff(tour_id);
        """)
    except Exception as e:
        logging.warning("ensure indexes: %s", e)
    conn.commit()

def _align_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    out = df.copy()
    for c in columns:
        if c not in out.columns:
            out[c] = None
    # conserve l'ordre demandé
    return out[columns]

def persist_sqlite(
    df_curr: pd.DataFrame,
    wk_kpis_d: dict,
    wk_diff_df: pd.DataFrame,
    mo_kpis_df: pd.DataFrame,
    mo_diff_df: pd.DataFrame,
    alerts_df: pd.DataFrame,
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

        # snapshots
        snap_cols = [c[1] for c in conn.execute('PRAGMA table_info("snapshots")').fetchall()]
        df_snap = df_curr.copy()
        df_snap["run_ts"] = run_ts
        df_snap = _align_columns(df_snap, snap_cols)
        df_snap.to_sql("snapshots", conn, if_exists="append", index=False)

        # weekly_kpis
        wk_df = pd.DataFrame([{**wk_kpis_d, "run_ts": run_ts}])
        wk_cols = [c[1] for c in conn.execute('PRAGMA table_info("weekly_kpis")').fetchall()]
        wk_df = _align_columns(wk_df, wk_cols)
        wk_df.to_sql("weekly_kpis", conn, if_exists="append", index=False)

        # weekly_diff (+flag s'il existe)
        if not wk_diff_df.empty:
            if "flag" not in wk_diff_df.columns:
                wk_diff_df = wk_diff_df.copy()
                wk_diff_df["flag"] = None
            wk_diff_df = wk_diff_df.copy()
            wk_diff_df["run_ts"] = run_ts
            wd_cols = [c[1] for c in conn.execute('PRAGMA table_info("weekly_diff")').fetchall()]
            wk_diff_df = _align_columns(wk_diff_df, wd_cols)
            wk_diff_df.to_sql("weekly_diff", conn, if_exists="append", index=False)

        # monthly_kpis
        if not mo_kpis_df.empty:
            mk = mo_kpis_df.copy()
            mk["run_ts"] = run_ts
            mk_cols = [c[1] for c in conn.execute('PRAGMA table_info("monthly_kpis")').fetchall()]
            mk = _align_columns(mk, mk_cols)
            mk.to_sql("monthly_kpis", conn, if_exists="append", index=False)

        # monthly_diff
        if not mo_diff_df.empty:
            md = mo_diff_df.copy()
            md["run_ts"] = run_ts
            md_cols = [c[1] for c in conn.execute('PRAGMA table_info("monthly_diff")').fetchall()]
            # si la table a été créée vide via SELECT ... WHERE 0, elle a le schéma attendu
            md = _align_columns(md, md_cols)
            md.to_sql("monthly_diff", conn, if_exists="append", index=False)

        # alerts
        if not alerts_df.empty:
            al = alerts_df.copy()
            al["run_ts"] = run_ts
            al_cols = [c[1] for c in conn.execute('PRAGMA table_info("alerts")').fetchall()]
            al = _align_columns(al, al_cols)
            al.to_sql("alerts", conn, if_exists="append", index=False)

        # tours
        if not df_tours.empty:
            t = df_tours.copy()
            t["run_ts"] = run_ts
            t_cols = [c[1] for c in conn.execute('PRAGMA table_info("tours")').fetchall()]
            t = _align_columns(t, t_cols)
            t.to_sql("tours", conn, if_exists="append", index=False)

        # same_date_diff
        if not same_d.empty:
            sd = same_d.copy()
            sd["run_ts"] = run_ts
            sd_cols = [c[1] for c in conn.execute('PRAGMA table_info("same_date_diff")').fetchall()]
            sd = _align_columns(sd, sd_cols)
            sd.to_sql("same_date_diff", conn, if_exists="append", index=False)

    finally:
        conn.close()
    logging.info("Persisté SQLite: %s", db_path)

# -------------------- Main --------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="weekly_report.xlsx", help="Chemin du rapport Excel")
    ap.add_argument("--sqlite", default="data/weroad.db", help="Chemin de la base SQLite (ou vide pour désactiver)")
    ap.add_argument("--alert-pct", type=float, default=float(os.getenv("ALERT_PCT", 0.10)),
                    help="Seuil variation % (0.10=10%)")
    ap.add_argument("--alert-eur", type=float, default=float(os.getenv("ALERT_EUR", 150.0)),
                    help="Seuil variation absolue €")
    ap.add_argument("--workers", type=int, default=int(os.getenv("WORKERS", 12)),
                    help="Threads pour récupérer les TOURS")
    ap.add_argument("--skip-tours", action="store_true",
                    help="Désactiver la récupération des TOURS")
    ap.add_argument("--money-pot", action="store_true",
                    help="Activer l'extraction du MoneyPot")
    ap.add_argument("--money-pot-workers", type=int, default=int(os.getenv("MONEYPOT_WORKERS", 12)),
                    help="Threads pour récupérer le MoneyPot")
    args = ap.parse_args()

    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    logging.info("Run timestamp (UTC): %s", run_ts)

    # Fetch courants
    travels = fetch_travels()
    df_curr  = normalize_travels(travels)

    if args.money_pot:
        df_curr = enrich_with_money_pot(df_curr, max_workers=args.money_pot_workers)
    else:
        for c in ("money_pot_min_eur","money_pot_max_eur","money_pot_raw","money_pot_med_eur","total_price_eur"):
            if c not in df_curr.columns:
                df_curr[c] = None

    if args.skip_tours:
        df_tours_curr = pd.DataFrame(columns=[
            "tour_id","slug","title","destination_label","country_name",
            "starting_date","ending_date","price_eur","base_price_eur",
            "discount_value_eur","discount_pct","sales_status","seatsToConfirm",
            "maxPax","weroadersCount","url","url_precise"
        ])
    else:
        df_tours_curr = normalize_tours(travels, max_workers=args.workers)

    # Snapshots précédents
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

    # KPI & Diffs
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

    # Alerts
    alert_pct = args.alert_pct
    alert_eur = args.alert_eur
    if not wk_d.empty:
        wk_d = wk_d.copy()
        wk_d["flag"] = (wk_d.get("delta_pct", 0).abs() > alert_pct) | (wk_d.get("delta_abs", 0).abs() > alert_eur)
        alerts = wk_d[wk_d["flag"]].copy()
    else:
        alerts = pd.DataFrame()

    # Same-date diff
    sdd = same_date_diff(df_tours_curr, df_tours_prev)

    # Export Excel (facultatif mais pratique)
    export_excel(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, df_tours_curr, sdd, out=args.out)

    # Persist SQLite (création de TOUTES les tables si besoin)
    if args.sqlite:
        persist_sqlite(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, df_tours_curr, sdd,
                       db_path=args.sqlite, run_ts=run_ts)

if __name__ == "__main__":
    main()
