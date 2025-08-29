# summarize.py — Génère docs/index.md à partir de data/weroad.db (schéma run_ts)
from pathlib import Path
from datetime import datetime, timezone
import os
import sqlite3
import pandas as pd

DOCS_DIR = Path("docs")
OUT = DOCS_DIR / "index.md"
DB = Path("data/weroad.db")

# Aperçu des N derniers mois pour certaines sections (si utile)
RECENT_MONTHS = 24

# Seuils d'alertes (peuvent être surchargés par le workflow via env)
ALERT_PCT = float(os.getenv("ALERT_PCT", "0.10"))   # 10%
ALERT_EUR = float(os.getenv("ALERT_EUR", "150"))    # 150 €

# -------- Helpers --------
def ensure_docs():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

def safe_read_sql(sql: str, conn, params: tuple = ()) -> pd.DataFrame:
    try:
        return pd.read_sql_query(sql, conn, params=params)
    except Exception:
        return pd.DataFrame()

def decorate_movement(df: pd.DataFrame) -> pd.DataFrame:
    """Wrap le champ 'movement' avec <code class='up|down|equal'>."""
    if df is None or df.empty or "movement" not in df.columns:
        return df
    m = df["movement"].fillna("=")
    cls = m.map(lambda x: "up" if x == "↑" else ("down" if x == "↓" else "equal"))
    out = df.copy()
    out["movement"] = [f"<code class='{c}'>{s}</code>" for c, s in zip(cls, m)]
    return out

def html_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    """
    Table HTML fiable, gestion précise des % et € :
      - delta_pct = ratio (0..1) => affiché en % via x100
      - *_pct (sauf delta_pct) = déjà 0..100 => affiché tel quel en %
      - colonnes prix/€ formatées en euros
    """
    if df is None or df.empty:
        return "<p><em>Aucune donnée</em></p>"

    df = df.copy().head(max_rows)

    # delta_pct = ratio -> % via x100
    if "delta_pct" in df.columns:
        s = pd.to_numeric(df["delta_pct"], errors="coerce")
        df["delta_pct"] = s.map(lambda v: f"{v*100:.1f}%" if pd.notna(v) else "")

    # *_pct (déjà 0..100) -> format direct, sauf delta_pct traité plus haut
    for c in [c for c in df.columns if c.endswith("_pct") and c != "delta_pct"]:
        s = pd.to_numeric(df[c], errors="coerce")
        df[c] = s.map(lambda v: f"{v:.1f}%" if pd.notna(v) else "")

    # Colonnes € (prix, delta_abs, etc.)
    money_cols = [c for c in df.columns if any(k in c for k in ["price", "prix", "delta_abs", "value_eur"])]
    for c in money_cols:
        s = pd.to_numeric(df[c], errors="coerce")
        df[c] = s.map(lambda v: f"{v:,.0f} €".replace(",", " ").replace(".", ",") if pd.notna(v) else "")

    return df.to_html(index=False, classes="rp-table", escape=False, border=0)

def load_last_and_prev_run_ts(conn):
    runs = safe_read_sql("SELECT DISTINCT run_ts FROM weekly_kpis ORDER BY run_ts", conn)
    if runs.empty:
        return None, None, runs
    last = runs["run_ts"].iloc[-1]
    prev = runs["run_ts"].iloc[-2] if len(runs) > 1 else None
    return last, prev, runs

# -------- Analyses métier --------
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
    base = [
        "sales_status","best_starting_date","best_ending_date",
        "title","destination_label","country_name",
        "price_eur","discount_pct","seatsToConfirm","maxPax","weroadersCount"
    ]
    # lien : prioriser url_precise si présente, sinon url
    link_col = "url_precise" if "url_precise" in x.columns else ("url" if "url" in x.columns else None)
    if link_col:
        base.append(link_col)
    return x[[c for c in base if c in x.columns]].reset_index(drop=True)

def big_movers(wk_diff: pd.DataFrame, pct_threshold=ALERT_PCT, abs_threshold=ALERT_EUR) -> pd.DataFrame:
    """Variations très fortes sur le meilleur prix par destination (vs run précédent)."""
    if wk_diff.empty:
        return pd.DataFrame()
    x = wk_diff.copy()
    # robustesse aux types
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

