# summarize.py — Génère docs/index.md à partir de data/weroad.db (schéma avec run_ts)
from pathlib import Path
from datetime import datetime, timezone
import os
import sqlite3
import pandas as pd
import re

DOCS_DIR = Path("docs")
OUT = DOCS_DIR / "index.md"
DB = Path("data/weroad.db")

# Conserver seulement l'équivalent de RECENT_MONTHS mois d'historique (approx. 4 runs/semaine)
RECENT_MONTHS = 24

# Seuils d'alertes
ALERT_PCT = float(os.getenv("ALERT_PCT", "0.10"))   # 10%
ALERT_EUR = float(os.getenv("ALERT_EUR", "150"))    # 150 €

# --- Simple-DataTables (CDN fiables) ---
DATATABLES_CSS = "https://cdn.jsdelivr.net/npm/simple-datatables@latest/dist/style.css"
DATATABLES_JS  = "https://cdn.jsdelivr.net/npm/simple-datatables@latest/dist/umd/simple-datatables.js"

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
    m = df["movement"].astype(str).replace({"nan": "="}).fillna("=")
    cls = m.map(lambda x: "up" if x == "↑" else ("down" if x == "↓" else "equal"))
    out = df.copy()
    out["movement"] = [f"<code class='{c}'>{s}</code>" for c, s in zip(cls, m)]
    return out

def html_table(df: pd.DataFrame, max_rows: int = 20, dt: bool = True, page: int = 25) -> str:
    """to_html + formats € / %, et balise data-dt pour activer Simple-DataTables côté client."""
    if df is None or df.empty:
        return "<p><em>Aucune donnée</em></p>"

    df = df.copy().head(max_rows)

    # Rendre les URLs cliquables
    for link_col in ["url_precise", "url"]:
        if link_col in df.columns:
            df[link_col] = df[link_col].map(
                lambda u: f'<a href="{u}" target="_blank" rel="noopener">🔗</a>' if isinstance(u, str) and u else ""
            )

    # delta_pct = ratio -> % via x100
    if "delta_pct" in df.columns:
        s = pd.to_numeric(df["delta_pct"], errors="coerce")
        df["delta_pct"] = s.map(lambda v: f"{v*100:.1f}%" if pd.notna(v) else "")

    # *_pct (déjà 0..100), hors delta_pct
    for c in [c for c in df.columns if c.endswith("_pct") and c != "delta_pct"]:
        s = pd.to_numeric(df[c], errors="coerce")
        df[c] = s.map(lambda v: f"{v:.1f}%" if pd.notna(v) else "")

    # Colonnes € (prix, delta_abs, value_eur, money_pot, etc.)
    money_cols = [c for c in df.columns if any(k in c for k in ["price", "prix", "delta_abs", "value_eur", "money_pot"])]
    for c in money_cols:
        s = pd.to_numeric(df[c], errors="coerce")
        df[c] = s.map(lambda v: f"{v:,.0f} €".replace(",", " ").replace(".", ",") if pd.notna(v) else "")

    html = df.to_html(index=False, classes="rp-table", escape=False, border=0)

    # Active DataTables (recherche/tri/pagination) si tableau non minuscule
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
        "price_eur","discount_pct","seatsToConfirm","maxPax","weroadersCount"
    ]
    link_col = "url_precise" if "url_precise" in x.columns else ("url" if "url" in x.columns else None)
    if link_col:
        base.append(link_col)
    return x[[c for c in base if c in x.columns]].reset_index(drop=True)

def big_movers(wk_diff: pd.DataFrame, pct_threshold=ALERT_PCT, abs_threshold=ALERT_EUR) -> pd.DataFrame:
    if wk_diff.empty:
        return pd.DataFrame()
    x = wk_diff.copy()
    x["delta_pct"] = pd.to_numeric(x.get("delta_pct"), errors="coerce")
    x["delta_abs"] = pd.to_numeric(x.get("delta_abs"), errors="coerce")
    flag_pct = x["delta_pct"].abs() > pct_threshold
    flag_abs = x["delta_abs"].abs() > abs_threshold
    x["flag"] = flag_pct.fillna(False) | flag_abs.fillna(False)

    cols = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement"]
    if "url_precise" in x.columns:
        cols.append("url_precise")
    elif "url" in x.columns:
        cols.append("url")
    cols = [c for c in cols if c in x.columns]

    out = x[x["flag"]].sort_values(["delta_pct","delta_abs"], ascending=[False,False])[cols].reset_index(drop=True)
    return decorate_movement(out)

