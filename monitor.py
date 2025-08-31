# monitor.py
import os
import re
import json
import logging
import sqlite3
import argparse
import concurrent.futures
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- Config ---
API_TRAVELS = "https://api-catalog.weroad.fr/travels"
API_TRAVEL  = "https://api-catalog.weroad.fr/travels/{slug}"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# ----------------- MoneyPot extractor -----------------
def extract_money_pot_eur(description: str):
    """
    Extrait min/max du moneyPot depuis HTML. Si '€/euros' est absent, on tolère un nombre si
    'pot commun' est mentionné dans le texte.
    """
    if not description:
        return None, None, None

    text = BeautifulSoup(description, "html.parser").get_text(" ", strip=True)
    raw = text

    # 200 euros / 200 € / €200
    matches = re.findall(r"(\d{2,5})(?:\s?(?:€|euros?))", text, flags=re.IGNORECASE)
    if not matches:
        matches = re.findall(r"(?:€\s?)(\d{2,5})", text, flags=re.IGNORECASE)

    values = [float(x) for x in matches if x.isdigit()]

    # Fallback: nombre seul si "pot commun" mentionné
    if not values and "pot commun" in text.lower():
        m = re.search(r"(\d{2,5})(?!\s?%)", text)
        if m:
            try:
                values.append(float(m.group(1)))
            except ValueError:
                pass

    if not values:
        return None, None, raw
    return min(values), max(values), raw


# ----------------- API fetchers -----------------
def fetch_travels_list(token: str):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    r = requests.get(API_TRAVELS, headers=headers, timeout=45)
    r.raise_for_status()
    data = r.json()
    return data.get("data", data) or []


def fetch_travel_detail(slug: str, token: str):
    url = API_TRAVEL.format(slug=slug)
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    r = requests.get(url, headers=headers, timeout=45)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], dict) and "travel" in data["data"]:
        return data["data"]["travel"]
    return data


# ----------------- MoneyPot enrichment -----------------
def enrich_with_money_pot(df_travels: pd.DataFrame, token: str, max_workers: int = 12) -> pd.DataFrame:
    results = {}
    slugs = df_travels["slug"].dropna().unique().tolist()

    def process(slug):
        try:
            detail = fetch_travel_detail(slug, token)
            mp = (detail or {}).get("moneyPot", {}) if isinstance(detail, dict) else {}
            return slug, extract_money_pot_eur(mp.get("description"))
        except Exception as e:
            logging.warning("Fail moneyPot %s: %s", slug, e)
            return slug, (None, None, None)

    if max_workers and max_workers > 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
            for slug, (vmin, vmax, raw) in ex.map(process, slugs):
                results[slug] = (vmin, vmax, raw)
    else:
        for slug in slugs:
            slug2, (vmin, vmax, raw) = process(slug)
            results[slug2] = (vmin, vmax, raw)

    out = df_travels.copy()
    out["money_pot_min_eur"] = out["slug"].map(lambda s: results.get(s, (None, None, None))[0])
    out["money_pot_max_eur"] = out["slug"].map(lambda s: results.get(s, (None, None, None))[1])
    out["money_pot_raw"]     = out["slug"].map(lambda s: results.get(s, (None, None, None))[2] or "")

    # Médiane & prix total
    out["money_pot_med_eur"] = out[["money_pot_min_eur", "money_pot_max_eur"]].mean(axis=1, skipna=True)
    out["total_price_eur"]   = out["price_eur"].fillna(0) + out["money_pot_med_eur"].fillna(0)

    logging.info("MoneyPot enrichi: %d/%d voyages détectés",
                 int(out[["money_pot_min_eur","money_pot_max_eur"]].notna().any(axis=1).sum()),
                 len(out))
    return out


