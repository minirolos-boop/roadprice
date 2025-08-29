# monitor.py — snapshot PAR DATE
import os
import json
import time
import math
import sqlite3
import argparse
import logging
from pathlib import Path
from datetime import datetime

import requests
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

API_TRAVELS = "https://api-catalog.weroad.fr/travels"
API_TOURS   = "https://api-catalog.weroad.fr/travels/{slug}/tours"

# -------------------- Utils --------------------
def g(d, path, default=None):
    cur = d
    for k in path:
        if isinstance(cur, dict) and (k in cur):
            cur = cur[k]
        else:
            return default
    return cur

def num(x):
    return x if isinstance(x, (int, float)) else None

def to_month(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").strftime("%Y-%m")
    except Exception:
        return None

def _sanitize_scalars(d: dict) -> dict:
    out = {}
    for k, v in d.items():
        if isinstance(v, (dict, list)):
            out[k] = json.dumps(v, ensure_ascii=False)
        else:
            out[k] = v
    return out

def session_with_headers():
    s = requests.Session()
    headers = {"accept": "application/json, text/plain, */*"}
    token = os.getenv("WEROAD_TOKEN")
    if token:
        headers["authorization"] = f"Bearer {token}"
    s.headers.update(headers)
    return s

# -------------------- Fetch --------------------
def fetch_travels_basic(sess: requests.Session) -> list[dict]:
    """Liste des voyages (pour récupérer slug, métadonnées niveau 'travel')."""
    r = sess.get(API_TRAVELS, timeout=30)
    r.raise_for_status()
    data = r.json()
    items = data.get("data", data) or []
    return items if isinstance(items, list) else []

def fetch_tours_for_slug(sess: requests.Session, slug: str) -> list[dict]:
    """Toutes les dates (tours) pour un slug donné."""
    url = API_TOURS.format(slug=slug)
    for attempt in range(3):
        try:
            r = sess.get(url, timeout=30)
            r.raise_for_status()
            data = r.json()
            items = data.get("data", data) or []
            if isinstance(items, list):
                return items
            return []
        except Exception as e:
            wait = 1.5 * (attempt + 1)
            logging.warning("fetch_tours_for_slug(%s) failed (%s), retry in %.1fs", slug, e, wait)
            time.sleep(wait)
    return []

# -------------------- Normalisation -> lignes PAR DATE --------------------
def normalize_per_date(travels: list[dict], sess: requests.Session) -> pd.DataFrame:
    """
    Pour chaque travel (slug), on va chercher /travels/{slug}/tours et on met
    une ligne par 'tour' (donc par date) avec tour_id, price/date/status, etc.
    """
    rows = []

    for t in travels:
        slug = t.get("slug")
        if not slug:
            continue

        # Métadonnées "voyage" (niveaux supérieurs /travels)
        travel_meta = {
            "id_travel": t.get("id"),
            "slug": slug,
            "url": f"https://www.weroad.fr/destinations/{slug}",
            "title": t.get("title") or t.get("destinationLabel") or slug,
            "destination_label": t.get("destinationLabel"),
            "country_name": g(t, ["primaryDestination", "name"]),
            "continent": g(t, ["primaryDestination", "primaryContinent", "name"]),
            "days": t.get("numberOfDays"),
            "style": g(t, ["travelStyle", "displayName"]),
            "types": ", ".join([x.get("displayName") for x in t.get("travelTypes", []) if x.get("displayName")]),
            "rating": g(t, ["userRating", "rating"]),
            "rating_count": g(t, ["userRating", "count"]),
        }

        tours = fetch_tours_for_slug(sess, slug)
        if not tours:
            continue

        for tour in tours:
            bt = tour or {}
            # prix
            price = num(g(bt, ["price", "EUR"]))
            base  = num(g(bt, ["basePrice", "EUR"]))
            disc_val = disc_pct = None
            if price is not None and base is not None and base > price:
                disc_val = base - price
                disc_pct = round((base - price) / base * 100, 1)

            # bornes min/max (juste utile pour KPIs)
            if price is None and base is None:
                min_p = max_p = None
            elif price is None:
                min_p = max_p = base
            elif base is None:
                min_p = max_p = price
            else:
                min_p = min(price, base)
                max_p = max(price, base)

            # sales status / dates / group
            sales_status = bt.get("salesStatus")
            row = {
                **travel_meta,
                # clés PAR DATE
                "tour_id": bt.get("id"),  # <-- identifiant unique de ce départ
                "url_precise": f"https://www.weroad.fr/destinations/{slug}/{bt.get('id')}" if bt.get("id") else None,
                "best_starting_date": bt.get("startingDate"),
                "best_ending_date": bt.get("endingDate"),
                "sales_status": sales_status,
                "seatsToConfirm": bt.get("seatsToConfirm"),
                "maxPax": bt.get("maxPax"),
                "weroadersCount": g(bt, ["groupInfo", "weroadersCount"]),
                # prix
                "price_eur": price,
                "base_price_eur": base,
                "discount_value_eur": disc_val,
                "discount_pct": disc_pct,
                "min_price_eur": min_p,
                "max_price_eur": max_p,
            }
            rows.append(row)

    df = pd.DataFrame(rows)

    # Mois pour analyses
    if not df.empty and "best_starting_date" in df.columns:
        df["month"] = df["best_starting_date"].map(to_month)

    # Filtrer lignes sans statut (demande précédente)
    if not df.empty:
        df = df.dropna(subset=["sales_status"])
        df = df[df["sales_status"].astype(str).str.strip() != ""]
    return df

# -------------------- Analyses --------------------
def weekly_kpis(df: pd.DataFrame) -> dict:
    out = {}
    for c in ["price_eur", "base_price_eur", "discount_value_eur", "discount_pct"]:
        series = df[c] if c in df else pd.Series(dtype=float)
        series = pd.to_numeric(series, errors="coerce").dropna()
        out[f"{c}_min"] = float(series.min()) if not series.empty else None
        out[f"{c}_max"] = float(series.max()) if not series.empty else None
        out[f"{c}_avg"] = float(series.mean()) if not series.empty else None
        out[f"{c}_med"] = float(series.median()) if not series.empty else None

    out["count_total"] = int(len(df))
    out["count_promos"] = int(df["discount_pct"].notna().sum())
    out["promo_share_pct"] = round(100 * out["count_promos"] / out["count_total"], 1) if out["count_total"] else 0.0

    s = df["month"].dropna() if "month" in df else pd.Series([], dtype=str)
    depart_by_month = s.value_counts().sort_index().to_dict()
    out["depart_by_month"] = json.dumps(depart_by_month, ensure_ascii=False)
    return out

def cheapest_by_destination(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=["destination_label", "price_eur"]).copy()
    if base.empty:
        return pd.DataFrame(columns=["destination_label","title","country_name","price_eur","url"])
    idxmin = base.groupby("destination_label")["price_eur"].idxmin()
    return base.loc[idxmin, ["destination_label","title","country_name","price_eur","url"]].reset_index(drop=True)

def weekly_diff(df_curr: pd.DataFrame, df_prev: pd.DataFrame | None) -> pd.DataFrame:
    """Comparaison 'meilleur prix par destination' pour le bloc 'Gros mouvements'."""
    L = cheapest_by_destination(df_curr)
    R = cheapest_by_destination(df_prev) if df_prev is not None and not df_prev.empty else L.iloc[0:0]
    diff = L.merge(R, on="destination_label", how="left", suffixes=("_curr","_prev"))
    diff["delta_abs"] = diff["price_eur_curr"] - diff["price_eur_prev"]
    diff["delta_pct"] = diff["delta_abs"] / diff["price_eur_prev"]
    diff.replace([np.inf, -np.inf], np.nan, inplace=True)
    diff["movement"] = diff["delta_abs"].apply(lambda v: "↓" if (pd.notna(v) and v < 0) else ("↑" if (pd.notna(v) and v > 0) else "="))
    # urls : on garde l'URL "voyage" (pas précise) ici
    diff["url"] = df_curr.set_index("destination_label").reindex(diff["destination_label"])["url"].values
    return diff

def monthly_kpis(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=["month"]).copy()
    if base.empty:
        return pd.DataFrame(columns=["month","destination_label","prix_min","prix_avg","nb_depart"])
    grp = base.groupby(["month", "destination_label"], dropna=False)
    agg = grp.agg(prix_min=("price_eur","min"), prix_avg=("price_eur","mean"), nb_depart=("tour_id","count")).reset_index()
    return agg

def monthly_diff(mo: pd.DataFrame) -> pd.DataFrame:
    mo = mo.sort_values(["destination_label","month"]).copy()
    for col in ["prix_min", "prix_avg", "nb_depart"]:
        mo[f"{col}_prev"] = mo.groupby("destination_label")[col].shift(1)
        mo[f"delta_{col}"] = mo[col] - mo[f"{col}_prev"]
        if col != "nb_depart":
            mo[f"delta_{col}_pct"] = mo[f"delta_{col}"] / mo[f"{col}_prev"]
    mo.replace([np.inf, -np.inf], np.nan, inplace=True)
    return mo

def find_alerts(weekly_diff_df: pd.DataFrame, pct_thr=0.10, abs_thr=150.0) -> pd.DataFrame:
    x = weekly_diff_df.copy()
    for c in ("delta_pct","delta_abs"):
        if c in x.columns:
            x[c] = pd.to_numeric(x[c], errors="coerce")
    x["flag"] = (x["delta_pct"].abs() > pct_thr) | (x["delta_abs"].abs() > abs_thr)
    cols = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url"]
    cols = [c for c in cols if c in x.columns]
    return x[x["flag"]].sort_values(["delta_pct","delta_abs"], ascending=[False,False])[cols]

def same_date_diff(df_curr: pd.DataFrame, df_prev: pd.DataFrame | None, min_abs_eur: float = 0.0) -> pd.DataFrame:
    """
    Comparaison 'même date' / même départ par tour_id :
      - on fait un INNER JOIN sur tour_id
      - on compare price_eur
    """
    if df_prev is None or df_prev.empty or df_curr.empty:
        return pd.DataFrame()

    left  = df_curr[["tour_id","slug","title","destination_label","country_name","best_starting_date",
                     "price_eur","sales_status","url_precise","url"]].copy()
    right = df_prev[["tour_id","price_eur"]].rename(columns={"price_eur":"price_eur_prev"}).copy()

    m = left.merge(right, on="tour_id", how="inner")
    m["price_eur_curr"] = m["price_eur"]
    m.drop(columns=["price_eur"], inplace=True)
    m["delta_abs"] = m["price_eur_curr"] - m["price_eur_prev"]
    m["delta_pct"] = m["delta_abs"] / m["price_eur_prev"]
    m["movement"] = m["delta_abs"].apply(lambda v: "↓" if (pd.notna(v) and v < 0) else ("↑" if (pd.notna(v) and v > 0) else "="))

    if min_abs_eur > 0:
        m = m[m["delta_abs"].abs() >= float(min_abs_eur)]
    m.replace([np.inf,-np.inf], np.nan, inplace=True)

    # colonnes finales attendues par summarize.py
    m = m[["tour_id","slug","title","destination_label","country_name","best_starting_date",
           "price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","sales_status","url_precise","url"]]
    return m.sort_values(["best_starting_date","destination_label","delta_abs"], ascending=[True, True, False])

# -------------------- Export / Persist --------------------
def export_excel(df_curr, wk_kpis, wk_diff, mo_kpis, mo_diff, alerts, out="weekly_report.xlsx"):
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        df_curr.to_excel(w, index=False, sheet_name="Dates_Week")
        pd.DataFrame([wk_kpis]).to_excel(w, index=False, sheet_name="Weekly_KPIs")
        wk_diff.sort_values(by=["delta_pct","delta_abs"], ascending=[False, False]).to_excel(
            w, index=False, sheet_name="Weekly_Diff"
        )
        alerts.to_excel(w, index=False, sheet_name="Alerts")
        mo_kpis.to_excel(w, index=False, sheet_name="Monthly_KPIs")
        mo_diff.to_excel(w, index=False, sheet_name="Monthly_Diff")
    logging.info("Exporté: %s", out)

def persist_sqlite(
    df_curr: pd.DataFrame,
    wk_kpis: dict,
    wk_diff: pd.DataFrame,
    mo_kpis: pd.DataFrame,
    mo_diff: pd.DataFrame,
    alerts: pd.DataFrame,
    same_date: pd.DataFrame,
    db_path: str,
    run_date: str,
):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        df_curr.assign(run_date=run_date).to_sql("snapshots", conn, if_exists="append", index=False)
        pd.DataFrame([{"run_date": run_date, **_sanitize_scalars(wk_kpis)}]).to_sql(
            "weekly_kpis", conn, if_exists="append", index=False
        )
        wk_diff.assign(run_date=run_date).to_sql("weekly_diff", conn, if_exists="append", index=False)
        mo_kpis.assign(run_date=run_date).to_sql("monthly_kpis", conn, if_exists="append", index=False)
        mo_diff.assign(run_date=run_date).to_sql("monthly_diff", conn, if_exists="append", index=False)
        alerts.assign(run_date=run_date).to_sql("alerts", conn, if_exists="append", index=False)
        if same_date is not None and not same_date.empty:
            same_date.assign(run_date=run_date).to_sql("same_date_diff", conn, if_exists="append", index=False)
    finally:
        conn.close()
    logging.info("Persisté SQLite: %s", db_path)

# -------------------- Main --------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="weekly_report.xlsx", help="Chemin du rapport Excel")
    ap.add_argument("--sqlite", default="data/weroad.db", help="Chemin de la base SQLite")
    ap.add_argument("--alert-pct", type=float, default=float(os.getenv("ALERT_PCT", 0.10)))
    ap.add_argument("--alert-eur", type=float, default=float(os.getenv("ALERT_EUR", 150.0)))
    ap.add_argument("--same-date-min-eur", type=float, default=float(os.getenv("SAME_DATE_MIN_EUR", 0.0)))
    args = ap.parse_args()

    run_date = datetime.utcnow().strftime("%Y-%m-%d")
    logging.info("Run date (UTC): %s", run_date)

    sess = session_with_headers()
    travels = fetch_travels_basic(sess)
    df_curr = normalize_per_date(travels, sess)

    # Charger dernier snapshot pour diff hebdo et same-date si DB existe
    df_prev = None
    if args.sqlite and Path(args.sqlite).exists():
        conn = sqlite3.connect(args.sqlite)
        try:
            runs = pd.read_sql_query("SELECT DISTINCT run_date FROM snapshots ORDER BY run_date", conn)
            if not runs.empty:
                last = runs["run_date"].iloc[-1]
                df_prev = pd.read_sql_query("SELECT * FROM snapshots WHERE run_date = ?", conn, params=(last,))
        finally:
            conn.close()

    wk_k = weekly_kpis(df_curr)
    wk_d = weekly_diff(df_curr, df_prev)
    mo_k = monthly_kpis(df_curr)
    mo_d = monthly_diff(mo_k)
    alerts = find_alerts(wk_d, pct_thr=args.alert_pct, abs_thr=args.alert_eur)
    same_d = same_date_diff(df_curr, df_prev, min_abs_eur=args.same_date_min_eur)

    export_excel(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, out=args.out)
    if args.sqlite:
        persist_sqlite(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, same_d, db_path=args.sqlite, run_date=run_date)

if __name__ == "__main__":
    main()