def best_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Meilleure date (prix min) par destination sur le snapshot courant."""
    base = df.dropna(subset=["destination_label", "price_eur"]).copy()
    if base.empty:
        return pd.DataFrame()
    idx = base.groupby("destination_label")["price_eur"].idxmin()
    out = base.loc[idx, [
        "destination_label","country_name","title",
        "price_eur","base_price_eur","discount_value_eur","discount_pct",
        "sales_status","best_starting_date","best_ending_date","url_precise"
    ]].sort_values(["country_name","destination_label"])
    out = out.reset_index(drop=True).rename(columns={"url_precise":"url"})
    return out

def cheapest_by_month(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Top N offres les moins chères par mois (sur snapshot courant)."""
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
    """Synthèse par pays (nb départs, min/med/moy)."""
    if df.empty:
        return pd.DataFrame()
    g = df.groupby("country_name", dropna=False)
    out = pd.DataFrame({
        "nb_depart": g.size(),
        "prix_min": pd.to_numeric(g["price_eur"], errors="coerce").min(),
        "prix_med": pd.to_numeric(g["price_eur"], errors="coerce").median(),
        "prix_moy": pd.to_numeric(g["price_eur"], errors="coerce").mean(),
        "taux_promos_pct": 100 * g["discount_pct"].apply(lambda s: pd.to_numeric(s, errors="coerce").notna().mean()),
        "rating_moy": pd.to_numeric(g["rating"], errors="coerce").mean(),
        "rating_count": pd.to_numeric(g["rating_count"], errors="coerce").sum(),
    }).reset_index().sort_values(["prix_med","prix_moy","nb_depart"], na_position="last")
    return out

def price_buckets(df: pd.DataFrame):
    """Répartition des offres par tranches de prix (en €)."""
    if df.empty:
        return pd.DataFrame()
    bins = [0, 800, 1000, 1200, 1500, 2000, 3000, 99999]
    labels = ["<800", "800–999", "1000–1199", "1200–1499", "1500–1999", "2000–2999", "≥3000"]
    x = df.dropna(subset=["price_eur"]).copy()
    x["bucket"] = pd.cut(pd.to_numeric(x["price_eur"], errors="coerce"), bins=bins, labels=labels, right=False)
    out = x["bucket"].value_counts().reindex(labels, fill_value=0).reset_index()
    out.columns = ["tranche_prix", "nb_offres"]
    return out

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

        # Snapshots courant & précédent
        df_curr = safe_read_sql("SELECT * FROM snapshots WHERE run_ts = ?", conn, (last,))
        df_prev = safe_read_sql("SELECT * FROM snapshots WHERE run_ts = ?", conn, (prev,)) if prev else pd.DataFrame()

        # KPIs
        kpi_last = safe_read_sql("SELECT * FROM weekly_kpis WHERE run_ts = ?", conn, (last,))
        kpi_hist = safe_read_sql(
            "SELECT run_ts, price_eur_min, price_eur_med, price_eur_avg, count_total, count_promos, promo_share_pct "
            "FROM weekly_kpis ORDER BY run_ts", conn
        )

        # Diff hebdo (meilleur prix par destination)
        wd = safe_read_sql("SELECT * FROM weekly_diff WHERE run_ts = ?", conn, (last,))
        movers = big_movers(wd, ALERT_PCT, ALERT_EUR) if not wd.empty else pd.DataFrame()

        # Changes sur le même départ (tour_id)
        same_date = safe_read_sql("SELECT * FROM same_date_diff WHERE run_ts = ?", conn, (last,))
        if not same_date.empty:
            same_date = decorate_movement(same_date)

        # KPIs mensuels calculés et stockés pour ce run
        mo_all = safe_read_sql(
            "SELECT month, destination_label, prix_min, prix_avg, nb_depart "
            "FROM monthly_kpis WHERE run_ts = ? ORDER BY month, destination_label", conn, (last,)
        )

        # Analyses enrichies
        bd      = best_dates(df_curr)
        topm    = cheapest_by_month(df_curr, top_n=15)
        ctry    = country_summary(df_curr)
        watch   = promo_watchlist(df_curr)
        buckets = price_buckets(df_curr)

        # Compteurs (entête)
        nb_depart = len(df_curr)
        nb_dest   = df_curr["destination_label"].nunique(dropna=True)
        nb_pays   = df_curr["country_name"].nunique(dropna=True)
        status_count = df_curr["sales_status"].value_counts(dropna=False).to_frame("count").reset_index().rename(columns={"index":"sales_status"})
    finally:
        conn.close()

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    coverage = f"_Historique des runs : du **{runs['run_ts'].iloc[0]}** au **{runs['run_ts'].iloc[-1]}** ({len(runs)} exécutions)._" if not runs.empty else ""

    # Rendus HTML
    kpi_html        = html_table(kpi_last, max_rows=1) if not kpi_last.empty else "<p><em>Aucune donnée</em></p>"
    kpi_hist_html   = html_table(kpi_hist, max_rows=500)
    movers_html     = html_table(movers, max_rows=200) if not movers.empty else "<p><em>Aucune donnée</em></p>"
    same_date_html  = html_table(same_date, max_rows=500) if not same_date.empty else "<p><em>Aucune donnée</em></p>"
    bd_html         = html_table(bd, max_rows=400)
    topm_html       = html_table(topm, max_rows=400)
    ctry_html       = html_table(ctry, max_rows=200)
    watch_html      = html_table(watch, max_rows=400)
    buckets_html    = html_table(buckets, max_rows=50)
    status_html     = html_table(status_count, max_rows=50)

    # Page unique
    page = f"""---
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

## **Watchlist** — départs proches / confirmés
{watch_html}

---

## Synthèse **par pays**
{ctry_html}

---

## Répartition par **tranches de prix**
{buckets_html}
"""
    ensure_docs()
    OUT.write_text(page, encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