def best_dates(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=["destination_label", "price_eur"]).copy()
    if base.empty:
        return pd.DataFrame()
    cols = [
        "destination_label","country_name","title",
        "price_eur","base_price_eur","discount_value_eur","discount_pct",
        "sales_status","best_starting_date","best_ending_date","url_precise"
    ]
    # colonnes money pot si dispo
    for c in ("money_pot_min_eur","money_pot_max_eur"):
        if c in base.columns:
            cols.append(c)
    idx = base.groupby("destination_label")["price_eur"].idxmin()
    out = base.loc[idx, cols].sort_values(["country_name","destination_label"]).reset_index(drop=True)
    return out.rename(columns={"url_precise":"url"})

def cheapest_by_month(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    tmp = df.dropna(subset=["best_starting_date","price_eur"]).copy()
    if tmp.empty:
        return pd.DataFrame()
    tmp["month_depart"] = pd.to_datetime(tmp["best_starting_date"], errors="coerce").dt.strftime("%Y-%m")
    tmp = tmp.dropna(subset=["month_depart"])
    tmp["rk"] = tmp.groupby("month_depart")["price_eur"].rank(method="first")
    out = tmp[tmp["rk"] <= top_n].sort_values(["month_depart","price_eur"])[[
        "month_depart","destination_label","title","country_name",
        "price_eur","discount_pct","sales_status","best_starting_date","url_precise"
    ]].reset_index(drop=True).rename(columns={"url_precise":"url"})
    return out

def country_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    x = df.copy()
    for col in ["price_eur", "discount_pct", "rating", "rating_count"]:
        if col in x.columns:
            x[col] = pd.to_numeric(x[col], errors="coerce")
    g = x.groupby("country_name", dropna=False)
    out = pd.DataFrame({
        "nb_depart": g.size(),
        "prix_min": g["price_eur"].min(),
        "prix_med": g["price_eur"].median(),
        "prix_moy": g["price_eur"].mean(),
        "taux_promos_pct": 100 * g["discount_pct"].apply(lambda s: s.notna().mean()),
        "rating_moy": g["rating"].mean(),
        "rating_count": g["rating_count"].sum(),
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

def money_pot_per_destination(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retourne un tableau 'MoneyPot par destination' :
    slug, title, destination_label, money_pot_min_eur, money_pot_max_eur, url
    (lignes où au moins une des valeurs min/max est définie)
    """
    if df.empty:
        return pd.DataFrame()
    cols_needed = ["slug","title","destination_label","money_pot_min_eur","money_pot_max_eur","url"]
    present = [c for c in cols_needed if c in df.columns]
    if not set(["money_pot_min_eur","money_pot_max_eur"]).issubset(df.columns):
        return pd.DataFrame(columns=present)
    x = df[present].copy()
    x = x[(x["money_pot_min_eur"].notna()) | (x["money_pot_max_eur"].notna())]
    if x.empty:
        return x
    x["money_pot_min_eur"] = pd.to_numeric(x["money_pot_min_eur"], errors="coerce")
    x["money_pot_max_eur"] = pd.to_numeric(x["money_pot_max_eur"], errors="coerce")
    x = x.sort_values(["money_pot_min_eur","money_pot_max_eur","destination_label","title"], na_position="last")
    return x.reset_index(drop=True)

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

        # Données courantes et précédentes
        df_curr = safe_read_sql("SELECT * FROM snapshots WHERE run_ts = ?", conn, (last,))
        df_prev = safe_read_sql("SELECT * FROM snapshots WHERE run_ts = ?", conn, (prev,)) if prev else pd.DataFrame()

        # KPIs courants et historique
        kpi_last = safe_read_sql("SELECT * FROM weekly_kpis WHERE run_ts = ?", conn, (last,))
        kpi_hist = safe_read_sql(
            "SELECT run_ts, price_eur_min, price_eur_med, price_eur_avg, count_total, count_promos, promo_share_pct "
            "FROM weekly_kpis ORDER BY run_ts", conn
        )
        if not kpi_hist.empty and RECENT_MONTHS:
            keep_n = RECENT_MONTHS * 4  # approx 4 semaines/mois
            kpi_hist = kpi_hist.tail(keep_n)

        # Diff hebdo et gros mouvements
        wd = safe_read_sql("SELECT * FROM weekly_diff WHERE run_ts = ?", conn, (last,))
        movers = big_movers(wd, ALERT_PCT, ALERT_EUR) if not wd.empty else pd.DataFrame()

        # Same-date diff (avec MoneyPot joint sur le run courant via slug)
        same_date = safe_read_sql("SELECT * FROM same_date_diff WHERE run_ts = ?", conn, (last,))
        if not same_date.empty:
            # jointure MoneyPot (par slug) depuis df_curr
            mcols = [c for c in ("slug","money_pot_min_eur","money_pot_max_eur") if c in df_curr.columns]
            same_date = same_date.merge(df_curr[mcols].drop_duplicates("slug"), on="slug", how="left")
            # ordre de colonnes: montrer MoneyPot juste après les deltas
            preferred = [
                "run_ts","tour_id","slug","destination_label","title","starting_date",
                "price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement",
                "money_pot_min_eur","money_pot_max_eur",
                "url_precise"
            ]
            cols = [c for c in preferred if c in same_date.columns] + [c for c in same_date.columns if c not in preferred]
            same_date = same_date[cols]
            same_date = decorate_movement(same_date)

        # Vues dérivées
        bd      = best_dates(df_curr)
        topm    = cheapest_by_month(df_curr, top_n=15)
        ctry    = country_summary(df_curr)
        watch   = promo_watchlist(df_curr)
        buckets = price_buckets(df_curr)
        mppd    = money_pot_per_destination(df_curr)

        # Stats globales + statuts
        nb_depart = len(df_curr)
        nb_dest   = df_curr["destination_label"].nunique(dropna=True)
        nb_pays   = df_curr["country_name"].nunique(dropna=True)

        status = df_curr["sales_status"].astype(str)
        status_count = (
            status.value_counts(dropna=False)
            .rename_axis("sales_status")
            .reset_index(name="count")
        )
        total_rows = int(status_count["count"].sum()) or 1
        status_count["share_pct"] = (100 * status_count["count"] / total_rows).round(1)
        status_count = status_count.sort_values("count", ascending=False)

    finally:
        conn.close()

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    coverage = (
        f"_Historique des runs : du **{runs['run_ts'].iloc[0]}** au **{runs['run_ts'].iloc[-1]}** ({len(runs)} exécutions)._"
        if not runs.empty else ""
    )

    # Rendus HTML des tableaux
    kpi_html        = html_table(kpi_last, max_rows=1,    dt=False) if not kpi_last.empty else "<p><em>Aucune donnée</em></p>"
    kpi_hist_html   = html_table(kpi_hist, max_rows=1000, dt=True,  page=25)
    movers_html     = html_table(movers,   max_rows=500,  dt=True,  page=25) if not movers.empty else "<p><em>Aucune donnée</em></p>"
    same_date_html  = html_table(same_date,max_rows=1000, dt=True,  page=25) if not same_date.empty else "<p><em>Aucune donnée</em></p>"
    bd_html         = html_table(bd,       max_rows=600,  dt=True,  page=25)
    topm_html       = html_table(topm,     max_rows=600,  dt=True,  page=25)
    ctry_html       = html_table(ctry,     max_rows=400,  dt=True,  page=25)
    watch_html      = html_table(watch,    max_rows=600,  dt=True,  page=25)
    buckets_html    = html_table(buckets,  max_rows=50,   dt=False)
    status_html     = html_table(status_count, max_rows=50, dt=False)
    mppd_html       = html_table(mppd,     max_rows=800,  dt=True,  page=25)

    content = f"""---
title: RoadPrice – Évolutions tarifaires
---

# RoadPrice — synthèse

**Dernier run (UTC)** : `{last}` — Build : `{ts}`  
**Départs suivis : {nb_depart}** — **Destinations : {nb_dest}** — **Pays : {nb_pays}**  
{coverage}

---

### Répartition des statuts de vente
{status_html}

---

## Indicateurs clés — Dernier run
{kpi_html}

---

## Historique des KPIs (derniers runs)
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

## MoneyPot par destination
{mppd_html}

---

## Top offres par **mois** (les moins chères)
{topm_html}

---

## **Watchlist** — départs proches / confirmés
{watch_html}

---

## Synthèse **par pays**
{ctry_html}

---

## Répartition par **tranches de prix**
{buckets_html}
"""

    # Assets + init robuste (attend que la lib soit chargée) + petits styles
    datatable_assets = f"""
<link rel="stylesheet" href="{DATATABLES_CSS}">
<style>
  .table-wrapper {{ overflow-x:auto; }}
  table.rp-table {{ border-collapse: collapse; width:100%; }}
  table.rp-table th, table.rp-table td {{ padding: 6px 10px; }}
  code.up {{ background:#e6ffed; color:#046b00; padding:2px 6px; border-radius:4px; }}
  code.down {{ background:#ffecec; color:#a40000; padding:2px 6px; border-radius:4px; }}
  code.equal {{ background:#f3f4f6; color:#374151; padding:2px 6px; border-radius:4px; }}
</style>
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
"""
    content += "\n\n" + datatable_assets

    ensure_docs()
    OUT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
