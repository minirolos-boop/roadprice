# summarize.py
from pathlib import Path
from datetime import datetime, timezone
import sqlite3
import pandas as pd

DOCS_DIR = Path("docs")
OUT = DOCS_DIR / "index.md"
DB = Path("data/weroad.db")


def md_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    """Rend un tableau Markdown propre, avec formats % et € si colonnes présentes."""
    if df is None or df.empty:
        return "_Aucune donnée_"

    df = df.copy().head(max_rows)

    # Pourcentages (ex: delta_pct)
    if "delta_pct" in df.columns:
        df["delta_pct"] = df["delta_pct"].map(lambda v: f"{v*100:.1f}%" if pd.notna(v) else "")

    # Argent (€) pour colonnes prix / delta_abs
    money_cols = [c for c in df.columns if any(k in c for k in ["price", "prix", "delta_abs"])]
    for c in money_cols:
        if c in df.columns:
            df[c] = df[c].map(
                lambda v: f"{v:,.2f} €".replace(",", " ").replace(".", ",") if pd.notna(v) else ""
            )

    # Nécessite 'tabulate' pour pandas.to_markdown()
    return df.to_markdown(index=False)


def safe_read_sql(sql: str, conn, params: tuple = ()) -> pd.DataFrame:
    try:
        return pd.read_sql_query(sql, conn, params=params)
    except Exception:
        return pd.DataFrame()


def choose_url_col(df: pd.DataFrame) -> pd.Series:
    """Retourne une série 'url' cohérente en combinant url_curr/url/url_prev si existants."""
    for c in ("url_curr", "url", "url_prev"):
        if c in df.columns:
            s = df[c]
            s.name = "url"
            return s
    return pd.Series([None] * len(df), index=df.index, name="url")


def main():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    if not DB.exists():
        OUT.write_text("# RoadPrice\n\n_Base SQLite absente : `data/weroad.db`_", encoding="utf-8")
        return

    conn = sqlite3.connect(DB)
    try:
        # Cherche la dernière date de run depuis weekly_diff, sinon weekly_kpis
        last_df = safe_read_sql("SELECT MAX(run_date) AS r FROM weekly_diff", conn)
        last = None
        if not last_df.empty and pd.notna(last_df["r"].iloc[0]):
            last = last_df["r"].iloc[0]
        else:
            last_df2 = safe_read_sql("SELECT MAX(run_date) AS r FROM weekly_kpis", conn)
            if not last_df2.empty and pd.notna(last_df2["r"].iloc[0]):
                last = last_df2["r"].iloc[0]

        if not last:
            OUT.write_text("# RoadPrice\n\n_Aucune donnée disponible pour l’instant._", encoding="utf-8")
            return

        # KPIs hebdo
        kpi = safe_read_sql("SELECT * FROM weekly_kpis WHERE run_date = ?", conn, (last,))

        # Weekly diff (toutes colonnes -> puis sous-sélection)
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

        # KPIs mensuels (aperçu)
        mo = safe_read_sql(
            "SELECT month, destination_label, prix_min, prix_avg, nb_depart "
            "FROM monthly_kpis ORDER BY month DESC, destination_label LIMIT 200",
            conn,
        )

    finally:
        conn.close()

    # Badges simples
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    badge_run = f"![last_run](https://img.shields.io/badge/last_run-{last}-blue)"
    badge_build = f"![build](https://img.shields.io/badge/build-{ts}-success)"

    # KPIs présentables
    if not kpi.empty:
        keep = [
            "price_eur_min",
            "price_eur_med",
            "price_eur_avg",
            "count_total",
            "count_promos",
            "promo_share_pct",
        ]
        keep = [c for c in keep if c in kpi.columns]
        show = kpi[keep].copy()
        if "promo_share_pct" in show.columns:
            show["promo_share_pct"] = show["promo_share_pct"].map(lambda v: f"{v:.1f}%" if pd.notna(v) else "")
        kpi_md = md_table(show, max_rows=1)
    else:
        kpi_md = "_Aucune donnée_"

    # Contenu Markdown
    content = f"""---
title: RoadPrice – Évolutions tarifaires
---

# RoadPrice — Évolutions tarifaires
{badge_run} {badge_build}

**Dernier run : `{last}`**  
Ce tableau de bord est généré automatiquement chaque semaine par GitHub Actions.

> Les fichiers détaillés (Excel & SQLite) sont disponibles dans l’onglet **Actions → Artifacts** du dépôt.

---

## Indicateurs clés (semaine)
{kpi_md}

---

## Top **hausses** (Δ% semaine)
{md_table(inc)}

---

## Top **baisses** (Δ% semaine)
{md_table(dec)}

---

## KPIs mensuels (aperçu récent)
{md_table(mo, max_rows=30)}

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
