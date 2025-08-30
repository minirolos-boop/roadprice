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

def _now_iso_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ---------- SQLite helpers (compat & migration) ----------
def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    cur = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1;", (name,))
    return cur.fetchone() is not None

def table_columns(conn: sqlite3.Connection, name: str) -> set[str]:
    cur = conn.execute(f'PRAGMA table_info("{name}")')
    return {row[1] for row in cur.fetchall()}

def pandas_dtype_to_sql(s: pd.Series) -> str:
    import pandas.api.types as pt
    if pt.is_integer_dtype(s) or pt.is_bool_dtype(s):
        return "INTEGER"
    if pt.is_float_dtype(s):
        return "REAL"
    return "TEXT"

def ensure_table_has_columns(conn: sqlite3.Connection, table: str, df: pd.DataFrame):
    """Ajoute dans SQLite les colonnes manquantes pour accueillir df (ALTER TABLE ...)."""
    if not table_exists(conn, table):
        return  # to_sql créera la table au premier append
    existing = table_columns(conn, table)
    missing = [c for c in df.columns if c not in existing]
    for c in missing:
        coltype = pandas_dtype_to_sql(df[c])
        conn.execute(f'ALTER TABLE "{table}" ADD COLUMN "{c}" {coltype}')
    conn.commit()

def pick_run_col(conn: sqlite3.Connection, table: str) -> str | None:
    """Retourne 'run_date' ou 'run_ts' si présent dans la table, sinon None."""
    if not table_exists(conn, table):
        return None
    cols = table_columns(conn, table)
    if "run_date" in cols:
        return "run_date"
    if "run_ts" in cols:
        return "run_ts"
    return None

def ensure_indexes(conn: sqlite3.Connection, table: str, run_col: str | None, extra: list[tuple[str,str]] = None):
    try:
        if run_col and table_exists(conn, table):
            conn.execute(f'CREATE INDEX IF NOT EXISTS idx_{table}_{run_col} ON {table}({run_col});')
        if extra:
            for t, sql in extra:
                if table_exists(conn, t):
                    conn.execute(sql)
        conn.commit()
    except Exception as e:
        logging.warning("ensure_indexes(%s): %s", table, e)

# -------------------- Fetch --------------------
def _session():
    s = requests.Session()
    headers = {"accept": "application/json, text/plain, */*"}
    token = os.getenv("WEROAD_TOKEN")
    if token:
        headers["authorization"] = f"Bearer {token}"
    s.headers.update(headers)
    return s

def fetch_travels() -> list[dict]:
    with _session() as s:
        r = s.get(API_TRAVELS, timeout=45)
        r.raise_for_status()
        data = r.json()
    items = data.get("data", data) or []
    return items if isinstance(items, list) else []

def fetch_tours_for_slug(slug: str) -> list[dict]:
    with _session() as s:
        url = API_TOURS.format(slug=slug)
        r = s.get(url, timeout=45)
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
    if not df.empty:
        df = df.dropna(subset=["sales_status"])
        df = df[df["sales_status"].astype(str).str.strip() != ""]
    return df

def normalize_tours(slug: str, tours_json: list[dict], meta: dict) -> pd.DataFrame:
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
            # meta from travels
            "destination_label": meta.get("destination_label"),
            "title": meta.get("title"),
            "country_name": meta.get("country_name"),
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
    for slug, meta in df_curr.set_index("slug")[["destination_label","title","country_name"]].dropna().to_dict("index").items():
        try:
            tours = fetch_tours_for_slug(slug)
            frames.append(normalize_tours(slug, tours, meta))
        except Exception as e:
            logging.warning("Tours fetch failed for slug %s: %s", slug, e)
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True)
    # filtre status vide
    out = out[out["status"].astype(str).str.strip() != ""]
    return out

