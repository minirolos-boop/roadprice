# monitor.py
import os
import json
import sqlite3
import argparse
import logging
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

API_URL = "https://api-catalog.weroad.fr/travels"


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
        return None


def _sanitize_scalars(d: dict) -> dict:
    """Convertit dict/list en JSON str pour compatibilité SQLite."""
    out = {}
    for k, v in d.items():
        if isinstance(v, (dict, list)):
            out[k] = json.dumps(v, ensure_ascii=False)
        else:
            out[k] = v
    return out


# -------------------- Fetch + normalize --------------------
def fetch_travels():
    s = requests.Session()
    headers = {"accept": "application/json, text/plain, */*"}
    token = os.getenv("WEROAD_TOKEN")  # optionnel
    if token:
        headers["authorization"] = f"Bearer {token}"
    s.headers.update(headers)

    r = s.get(API_URL, timeout=30)
    r.raise_for_status()
    data = r.json()
    items = data.get("data", data) or []
    return items if isinstance(items, list) else []


def normalize(travels):
    rows = []
    for t in travels:
        bt = t.get("bestTour") or {}
        price = num(g(bt, ["price", "EUR"]))
        base = num(g(bt, ["basePrice", "EUR"]))

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

        rows.append(
            {
                "id": t.get("id"),
                "slug": t.get("slug"),
                "url": f"https://www.weroad.fr/voyages/{t.get('slug')}" if t.get("slug") else None,
                "title": t.get("title") or t.get("destinationLabel") or t.get("slug"),
                "destination_label": t.get("destinationLabel"),
                "country_name": g(t, ["primaryDestination", "name"]),
                "continent": g(t, ["primaryDestination", "primaryContinent", "name"]),
                "status": t.get("status"),
                "isBookable": t.get("isBookable"),
                "days": t.get("numberOfDays"),
                "style": g(t, ["travelStyle", "displayName"]),
                "types": ", ".join(
                    [x.get("displayName") for x in t.get("travelTypes", []) if x.get("displayName")]
                ),
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
    out["count_promos"] = int(df["discount_pct"].notna().sum())
    out["promo_share_pct"] = round(100 * out["count_promos"] / out["count_total"], 1) if out["count_total"] else 0.0

    # dict -> JSON pour SQLite
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
    return diff.reset_index()


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
    x = weekly_diff_df.copy()
    x["flag"] = (x["delta_pct"].abs() > pct_threshold) | (x["delta_abs"].abs() > abs_threshold)
    cols = [
        "destination_label",
        "title_curr",
        "price_eur_prev",
        "price_eur_curr",
        "delta_abs",
        "delta_pct",
        "movement",
        "url",
    ]
    cols = [c for c in cols if c in x.columns]
    return x[x["flag"]].sort_values(["delta_pct", "delta_abs"], ascending=[False, False])[cols]


# -------------------- Export / Persist --------------------
def export_excel(
    df_curr: pd.DataFrame,
    wk_kpis: dict,
    wk_diff: pd.DataFrame,
    mo_kpis: pd.DataFrame,
    mo_diff: pd.DataFrame,
    alerts: pd.DataFrame,
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
    logging.info("Exporté: %s", out)


def persist_sqlite(
    df_curr: pd.DataFrame,
    wk_kpis: dict,
    wk_diff: pd.DataFrame,
    mo_kpis: pd.DataFrame,
    mo_diff: pd.DataFrame,
    alerts: pd.DataFrame,
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
    args = ap.parse_args()

    run_date = datetime.now().strftime("%Y-%m-%d")
    logging.info("Run date: %s", run_date)

    items = fetch_travels()
    df_curr = normalize(items)

    # Charger dernier snapshot pour le diff hebdo si DB existe
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
    alerts = find_alerts(wk_d, pct_threshold=args.alert_pct, abs_threshold=args.alert_eur)

    export_excel(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, out=args.out)

    if args.sqlite:
        persist_sqlite(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, db_path=args.sqlite, run_date=run_date)


if __name__ == "__main__":
    main()
