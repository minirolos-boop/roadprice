# monitor.py — Snapshot par DATE (tour_id), diffs & persistance run_ts
import os
import json
import time
import sqlite3
import argparse
import logging
from pathlib import Path
from datetime import datetime, UTC

import numpy as np
import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

API_TRAVELS = "https://api-catalog.weroad.fr/travels"
API_TOURS   = "https://api-catalog.weroad.fr/travels/{slug}/tours"

# -------- Utils --------
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
        out[k] = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
    return out

def ensure_data_dir():
    Path("data").mkdir(parents=True, exist_ok=True)

# -------- HTTP session & fetch --------
def session_with_headers() -> requests.Session:
    s = requests.Session()
    headers = {"accept": "application/json, text/plain, */*"}
    token = os.getenv("WEROAD_TOKEN")  # optionnel
    if token:
        headers["authorization"] = f"Bearer {token}"
    s.headers.update(headers)
    return s

def fetch_travels_basic(sess: requests.Session) -> list[dict]:
    r = sess.get(API_TRAVELS, timeout=30)
    r.raise_for_status()
    data = r.json()
    items = data.get("data", data) or []
    return items if isinstance(items, list) else []

def fetch_tours_for_slug(sess: requests.Session, slug: str, max_retry: int = 3) -> list[dict]:
    url = API_TOURS.format(slug=slug)
    for attempt in range(max_retry):
        try:
            r = sess.get(url, timeout=30)
            r.raise_for_status()
            data = r.json()
            items = data.get("data", data) or []
            return items if isinstance(items, list) else []
        except Exception as e:
            backoff = 1.0 * (attempt + 1)
            logging.warning("fetch_tours_for_slug(%s) error: %s (retry in %.1fs)", slug, e, backoff)
            time.sleep(backoff)
    return []

# -------- Normalisation: 1 ligne = 1 départ (tour_id) --------
def normalize_per_date(travels: list[dict], sess: requests.Session, sleep_between_slugs: float = 0.2) -> pd.DataFrame:
    rows = []
    for t in travels:
        slug = t.get("slug")
        if not slug:
            continue

        # métadonnées "voyage"
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
        # politesse API
        if sleep_between_slugs > 0:
            time.sleep(float(sleep_between_slugs))

        for tour in tours:
            price = num(g(tour, ["price", "EUR"]))
            base  = num(g(tour, ["basePrice", "EUR"]))

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

            rows.append({
                **travel_meta,
                "tour_id": tour.get("id"),
                "url_precise": f"https://www.weroad.fr/destinations/{slug}/{tour.get('id')}" if tour.get("id") else None,
                "best_starting_date": tour.get("startingDate"),
                "best_ending_date": tour.get("endingDate"),
                "sales_status": tour.get("salesStatus"),
                "seatsToConfirm": tour.get("seatsToConfirm"),
                "maxPax": tour.get("maxPax"),
                "weroadersCount": g(tour, ["groupInfo", "weroadersCount"]),
                "price_eur": price,
                "base_price_eur": base,
                "discount_value_eur": disc_val,
                "discount_pct": disc_pct,
                "min_price_eur": min_p,
                "max_price_eur": max_p,
            })

    df = pd.DataFrame(rows)

    if not df.empty and "best_starting_date" in df.columns:
        df["month"] = df["best_starting_date"].map(to_month)

    # filtre: sales_status requis
    if not df.empty:
        df = df.dropna(subset=["sales_status"])
        df = df[df["sales_status"].astype(str).str.strip() != ""]

    return df

# -------- Analyses --------
def weekly_kpis(df: pd.DataFrame) -> dict:
    out = {}
    for c in ["price_eur", "base_price_eur", "discount_value_eur", "discount_pct"]:
        s = pd.to_numeric(df[c], errors="coerce") if c in df else pd.Series(dtype=float)
        s = s.dropna()
        out[f"{c}_min"] = float(s.min()) if not s.empty else None
        out[f"{c}_max"] = float(s.max()) if not s.empty else None
        out[f"{c}_avg"] = float(s.mean()) if not s.empty else None
        out[f"{c}_med"] = float(s.median()) if not s.empty else None

    out["count_total"] = int(len(df))
    out["count_promos"] = int(pd.to_numeric(df["discount_pct"], errors="coerce").notna().sum()) if "discount_pct" in df else 0
    out["promo_share_pct"] = round(100 * out["count_promos"] / out["count_total"], 1) if out["count_total"] else 0.0

    s = df["month"].dropna() if "month" in df else pd.Series([], dtype=str)
    out["depart_by_month"] = json.dumps(s.value_counts().sort_index().to_dict(), ensure_ascii=False)
    return out

def cheapest_by_destination(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=["destination_label", "price_eur"]).copy()
    if base.empty:
        return pd.DataFrame(columns=["destination_label","title","country_name","price_eur","url","url_precise"])
    idx = base.groupby("destination_label")["price_eur"].idxmin()
    return base.loc[idx, ["destination_label","title","country_name","price_eur","url","url_precise"]].reset_index(drop=True)

