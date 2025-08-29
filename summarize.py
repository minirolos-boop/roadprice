# summarize.py — Dashboard HTML (single page) pour snapshots PAR DATE (tour_id)
# Génère docs/index.md

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
ALERT_PCT = float(os.getenv("ALERT_PCT", "0.10"))   # 0.10 = 10%
ALERT_EUR = float(os.getenv("ALERT_EUR", "150"))    # 150 €

# ---------- Helpers ----------
def ensure_docs():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

def safe_read_sql(sql: str, conn, params: tuple = ()) -> pd.DataFrame:
    try:
        return pd.read_sql_query(sql, conn, params=params)
    except Exception:
        return pd.DataFrame()

def choose_url_precise_col(df: pd.DataFrame) -> pd.Series:
    for c in ("url_precise", "url"):
        if c in df.columns:
            s = df[c]
            s.name = "url_precise"
            return s
    return pd.Series([None] * len(df), index=df.index, name="url_precise")

def decorate_movement(df: pd.DataFrame) -> pd.DataFrame:
    """Colorise mouvement: ↑ rouge, ↓ vert, = gris (via <code class='up|down|equal'>)."""
    if df is None or df.empty or "movement" not in df.columns:
        return df
    m = df["movement"].fillna("=")
    cls = m.map(lambda x: "up" if x == "↑" else ("down" if x == "↓" else "equal"))
    out = df.copy()
    out["movement"] = [f"<code class='{c}'>{s}</code>" for c, s in zip(cls, m)]
    return out

def html_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    """
    Table HTML fiable (pandas.to_html), avec formats % et €.
    - Colonnes *delta_pct* sont des ratios (0..1) -> formatage x100.
    - Colonnes terminant par *_pct* (ex: discount_pct, promo_share_pct) sont déjà en % 0..100 -> pas de *100.
    - Colonnes prix/€, delta_abs en €.
    """
    if df is None or df.empty:
        return "<p><em>Aucune donnée</em></p>"

    df = df.copy().head(max_rows)

    # Liens cliquables si la colonne url ou url_precise existe
    for url_col in ("url_precise", "url"):
        if url_col in df.columns:
            df[url_col] = df[url_col].map(lambda u: f"<a href='{u}' target='_blank'>{u}</a>" if isinstance(u, str) else u)

    # Format % pour delta_pct (ratio) -> x100
    if "delta_pct" in df.columns:
        df["delta_pct"] = df["delta_pct"].map(
            lambda v: (f"{v*100:.1f}%" if pd.notna(v) else "")
        )

    # Format % pour colonnes *_pct (déjà en 0..100)
    pct_cols = [c for c in df.columns if c.endswith("_pct") and c != "delta_pct"]
    for c in pct_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
        df[c] = df[c].map(lambda v: f"{v:.1f}%" if pd.notna(v) else "")

    # Colonnes montants €
    money_cols = [c for c in df.columns if any(k in c for k in ["price", "prix", "delta_abs", "value_eur"])]
    for c in money_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
        df[c] = df[c].map(lambda v: f"{v:,.0f} €".replace(",", " ").replace(".", ",") if pd.notna(v) else "")

    return df.to_html(index=False, classes="rp-table", escape=False)

def load_last_run(conn) -> str | None:
    last_df = safe_read_sql("SELECT MAX(run_date) AS r FROM snapshots", conn)
    if not last_df.empty and pd.notna(last_df.loc[0, "r"]):
        return last_df.loc[0, "r"]
    return None

def load_prev_run(conn, last: str) -> str | None:
    df = safe_read_sql("SELECT DISTINCT run_date FROM snapshots WHERE run_date < ? ORDER BY run_date", conn, (last,))
    if not df.empty:
        return df["run_date"].iloc[-1]
    return None

