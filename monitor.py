# monitor.py
import os
import re
import json
import time
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

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ----------------- MoneyPot extractor -----------------
def extract_money_pot_eur(description: str):
    """
    Extrait min/max du moneyPot depuis le champ HTML "description".
    Si "euros/€" est manquant, tolère les nombres si 'pot commun' est présent.
    """
    if not description:
        return None, None, None

    text = BeautifulSoup(description, "html.parser").get_text(" ", strip=True)
    raw = text

    # Standard: 200 euros / 200 € / €200
    matches = re.findall(r"(\d{2,5})(?:\s?(?:€|euros?))", text, flags=re.IGNORECASE)
    if not matches:
        matches = re.findall(r"(?:€\s?)(\d{2,5})", text, flags=re.IGNORECASE)

    values = [float(x) for x in matches if x.isdigit()]

    # Fallback: nombre seul si "pot commun" est mentionné
    if not values and "pot commun" in text.lower():
        m = re.search(r"(\d{2,5})(?!\s?(?:%))", text)
        if m:
            try:
                values.append(float(m.group(1)))
            except ValueError:
                pass

    if not values:
        return None, None, raw

    return min(values), max(values), raw

# ----------------- Data Fetchers -----------------
def fetch_travels_list(token: str):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = requests.get(API_TRAVELS, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("data", data)  # compat

def fetch_travel_detail(slug: str, token: str):
    url = API_TRAVEL.format(slug=slug)
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # certaines réponses sont sous {"data": {"travel": {...}}}
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], dict) and "travel" in data["data"]:
        return data["data"]["travel"]
    # sinon, retour direct
    return data

# ----------------- MoneyPot Enrichment -----------------
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
            s, vals = process(slug), None  # just to keep structure obvious
            slug_out, (vmin, vmax, raw) = s
            results[slug_out] = (vmin, vmax, raw)

    out = df_travels.copy()
    out["money_pot_min_eur"] = out["slug"].map(lambda s: results.get(s, (None, None, None))[0])
    out["money_pot_max_eur"] = out["slug"].map(lambda s: results.get(s, (None, None, None))[1])
    out["money_pot_raw"]     = out["slug"].map(lambda s: results.get(s, (None, None, None))[2] or "")

    # Médiane
    out["money_pot_med_eur"] = out[["money_pot_min_eur", "money_pot_max_eur"]].mean(axis=1, skipna=True)

    # Prix total (voyage + moneypot médian)
    if "price_eur" in out.columns:
        out["total_price_eur"] = out["price_eur"].fillna(0) + out["money_pot_med_eur"].fillna(0)
    else:
        out["total_price_eur"] = out["money_pot_med_eur"].fillna(0)

    found = int(out["money_pot_min_eur"].notna().sum() | out["money_pot_max_eur"].notna().sum())
    logging.info("MoneyPot enrichi: ~%d/%d voyages détectés", 
                 out[["money_pot_min_eur","money_pot_max_eur"]].notna().any(axis=1).sum(),
                 len(out))
    return out

# ----------------- SQLite Storage -----------------
def ensure_schema(conn: sqlite3.Connection):
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
    conn.commit()

def save_snapshot(conn: sqlite3.Connection, run_ts: str, df: pd.DataFrame):
    ensure_schema(conn)
    df2 = df.copy()
    df2["run_ts"] = run_ts
    df2.to_sql("snapshots", conn, if_exists="append", index=False)

# ----------------- Main -----------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sqlite", type=str, default="data/weroad.db",
                        help="Chemin du fichier SQLite")
    parser.add_argument("--out", type=str, default="weekly_report.xlsx",
                        help="Chemin du rapport Excel")
    parser.add_argument("--money-pot", action="store_true",
                        help="Activer l’enrichissement MoneyPot")
    parser.add_argument("--workers", type=int, default=12,
                        help="(Accepté) Nombre de workers pour la collecte principale (réservé)")
    parser.add_argument("--money-pot-workers", type=int, default=12,
                        help="Nombre de workers pour l’enrichissement MoneyPot")
    args = parser.parse_args()

    token = os.getenv("WEROAD_TOKEN", "")

    logging.info("Fetching travels list… (workers=%s; money-pot-workers=%s)",
                 args.workers, args.money_pot_workers)
    travels = fetch_travels_list(token)
    rows = []
    for t in travels:
        best = t.get("bestTour", {}) or {}
        price_eur = (best.get("price") or {}).get("EUR")
        base_eur  = (best.get("basePrice") or {}).get("EUR")
        rows.append({
            "slug": t.get("slug"),
            "title": t.get("title"),
            "destination_label": (t.get("primaryDestination") or {}).get("name"),
            "country_name": ((t.get("breadcrumbs") or {}).get("destination") or {}).get("name"),
            "price_eur": price_eur,
            "base_price_eur": base_eur,
            "discount_value_eur": (base_eur or 0) - (price_eur or 0) if (price_eur is not None or base_eur is not None) else None,
            "discount_pct": best.get("discountPercentage"),
            "best_starting_date": (t.get("firstTour") or {}).get("startingDate"),
            "best_ending_date": (t.get("firstTour") or {}).get("endingDate"),
            "url_precise": f"https://www.weroad.fr/travel/{t.get('slug')}" if t.get("slug") else None,
            "rating": ((t.get("userRating") or {})).get("rating"),
            "rating_count": ((t.get("userRating") or {})).get("count"),
            # certains champs (sales_status, seatsToConfirm, ...) ne sont pas au niveau "travels" mais au niveau tour
        })
    df = pd.DataFrame(rows)

    if args.money_pot:
        df = enrich_with_money_pot(df, token=token, max_workers=args.money_pot_workers)
    else:
        for c in ["money_pot_min_eur","money_pot_max_eur","money_pot_raw"]:
            if c not in df.columns:
                df[c] = None
        df["money_pot_med_eur"] = None
        df["total_price_eur"] = df["price_eur"].fillna(0)

    # --- Persist ---
    Path(args.sqlite).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(args.sqlite)
    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    save_snapshot(conn, run_ts, df)
    conn.close()

    # Excel export
    with pd.ExcelWriter(args.out, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="travels", index=False)

    logging.info("Done: %d voyages, snapshot %s", len(df), run_ts)

if __name__ == "__main__":
    main()