def weekly_diff(df_curr: pd.DataFrame, df_prev: pd.DataFrame | None) -> pd.DataFrame:
    """Compare prix MIN par destination (run courant vs précédent)."""
    if df_curr.empty:
        return pd.DataFrame()

    L = cheapest_by_destination(df_curr).rename(columns={"title":"title_curr","price_eur":"price_eur_curr"})
    if df_prev is None or df_prev.empty:
        R = pd.DataFrame(columns=["destination_label","title_prev","price_eur_prev","url","url_precise"])
    else:
        R = cheapest_by_destination(df_prev).rename(columns={"title":"title_prev","price_eur":"price_eur_prev"})

    diff = L.merge(R, on="destination_label", how="left", suffixes=("_curr","_prev"))
    diff["delta_abs"] = pd.to_numeric(diff["price_eur_curr"], errors="coerce") - pd.to_numeric(diff["price_eur_prev"], errors="coerce")
    base_prev = pd.to_numeric(diff["price_eur_prev"], errors="coerce")
    diff["delta_pct"] = diff["delta_abs"] / base_prev
    diff.replace([np.inf, -np.inf], np.nan, inplace=True)
    diff["movement"] = diff["delta_abs"].apply(lambda v: "↓" if (pd.notna(v) and v < 0) else ("↑" if (pd.notna(v) and v > 0) else "="))
    # prioriser url_precise si dispo
    diff["url"] = diff.get("url_precise_curr", pd.Series(index=diff.index)).fillna(diff.get("url_curr"))
    return diff.reset_index(drop=True)

def monthly_kpis(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=["month"]).copy()
    if base.empty:
        return pd.DataFrame(columns=["month","destination_label","prix_min","prix_avg","nb_depart"])
    grp = base.groupby(["month", "destination_label"], dropna=False)
    agg = grp.agg(prix_min=("price_eur","min"), prix_avg=("price_eur","mean"), nb_depart=("tour_id","count")).reset_index()
    return agg

def monthly_diff(mo: pd.DataFrame) -> pd.DataFrame:
    mo = mo.sort_values(["destination_label","month"]).copy()
    for col in ["prix_min","prix_avg","nb_depart"]:
        mo[f"{col}_prev"] = mo.groupby("destination_label")[col].shift(1)
        mo[f"delta_{col}"] = mo[col] - mo[f"{col}_prev"]
        if col != "nb_depart":
            mo[f"delta_{col}_pct"] = mo[f"delta_{col}"] / mo[f"{col}_prev"]
    mo.replace([np.inf, -np.inf], np.nan, inplace=True)
    return mo

def find_alerts(weekly_diff_df: pd.DataFrame, pct_thr=0.10, abs_thr=150.0) -> pd.DataFrame:
    if weekly_diff_df.empty:
        return pd.DataFrame()
    x = weekly_diff_df.copy()
    x["delta_pct"] = pd.to_numeric(x.get("delta_pct"), errors="coerce").fillna(0.0)
    x["delta_abs"] = pd.to_numeric(x.get("delta_abs"), errors="coerce").fillna(0.0)
    x["flag"] = (x["delta_pct"].abs() > pct_thr) | (x["delta_abs"].abs() > abs_thr)
    cols = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url"]
    cols = [c for c in cols if c in x.columns]
    return x[x["flag"]].sort_values(["delta_pct","delta_abs"], ascending=[False,False])[cols]

def same_date_diff(df_curr: pd.DataFrame, df_prev: pd.DataFrame | None, min_abs_eur: float = 0.0) -> pd.DataFrame:
    """Compare PRIX sur le même départ (même tour_id) entre runs."""
    if df_prev is None or df_prev.empty or df_curr.empty:
        return pd.DataFrame()

    left  = df_curr[["tour_id","slug","title","destination_label","country_name","best_starting_date",
                     "price_eur","sales_status","url_precise","url"]].copy()
    right = df_prev[["tour_id","price_eur"]].rename(columns={"price_eur":"price_eur_prev"}).copy()

    m = left.merge(right, on="tour_id", how="inner")
    m["price_eur_curr"] = pd.to_numeric(m["price_eur"], errors="coerce")
    m["price_eur_prev"] = pd.to_numeric(m["price_eur_prev"], errors="coerce")
    m.drop(columns=["price_eur"], inplace=True)

    m["delta_abs"] = m["price_eur_curr"] - m["price_eur_prev"]
    m["delta_pct"] = m["delta_abs"] / m["price_eur_prev"]
    m.replace([np.inf, -np.inf], np.nan, inplace=True)
    m["movement"] = m["delta_abs"].apply(lambda v: "↓" if (pd.notna(v) and v < 0) else ("↑" if (pd.notna(v) and v > 0) else "="))

    if min_abs_eur > 0:
        m = m[m["delta_abs"].abs() >= float(min_abs_eur)]

    cols = ["tour_id","slug","title","destination_label","country_name","best_starting_date",
            "price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","sales_status","url_precise","url"]
    return m[cols].sort_values(["best_starting_date","destination_label","delta_abs"], ascending=[True, True, False])

