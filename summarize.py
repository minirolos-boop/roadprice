# summarize.py — Dashboard HTML enrichi pour GitHub Pages
from pathlib import Path
from datetime import datetime, timezone
import os
import sqlite3
import pandas as pd

DOCS_DIR = Path("docs")
OUT = DOCS_DIR / "index.md"
DB = Path("data/weroad.db")

# nb de mois récents à mettre en avant (aperçu)
RECENT_MONTHS = 24

# Seuils d'alertes (peuvent être surchargés par le workflow via env)
ALERT_PCT = float(os.getenv("ALERT_PCT", "0.10"))   # 10%
ALERT_EUR = float(os.getenv("ALERT_EUR", "150"))    # 150 €

# ---------- Helpers ----------
def html_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    """Table HTML fiable (pandas.to_html), formats % et € si colonnes présentes."""
    if df is None or df.empty:
        return "<p><em>Aucune donnée</em></p>"

    df = df.copy().head(max_rows)

    # Colonnes % (delta_pct, *_pct, promo_share_pct)
    pct_cols = [c for c in df.columns if c.endswith("_pct") or c == "delta_pct" or c == "promo_share_pct"]
    for c in pct_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0) / 100.0
            df[c] = df[c].map(lambda v: f"{v*100:.1f}%" if pd.notna(v) else "")

    # Colonnes montants €
    money_cols = [c for c in df.columns if any(k in c for k in ["price", "prix", "delta_abs", "value_eur"])]
    for c in money_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
            df[c] = df[c].map(lambda v: f"{v:,.2f} €".replace(",", " ").replace(".", ",") if pd.notna(v) else "")

    return df.to_html(index=False, classes="rp-table display", escape=False, border=0)

def decorate_movement(df: pd.DataFrame) -> pd.DataFrame:
    """Colorise mouvement: ↑ rouge, ↓ vert, = gris (via <code class='up|down|equal'>)."""
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

def load_last_run(conn) -> str | None:
    last_df = safe_read_sql("SELECT MAX(run_date) AS r FROM weekly_diff", conn)
    if not last_df.empty and pd.notna(last_df.loc[0, "r"]):
        return last_df.loc[0, "r"]
    last_df2 = safe_read_sql("SELECT MAX(run_date) AS r FROM weekly_kpis", conn)
    if not last_df2.empty and pd.notna(last_df2.loc[0, "r"]):
        return last_df2.loc[0, "r"]
    return None

def load_prev_run(conn, last: str) -> str | None:
    df = safe_read_sql("SELECT DISTINCT run_date FROM snapshots WHERE run_date < ? ORDER BY run_date", conn, (last,))
    if not df.empty:
        return df["run_date"].iloc[-1]
    return None

def to_month(s: str | None) -> str | None:
    try:
        return pd.to_datetime(s).strftime("%Y-%m")
    except Exception:
        return None

# ---------- Analyses enrichies ----------
def promo_watchlist(df: pd.DataFrame) -> pd.DataFrame:
    """Départs à surveiller (ALMOST_CONFIRMED / CONFIRMED / GUARANTEED)."""
    if df.empty:
        return pd.DataFrame()
    x = df[df["sales_status"].isin(["ALMOST_CONFIRMED","CONFIRMED","GUARANTEED"])].copy()
    x = x.sort_values(
        by=["sales_status","best_starting_date","seatsToConfirm","price_eur"],
        ascending=[True, True, True, True],
        na_position="last"
    )
    base_cols = [
        "sales_status","best_starting_date","best_ending_date",
        "title","destination_label","country_name",
        "price_eur","discount_pct","seatsToConfirm","maxPax","weroadersCount"
    ]
    if "url_precise" in x.columns:
        base_cols.append("url_precise")
    elif "url" in x.columns:
        base_cols.append("url")
    base_cols = [c for c in base_cols if c in x.columns]
    return x[base_cols].reset_index(drop=True)

