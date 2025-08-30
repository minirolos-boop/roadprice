# summarize.py — docs/index.md
from pathlib import Path
from datetime import datetime, timezone
import os
import sqlite3
import pandas as pd

DOCS_DIR = Path("docs")
OUT = DOCS_DIR / "index.md"
DB = Path("data/weroad.db")

RECENT_MONTHS = 24
ALERT_PCT = float(os.getenv("ALERT_PCT", "0.10"))
ALERT_EUR = float(os.getenv("ALERT_EUR", "150"))

# ---------- helpers ----------
def ensure_docs():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

def pick_run_col(conn, table: str) -> str | None:
    cur = conn.execute(f'PRAGMA table_info("{table}")')
    cols = {row[1] for row in cur.fetchall()}
    if "run_date" in cols: return "run_date"
    if "run_ts" in cols: return "run_ts"
    return None

def safe_read_sql(sql: str, conn, params: tuple = ()) -> pd.DataFrame:
    try:
        return pd.read_sql_query(sql, conn, params=params)
    except Exception:
        return pd.DataFrame()

def html_table(df: pd.DataFrame, max_rows=20) -> str:
    if df is None or df.empty:
        return "<p><em>Aucune donnée</em></p>"
    df = df.copy().head(max_rows)
    pct_cols = [c for c in df.columns if c.endswith("_pct") or c in ("promo_share_pct",)]
    for c in pct_cols:
        if c in df.columns:
            df[c] = df[c].map(lambda v: f"{v*100:.1f}%" if pd.notna(v) else "")
    money_cols = [c for c in df.columns if any(k in c for k in ["price", "prix", "delta_abs"])]
    for c in money_cols:
        df[c] = df[c].map(lambda v: f"{v:,.2f} €".replace(",", " ").replace(".", ",") if pd.notna(v) else "")
    return df.to_html(index=False, classes="rp-table", escape=False)