# -------- Export & Persist --------
def export_excel(df_curr, wk_kpis, wk_diff, mo_kpis, mo_diff, alerts, same_date, out="weekly_report.xlsx"):
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        df_curr.to_excel(w, index=False, sheet_name="Dates_Week")
        pd.DataFrame([wk_kpis]).to_excel(w, index=False, sheet_name="Weekly_KPIs")
        wk_diff.sort_values(by=["delta_pct","delta_abs"], ascending=[False, False]).to_excel(w, index=False, sheet_name="Weekly_Diff")
        alerts.to_excel(w, index=False, sheet_name="Alerts")
        same_date.to_excel(w, index=False, sheet_name="SameDate_Diff")
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
    run_ts: str,
):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        df_curr.assign(run_ts=run_ts).to_sql("snapshots", conn, if_exists="append", index=False)
        pd.DataFrame([{"run_ts": run_ts, **_sanitize_scalars(wk_kpis)}]).to_sql("weekly_kpis", conn, if_exists="append", index=False)
        wk_diff.assign(run_ts=run_ts).to_sql("weekly_diff", conn, if_exists="append", index=False)
        mo_kpis.assign(run_ts=run_ts).to_sql("monthly_kpis", conn, if_exists="append", index=False)
        mo_diff.assign(run_ts=run_ts).to_sql("monthly_diff", conn, if_exists="append", index=False)
        alerts.assign(run_ts=run_ts).to_sql("alerts", conn, if_exists="append", index=False)
        if same_date is not None and not same_date.empty:
            same_date.assign(run_ts=run_ts).to_sql("same_date_diff", conn, if_exists="append", index=False)
    finally:
        conn.close()
    logging.info("Persisté SQLite: %s", db_path)

def ensure_indexes(db_path: str):
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript("""
            CREATE INDEX IF NOT EXISTS idx_snapshots_run_ts ON snapshots(run_ts);
            CREATE INDEX IF NOT EXISTS idx_snapshots_tour   ON snapshots(tour_id);
            CREATE INDEX IF NOT EXISTS idx_weekly_diff_run  ON weekly_diff(run_ts);
            CREATE INDEX IF NOT EXISTS idx_same_date_run    ON same_date_diff(run_ts);
            CREATE INDEX IF NOT EXISTS idx_monthly_kpis_run ON monthly_kpis(run_ts);
        """)
        conn.commit()
    finally:
        conn.close()

# -------- Main --------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="weekly_report.xlsx", help="Chemin du rapport Excel")
    ap.add_argument("--sqlite", default="data/weroad.db", help="Chemin de la base SQLite")
    ap.add_argument("--alert-pct", type=float, default=float(os.getenv("ALERT_PCT", 0.10)))
    ap.add_argument("--alert-eur", type=float, default=float(os.getenv("ALERT_EUR", 150.0)))
    ap.add_argument("--same-date-min-eur", type=float, default=float(os.getenv("SAME_DATE_MIN_EUR", 0.0)))
    ap.add_argument("--sleep-between-slugs", type=float, default=float(os.getenv("WEROAD_SLEEP_BETWEEN_SLUGS", 0.2)))
    args = ap.parse_args()

    ensure_data_dir()

    run_ts = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    logging.info("Run timestamp (UTC): %s", run_ts)

    sess = session_with_headers()
    travels = fetch_travels_basic(sess)
    df_curr = normalize_per_date(travels, sess, sleep_between_slugs=args.sleep_between_slugs)

    # Charger run précédent
    df_prev = None
    last_ts_prev = None
    if args.sqlite and Path(args.sqlite).exists():
        conn = sqlite3.connect(args.sqlite)
        try:
            runs = pd.read_sql_query("SELECT DISTINCT run_ts FROM snapshots ORDER BY run_ts", conn)
            if not runs.empty:
                last_ts_prev = runs["run_ts"].iloc[-1]
                df_prev = pd.read_sql_query("SELECT * FROM snapshots WHERE run_ts = ?", conn, params=(last_ts_prev,))
        finally:
            conn.close()

    wk_k = weekly_kpis(df_curr)
    wk_d = weekly_diff(df_curr, df_prev)
    mo_k = monthly_kpis(df_curr)
    mo_d = monthly_diff(mo_k)
    alerts = find_alerts(wk_d, pct_thr=args.alert_pct, abs_thr=args.alert_eur)
    same_d = same_date_diff(df_curr, df_prev, min_abs_eur=args.same_date_min_eur)

    export_excel(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, same_d, out=args.out)

    if args.sqlite:
        persist_sqlite(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, same_d, db_path=args.sqlite, run_ts=run_ts)
        ensure_indexes(args.sqlite)

if __name__ == "__main__":
    main()
