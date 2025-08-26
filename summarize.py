# summarize.py
import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd

DOCS_DIR = Path("docs")
DOCS_DIR.mkdir(parents=True, exist_ok=True)
OUT = DOCS_DIR / "index.md"
DB = Path("data/weroad.db")

def md_table(df: pd.DataFrame, floatfmt=".2f", max_rows=20):
    if df is None or df.empty:
        return "_Aucune donnée_"
    df = df.copy().head(max_rows)

    # format % si present
    if "delta_pct" in df.columns:
        df["delta_pct"] = (df["delta_pct"] * 100).map(lambda x: f"{x:.1f}%")

    # format € si colonnes de prix/delta_abs
    money_cols = [c for c in df.columns if any(k in c for k in ["price", "prix", "delta_abs"])]
    for c in money_cols:
        if c in df.columns:
            df[c] = df[c].map(lambda x: f"{x:,.2f} €".replace(",", " ").replace(".", ",")) if pd.notna(x) else x

    return df.to_markdown(index=False)

def safe_read_sql(sql: str, conn, params=()):
    try:
        return pd.read_sql_query(sql, conn, params=params)
    except Exception:
        return pd.DataFrame()

def choose_url_cols(df: pd.DataFrame) -> pd.Series:
    # Compose une colonne unique 'url' à partir des variantes possibles
    for c in ["url_curr", "url", "url_prev"]:
        if c in df.columns:
            return df[c]
    return pd.Series([None] * len(df), index=df.index, name="url")

def main():
    if not DB.exists():
        OUT.write_text("# RoadPrice\n\n_Database manquante : data/weroad.db_", encoding="utf-8")
        return

    conn = sqlite3.connect(DB)
    try:
        last_df = safe_read_sql("SELECT MAX(run_date) AS r FROM weekly_diff", conn)
        if last_df.empty or pd.isna(last_df["r"].iloc[0]):
            OUT.write_text("# RoadPrice\n\n_Aucune donnée pour le moment._", encoding="utf-8")
            return
        last = last_df["r"].iloc[0]

        kpi = safe_read_sql("SELECT * FROM weekly_kpis WHERE run_date = ?", conn, (last,))

        # Récupère toutes les colonnes utiles sans se restreindre pour éviter les 'no such column'
        wd = safe_read_sql("SELECT * FROM weekly_diff WHERE run_date = ?", conn, (last,))
        if not wd.empty:
            # normaliser la colonne url
            wd["url"] = choose_url_cols(wd)

            # colonnes sûres pour les tops
            base_cols = ["destination_label", "title_curr", "price_eur_prev", "price_eur_curr", "delta_abs", "delta_pct", "url"]
            base_cols = [c for c in base_cols if c in wd.columns]
            wd_base = wd[base_cols].copy()

            inc = wd_base[wd_base["delta_pct"].notna()].sort_values("delta_pct", ascending=False).head(15)
            dec = wd_base[wd_base["delta_pct"].notna()].sort_values("delta_pct", ascending=True).head(15)
        else:
            inc = pd.DataFrame()
            dec = pd.DataFrame()

        mo = safe_read_sql(
            "SELECT month, destination_label, prix_min, prix_avg, nb_depart "
            "FROM monthly_kpis ORDER BY month DESC, destination_label LIMIT 200",
            conn,
        )
    finally:
        conn.close()

    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    badge_run = f"![run-date](https://img.shields.io/badge/last_run-{last}-blue)"
    badge_build = f"![build](https://img.shields.io/badge/build-{ts}-success)"

    # KPIs hebdo présentables
    kpi_md = "_Aucune donnée_"
    if not kpi.empty:
        keep = [c for c in [
            "price_eur_min","price_eur_med","price_eur_avg",
            "count_total","count_promos","promo_share_pct"
        ] if c in kpi.columns]
        show = kpi[keep].copy()
        if "promo_share_pct" in show.columns:
            show["promo_share_pct"] = show["promo_share_pct"].map(lambda x: f"{x:.1f}%")
        kpi_md = md_table(show, max_rows=1)

    content = f"""---
title: RoadPrice – Évolutions tarifaires
---

# RoadPrice — Évolutions tarifaires
{badge_run} {badge_build}

**Dernier run : `{last}`**  
Ce tableau de bord est généré automatiquement chaque semaine par GitHub Actions.  
Téléchargements : [rapport Excel](../weekly_report.xlsx) • [snapshot SQLite](../data/weroad.db)

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
- Les liens mènent à la page WeRoad de l’offre.
"""
    OUT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