# -------------------- Analyses --------------------
def weekly_kpis(df: pd.DataFrame) -> dict:
    out = {}
    for c in ["price_eur", "base_price_eur", "discount_value_eur", "discount_pct"]:
        s = df[c] if c in df else pd.Series(dtype=float)
        s = s.dropna()
        out[f"{c}_min"] = float(s.min()) if not s.empty else None
        out[f"{c}_max"] = float(s.max()) if not s.empty else None
        out[f"{c}_avg"] = float(s.mean()) if not s.empty else None
        out[f"{c}_med"] = float(s.median()) if not s.empty else None
    out["count_total"] = int(len(df))
    out["count_promos"] = int(df["discount_pct"].notna().sum()) if "discount_pct" in df.columns else 0
    out["promo_share_pct"] = round(100 * out["count_promos"] / out["count_total"], 1) if out["count_total"] else 0.0
    s = df["month"].dropna() if "month" in df.columns else pd.Series([], dtype=object)
    out["depart_by_month"] = json.dumps(s.value_counts().sort_index().to_dict(), ensure_ascii=False)
    return out

def cheapest_by_destination(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=["destination_label", "price_eur"]).copy()
    if base.empty:
        idx = pd.Index([], name="destination_label")
        return pd.DataFrame(columns=["title", "country_name", "price_eur", "url"]).set_index(idx)
    idxmin = base.groupby("destination_label")["price_eur"].idxmin()
    return base.loc[idxmin, ["destination_label", "title", "country_name", "price_eur", "url"]].set_index("destination_label")

def weekly_diff(df_curr: pd.DataFrame, df_prev: pd.DataFrame | None) -> pd.DataFrame:
    L = cheapest_by_destination(df_curr)
    R = cheapest_by_destination(df_prev) if df_prev is not None and not df_prev.empty else L.iloc[0:0]
    diff = L.join(R, how="left", lsuffix="_curr", rsuffix="_prev")
    diff["delta_abs"] = diff["price_eur_curr"] - diff["price_eur_prev"]
    diff["delta_pct"] = diff["delta_abs"] / diff["price_eur_prev"]
    diff.replace([np.inf, -np.inf], np.nan, inplace=True)
    diff["movement"] = diff["delta_abs"].apply(lambda v: "↓" if (pd.notna(v) and v < 0) else ("↑" if (pd.notna(v) and v > 0) else "="))
    out = diff.reset_index()
    # url = url_curr si dispo sinon url_prev sinon None
    if "url_curr" in out.columns:
        out["url"] = out["url_curr"]
    elif "url_prev" in out.columns:
        out["url"] = out["url_prev"]
    return out

def monthly_kpis(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=["month"]).copy()
    grp = base.groupby(["month","destination_label"], dropna=False)
    agg = grp.agg(prix_min=("price_eur","min"), prix_avg=("price_eur","mean"), nb_depart=("best_starting_date","count")).reset_index()
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

def find_alerts(wd: pd.DataFrame, pct_threshold=0.10, abs_threshold=150.0) -> pd.DataFrame:
    if wd is None or wd.empty:
        return pd.DataFrame(columns=["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url"])
    x = wd.copy()
    x["flag"] = (x["delta_pct"].abs() > pct_threshold) | (x["delta_abs"].abs() > abs_threshold)
    keep = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url","flag"]
    return x[keep][x["flag"]].drop(columns=["flag"]).sort_values(["delta_pct","delta_abs"], ascending=[False,False])

def same_date_price_diff(df_tours_curr: pd.DataFrame, df_tours_prev: pd.DataFrame) -> pd.DataFrame:
    if df_tours_curr is None or df_tours_curr.empty or df_tours_prev is None or df_tours_prev.empty:
        return pd.DataFrame(columns=["tour_id","slug","destination_label","price_prev","price_curr","delta_abs","delta_pct","url_precise"])
    L = df_tours_curr[["tour_id","slug","destination_label","price_eur","url_precise"]].dropna(subset=["tour_id"]).copy()
    R = df_tours_prev[["tour_id","price_eur"]].dropna(subset=["tour_id"]).copy().rename(columns={"price_eur":"price_prev"})
    diff = L.merge(R, on="tour_id", how="left")
    diff = diff[diff["price_prev"].notna()].copy()
    diff.rename(columns={"price_eur":"price_curr"}, inplace=True)
    diff["delta_abs"] = diff["price_curr"] - diff["price_prev"]
    diff["delta_pct"] = diff["delta_abs"] / diff["price_prev"]
    diff.replace([np.inf, -np.inf], np.nan, inplace=True)
    return diff.sort_values(["delta_pct","delta_abs"], ascending=[False,False]).reset_index(drop=True)

