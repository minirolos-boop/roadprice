# summarize.py — Génère docs/index.md à partir de data/weroad.db
from pathlib import Path
from datetime import datetime, timezone
import os
import sqlite3
import pandas as pd
import re

DOCS_DIR = Path("docs")
OUT = DOCS_DIR / "index.md"
DB = Path("data/weroad.db")

RECENT_MONTHS = 24

# Seuils d'alertes
ALERT_PCT = float(os.getenv("ALERT_PCT", "0.10"))   # 10%
ALERT_EUR = float(os.getenv("ALERT_EUR", "150"))    # 150 €

# --- Simple-DataTables (CDN fiables) ---
DATATABLES_CSS = "https://cdn.jsdelivr.net/npm/simple-datatables@latest/dist/style.css"
DATATABLES_JS  = "https://cdn.jsdelivr.net/npm/simple-datatables@latest"

# -------- Helpers --------
def ensure_docs():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

def safe_read_sql(sql: str, conn, params: tuple = ()) -> pd.DataFrame:
    try:
        return pd.read_sql_query(sql, conn, params=params)
    except Exception:
        return pd.DataFrame()

def decorate_movement(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty or "movement" not in df.columns:
        return df
    m = df["movement"].fillna("=")
    cls = m.map(lambda x: "up" if x == "↑" else ("down" if x == "↓" else "equal"))
    out = df.copy()
    out["movement"] = [f"<code class='{c}'>{s}</code>" for c, s in zip(cls, m)]
    return out

def html_table(df: pd.DataFrame, max_rows: int = 20, dt: bool = True, page: int = 25) -> str:
    """to_html + formats € / %, et balise data-dt pour activer Simple-DataTables côté client."""
    if df is None or df.empty:
        return "<p><em>Aucune donnée</em></p>"

    df = df.copy().head(max_rows)

    # delta_pct = ratio -> % via x100
    if "delta_pct" in df.columns:
        s = pd.to_numeric(df["delta_pct"], errors="coerce")
        df["delta_pct"] = s.map(lambda v: f"{v*100:.1f}%" if pd.notna(v) else "")

    # *_pct (déjà 0..100), hors delta_pct
    for c in [c for c in df.columns if c.endswith("_pct") and c != "delta_pct"]:
        s = pd.to_numeric(df[c], errors="coerce")
        df[c] = s.map(lambda v: f"{v:.1f}%" if pd.notna(v) else "")

    # Colonnes € (prix, delta_abs, value_eur, etc.)
    money_cols = [c for c in df.columns if any(k in c for k in ["price", "prix", "delta_abs", "value_eur", "money_pot"])]
    for c in money_cols:
        s = pd.to_numeric(df[c], errors="coerce")
        df[c] = s.map(lambda v: f"{v:,.0f} €".replace(",", " ").replace(".", ",") if pd.notna(v) else "")

    html = df.to_html(index=False, classes="rp-table", escape=False, border=0)

    # Active DataTables si tableau non minuscule
    if dt and len(df) >= 6:
        html = html.replace("<table ", f'<table data-dt="1" data-page-size="{page}" ', 1)

    return f'<div class="table-wrapper">{html}</div>'

def load_last_and_prev_run_ts(conn):
    runs = safe_read_sql("SELECT DISTINCT run_ts FROM weekly_kpis ORDER BY run_ts", conn)
    if runs.empty:
        return None, None, runs
    last = runs["run_ts"].iloc[-1]
    prev = runs["run_ts"].iloc[-2] if len(runs) > 1 else None
    return last, prev, runs

# -------- Analyses --------
def promo_watchlist(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    x = df[df["sales_status"].isin(["ALMOST_CONFIRMED","CONFIRMED","GUARANTEED"])].copy()
    x = x.sort_values(
        by=["sales_status","best_starting_date","seatsToConfirm","price_eur"],
        ascending=[True, True, True, True],
        na_position="last"
    )
    base = [
        "sales_status","best_starting_date","best_ending_date",
        "title","destination_label","country_name",
        "price_eur","total_price_eur",
        "money_pot_min_eur","money_pot_max_eur","money_pot_med_eur",
        "discount_pct","seatsToConfirm","maxPax","weroadersCount"
    ]
    link_col = "url" if "url" in x.columns else None
    if link_col:
        base.append(link_col)
    cols = [c for c in base if c in x.columns]
    return x[cols].reset_index(drop=True)

def big_movers(wk_diff: pd.DataFrame, pct_threshold=ALERT_PCT, abs_threshold=ALERT_EUR) -> pd.DataFrame:
    if wk_diff.empty:
        return pd.DataFrame()
    x = wk_diff.copy()
    x["delta_pct"] = pd.to_numeric(x.get("delta_pct"), errors="coerce").fillna(0.0)
    x["delta_abs"] = pd.to_numeric(x.get("delta_abs"), errors="coerce").fillna(0.0)
    x["flag"] = (x["delta_pct"].abs() > pct_threshold) | (x["delta_abs"].abs() > abs_threshold)

    cols = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement"]
    if "url" in x.columns:
        cols.append("url")
    cols = [c for c in cols if c in x.columns]

    out = x[x["flag"]].sort_values(["delta_pct","delta_abs"], ascending=[False,False])[cols].reset_index(drop=True)
    return decorate_movement(out)

def best_dates(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=["destination_label", "price_eur"]).copy()
    if base.empty:
        return pd.DataFrame()
    idx = base.groupby("destination_label")["price_eur"].idxmin()
    keep = [
        "destination_label","country_name","title",
        "price_eur","total_price_eur",
        "money_pot_min_eur","money_pot_max_eur","money_pot_med_eur",
        "discount_pct","sales_status","best_starting_date","best_ending_date","url"
    ]
    keep = [c for c in keep if c in base.columns]
    out = base.loc[idx, keep].sort_values(["country_name","destination_label"]).reset_index(drop=True)
    return out

def cheapest_by_month(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    tmp = df.dropna(subset=["best_starting_date","price_eur"]).copy()
    if tmp.empty:
        return pd.DataFrame()
    tmp["month_depart"] = pd.to_datetime(tmp["best_starting_date"], errors="coerce").dt.strftime("%Y-%m")
    tmp = tmp.dropna(subset=["month_depart"])
    tmp["rk"] = tmp.groupby("month_depart")["price_eur"].rank(method="first")
    keep = [
        "month_depart","destination_label","title","country_name",
        "price_eur","total_price_eur",
        "money_pot_med_eur","discount_pct","sales_status","best_starting_date","url"
    ]
    keep = [c for c in keep if c in tmp.columns]
    out = tmp[tmp["rk"] <= top_n].sort_values(["month_depart","price_eur"])[keep].reset_index(drop=True)
    return out

def country_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    g = df.groupby("country_name", dropna=False)
    out = pd.DataFrame({
        "nb_depart": g.size(),
        "prix_min": pd.to_numeric(g["price_eur"], errors="coerce").min(),
        "prix_med": pd.to_numeric(g["price_eur"], errors="coerce").median(),
        "prix_moy": pd.to_numeric(g["price_eur"], errors="coerce").mean(),
        "total_min": pd.to_numeric(g["total_price_eur"], errors="coerce").min(),
        "total_med": pd.to_numeric(g["total_price_eur"], errors="coerce").median(),
        "total_moy": pd.to_numeric(g["total_price_eur"], errors="coerce").mean(),
        "taux_promos_pct": 100 * g["discount_pct"].apply(lambda s: pd.to_numeric(s, errors="coerce").notna().mean()),
        "rating_moy": pd.to_numeric(g["rating"], errors="coerce").mean(),
        "rating_count": pd.to_numeric(g["rating_count"], errors="coerce").sum(),
    }).reset_index().sort_values(["prix_med","prix_moy","nb_depart"], na_position="last")
    return out

def price_buckets(df: pd.DataFrame):
    if df.empty:
        return pd.DataFrame()
    bins = [0, 800, 1000, 1200, 1500, 2000, 3000, 99999]
    labels = ["<800", "800–999", "1000–1199", "1200–1499", "1500–1999", "2000–2999", "≥3000"]
    x = df.dropna(subset=["price_eur"]).copy()
    x["bucket"] = pd.cut(pd.to_numeric(x["price_eur"], errors="coerce"), bins=bins, labels=labels, right=False)
    out = x["bucket"].value_counts().reindex(labels, fill_value=0).reset_index()
    out.columns = ["tranche_prix", "nb_offres"]
    return out

def price_buckets_total(df: pd.DataFrame):
    if df.empty or "total_price_eur" not in df.columns:
        return pd.DataFrame()
    bins = [0, 1000, 1300, 1600, 2000, 2500, 3000, 4000, 99999]
    labels = ["<1000", "1000–1299", "1300–1599", "1600–1999", "2000–2499", "2500–2999", "3000–3999", "≥4000"]
    x = df.dropna(subset=["total_price_eur"]).copy()
    x["bucket_total"] = pd.cut(pd.to_numeric(x["total_price_eur"], errors="coerce"), bins=bins, labels=labels, right=False)
    out = x["bucket_total"].value_counts().reindex(labels, fill_value=0).reset_index()
    out.columns = ["tranche_total", "nb_offres"]
    return out

# --- NOUVEAU RAPPORT : Pas de chambre privée gratuite ---
def no_free_private_room_report(df_tours: pd.DataFrame) -> pd.DataFrame:
    # On vérifie si la colonne existe (pour éviter le crash si monitor.py n'a pas été mis à jour)
    if df_tours.empty or "private_room_free" not in df_tours.columns:
        return pd.DataFrame()

    # Filtre: on garde ceux où private_room_free est 0 (False)
    # Attention: SQLite stocke les booléens comme 0 ou 1.
    mask = (df_tours["private_room_free"] == 0)
    df = df_tours[mask].copy()

    if df.empty:
        return pd.DataFrame()

    # Sélection des colonnes
    cols = ["destination_label", "title", "starting_date", "price_eur", "sales_status", "url"]
    cols = [c for c in cols if c in df.columns]
    
    # Tri par destination puis date
    return df[cols].sort_values(["destination_label", "starting_date"]).reset_index(drop=True)


# -------- Main --------
def main():
    ensure_docs()
    if not DB.exists():
        OUT.write_text("# RoadPrice\n\n_Base SQLite absente : `data/weroad.db`_", encoding="utf-8")
        print("No DB found.")
        return

    conn = sqlite3.connect(DB)
    try:
        last, prev, runs = load_last_and_prev_run_ts(conn)
        if not last:
            OUT.write_text("# RoadPrice\n\n_Aucune donnée disponible._", encoding="utf-8")
            print("No runs in DB.")
            return

        df_curr = safe_read_sql("SELECT * FROM snapshots WHERE run_ts = ?", conn, (last,))
        df_prev = safe_read_sql("SELECT * FROM snapshots WHERE run_ts = ?", conn, (prev,)) if prev else pd.DataFrame()
        
        # On charge aussi la table 'tours' pour le rapport 'chambre privée'
        df_tours_last = safe_read_sql("SELECT * FROM tours WHERE run_ts = ?", conn, (last,))

        kpi_last = safe_read_sql("SELECT * FROM weekly_kpis WHERE run_ts = ?", conn, (last,))
        kpi_hist = safe_read_sql(
            "SELECT run_ts, price_eur_min, price_eur_med, price_eur_avg, "
            "total_price_eur_med, total_price_eur_avg, "
            "count_total, count_promos, promo_share_pct "
            "FROM weekly_kpis ORDER BY run_ts", conn
        )
        wd = safe_read_sql("SELECT * FROM weekly_diff WHERE run_ts = ?", conn, (last,))
        movers = big_movers(wd, ALERT_PCT, ALERT_EUR) if not wd.empty else pd.DataFrame()

        same_date = safe_read_sql("SELECT * FROM same_date_diff WHERE run_ts = ?", conn, (last,))
        if not same_date.empty:
            same_date = decorate_movement(same_date)

        mo_all = safe_read_sql(
            "SELECT month, destination_label, prix_min, prix_avg, nb_depart "
            "FROM monthly_kpis WHERE run_ts = ? ORDER BY month, destination_label", conn, (last,)
        )

        bd      = best_dates(df_curr)
        topm    = cheapest_by_month(df_curr, top_n=15)
        ctry    = country_summary(df_curr)
        watch   = promo_watchlist(df_curr)
        buckets = price_buckets(df_curr)
        buckets_total = price_buckets_total(df_curr)
        
        # Génération du rapport Chambre Privée
        no_free_pvt = no_free_private_room_report(df_tours_last)

        nb_depart = len(df_curr)
        nb_dest   = df_curr["destination_label"].nunique(dropna=True)
        nb_pays   = df_curr["country_name"].nunique(dropna=True)
        status_count = df_curr["sales_status"].value_counts(dropna=False).to_frame("count").reset_index().rename(columns={"index":"sales_status"})
    finally:
        conn.close()

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    coverage = f"_Historique des runs : du **{runs['run_ts'].iloc[0]}** au **{runs['run_ts'].iloc[-1]}** ({len(runs)} exécutions)._" if not runs.empty else ""

    # Rendus HTML
    kpi_html            = html_table(kpi_last, max_rows=1,    dt=False) if not kpi_last.empty else "<p><em>Aucune donnée</em></p>"
    kpi_hist_html       = html_table(kpi_hist, max_rows=1000, dt=True,  page=25)
    movers_html         = html_table(movers,   max_rows=500,  dt=True,  page=25) if not movers.empty else "<p><em>Aucune donnée</em></p>"
    same_date_html      = html_table(same_date,max_rows=1000, dt=True,  page=25) if not same_date.empty else "<p><em>Aucune donnée</em></p>"
    bd_html             = html_table(bd,       max_rows=600,  dt=True,  page=25)
    topm_html           = html_table(topm,     max_rows=600,  dt=True,  page=25)
    ctry_html           = html_table(ctry,     max_rows=400,  dt=True,  page=25)
    watch_html          = html_table(watch,    max_rows=600,  dt=True,  page=25)
    buckets_html        = html_table(buckets,  max_rows=50,   dt=False)
    buckets_total_html = html_table(buckets_total, max_rows=50, dt=False)
    status_html         = html_table(status_count, max_rows=50, dt=False)
    
    # Rendu HTML pour le nouveau rapport
    no_free_pvt_html    = html_table(no_free_pvt, max_rows=1000, dt=True, page=25) if not no_free_pvt.empty else "<p><em>Toutes les destinations semblent avoir l'option gratuite (ou donnée manquante).</em></p>"

    content = f"""---
title: RoadPrice – Évolutions tarifaires
---

# RoadPrice — synthèse

**Dernier run (UTC)** : `{last}` — Build : `{ts}`  
**Départs suivis : {nb_depart}** — **Destinations : {nb_dest}** — **Pays : {nb_pays}** {coverage}

---

### Répartition des statuts de vente
{status_html}

---

## Indicateurs clés — Dernier run
{kpi_html}

---

## Historique des KPIs (tous les runs)
{kpi_hist_html}

---

## Gros mouvements de prix (Δ% ≥ {ALERT_PCT*100:.0f}% ou Δ€ ≥ {ALERT_EUR:.0f}€) — meilleur prix par destination
{movers_html}

---

## Changements de prix sur mêmes départs (même `tour_id`, même date)
{same_date_html}

---

## Meilleures **dates à réserver** (prix mini par destination, vue actuelle)
{bd_html}

---

## Top offres par **mois** (les moins chères)
{topm_html}

---

## 🚫 Destinations sans "Chambre privée gratuite"
_Liste des départs où l'option `privateRoomForFree` n'est pas disponible._
{no_free_pvt_html}

---

## **Watchlist** — départs proches / confirmés
{watch_html}

---

## Synthèse **par pays**
{ctry_html}

---

## Répartition par **tranches de prix** (prix affiché)
{buckets_html}

---

## Répartition par **tranches de prix totaux** (prix affiché + pot commun médian)
{buckets_total_html}
"""

    # Assets + init robuste (attend que la lib soit chargée)
    datatable_assets = f"""
<link rel="stylesheet" href="{DATATABLES_CSS}">
<script src="{DATATABLES_JS}" defer></script>
<script>
(function() {{
  function initDT() {{
    if (!window.simpleDatatables || !document.querySelectorAll) {{
      return setTimeout(initDT, 120);
    }}
    document.querySelectorAll('table[data-dt="1"]').forEach(function(tbl) {{
      var per = parseInt(tbl.getAttribute('data-page-size') || '25', 10);
      new simpleDatatables.DataTable(tbl, {{
        perPage: per,
        perPageSelect: [10, 25, 50, 100],
        labels: {{
          placeholder: "Rechercher…",
          perPage: "{{select}} lignes par page",
          noRows: "Aucune ligne à afficher",
          info: "Affichage {{start}}–{{end}} sur {{rows}}"
        }},
        fixedHeight: true
      }});
    }});
  }}
  document.addEventListener('DOMContentLoaded', initDT);
}})();
</script>
<style>
.table-wrapper {{ overflow-x:auto; }}
.rp-table {{ width:100%; border-collapse:collapse; }}
.rp-table th, .rp-table td {{ padding:6px 10px; border-bottom:1px solid #eee; }}
code.up {{ color:#0a0; font-weight:700; }}
code.down {{ color:#c00; font-weight:700; }}
code.equal {{ color:#555; }}
</style>
"""
    content += "\n\n" + datatable_assets

    ensure_docs()
    OUT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