def decorate_movement(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty or "movement" not in df.columns:
        return df
    m = df["movement"].fillna("=")
    cls = m.map(lambda x: "up" if x == "↑" else ("down" if x == "↓" else "equal"))
    out = df.copy()
    out["movement"] = [f"<code class='{c}'>{s}</code>" for c, s in zip(cls, m)]
    return out

# ---------- main ----------
def main():
    ensure_docs()
    if not DB.exists():
        OUT.write_text("# RoadPrice\n\n_Base SQLite absente : `data/weroad.db`_", encoding="utf-8"); return

    conn = sqlite3.connect(DB)
    try:
        # trouver last run (weekly_kpis prioritaire, sinon snapshots)
        run_col = pick_run_col(conn, "weekly_kpis")
        last = None
        if run_col:
            df_last = safe_read_sql(f"SELECT MAX({run_col}) AS r FROM weekly_kpis", conn)
            last = df_last.loc[0, "r"] if (not df_last.empty and pd.notna(df_last.loc[0, "r"])) else None
        if not last:
            run_col = pick_run_col(conn, "snapshots")
            if run_col:
                df_last2 = safe_read_sql(f"SELECT MAX({run_col}) AS r FROM snapshots", conn)
                last = df_last2.loc[0, "r"] if (not df_last2.empty and pd.notna(df_last2.loc[0, "r"])) else None
        if not last:
            OUT.write_text("# RoadPrice\n\n_Aucune donnée disponible pour l’instant._", encoding="utf-8"); return

        # runs coverage
        rc_kpi = pick_run_col(conn, "weekly_kpis")
        runs = safe_read_sql(f"SELECT DISTINCT {rc_kpi} AS run FROM weekly_kpis ORDER BY {rc_kpi}", conn) if rc_kpi else pd.DataFrame()
        start_run = runs["run"].iloc[0] if not runs.empty else None
        end_run   = runs["run"].iloc[-1] if not runs.empty else None

        # data for last run
        rc_snap = pick_run_col(conn, "snapshots")
        df_curr = safe_read_sql(f"SELECT * FROM snapshots WHERE {rc_snap} = ?", conn, (last,)) if rc_snap else pd.DataFrame()

        kpi_last = safe_read_sql(f"SELECT * FROM weekly_kpis WHERE {rc_kpi} = ?", conn, (last,)) if rc_kpi else pd.DataFrame()
        kpi_hist = safe_read_sql(
            f"SELECT {rc_kpi} AS run_date, price_eur_min, price_eur_med, price_eur_avg, count_total, count_promos, promo_share_pct "
            f"FROM weekly_kpis ORDER BY {rc_kpi}", conn
        ) if rc_kpi else pd.DataFrame()

        rc_wd = pick_run_col(conn, "weekly_diff")
        wd = safe_read_sql(f"SELECT * FROM weekly_diff WHERE {rc_wd} = ?", conn, (last,)) if rc_wd else pd.DataFrame()
        if not wd.empty:
            base_cols = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url"]
            wd = wd[[c for c in base_cols if c in wd.columns]]

        rc_mk = pick_run_col(conn, "monthly_kpis")
        mo_all = safe_read_sql(
            "SELECT month, destination_label, prix_min, prix_avg, nb_depart "
            "FROM monthly_kpis ORDER BY month, destination_label", conn
        ) if rc_mk else pd.DataFrame()

        # tours / same-date / coord
        rc_tours = pick_run_col(conn, "tours")
        tours = safe_read_sql(
            f"SELECT slug, destination_label, tour_id, date_start, status, price_eur, base_price_eur, url_precise, "
            f"coordinator_id, coordinator_nickname, coordinator_city "
            f"FROM tours WHERE {rc_tours} = ? ORDER BY slug, date_start", conn, (last,)
        ) if rc_tours else pd.DataFrame()

        rc_sdd = pick_run_col(conn, "same_date_diff")
        same_d = safe_read_sql(
            f"SELECT tour_id, slug, destination_label, price_prev, price_curr, delta_abs, delta_pct, url_precise "
            f"FROM same_date_diff WHERE {rc_sdd} = ? ORDER BY delta_pct DESC, delta_abs DESC", conn, (last,)
        ) if rc_sdd else pd.DataFrame()

        rc_cs = pick_run_col(conn, "coordinator_stats")
        coord = safe_read_sql(
            f"SELECT coordinator_id, coordinator_nickname, appearances "
            f"FROM coordinator_stats WHERE {rc_cs} = ? ORDER BY appearances DESC, coordinator_nickname ASC", conn, (last,)
        ) if rc_cs else pd.DataFrame()
        if not coord.empty:
            coord["coordinator_nickname"] = coord["coordinator_nickname"].fillna("").replace("", "(sans pseudo)")

    finally:
        conn.close()

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    coverage = f"_Historique des runs : du **{start_run}** au **{end_run}** ({len(runs)} exécutions)._ " if start_run and end_run else ""

    # render
    kpi_html = html_table(kpi_last[[
        c for c in ["price_eur_min","price_eur_med","price_eur_avg","count_total","count_promos","promo_share_pct"]
        if c in kpi_last.columns
    ]], max_rows=1) if not kpi_last.empty else "<p><em>Aucune donnée</em></p>"

    kpi_hist_html = html_table(kpi_hist, max_rows=500) if not kpi_hist.empty else "<p><em>Aucune donnée</em></p>"
    wd_html       = html_table(decorate_movement(wd), max_rows=400)
    mo_all_html   = html_table(mo_all, max_rows=1000)
    tours_html    = html_table(tours, max_rows=400)
    same_html     = html_table(same_d, max_rows=400)
    coord_html    = html_table(coord, max_rows=200)

    total_offers = int(kpi_last["count_total"].iloc[0]) if (not kpi_last.empty and "count_total" in kpi_last.columns) else 0

    content = f"""---
title: RoadPrice – Évolutions tarifaires
---

# RoadPrice — synthèse
Dernière génération : **{ts}**  
**Offres disponibles (dernier run)** : **{total_offers}**  
{coverage}

> Les fichiers détaillés (Excel & SQLite) sont disponibles dans l’onglet **Actions → Artifacts** du dépôt.

---

## Indicateurs clés — Dernier run
{kpi_html}

---

## Historique des KPIs hebdo (tous les runs)
{kpi_hist_html}

---

## Gros mouvements de prix (Δ% ≥ {ALERT_PCT*100:.0f}% ou Δ€ ≥ {ALERT_EUR:.0f}€) — meilleur prix par destination
{wd_html}

---

## Changements de prix sur mêmes départs (**même** `tour_id`, même date)
{same_html}

---

## Vue complète des départs (tours) — run courant
{tours_html}

---

## Coordinateurs — apparitions (dernier run)
Nombre de départs (tours-dates) par coordinateur·rice sur le run courant.
{coord_html}

---

## KPIs mensuels — Vue complète (toutes années)
{mo_all_html}

---

### Légende
- <strong>Δ%</strong> : variation relative vs snapshot précédent.  
- <strong>Δ€</strong> : variation absolue en euros.  
- Les liens mènent à la page WeRoad de l’offre (si disponible).
"""
    OUT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