def coordinator_stats(df_tours: pd.DataFrame) -> pd.DataFrame:
    if df_tours is None or df_tours.empty:
        return pd.DataFrame(columns=["coordinator_id","coordinator_nickname","appearances"])
    x = df_tours.dropna(subset=["coordinator_id"]).copy()
    x["coordinator_nickname"] = x["coordinator_nickname"].fillna("").replace("", "(sans pseudo)")
    grp = (x.groupby(["coordinator_id","coordinator_nickname"], dropna=False)
             .size().reset_index(name="appearances")
             .sort_values(["appearances","coordinator_nickname"], ascending=[False,True]))
    return grp

# -------------------- Export --------------------
def _to_excel_sorted(df: pd.DataFrame, writer, sheet: str, by=None, ascending=None):
    out = df.copy()
    try:
        if by:
            cols = by if isinstance(by,(list,tuple)) else [by]
            if all(c in out.columns for c in cols):
                out = out.sort_values(by=cols, ascending=ascending if ascending is not None else True)
    except Exception:
        pass
    out.to_excel(writer, index=False, sheet_name=sheet)

def export_excel(df_curr, wk_kpis, wk_diff, mo_kpis, mo_diff, alerts, df_tours, same_d, coord_stats, out="weekly_report.xlsx"):
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        df_curr.to_excel(w, index=False, sheet_name="Voyages_Week")
        pd.DataFrame([wk_kpis]).to_excel(w, index=False, sheet_name="Weekly_KPIs")
        _to_excel_sorted(wk_diff, w, "Weekly_Diff", by=["delta_pct","delta_abs"], ascending=[False,False])
        alerts.to_excel(w, index=False, sheet_name="Alerts")
        mo_kpis.to_excel(w, index=False, sheet_name="Monthly_KPIs")
        mo_diff.to_excel(w, index=False, sheet_name="Monthly_Diff")
        df_tours.to_excel(w, index=False, sheet_name="Tours_View")
        _to_excel_sorted(same_d, w, "SameDateDiff", by=["delta_pct","delta_abs"], ascending=[False,False])
        coord_stats.to_excel(w, index=False, sheet_name="Coordinators")
    logging.info("Exporté: %s", out)

# -------------------- Persist --------------------
def persist_sqlite(conn: sqlite3.Connection, table: str, df: pd.DataFrame, run_iso: str):
    """
    Append df into table, ensuring:
      - both run_date and run_ts columns exist (compat)
      - all df columns exist (auto-migration)
    """
    if df is None:
        return
    df2 = df.copy()
    # Ajoute les deux colonnes de run (compat)
    df2["run_date"] = run_iso
    df2["run_ts"] = run_iso
    ensure_table_has_columns(conn, table, df2)
    df2.to_sql(table, conn, if_exists="append", index=False)

