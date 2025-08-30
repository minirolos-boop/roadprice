# monitor.py
import os
import json
import sqlite3
import argparse
import logging
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

API_TRAVELS = "https://api-catalog.weroad.fr/travels"
API_TOURS   = "https://api-catalog.weroad.fr/travels/{slug}/tours"

# -------------------- Utils --------------------
def _get(d, path, default=None):
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
        return pd.to_datetime(s).strftime("%Y-%m")
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

def _dt_utc_now_iso():
    # string ISO courte et stable: 2025-08-30T10:32:28Z
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# -------------------- Fetch --------------------
def _session():
    s = requests.Session()
    headers = {"accept": "application/json, text/plain, */*"}
    token = os.getenv("WEROAD_TOKEN")
    if token:
        headers["authorization"] = f"Bearer {token}"
    s.headers.update(headers)
    return s

def fetch_travels():
    s = _session()
    r = s.get(API_TRAVELS, timeout=30)
    r.raise_for_status()
    data = r.json()
    items = data.get("data", data) or []
    return items if isinstance(items, list) else []

def fetch_tours_for_slug(slug: str) -> list[dict]:
    s = _session()
    url = API_TOURS.format(slug=slug)
    r = s.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    items = data.get("data", data) or []
    return items if isinstance(items, list) else []

# -------------------- Normalize --------------------
def normalize_travels(travels: list[dict]) -> pd.DataFrame:
    rows = []
    for t in travels:
        bt = t.get("bestTour") or {}
        price = num(_get(bt, ["price", "EUR"]))
        base  = num(_get(bt, ["basePrice", "EUR"]))

        disc_val = disc_pct = None
        if price is not None and base is not None and base > price:
            disc_val = base - price
            disc_pct = round((base - price) / base * 100.0, 1)

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
        rows.append(
            {
                "id": t.get("id"),
                "slug": slug,
                "url": f"https://www.weroad.fr/destinations/{slug}" if slug else None,
                "title": t.get("title") or t.get("destinationLabel") or slug,
                "destination_label": t.get("destinationLabel"),
                "country_name": _get(t, ["primaryDestination", "name"]),
                "continent": _get(t, ["primaryDestination", "primaryContinent", "name"]),
                "status": t.get("status"),
                "isBookable": t.get("isBookable"),
                "days": t.get("numberOfDays"),
                "style": _get(t, ["travelStyle", "displayName"]),
                "types": ", ".join([x.get("displayName") for x in t.get("travelTypes", []) if x.get("displayName")]),
                "price_eur": price,
                "base_price_eur": base,
                "discount_value_eur": disc_val,
                "discount_pct": disc_pct,
                "sales_status": _get(bt, ["salesStatus"]),
                "seatsToConfirm": _get(bt, ["seatsToConfirm"]),
                "maxPax": _get(bt, ["maxPax"]),
                "weroadersCount": _get(bt, ["groupInfo", "weroadersCount"]),
                "min_price_eur": min_p,
                "max_price_eur": max_p,
                "best_starting_date": _get(bt, ["startingDate"]),
                "best_ending_date": _get(bt, ["endingDate"]),
                "rating": _get(t, ["userRating", "rating"]),
                "rating_count": _get(t, ["userRating", "count"]),
            }
        )
    df = pd.DataFrame(rows)
    df["month"] = df["best_starting_date"].map(to_month)
    # garder que les voyages avec un sales_status non vide
    if not df.empty:
        df = df.dropna(subset=["sales_status"])
        df = df[df["sales_status"].astype(str).str.strip() != ""]
    return df