# ---------- Blocs d’analyse pour le site ----------
def best_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Meilleur prix (min) par destination_label (vue actuelle)."""
    base = df.dropna(subset=["destination_label", "price_eur"]).copy()
    if base.empty:
        return pd.DataFrame()
    idx = base.groupby("destination_label")["price_eur"].idxmin()
    out = base.loc[idx, [
        "destination_label","country_name","title",
        "price_eur","base_price_eur","discount_value_eur","discount_pct",
        "sales_status","best_starting_date","best_ending_date","url_precise"
    ]].sort_values(["country_name","destination_label"]).reset_index(drop=True)
    out.rename(columns={"url_precise":"url"}, inplace=True)
    return out

def cheapest_by_month(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Top N offres les moins chères par mois (à partir de best_starting_date)."""
    tmp = df.dropna(subset=["best_starting_date","price_eur"]).copy()
    if tmp.empty:
        return pd.DataFrame()
    tmp["month_depart"] = pd.to_datetime(tmp["best_starting_date"], errors="coerce").dt.strftime("%Y-%m")
    tmp = tmp.dropna(subset=["month_depart"])
    tmp["rk"] = tmp.groupby("month_depart")["price_eur"].rank(method="first")
    out = tmp[tmp["rk"] <= top_n].sort_values(["month_depart","price_eur"])[[
        "month_depart","destination_label","title","country_name",
        "price_eur","discount_pct","sales_status","best_starting_date","url_precise"
    ]]
    out.rename(columns={"url_precise":"url"}, inplace=True)
    return out.reset_index(drop=True)

def country_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Synthèse par pays."""
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
    cols = [
        "sales_status","best_starting_date","best_ending_date",
        "title","destination_label","country_name",
        "price_eur","discount_pct","seatsToConfirm","maxPax","weroadersCount","url_precise"
    ]
    x.rename(columns={"url_precise":"url"}, inplace=True)
    return x[cols].reset_index(drop=True)

def big_movers_from_sql(conn, last: str) -> pd.DataFrame:
    """Lit weekly_diff (meilleur prix par destination) et la décore."""
    wd = safe_read_sql("SELECT * FROM weekly_diff WHERE run_date = ?", conn, (last,))
    if wd.empty:
        return wd
    # petite normalisation de colonnes attendues
    base_cols = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url"]
    wd = wd[[c for c in base_cols if c in wd.columns]].copy()
    return decorate_movement(wd)

# ---------- Page ----------
def main():
    ensure_docs()

    if not DB.exists():
        OUT.write_text("# RoadPrice\n\n_Base SQLite absente : `data/weroad.db`_", encoding="utf-8")
        print("No DB found, wrote placeholder page.")
        return

    conn = sqlite3.connect(DB)
    try:
        last = load_last_run(conn)
        if not last:
            OUT.write_text("# RoadPrice\n\n_Aucune donnée disponible pour l’instant._", encoding="utf-8")
            print("No runs in DB, wrote placeholder page.")
            return

        prev = load_prev_run(conn, last)

        # Snapshots courant (PAR DATE)
        df_curr = safe_read_sql("SELECT * FROM snapshots WHERE run_date = ?", conn, (last,))
        df_prev = safe_read_sql("SELECT * FROM snapshots WHERE run_date = ?", conn, (prev,)) if prev else pd.DataFrame()

        # Total de départs suivis au run courant
        total_departures = len(df_curr)

        # KPIs dernier run + historique
        kpi_last = safe_read_sql("SELECT * FROM weekly_kpis WHERE run_date = ?", conn, (last,))
        kpi_hist = safe_read_sql(
            "SELECT run_date, price_eur_min, price_eur_med, price_eur_avg, "
            "count_total, count_promos, promo_share_pct "
            "FROM weekly_kpis ORDER BY run_date", conn
        )

        # Diff hebdo (meilleurs prix par destination)
        movers = big_movers_from_sql(conn, last)

        # Mensuel (complet)
        mo_all = safe_read_sql(
            "SELECT month, destination_label, prix_min, prix_avg, nb_depart "
            "FROM monthly_kpis ORDER BY month, destination_label", conn
        )

        # Analyses enrichies basées sur df_curr
        bd    = best_dates(df_curr)
        topm  = cheapest_by_month(df_curr, top_n=15)
        ctry  = country_summary(df_curr)
        watch = promo_watchlist(df_curr)

        # Same date diff (même tour_id entre runs)
        same_date = safe_read_sql("SELECT * FROM same_date_diff WHERE run_date = ?", conn, (last,))
        if not same_date.empty:
            # Choisir url précise si dispo
            same_date["url_precise"] = choose_url_precise_col(same_date)
            # décoration ↑↓
            same_date = decorate_movement(same_date)

        # Aperçu des N derniers mois
        mo_recent = pd.DataFrame()
        if not mo_all.empty:
            unique_months = sorted(mo_all["month"].dropna().unique())
            recent_months = unique_months[-RECENT_MONTHS:] if len(unique_months) > RECENT_MONTHS else unique_months
            mo_recent = mo_all[mo_all["month"].isin(recent_months)].copy()
    finally:
        conn.close()

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Rendus HTML
    kpi_html        = html_table(kpi_last[[c for c in ["price_eur_min","price_eur_med","price_eur_avg","count_total","count_promos","promo_share_pct"] if c in kpi_last.columns]], max_rows=1) if not kpi_last.empty else "<p><em>Aucune donnée</em></p>"
    kpi_hist_html   = html_table(kpi_hist, max_rows=500) if not kpi_hist.empty else "<p><em>Aucune donnée</em></p>"
    movers_html     = html_table(movers, max_rows=200) if not movers.empty else "<p><em>Aucune donnée</em></p>"
    bd_html         = html_table(bd, max_rows=400)
    topm_html       = html_table(topm, max_rows=400)
    ctry_html       = html_table(ctry, max_rows=200)
    watch_html      = html_table(watch, max_rows=400)
    same_date_html  = html_table(same_date, max_rows=500) if not same_date.empty else "<p><em>Aucune donnée</em></p>"
    mo_all_html     = html_table(mo_all, max_rows=1000)
    mo_recent_html  = html_table(mo_recent, max_rows=300)

    # Page (une seule)
    content = f"""---
