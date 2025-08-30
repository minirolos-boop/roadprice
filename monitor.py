# monitor.py
# Collector + KPIs + persistance SQLite (avec auto-migration de schéma)
# + Récupération des TOURS (départs par date) et comparaison même-date

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
    headers = {"accept": "application/json, text/plain, */*"}
    token = os.getenv("WEROAD_TOKEN")
    if token:
        headers["authorization"] = f"Bearer {token}"
    s.headers.update(headers)
    return s


# -------------------- Fetch + normalize --------------------
def fetch_travels():
    with _session() as s:
        r = s.get(API_TRAVELS, timeout=45)
        r.raise_for_status()
        data = r.json()
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
    with _session() as s:
        r = s.get(url, timeout=45)
        r.raise_for_status()
        data = r.json()
    items = data.get("data", data) or []
    return items if isinstance(items, list) else []


def normalize_tours(travels: list[dict]) -> pd.DataFrame:
    rows = []
    for t in travels:
        slug = t.get("slug")
        if not slug:
            continue
        tours = fetch_tours_for_slug(slug)
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
    diff["delta_pct"] = diff["delta_abs"] / diff["price_eur_prev"]
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
    out["delta_pct"] = out["delta_abs"] / out["price_eur_prev"]
    out.replace([np.inf, -np.inf], np.nan, inplace=True)
    out["movement"] = out["delta_abs"].apply(
        lambda v: "↓" if (pd.notna(v) and v < 0) else ("↑" if (pd.notna(v) and v > 0) else "=")
    )
    return out


# -------------------- Export --------------------
def _to_excel_sorted(df: pd.DataFrame, writer, sheet_name: str, by=None, ascending=None):
    """
    Ecrit df dans Excel. Si 'by' est fourni et présent dans les colonnes, tri avant écriture.
    Tolérant si colonnes manquantes.
    """
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
        # Tri seulement si colonnes présentes (sinon on écrit tel quel)
        _to_excel_sorted(same_d, w, "Same_Date_Diff", by=["delta_pct", "delta_abs"], ascending=[False, False])
    logging.info("Exporté: %s", out)


# ---------- Auto-migration du schéma SQLite ----------
def _sqlite_type_from_series(s: pd.Series) -> str:
    import pandas.api.types as pt
    if pt.is_integer_dtype(s) or pt.is_bool_dtype(s):
        return "INTEGER"
    if pt.is_float_dtype(s):
        return "REAL"
    return "TEXT"


def ensure_sqlite_columns(conn: sqlite3.Connection, table: str, df: pd.DataFrame) -> None:
    cur = conn.execute(f'PRAGMA table_info("{table}")')
    existing = {row[1] for row in cur.fetchall()}
    missing = [c for c in df.columns if c not in existing]
    for c in missing:
        coltype = _sqlite_type_from_series(df[c])
        conn.execute(f'ALTER TABLE "{table}" ADD COLUMN "{c}" {coltype}')
    conn.commit()


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    cur = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1", (name,)
    )
    return cur.fetchone() is not None