# -------------------- Main --------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="weekly_report.xlsx")
    ap.add_argument("--sqlite", default="data/weroad.db")
    ap.add_argument("--alert-pct", type=float, default=float(os.getenv("ALERT_PCT", 0.10)))
    ap.add_argument("--alert-eur", type=float, default=float(os.getenv("ALERT_EUR", 150.0)))
    args = ap.parse_args()

    run_iso = _now_iso_utc()
    logging.info("Run timestamp (UTC): %s", run_iso)

    travels = fetch_travels()
    df_curr  = normalize_travels(travels)

    # Previous snapshots (compat run_date/run_ts)
    df_prev = pd.DataFrame()
    df_tours_prev = pd.DataFrame()
    if args.sqlite and Path(args.sqlite).exists():
        conn = sqlite3.connect(args.sqlite)
        try:
            rc = pick_run_col(conn, "snapshots")
            if rc:
                runs = pd.read_sql_query(f"SELECT MAX({rc}) AS last_run FROM snapshots;", conn)
                last_run = runs["last_run"].iloc[0] if not runs.empty else None
                if last_run:
                    df_prev = pd.read_sql_query(f"SELECT * FROM snapshots WHERE {rc} = ?", conn, params=(last_run,))
            # tours prev
            rtc = pick_run_col(conn, "tours")
            if rtc:
                runs_t = pd.read_sql_query(f"SELECT MAX({rtc}) AS last_run FROM tours;", conn)
                last_t = runs_t["last_run"].iloc[0] if not runs_t.empty else None
                if last_t:
                    df_tours_prev = pd.read_sql_query(f"SELECT * FROM tours WHERE {rtc} = ?", conn, params=(last_t,))
        finally:
            conn.close()

    wk_k  = weekly_kpis(df_curr)
    wk_d  = weekly_diff(df_curr, df_prev)
    mo_k  = monthly_kpis(df_curr)
    mo_d  = monthly_diff(mo_k)
    alerts = find_alerts(wk_d, pct_threshold=args.alert_pct, abs_threshold=args.alert_eur)

    # All tours (current)
    df_tours_curr = build_df_tours(df_curr)
    same_d = same_date_price_diff(df_tours_curr, df_tours_prev)
    coord_stats = coordinator_stats(df_tours_curr)

    export_excel(df_curr, wk_k, wk_d, mo_k, mo_d, alerts, df_tours_curr, same_d, coord_stats, out=args.out)

    if args.sqlite:
        Path(args.sqlite).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(args.sqlite)
        try:
            persist_sqlite(conn, "snapshots", df_curr, run_iso)
            persist_sqlite(conn, "weekly_kpis", pd.DataFrame([wk_kpis := wk_k]), run_iso)
            persist_sqlite(conn, "weekly_diff", wk_d, run_iso)
            persist_sqlite(conn, "monthly_kpis", mo_k, run_iso)
            persist_sqlite(conn, "monthly_diff", mo_d, run_iso)
            persist_sqlite(conn, "alerts", alerts, run_iso)
            persist_sqlite(conn, "tours", df_tours_curr, run_iso)
            persist_sqlite(conn, "same_date_diff", same_d, run_iso)
            persist_sqlite(conn, "coordinator_stats", coord_stats, run_iso)

            # indexes (crée selon colonnes présentes)
            ensure_indexes(conn, "snapshots", pick_run_col(conn, "snapshots"))
            ensure_indexes(conn, "weekly_kpis", pick_run_col(conn, "weekly_kpis"))
            ensure_indexes(conn, "weekly_diff", pick_run_col(conn, "weekly_diff"))
            ensure_indexes(conn, "monthly_kpis", pick_run_col(conn, "monthly_kpis"))
            ensure_indexes(conn, "monthly_diff", pick_run_col(conn, "monthly_diff"))
            ensure_indexes(conn, "alerts", pick_run_col(conn, "alerts"))
            ensure_indexes(conn, "tours", pick_run_col(conn, "tours"),
                           extra=[("tours", "CREATE INDEX IF NOT EXISTS idx_tours_tour_id ON tours(tour_id);"),
                                  ("tours", "CREATE INDEX IF NOT EXISTS idx_tours_coord ON tours(coordinator_id);")])
            ensure_indexes(conn, "same_date_diff", pick_run_col(conn, "same_date_diff"),
                           extra=[("same_date_diff", "CREATE INDEX IF NOT EXISTS idx_same_tour ON same_date_diff(tour_id);")])
            ensure_indexes(conn, "coordinator_stats", pick_run_col(conn, "coordinator_stats"),
                           extra=[("coordinator_stats", "CREATE INDEX IF NOT EXISTS idx_coord_coord ON coordinator_stats(coordinator_id);")])
        finally:
            conn.close()

if __name__ == "__main__":
    main()
