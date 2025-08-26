# summarize.py
import sqlite3
from pathlib import Path
import pandas as pd
from datetime import datetime

DOCS_DIR = Path("docs")
DOCS_DIR.mkdir(parents=True, exist_ok=True)
OUT = DOCS_DIR / "index.md"
DB = Path("data/weroad.db")

def md_table(df: pd.DataFrame, floatfmt=".2f", max_rows=20):
    if df is None or df.empty:
        return "_Aucune donnée_"
    df = df.copy().head(max_rows)
    # Format pourcentages si colonne delta_pct
    if "delta_pct" in df.columns:
        df["delta_pct"] = (df["delta_pct"] * 100).map(lambda x: f"{x:.1f}%")
    # € pour delta_abs / prix
    for c in [c for c in df.columns if "price" in c or "prix" in c or c=="delta_abs"]:
        if c in df:
            df[c] = df[c].map(lambda x: f"{x:,.2f} €".replace(",", " ").replace(".", ",")) if pd.notna(x) else x
    return df.to_markdown(index=False)

def main():
    if not DB.exists():
        OUT.write_text("# RoadPrice\n\n_Database manquante : data/weroad.db_", encoding="utf-8")
        return

    conn = sqlite3.connect(DB)
    try:
        # Dernier run
        last = pd.read_sql_query("SELECT MAX(run_date) AS r FROM weekly_diff", conn)["r"].iloc[0]
        # KPIs hebdo
        kpi = pd.read_sql_query("SELECT * FROM weekly_kpis WHERE run_date = ?",
                                conn, params=(last,))
        # Weekly diff
        wd = pd.read_sql_query("SELECT destination_label, title_curr, price_eur_prev, price_eur_curr, delta_abs, delta_pct, movement, url \
                                FROM weekly_diff WHERE run_date = ?",
                                conn, params=(last,))
        # Tops
        inc = wd[wd["delta_pct"].notna()].sort_values("delta_pct", ascending=False)\
              .head(15)[["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","url"]]
        dec = wd[wd["delta_pct"].notna()].sort_values("delta_pct", ascending=True)\
              .head(15)[["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","url"]]

        # Monthly KPIs derniers mois dispo
        mo = pd.read_sql_query(
            "SELECT month, destination_label, prix_min, prix_avg, nb_depart \
             FROM monthly_kpis ORDER BY month DESC, destination_label LIMIT 200", conn
        )

    finally:
        conn.close()

    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    # Petits badges Markdown
    badge_run = f"![run-date](https://img.shields.io/badge/last_run-{last}-blue)"
    badge_build = f"![build](https://img.shields.io/badge/build-{ts}-success)"

    kpi_md = ""
    if not kpi.empty:
        cols = ["price_eur_min","price_eur_med","price_eur_avg","count_total","count_promos","promo_share_pct"]
        present = [c for c in cols if c in kpi.columns]
        show = kpi[present].copy()
        if "promo_share_pct" in show:
            show["promo_share_pct"] = show["promo_share_pct"].map(lambda x: f"{x:.1f}%")
        kpi_md = md_table(show)

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
