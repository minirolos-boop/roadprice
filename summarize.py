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

# Seuils d'alertes
ALERT_PCT = float(os.getenv("ALERT_PCT", "0.10"))   # 10%
ALERT_EUR = float(os.getenv("ALERT_EUR", "150"))    # 150 €

# ---------- Helpers ----------
def html_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    """Table HTML fiable avec formats % et €."""
    if df is None or df.empty:
        return "<p><em>Aucune donnée</em></p>"

    df = df.copy().head(max_rows)

    # Colonnes % (corrigées ÷100 si besoin)
    pct_cols = [c for c in df.columns if c.endswith("_pct") or c in ("delta_pct","promo_share_pct")]
    for c in pct_cols:
        if c in df.columns:
            df[c] = df[c].map(lambda v: f"{v:.1f}%" if pd.notna(v) else "")

    # Colonnes montants €
    money_cols = [c for c in df.columns if any(k in c for k in ["price", "prix", "delta_abs","value_eur"])]
    for c in money_cols:
        if c in df.columns:
            df[c] = df[c].map(lambda v: f"{v:,.2f} €".replace(",", " ").replace(".", ",") if pd.notna(v) else "")

    return df.to_html(index=False, classes="display compact", escape=False)


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

# ---------- Analyses ----------
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
    return x[[c for c in base_cols if c in x.columns]].reset_index(drop=True)


def big_movers(wk_diff: pd.DataFrame, pct_threshold=ALERT_PCT, abs_threshold=ALERT_EUR) -> pd.DataFrame:
    if wk_diff.empty:
        return pd.DataFrame()
    x = wk_diff.copy()
    x["flag"] = (x["delta_pct"].abs() > pct_threshold) | (x["delta_abs"].abs() > abs_threshold)
    cols = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url"]
    cols = [c for c in cols if c in x.columns]
    out = x[x["flag"]].sort_values(["delta_pct","delta_abs"], ascending=[False,False])[cols].reset_index(drop=True)
    return decorate_movement(out)

def price_buckets(df: pd.DataFrame):
    if df.empty:
        return pd.DataFrame()
    bins = [0, 800, 1000, 1200, 1500, 2000, 3000, 99999]
    labels = ["<800", "800–999", "1000–1199", "1200–1499", "1500–1999", "2000–2999", "≥3000"]
    x = df.dropna(subset=["price_eur"]).copy()
    x["bucket"] = pd.cut(x["price_eur"], bins=bins, labels=labels, right=False)
    out = x["bucket"].value_counts().reindex(labels, fill_value=0).reset_index()
    out.columns = ["tranche_prix", "nb_offres"]
    return out

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
            OUT.write_text("# RoadPrice\n\n_Aucune donnée disponible._", encoding="utf-8")
            return

        # Snapshots
        df_curr = safe_read_sql("SELECT * FROM snapshots WHERE run_date = ?", conn, (last,))

        # KPIs
        kpi_last = safe_read_sql("SELECT * FROM weekly_kpis WHERE run_date = ?", conn, (last,))
        wd = safe_read_sql("SELECT * FROM weekly_diff WHERE run_date = ?", conn, (last,))
        movers = big_movers(wd) if not wd.empty else pd.DataFrame()
        watch = promo_watchlist(df_curr)
        buckets = price_buckets(df_curr)

    finally:
        conn.close()

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Rendus
    kpi_html = html_table(kpi_last, max_rows=1) if not kpi_last.empty else "<p><em>Aucune donnée</em></p>"
    movers_html = html_table(movers, max_rows=200)
    watch_html  = html_table(watch, max_rows=200)
    buckets_html= html_table(buckets, max_rows=50)

    content = f"""---
title: RoadPrice – Évolutions tarifaires
---

# RoadPrice — Évolutions tarifaires
**Dernier run : `{last}`**  
_(généré {ts})_

---

## Indicateurs clés — Dernier run
{kpi_html}

---

## Gros mouvements de prix (Δ% ≥ {ALERT_PCT*100:.0f}% ou Δ€ ≥ {ALERT_EUR:.0f}€)
{movers_html}

---

## Watchlist — Départs proches / confirmés
{watch_html}

---

## Répartition par tranches de prix
{buckets_html}
"""
    OUT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
