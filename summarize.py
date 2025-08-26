# summarize.py (version complète multi-années + historique)
from pathlib import Path
from datetime import datetime, timezone
import sqlite3
import pandas as pd

DOCS_DIR = Path("docs")
OUT = DOCS_DIR / "index.md"
DB = Path("data/weroad.db")

# combien de mois pour l'aperçu "récent" (sans limiter la vue complète)
RECENT_MONTHS = 24


def md_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    """Table Markdown avec formats % et € si colonnes présentes."""
    if df is None or df.empty:
        return "_Aucune donnée_"
    df = df.copy().head(max_rows)

    # Δ% / pourcentages
    pct_cols = [c for c in df.columns if c.endswith("_pct") or c == "delta_pct" or c == "promo_share_pct"]
    for c in pct_cols:
        if c in df.columns:
            df[c] = df[c].map(lambda v: f"{v*100:.1f}%" if pd.notna(v) else "")

    # € / prix et deltas
    money_cols = [c for c in df.columns if any(k in c for k in ["price", "prix", "delta_abs"])]
    for c in money_cols:
        if c in df.columns:
            df[c] = df[c].map(lambda v: f"{v:,.2f} €".replace(",", " ").replace(".", ",") if pd.notna(v) else "")

    return df.to_markdown(index=False)


def safe_read_sql(sql: str, conn, params: tuple = ()) -> pd.DataFrame:
    try:
        return pd.read_sql_query(sql, conn, params=params)
    except Exception:
        return pd.DataFrame()


def choose_url_col(df: pd.DataFrame) -> pd.Series:
    """Colonne 'url' en conciliant url_curr/url/url_prev si existants."""
    for c in ("url_curr", "url", "url_prev"):
        if c in df.columns:
            s = df[c]
            s.name = "url"
            return s
    return pd.Series([None] * len(df), index=df.index, name="url")


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


def load_runs_coverage(conn):
    runs = safe_read_sql("SELECT DISTINCT run_date FROM weekly_kpis ORDER BY run_date", conn)
    if runs.empty:
        return runs, None, None
    start = runs["run_date"].iloc[0]
    end = runs["run_date"].iloc[-1]
    return runs, start, end


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

        # Couverture (toutes les dates de run)
        runs, start_run, end_run = load_runs_coverage(conn)

        # KPIs du dernier run
        kpi_last = safe_read_sql("SELECT * FROM weekly_kpis WHERE run_date = ?", conn, (last,))

        # Historique des KPIs hebdo (tous les runs)
        kpi_hist = safe_read_sql(
            "SELECT run_date, price_eur_min, price_eur_med, price_eur_avg, "
            "count_total, count_promos, promo_share_pct "
            "FROM weekly_kpis ORDER BY run_date",
            conn,
        )

        # Weekly diff du dernier run (tops hausses/baisses)
        wd = safe_read_sql("SELECT * FROM weekly_diff WHERE run_date = ?", conn, (last,))
        if not wd.empty:
            wd["url"] = choose_url_col(wd)
            base_cols = [
                "destination_label",
                "title_curr",
                "price_eur_prev",
                "price_eur_curr",
                "delta_abs",
                "delta_pct",
                "url",
            ]
            base_cols = [c for c in base_cols if c in wd.columns]
            wd_base = wd[base_cols].copy()
            inc = wd_base[wd_base.get("delta_pct").notna()].sort_values("delta_pct", ascending=False).head(15)
            dec = wd_base[wd_base.get("delta_pct").notna()].sort_values("delta_pct", ascending=True).head(15)
        else:
            inc = pd.DataFrame()
            dec = pd.DataFrame()

        # KPIs mensuels – COMPLET (toutes années, pas de LIMIT)
        mo_all = safe_read_sql(
            "SELECT month, destination_label, prix_min, prix_avg, nb_depart "
            "FROM monthly_kpis "
            "ORDER BY month, destination_label",
            conn,
        )

        # Synthèse par année (à partir de monthly_kpis)
        year_summary = pd.DataFrame()
        if not mo_all.empty:
            tmp = mo_all.copy()
            tmp["year"] = tmp["month"].str.slice(0, 4)
            year_summary = (
                tmp.groupby("year", dropna=False)
                .agg(
                    nb_rows=("destination_label", "count"),
                    prix_avg_moyen=("prix_avg", "mean"),
                    prix_min_moyen=("prix_min", "mean"),
                    nb_depart_total=("nb_depart", "sum"),
                )
                .reset_index()
                .sort_values("year")
            )

        # Aperçu récentes périodes (N derniers mois distincts)
        mo_recent = pd.DataFrame()
        if not mo_all.empty:
            unique_months = sorted(mo_all["month"].dropna().unique())
            recent_months = unique_months[-RECENT_MONTHS:] if len(unique_months) > RECENT_MONTHS else unique_months
            mo_recent = mo_all[mo_all["month"].isin(recent_months)].copy()

    finally:
        conn.close()

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    badge_run = f"![last_run](https://img.shields.io/badge/last_run-{last}-blue)"
    badge_build = f"![build](https://img.shields.io/badge/build-{ts}-success)"
    coverage = ""
    if start_run and end_run:
        coverage = f"_Historique des runs : du **{start_run}** au **{end_run}** ({len(runs)} exécutions)._"

    # KPIs (dernier run)
    if not kpi_last.empty:
        keep = [
            "price_eur_min",
            "price_eur_med",
            "price_eur_avg",
            "count_total",
            "count_promos",
            "promo_share_pct",
        ]
        keep = [c for c in keep if c in kpi_last.columns]
        kpi_md = md_table(kpi_last[keep], max_rows=1)
    else:
        kpi_md = "_Aucune donnée_"

    # Historique des KPIs (tous les runs)
    kpi_hist_md = md_table(kpi_hist, max_rows=200) if not kpi_hist.empty else "_Aucune donnée_"

    # Contenu Markdown complet
    content = f"""---
title: RoadPrice – Évolutions tarifaires
---

# RoadPrice — Évolutions tarifaires
{badge_run} {badge_build}

**Dernier run : `{last}`**  
{coverage}

> Les fichiers détaillés (Excel & SQLite) sont disponibles dans l’onglet **Actions → Artifacts** du dépôt.

---

## Indicateurs clés — Dernier run
{kpi_md}

---

## Historique des KPIs hebdo (tous les runs)
{ kpi_hist_md }

---

## Top **hausses** (Δ% — dernier run)
{ md_table(inc) }

---

## Top **baisses** (Δ% — dernier run)
{ md_table(dec) }

---

## KPIs mensuels — Vue complète (toutes années)
{ md_table(mo_all, max_rows=500) }

---

## KPIs mensuels — Aperçu {RECENT_MONTHS} derniers mois
{ md_table(mo_recent, max_rows=300) }

---

## Synthèse par année (depuis monthly_kpis)
{ md_table(year_summary, max_rows=50) }

---

### Légende
- **Δ%** : variation relative vs snapshot précédent.  
- **Δ€** : variation absolue en euros.  
- Les liens mènent à la page WeRoad de l’offre (si disponible).
"""

    OUT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