def normalize_tours(slug: str, tours_json: list[dict]) -> pd.DataFrame:
    rows = []
    for t in tours_json or []:
        rows.append({
            "slug": slug,
            "tour_id": _get(t, ["id"]),
            "date_start": _get(t, ["startingDate"]),
            "date_end": _get(t, ["endingDate"]),
            "status": _get(t, ["salesStatus"]),
            "price_eur": _get(t, ["price", "EUR"]),
            "base_price_eur": _get(t, ["basePrice", "EUR"]),
            # coordinator
            "coordinator_id": _get(t, ["coordinator", "id"]),
            "coordinator_nickname": (_get(t, ["coordinator", "nickname"]) or "").strip(),
            "coordinator_city": (_get(t, ["coordinator", "city"]) or "").strip(),
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df["url_precise"] = df.apply(
            lambda r: f"https://www.weroad.fr/destinations/{r['slug']}/{r['tour_id']}" if pd.notna(r["tour_id"]) else None,
            axis=1
        )
    return df

def build_df_tours(df_curr: pd.DataFrame) -> pd.DataFrame:
    if df_curr is None or df_curr.empty:
        return pd.DataFrame()
    frames = []
    for slug in sorted(df_curr["slug"].dropna().unique()):
        try:
            tours = fetch_tours_for_slug(slug)
            frames.append(normalize_tours(slug, tours))
        except Exception as e:
            logging.warning("Tours fetch failed for slug %s: %s", slug, e)
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True)
    # map some label for join convenience
    lab = df_curr[["slug", "destination_label", "title", "country_name"]].drop_duplicates()
    out = out.merge(lab, on="slug", how="left")
    return out

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
    out["count_promos"] = int(df["discount_pct"].notna().sum())
    out["promo_share_pct"] = round(100 * out["count_promos"] / out["count_total"], 1) if out["count_total"] else 0.0

    s = df["month"].dropna()
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
    diff["delta_pct"] = diff["delta_abs"] / diff["price_eur_prev"]
    diff.replace([np.inf, -np.inf], np.nan, inplace=True)
    diff["movement"] = diff["delta_abs"].apply(
        lambda v: "↓" if (pd.notna(v) and v < 0) else ("↑" if (pd.notna(v) and v > 0) else "=")
    )
    # url (curr)
    diff = diff.reset_index()
    url_map = df_curr.set_index(["destination_label"])["url"].to_dict()
    diff["url"] = diff["destination_label"].map(url_map)
    return diff

def monthly_kpis(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=["month"]).copy()
    grp = base.groupby(["month", "destination_label"], dropna=False)
    agg = grp.agg(
        prix_min=("price_eur", "min"),
        prix_avg=("price_eur", "mean"),
        nb_depart=("best_starting_date", "count"),
    ).reset_index()
    return agg

def monthly_diff(mo: pd.DataFrame) -> pd.DataFrame:
    mo = mo.sort_values(["destination_label", "month"]).copy()
    for col in ["prix_min", "prix_avg", "nb_depart"]:
        mo[f"{col}_prev"] = mo.groupby("destination_label")[col].shift(1)
        mo[f"delta_{col}"] = mo[col] - mo[f"{col}_prev"]
        if col != "nb_depart":
            mo[f"delta_{col}_pct"] = mo[f"delta_{col}"] / mo[f"{col}_prev"]
    mo.replace([np.inf, -np.inf], np.nan, inplace=True)
    return mo

def find_alerts(weekly_diff_df: pd.DataFrame, pct_threshold=0.10, abs_threshold=150.0) -> pd.DataFrame:
    if weekly_diff_df is None or weekly_diff_df.empty:
        return pd.DataFrame(columns=["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url"])
    x = weekly_diff_df.copy()
    x["flag"] = (x["delta_pct"].abs() > pct_threshold) | (x["delta_abs"].abs() > abs_threshold)
    cols = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url"]
    cols = [c for c in cols if c in x.columns]
    out = x[x["flag"]].sort_values(["delta_pct","delta_abs"], ascending=[False,False])[cols].reset_index(drop=True)
    return out

def same_date_price_diff(df_tours_curr: pd.DataFrame, df_tours_prev: pd.DataFrame) -> pd.DataFrame:
    """Compare, pour un même tour_id, le prix courant vs précédent."""
    if df_tours_curr is None or df_tours_curr.empty or df_tours_prev is None or df_tours_prev.empty:
        return pd.DataFrame(columns=["tour_id","slug","destination_label","price_prev","price_curr","delta_abs","delta_pct","url_precise"])

    L = df_tours_curr[["tour_id","slug","destination_label","price_eur","url_precise"]].dropna(subset=["tour_id"]).copy()
    R = df_tours_prev[["tour_id","price_eur"]].dropna(subset=["tour_id"]).copy()
    R = R.rename(columns={"price_eur": "price_prev"})
    diff = L.merge(R, on="tour_id", how="left")
    diff = diff[diff["price_prev"].notna()].copy()
    diff.rename(columns={"price_eur": "price_curr"}, inplace=True)
    diff["delta_abs"] = diff["price_curr"] - diff["price_prev"]
    diff["delta_pct"] = diff["delta_abs"] / diff["price_prev"]
    diff.replace([np.inf, -np.inf], np.nan, inplace=True)
    # tri par variation la plus forte
    diff = diff.sort_values(["delta_pct","delta_abs"], ascending=[False, False]).reset_index(drop=True)
    return diff

def coordinator_stats(df_tours: pd.DataFrame) -> pd.DataFrame:
    """Classement des coordinateurs (nb d'apparitions sur le run courant)."""
    if df_tours is None or df_tours.empty:
        return pd.DataFrame(columns=["coordinator_id","coordinator_nickname","appearances"])
    x = df_tours.dropna(subset=["coordinator_id"]).copy()
    x["coordinator_nickname"] = x["coordinator_nickname"].fillna("").replace("", "(sans pseudo)")
    grp = (x.groupby(["coordinator_id","coordinator_nickname"], dropna=False)
             .size()
             .reset_index(name="appearances")
             .sort_values(["appearances","coordinator_nickname"], ascending=[False, True]))
    return grp

# -------------------- Export / Persist --------------------
def export_excel(
    df_curr: pd.DataFrame,
    wk_kpis: dict,
    wk_diff: pd.DataFrame,
    mo_kpis: pd.DataFrame,
    mo_diff: pd.DataFrame,
    alerts: pd.DataFrame,
    df_tours: pd.DataFrame,
    same_date_diff: pd.DataFrame,
    coord_stats: pd.DataFrame,
    out="weekly_report.xlsx",
):
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        df_curr.to_excel(w, index=False, sheet_name="Voyages_Week")
        pd.DataFrame([wk_kpis]).to_excel(w, index=False, sheet_name="Weekly_KPIs")
        wk_diff.sort_values(by=["delta_pct", "delta_abs"], ascending=[False, False]).to_excel(
            w, index=False, sheet_name="Weekly_Diff"
        )
        alerts.to_excel(w, index=False, sheet_name="Alerts")
        mo_kpis.to_excel(w, index=False, sheet_name="Monthly_KPIs")
        mo_diff.to_excel(w, index=False, sheet_name="Monthly_Diff")
        df_tours.to_excel(w, index=False, sheet_name="Tours_View")
        same_date_diff.to_excel(w, index=False, sheet_name="SameDateDiff")
        coord_stats.to_excel(w, index=False, sheet_name="Coordinators")
    logging.info("Exporté: %s", out)

def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    cur = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1;", (name,))
    return cur.fetchone() is not None

def persist_sqlite(
    df_curr: pd.DataFrame,
    wk_kpis: dict,
    wk_diff: pd.DataFrame,
    mo_kpis: pd.DataFrame,
    mo_diff: pd.DataFrame,
    alerts: pd.DataFrame,
    df_tours: pd.DataFrame,
    same_date_diff: pd.DataFrame,
    coord_stats: pd.DataFrame,
    db_path: str,
    run_ts: str,
):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        df_curr.assign(run_date=run_ts).to_sql("snapshots", conn, if_exists="append", index=False)
        pd.DataFrame([{"run_date": run_ts, **_sanitize_scalars(wk_kpis)}]).to_sql(
            "weekly_kpis", conn, if_exists="append", index=False
        )
        wk_diff.assign(run_date=run_ts).to_sql("weekly_diff", conn, if_exists="append", index=False)
        mo_kpis.assign(run_date=run_ts).to_sql("monthly_kpis", conn, if_exists="append", index=False)
        mo_diff.assign(run_date=run_ts).to_sql("monthly_diff", conn, if_exists="append", index=False)
        alerts.assign(run_date=run_ts).to_sql("alerts", conn, if_exists="append", index=False)
        df_tours.assign(run_date=run_ts).to_sql("tours", conn, if_exists="append", index=False)
        same_date_diff.assign(run_date=run_ts).to_sql("same_date_diff", conn, if_exists="append", index=False)
        coord_stats.assign(run_date=run_ts).to_sql("coordinator_stats", conn, if_exists="append", index=False)
    finally:
        conn.close()
    logging.info("Persisté SQLite: %s", db_path)

def ensure_indexes(db_path: str):
    conn = sqlite3.connect(db_path)
    try:
        # créer index uniquement si la table existe (évite "no such table")
        def idx(table: str, sql: str):
            if _table_exists(conn, table):
                conn.execute(sql)

        idx("tours", "CREATE INDEX IF NOT EXISTS idx_tours_run ON tours(run_date);")
        idx("tours", "CREATE INDEX IF NOT EXISTS idx_tours_coord ON tours(coordinator_id);")

        idx("coordinator_stats", "CREATE INDEX IF NOT EXISTS idx_coordstats_run ON coordinator_stats(run_date);")
        idx("coordinator_stats", "CREATE INDEX IF NOT EXISTS idx_coordstats_coord ON coordinator_stats(coordinator_id);")

        idx("same_date_diff", "CREATE INDEX IF NOT EXISTS idx_samedate_run ON same_date_diff(run_date);")
        idx("weekly_diff", "CREATE INDEX IF NOT EXISTS idx_weeklydiff_run ON weekly_diff(run_date);")
        idx("snapshots", "CREATE INDEX IF NOT EXISTS idx_snapshots_run ON snapshots(run_date);")
    finally:
        conn.close()

# -------------------- Main --------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="weekly_report.xlsx", help="Chemin du rapport Excel")
    ap.add_argument("--sqlite", default="data/weroad.db", help="Chemin de la base SQLite")
    ap.add_argument("--alert-pct", type=float, default=float(os.getenv("ALERT_PCT", 0.10)))
    ap.add_argument("--alert-eur", type=float, default=float(os.getenv("ALERT_EUR", 150.0)))
    args = ap.parse_args()

    run_ts = _dt_utc_now_iso()
    logging.info("Run timestamp (UTC): %s", run_ts)

    travels = fetch_travels()
    df_curr = normalize_travels(travels)

    # Previous run snapshots (for weekly_diff)
    df_prev = None
    df_tours_prev = pd.DataFrame()
    last_run = None
    if args.sqlite and Path(args.sqlite).exists():
        conn = sqlite3.connect(args.sqlite)
        try:
            runs = pd.read_sql_query(
                "SELECT MAX(run_date) AS last_run FROM snapshots;", conn
            )
            if not runs.empty and pd.notna(runs.loc[0, "last_run"]):
                last_run = runs.loc[0, "last_run"]
                df_prev = pd.read_sql_query("SELECT * FROM snapshots WHERE run_date = ?", conn, params=(last_run,))
                # tours du run précédent (pour same-date diff)
                if _table_exists(conn, "tours"):
                    df_tours_prev = pd.read_sql_query("SELECT * FROM tours WHERE run_date = ?", conn, params=(last_run,))
        finally:
            conn.close()

    wk_k = weekly_kpis(df_curr)
    wk_d = weekly_diff(df_curr, df_prev)
    mo_k = monthly_kpis(df_curr)
    mo_d = monthly_diff(mo_k)
    alerts = find_alerts(wk_d, pct_threshold=args.alert_pct, abs_threshold=args.alert_eur)

    # tours (toutes dates de chaque slug)
    df_tours_curr = build_df_tours(df_curr)
    same_date_diffs = same_date_price_diff(df_tours_curr, df_tours_prev)
    coord_stats = coordinator_stats(df_tours_curr)

    export_excel(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, df_tours_curr, same_date_diffs, coord_stats, out=args.out)

    if args.sqlite:
        persist_sqlite(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, df_tours_curr, same_date_diffs, coord_stats,
                       db_path=args.sqlite, run_ts=run_ts)
        ensure_indexes(args.sqlite)

if __name__ == "__main__":
    main()