def ensure_indexes(conn: sqlite3.Connection):
    try:
        if table_exists(conn, "snapshots"):
            conn.execute("CREATE INDEX IF NOT EXISTS idx_snapshots_run_ts ON snapshots(run_ts)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_snapshots_dest ON snapshots(destination_label)")
        if table_exists(conn, "weekly_diff"):
            conn.execute("CREATE INDEX IF NOT EXISTS idx_weekly_diff_run_ts ON weekly_diff(run_ts)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_weekly_diff_dest ON weekly_diff(destination_label)")
        if table_exists(conn, "weekly_kpis"):
            conn.execute("CREATE INDEX IF NOT EXISTS idx_weekly_kpis_run_ts ON weekly_kpis(run_ts)")
        if table_exists(conn, "monthly_kpis"):
            conn.execute("CREATE INDEX IF NOT EXISTS idx_monthly_kpis_run_ts ON monthly_kpis(run_ts)")
        if table_exists(conn, "monthly_diff"):
            conn.execute("CREATE INDEX IF NOT EXISTS idx_monthly_diff_run_ts ON monthly_diff(run_ts)")
        if table_exists(conn, "alerts"):
            conn.execute("CREATE INDEX IF NOT EXISTS idx_alerts_run_ts ON alerts(run_ts)")

        if table_exists(conn, "tours"):
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tours_run_ts ON tours(run_ts)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tours_tour_id ON tours(tour_id)")
        if table_exists(conn, "same_date_diff"):
            conn.execute("CREATE INDEX IF NOT EXISTS idx_same_date_diff_run_ts ON same_date_diff(run_ts)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_same_date_diff_tour_id ON same_date_diff(tour_id)")
        conn.commit()
    except Exception as e:
        logging.warning("ensure_indexes: %s", e)


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
        df_snap = df_curr.copy()
        df_snap["run_ts"] = run_ts
        try:
            ensure_sqlite_columns(conn, "snapshots", df_snap)
        except sqlite3.OperationalError:
            pass
        df_snap.to_sql("snapshots", conn, if_exists="append", index=False)

        wk_k_df = pd.DataFrame([{**wk_kpis, "run_ts": run_ts}])
        try:
            ensure_sqlite_columns(conn, "weekly_kpis", wk_k_df)
        except sqlite3.OperationalError:
            pass
        wk_k_df.to_sql("weekly_kpis", conn, if_exists="append", index=False)

        wk_diff2 = wk_diff.copy()
        wk_diff2["run_ts"] = run_ts
        try:
            ensure_sqlite_columns(conn, "weekly_diff", wk_diff2)
        except sqlite3.OperationalError:
            pass
        wk_diff2.to_sql("weekly_diff", conn, if_exists="append", index=False)

        mo_k_df = mo_kpis.copy()
        mo_k_df["run_ts"] = run_ts
        try:
            ensure_sqlite_columns(conn, "monthly_kpis", mo_k_df)
        except sqlite3.OperationalError:
            pass
        mo_k_df.to_sql("monthly_kpis", conn, if_exists="append", index=False)

        mo_diff2 = mo_diff.copy()
        mo_diff2["run_ts"] = run_ts
        try:
            ensure_sqlite_columns(conn, "monthly_diff", mo_diff2)
        except sqlite3.OperationalError:
            pass
        mo_diff2.to_sql("monthly_diff", conn, if_exists="append", index=False)

        alerts2 = alerts.copy()
        alerts2["run_ts"] = run_ts
        try:
            ensure_sqlite_columns(conn, "alerts", alerts2)
        except sqlite3.OperationalError:
            pass
        alerts2.to_sql("alerts", conn, if_exists="append", index=False)

        tours2 = df_tours.copy()
        tours2["run_ts"] = run_ts
        try:
            ensure_sqlite_columns(conn, "tours", tours2)
        except sqlite3.OperationalError:
            pass
        tours2.to_sql("tours", conn, if_exists="append", index=False)

        sdd2 = same_d.copy()
        sdd2["run_ts"] = run_ts
        try:
            ensure_sqlite_columns(conn, "same_date_diff", sdd2)
        except sqlite3.OperationalError:
            pass
        sdd2.to_sql("same_date_diff", conn, if_exists="append", index=False)

        ensure_indexes(conn)
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

    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    logging.info("Run timestamp (UTC): %s", run_ts)

    travels = fetch_travels()
    df_curr  = normalize_travels(travels)
    df_tours_curr = normalize_tours(travels)

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
        mo_k["delta_prix_min_pct"] = mo_k["delta_prix_min"] / mo_k["prix_min_prev"]
        mo_k["delta_prix_avg_pct"] = mo_k["delta_prix_avg"] / mo_k["prix_avg_prev"]
        mo_k.replace([np.inf, -np.inf], np.nan, inplace=True)
        mo_d = mo_k.copy()
    else:
        mo_k = pd.DataFrame(columns=["month","destination_label","prix_min","prix_avg","nb_depart"])
        mo_d = pd.DataFrame()

    alert_pct = float(os.getenv("ALERT_PCT", 0.10))
    alert_eur = float(os.getenv("ALERT_EUR", 150.0))
    if not wk_d.empty:
        wk_d["flag"] = (wk_d["delta_pct"].abs() > alert_pct) | (wk_d["delta_abs"].abs() > alert_eur)
        alerts = wk_d[wk_d["flag"]].copy()
    else:
        alerts = pd.DataFrame()

    sdd = same_date_diff(df_tours_curr, df_tours_prev)

    export_excel(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, df_tours_curr, sdd, out=args.out)

    if args.sqlite:
        persist_sqlite(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, df_tours_curr, sdd, db_path=args.sqlite, run_ts=run_ts)


if __name__ == "__main__":
    main()