# ----------------- KPIs (minimaux pour résumer/charger le dashboard) -----------------
def compute_weekly_kpis_from_df(df: pd.DataFrame) -> dict:
    out = {}
    for c in ["price_eur", "base_price_eur", "discount_value_eur", "discount_pct"]:
        s = pd.to_numeric(df.get(c), errors="coerce").dropna()
        out[f"{c}_min"] = float(s.min()) if not s.empty else None
        out[f"{c}_max"] = float(s.max()) if not s.empty else None
        out[f"{c}_avg"] = float(s.mean()) if not s.empty else None
        out[f"{c}_med"] = float(s.median()) if not s.empty else None

    out["count_total"] = int(len(df))
    out["count_promos"] = int(pd.to_numeric(df.get("discount_pct"), errors="coerce").notna().sum())
    out["promo_share_pct"] = round(100 * out["count_promos"] / out["count_total"], 1) if out["count_total"] else 0.0

    # depart_by_month attendu comme JSON dans ta version ancienne
    month = pd.to_datetime(df.get("best_starting_date"), errors="coerce").dt.strftime("%Y-%m")
    month = month.dropna()
    depart_by_month = month.value_counts().sort_index().to_dict()
    out["depart_by_month"] = json.dumps(depart_by_month, ensure_ascii=False)
    return out


# ----------------- SQLite schema & persistence -----------------
def _columns_of(conn: sqlite3.Connection, table: str) -> set:
    cur = conn.execute(f'PRAGMA table_info("{table}")')
    return {row[1] for row in cur.fetchall()}

def ensure_schema(conn: sqlite3.Connection):
    """
    Crée toutes les tables si absentes et ajoute les colonnes manquantes
    (migration douce) pour assurer la compatibilité avec summarize.py.
    """
    # 1) snapshots
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS snapshots (
      run_ts TEXT,
      slug TEXT,
      title TEXT,
      destination_label TEXT,
      country_name TEXT,
      sales_status TEXT,
      best_starting_date TEXT,
      best_ending_date TEXT,
      price_eur REAL,
      base_price_eur REAL,
      discount_value_eur REAL,
      discount_pct REAL,
      url_precise TEXT,
      rating REAL,
      rating_count INTEGER,
      seatsToConfirm INTEGER,
      maxPax INTEGER,
      weroadersCount INTEGER,
      money_pot_min_eur REAL,
      money_pot_max_eur REAL,
      money_pot_med_eur REAL,
      total_price_eur REAL,
      money_pot_raw TEXT
    );
    """)
    # migration douce
    want = {
        "money_pot_min_eur": "REAL",
        "money_pot_max_eur": "REAL",
        "money_pot_med_eur": "REAL",
        "total_price_eur": "REAL",
        "money_pot_raw": "TEXT",
    }
    existing = _columns_of(conn, "snapshots")
    for col, typ in want.items():
        if col not in existing:
            conn.execute(f'ALTER TABLE "snapshots" ADD COLUMN "{col}" {typ}')

    # 2) weekly_kpis (utilisé par summarize pour trouver les runs)
    conn.executescript("""
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
    """)

    # 3) weekly_diff (summarize lira, ok s'il est vide)
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS weekly_diff (
      run_ts TEXT,
      destination_label TEXT,
      title_curr TEXT,
      price_eur_prev REAL,
      price_eur_curr REAL,
      delta_abs REAL,
      delta_pct REAL,
      movement TEXT,
      url TEXT
    );
    """)

    # 4) monthly_kpis (affiché par summarize)
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS monthly_kpis (
      run_ts TEXT,
      month TEXT,
      destination_label TEXT,
      prix_min REAL,
      prix_avg REAL,
      nb_depart INTEGER
    );
    """)

    # 5) monthly_diff (optionnel)
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS monthly_diff (
      run_ts TEXT,
      month TEXT,
      destination_label TEXT,
      delta_prix_min REAL,
      delta_prix_avg REAL,
      delta_nb_depart REAL,
      delta_prix_min_pct REAL,
      delta_prix_avg_pct REAL
    );
    """)

    # 6) tours (pour compat futur)
    conn.executescript("""
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
    """)

    # 7) same_date_diff (affiché par summarize s’il y a des données)
    conn.executescript("""
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

    # 8) alerts (optionnel)
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS alerts (
      run_ts TEXT,
      destination_label TEXT,
      title TEXT,
      price_eur_prev REAL,
      price_eur_curr REAL,
      delta_abs REAL,
      delta_pct REAL,
      movement TEXT,
      url TEXT
    );
    """)

    conn.commit()