title: RoadPrice – Évolutions tarifaires
---

# RoadPrice — synthèse

**Dernier run : `{last}`** — Build: `{ts}`  
**Nombre total de départs suivis : {total_departures}**

> Les fichiers détaillés (Excel & SQLite) sont disponibles dans l’onglet **Actions → Artifacts** du dépôt.

---

## Indicateurs clés — Dernier run
{kpi_html}

---

## Historique des KPIs hebdo (tous les runs)
{kpi_hist_html}

---

## Gros mouvements de prix (Δ% ≥ {ALERT_PCT*100:.0f}% ou Δ€ ≥ {ALERT_EUR:.0f}€) — meilleurs prix par destination
{movers_html}

---

## Changements de prix sur mêmes départs (même date, même voyage)
{same_date_html}

---

## Meilleures **dates à réserver** (prix mini par destination, vue actuelle)
{bd_html}

---

## Top offres par **mois** (les moins chères)
{topm_html}

---

## **Watchlist** — départs proches / presque confirmés
{watch_html}

---

## Synthèse **par pays**
{ctry_html}

---

## KPIs mensuels — Vue complète (toutes années)
{mo_all_html}

---

## KPIs mensuels — Aperçu {RECENT_MONTHS} derniers mois
{mo_recent_html}

---

### Légende
- <strong>Δ%</strong> : variation **relative** (ratio) vs snapshot précédent (affiché x100 en %).  
- <strong>Δ€</strong> : variation **absolue** en euros.  
- Les liens mènent de préférence à la page **départ précis** (quand disponible).
"""
    OUT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
