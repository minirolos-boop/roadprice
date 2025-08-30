# summarize.py — page unique Markdown (docs/index.md)
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

# ---------- Helpers ----------
def html_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    if df is None or df.empty:
        return "<p><em>Aucune donnée</em></p>"
    df = df.copy().head(max_rows)

    pct_cols = [c for c in df.columns if c.endswith("_pct") or c in ("promo_share_pct",)]
    for c in pct_cols:
        if c in df.columns:
            df[c] = df[c].map(lambda v: f"{v*100:.1f}%" if pd.notna(v) else "")

    money_cols = [c for c in df.columns if any(k in c for k in ["price", "prix", "delta_abs"])]
    for c in money_cols:
        if c in df.columns:
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

def safe_read_sql(sql: str, conn, params: tuple = ()) -> pd.DataFrame:
    try:
        return pd.read_sql_query(sql, conn, params=params)
    except Exception:
        return pd.DataFrame()

def ensure_docs():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

# ---------- Main ----------
def main():
    ensure_docs()

    if not DB.exists():
        OUT.write_text("# RoadPrice\n\n_Base SQLite absente : `data/weroad.db`_", encoding="utf-8")
        return

    conn = sqlite3.connect(DB)
    try:
        last_df = safe_read_sql("SELECT MAX(run_date) AS r FROM weekly_kpis", conn)
        last = last_df.loc[0, "r"] if (not last_df.empty and pd.notna(last_df.loc[0, "r"])) else None
        if not last:
            OUT.write_text("# RoadPrice\n\n_Aucune donnée disponible pour l’instant._", encoding="utf-8")
            return

        runs = safe_read_sql("SELECT DISTINCT run_date FROM weekly_kpis ORDER BY run_date", conn)
        start_run = runs["run_date"].iloc[0] if not runs.empty else None
        end_run   = runs["run_date"].iloc[-1] if not runs.empty else None

        df_curr = safe_read_sql("SELECT * FROM snapshots WHERE run_date = ?", conn, (last,))
        kpi_last = safe_read_sql("SELECT * FROM weekly_kpis WHERE run_date = ?", conn, (last,))
        kpi_hist = safe_read_sql(
            "SELECT run_date, price_eur_min, price_eur_med, price_eur_avg, count_total, count_promos, promo_share_pct "
            "FROM weekly_kpis ORDER BY run_date", conn
        )
        wd = safe_read_sql("SELECT * FROM weekly_diff WHERE run_date = ?", conn, (last,))
        if not wd.empty:
            base_cols = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url"]
            base_cols = [c for c in base_cols if c in wd.columns]
            wd = wd[base_cols].copy()
        mo_all = safe_read_sql(
            "SELECT month, destination_label, prix_min, prix_avg, nb_depart "
            "FROM monthly_kpis ORDER BY month, destination_label", conn
        )

        # tours / same-date diff / coord stats
        tours = safe_read_sql(
            "SELECT slug, destination_label, tour_id, date_start, status, price_eur, base_price_eur, url_precise, "
            "coordinator_id, coordinator_nickname, coordinator_city "
            "FROM tours WHERE run_date = ? ORDER BY slug, date_start", conn, (last,)
        )
        same_d = safe_read_sql(
            "SELECT tour_id, slug, destination_label, price_prev, price_curr, delta_abs, delta_pct, url_precise "
            "FROM same_date_diff WHERE run_date = ? "
            "ORDER BY delta_pct DESC, delta_abs DESC", conn, (last,)
        )
        coord = safe_read_sql(
            "SELECT coordinator_id, coordinator_nickname, appearances "
            "FROM coordinator_stats WHERE run_date = ? "
            "ORDER BY appearances DESC, coordinator_nickname ASC", conn, (last,)
        )
        coord["coordinator_nickname"] = coord["coordinator_nickname"].fillna("").replace("", "(sans pseudo)")

    finally:
        conn.close()

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    coverage = ""
    if start_run and end_run:
        coverage = f"_Historique des runs : du **{start_run}** au **{end_run}** ({len(runs)} exécutions)._"

    # Render
    kpi_html = html_table(kpi_last[[
        c for c in ["price_eur_min","price_eur_med","price_eur_avg","count_total","count_promos","promo_share_pct"]
        if c in kpi_last.columns
    ]], max_rows=1) if not kpi_last.empty else "<p><em>Aucune donnée</em></p>"

    kpi_hist_html    = html_table(kpi_hist, max_rows=500) if not kpi_hist.empty else "<p><em>Aucune donnée</em></p>"
    wd_html          = html_table(decorate_movement(wd), max_rows=400)
    mo_all_html      = html_table(mo_all, max_rows=1000)
    tours_html       = html_table(tours, max_rows=400)
    same_html        = html_table(same_d, max_rows=400)
    coord_html       = html_table(coord, max_rows=200)

    total_offers = int(kpi_last["count_total"].iloc[0]) if "count_total" in kpi_last.columns and not kpi_last.empty else 0

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