def save_snapshot(conn: sqlite3.Connection, run_ts: str, df: pd.DataFrame):
    ensure_schema(conn)
    df2 = df.copy()
    df2["run_ts"] = run_ts
    df2.to_sql("snapshots", conn, if_exists="append", index=False)


def save_weekly_kpis(conn: sqlite3.Connection, run_ts: str, kpi: dict):
    ensure_schema(conn)
    row = {**kpi, "run_ts": run_ts}
    pd.DataFrame([row]).to_sql("weekly_kpis", conn, if_exists="append", index=False)


# ----------------- Main -----------------
def main():
    ap = argparse.ArgumentParser(description="WeRoad monitor: snapshot + MoneyPot + minimal KPIs")
    ap.add_argument("--sqlite", default="data/weroad.db", help="Chemin du fichier SQLite")
    ap.add_argument("--out", default="weekly_report.xlsx", help="Chemin du rapport Excel")
    ap.add_argument("--money-pot", action="store_true", help="Activer l’enrichissement MoneyPot")
    ap.add_argument("--workers", type=int, default=12,
                    help="(Accepté) workers collecte principale (réservé)")
    ap.add_argument("--money-pot-workers", type=int, default=12,
                    help="Workers pour l’enrichissement MoneyPot")
    args = ap.parse_args()

    token = os.getenv("WEROAD_TOKEN", "")

    logging.info("Fetching travels list… (workers=%s; money-pot-workers=%s)",
                 args.workers, args.money_pot_workers)
    travels = fetch_travels_list(token)

    # Normalisation minimale côté "travels"
    rows = []
    for t in travels:
        best = (t.get("bestTour") or {})
        price_eur = (best.get("price") or {}).get("EUR")
        base_eur  = (best.get("basePrice") or {}).get("EUR")
        rows.append({
            "slug": t.get("slug"),
            "title": t.get("title"),
            "destination_label": (t.get("primaryDestination") or {}).get("name"),
            "country_name": ((t.get("breadcrumbs") or {}).get("destination") or {}).get("name"),
            "price_eur": price_eur,
            "base_price_eur": base_eur,
            "discount_value_eur": ((base_eur or 0) - (price_eur or 0)) if (price_eur is not None or base_eur is not None) else None,
            "discount_pct": best.get("discountPercentage"),
            "best_starting_date": (t.get("firstTour") or {}).get("startingDate"),
            "best_ending_date": (t.get("firstTour") or {}).get("endingDate"),
            "url_precise": f"https://www.weroad.fr/travel/{t.get('slug')}" if t.get("slug") else None,
            "rating": ((t.get("userRating") or {})).get("rating"),
            "rating_count": ((t.get("userRating") or {})).get("count"),
        })
    df = pd.DataFrame(rows)

    # MoneyPot
    if args.money_pot:
        df = enrich_with_money_pot(df, token=token, max_workers=args.money_pot_workers)
    else:
        for c in ("money_pot_min_eur","money_pot_max_eur","money_pot_raw","money_pot_med_eur"):
            if c not in df.columns:
                df[c] = None
        df["total_price_eur"] = df["price_eur"].fillna(0)

    # --- Persist & KPIs ---
    Path(args.sqlite).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(args.sqlite)
    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    try:
        ensure_schema(conn)
        save_snapshot(conn, run_ts, df)

        # KPIs minimaux (pour que summarize trouve des runs)
        wk = compute_weekly_kpis_from_df(df)
        save_weekly_kpis(conn, run_ts, wk)
    finally:
        conn.close()

    # Excel (simple dump pour debug/analyse)
    with pd.ExcelWriter(args.out, engine="openpyxl") as w:
        df.to_excel(w, sheet_name="travels", index=False)

    logging.info("Done: %d voyages, snapshot %s", len(df), run_ts)


if __name__ == "__main__":
    main()