def big_movers(wk_diff: pd.DataFrame, pct_threshold=ALERT_PCT, abs_threshold=ALERT_EUR) -> pd.DataFrame:
    """Var. > seuils, triées par Δ% puis Δ€."""
    if wk_diff.empty:
        return pd.DataFrame()
    x = wk_diff.copy()
    x["delta_pct"] = pd.to_numeric(x.get("delta_pct"), errors="coerce").fillna(0.0)
    x["delta_abs"] = pd.to_numeric(x.get("delta_abs"), errors="coerce").fillna(0.0)

    x["flag"] = (x["delta_pct"].abs() > pct_threshold) | (x["delta_abs"].abs() > abs_threshold)
    cols = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement"]
    if "url_precise" in x.columns:
        cols.append("url_precise")
    elif "url" in x.columns:
        cols.append("url")
    cols = [c for c in cols if c in x.columns]

    out = x[x["flag"]].sort_values(["delta_pct","delta_abs"], ascending=[False,False])[cols].reset_index(drop=True)
    return decorate_movement(out)

# ---------- Main ----------
def main():
    ensure_docs()

    if not DB.exists():
        OUT.write_text("# RoadPrice\n\n_Base SQLite absente : `data/weroad.db`_", encoding="utf-8")
        return

    conn = sqlite3.connect(DB)
    try:
        last = load_last_run(conn)
        if not last:
            OUT.write_text("# RoadPrice\n\n_Aucune donnée disponible pour l’instant._", encoding="utf-8")
            return
        prev = load_prev_run(conn, last)

        runs = safe_read_sql("SELECT DISTINCT run_date FROM weekly_kpis ORDER BY run_date", conn)
        start_run = runs["run_date"].iloc[0] if not runs.empty else None
        end_run = runs["run_date"].iloc[-1] if not runs.empty else None

        df_curr = safe_read_sql("SELECT * FROM snapshots WHERE run_date = ?", conn, (last,))
        df_prev = safe_read_sql("SELECT * FROM snapshots WHERE run_date = ?", conn, (prev,)) if prev else pd.DataFrame()

        kpi_last = safe_read_sql("SELECT * FROM weekly_kpis WHERE run_date = ?", conn, (last,))
        kpi_hist = safe_read_sql(
            "SELECT run_date, price_eur_min, price_eur_med, price_eur_avg, count_total, count_promos, promo_share_pct FROM weekly_kpis ORDER BY run_date", conn
        )

        wd = safe_read_sql("SELECT * FROM weekly_diff WHERE run_date = ?", conn, (last,))
        if not wd.empty:
            wd = wd.copy()

        mo_all = safe_read_sql("SELECT * FROM monthly_kpis ORDER BY month, destination_label", conn)

        watch = promo_watchlist(df_curr)
        movers = big_movers(wd, ALERT_PCT, ALERT_EUR) if not wd.empty else pd.DataFrame()

    finally:
        conn.close()

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    coverage = ""
    if start_run and end_run:
        coverage = f"_Historique des runs : du **{start_run}** au **{end_run}** ({len(runs)} exécutions)._"

    # Rendus HTML
    kpi_html = html_table(kpi_last, max_rows=1) if not kpi_last.empty else "<p><em>Aucune donnée</em></p>"
    kpi_hist_html = html_table(kpi_hist, max_rows=500)
    movers_html = html_table(movers, max_rows=200)
    watch_html = html_table(watch, max_rows=200)
    mo_all_html = html_table(mo_all, max_rows=1000)

    # Page
    content = f"""---
title: RoadPrice – Évolutions tarifaires
---

# RoadPrice — Évolutions tarifaires

**Dernier run : `{last}`**  
{coverage}  

---

## Indicateurs clés — Dernier run
{kpi_html}

---

## Historique des KPIs hebdo
{kpi_hist_html}

---

## Gros mouvements de prix (Δ% ≥ {ALERT_PCT*100:.0f}% ou Δ€ ≥ {ALERT_EUR:.0f}€)
{movers_html}

---

## Watchlist — départs confirmés
{watch_html}

---

## KPIs mensuels
{mo_all_html}

"""

    OUT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
