# summarize.py — Dashboard HTML enrichi pour GitHub Pages (Jekyll)
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

# ---------- Helpers de rendu ----------
def html_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    """Table HTML fiable (pandas.to_html), formats % et € si colonnes présentes."""
    if df is None or df.empty:
        return "<p><em>Aucune donnée</em></p>"

    df = df.copy().head(max_rows)

    # Colonnes % (delta_pct, *_pct, promo_share_pct)
    pct_cols = [c for c in df.columns if c.endswith("_pct") or c == "delta_pct" or c == "promo_share_pct"]
    for c in pct_cols:
        if c in df.columns:
            df[c] = df[c].map(lambda v: f"{v*100:.1f}%" if pd.notna(v) else "")

    # Colonnes montants €
    money_cols = [c for c in df.columns if any(k in c for k in ["price", "prix", "delta_abs"])]
    for c in money_cols:
        if c in df.columns:
            df[c] = df[c].map(lambda v: f"{v:,.2f} €".replace(",", " ").replace(".", ",") if pd.notna(v) else "")

    return df.to_html(index=False, classes="rp-table", escape=False)


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

def choose_url_col(df: pd.DataFrame) -> pd.Series:
    for c in ("url_curr", "url", "url_prev"):
        if c in df.columns:
            s = df[c]; s.name = "url"; return s
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

# ---------- Blocs d'analyse pour le site ----------
def best_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Meilleure date (prix min) par destination_label."""
    base = df.dropna(subset=["destination_label", "price_eur"]).copy()
    if base.empty:
        return pd.DataFrame()
    idx = base.groupby("destination_label")["price_eur"].idxmin()
    out = base.loc[idx, [
        "destination_label","country_name","title","price_eur","base_price_eur",
        "discount_value_eur","discount_pct","sales_status",
        "best_starting_date","best_ending_date","url"
    ]].sort_values(["country_name","destination_label"]).reset_index(drop=True)
    out.rename(columns={
        "price_eur":"best_price_eur",
        "base_price_eur":"base_price_at_best",
        "best_starting_date":"date_debut",
        "best_ending_date":"date_fin"
    }, inplace=True)
    return out

def cheapest_by_month(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Top N offres les moins chères par mois (à partir de best_starting_date)."""
    tmp = df.dropna(subset=["best_starting_date","price_eur"]).copy()
    if tmp.empty:
        return pd.DataFrame()
    tmp["month_depart"] = tmp["best_starting_date"].map(to_month)
    tmp = tmp.dropna(subset=["month_depart"])
    tmp["rk"] = tmp.groupby("month_depart")["price_eur"].rank(method="first")
    out = tmp[tmp["rk"] <= top_n].sort_values(["month_depart","price_eur"])[[
        "month_depart","destination_label","title","country_name",
        "price_eur","discount_pct","sales_status","best_starting_date","url"
    ]]
    out.rename(columns={"price_eur":"price_eur_min_month"}, inplace=True)
    return out.reset_index(drop=True)

def country_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Synthèse par pays."""
    if df.empty:
        return pd.DataFrame()
    g = df.groupby("country_name", dropna=False)
    out = pd.DataFrame({
        "nb_offres": g.size(),
        "prix_min": g["price_eur"].min(numeric_only=True),
        "prix_med": g["price_eur"].median(numeric_only=True),
        "prix_moy": g["price_eur"].mean(numeric_only=True),
        "taux_promos_pct": 100 * g["discount_pct"].apply(lambda s: s.notna().mean()),
        "rating_moy": g["rating"].mean(numeric_only=True),
        "rating_count": g["rating_count"].sum(numeric_only=True),
    }).reset_index().sort_values(["prix_med","prix_moy","nb_offres"], na_position="last")
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
        "price_eur","discount_pct","seatsToConfirm","maxPax","weroadersCount","url"
    ]
    return x[cols].reset_index(drop=True)

def big_movers(wk_diff: pd.DataFrame, pct_threshold=ALERT_PCT, abs_threshold=ALERT_EUR) -> pd.DataFrame:
    """Var. > seuils, triées par Δ% puis Δ€."""
    if wk_diff.empty:
        return pd.DataFrame()
    x = wk_diff.copy()
    x["flag"] = (x["delta_pct"].abs() > pct_threshold) | (x["delta_abs"].abs() > abs_threshold)
    cols = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url"]
    cols = [c for c in cols if c in x.columns]
    out = x[x["flag"]].sort_values(["delta_pct","delta_abs"], ascending=[False,False])[cols].reset_index(drop=True)
    return decorate_movement(out)

def new_vs_gone(df_curr: pd.DataFrame, df_prev: pd.DataFrame | None):
    """Nouvelles destinations vs disparues (run précédent)."""
    if df_prev is None or df_prev.empty or df_curr.empty:
        return pd.DataFrame(), pd.DataFrame()
    curr = set(df_curr["destination_label"].dropna().unique())
    prev = set(df_prev["destination_label"].dropna().unique())
    new_labels = curr - prev
    gone_labels = prev - curr

    # Nouvelles: on retient le prix min actuel pour un aperçu
    new = df_curr[df_curr["destination_label"].isin(new_labels)].copy()
    if not new.empty:
        idx = new.groupby("destination_label")["price_eur"].idxmin()
        new = new.loc[idx, ["destination_label","country_name","title","price_eur","discount_pct","best_starting_date","url"]]
        new = new.sort_values(["country_name","destination_label"]).reset_index(drop=True)

    # Disparues: on liste du précédent run (sans prix actuel)
    gone = df_prev[df_prev["destination_label"].isin(gone_labels)].copy()
    if not gone.empty:
        idx2 = gone.groupby("destination_label")["price_eur"].idxmin()
        gone = gone.loc[idx2, ["destination_label","country_name","title","price_eur","best_starting_date","url"]]
        gone.rename(columns={"price_eur":"last_seen_price_eur","best_starting_date":"last_seen_date"}, inplace=True)
        gone = gone.sort_values(["country_name","destination_label"]).reset_index(drop=True)

    return new, gone

def price_buckets(df: pd.DataFrame):
    """Répartition nombre d’offres par tranches de prix (en €)."""
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
            OUT.write_text("# RoadPrice\n\n_Aucune donnée disponible pour l’instant._", encoding="utf-8")
            return

        prev = load_prev_run(conn, last)

        # Couverture historique pour l'en-tête
        runs = safe_read_sql("SELECT DISTINCT run_date FROM weekly_kpis ORDER BY run_date", conn)
        start_run = runs["run_date"].iloc[0] if not runs.empty else None
        end_run = runs["run_date"].iloc[-1] if not runs.empty else None

        # Snapshots courant / précédent (pour les nouvelles/disparues)
        df_curr = safe_read_sql("SELECT * FROM snapshots WHERE run_date = ?", conn, (last,))
        df_prev = safe_read_sql("SELECT * FROM snapshots WHERE run_date = ?", conn, (prev,)) if prev else pd.DataFrame()

        # KPIs dernier run + historique
        kpi_last = safe_read_sql("SELECT * FROM weekly_kpis WHERE run_date = ?", conn, (last,))
        kpi_hist = safe_read_sql(
            "SELECT run_date, price_eur_min, price_eur_med, price_eur_avg, "
            "count_total, count_promos, promo_share_pct "
            "FROM weekly_kpis ORDER BY run_date", conn
        )

        # Weekly diff (dernier run)
        wd = safe_read_sql("SELECT * FROM weekly_diff WHERE run_date = ?", conn, (last,))
        if not wd.empty:
            wd["url"] = choose_url_col(wd)
            base_cols = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url"]
            base_cols = [c for c in base_cols if c in wd.columns]
            wd = wd[base_cols].copy()

        # Mensuel (complet)
        mo_all = safe_read_sql(
            "SELECT month, destination_label, prix_min, prix_avg, nb_depart "
            "FROM monthly_kpis ORDER BY month, destination_label", conn
        )

        # Analyses enrichies
        bd = best_dates(df_curr)
        topm = cheapest_by_month(df_curr, top_n=15)
        ctry = country_summary(df_curr)
        watch = promo_watchlist(df_curr)
        movers = big_movers(wd, ALERT_PCT, ALERT_EUR) if not wd.empty else pd.DataFrame()
        new_df, gone_df = new_vs_gone(df_curr, df_prev)
        buckets = price_buckets(df_curr)

        # Aperçu des N derniers mois
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

    # Rendus HTML
    kpi_html = html_table(kpi_last[[
        c for c in ["price_eur_min","price_eur_med","price_eur_avg","count_total","count_promos","promo_share_pct"]
        if c in kpi_last.columns
    ]], max_rows=1) if not kpi_last.empty else "<p><em>Aucune donnée</em></p>"

    kpi_hist_html    = html_table(kpi_hist, max_rows=500) if not kpi_hist.empty else "<p><em>Aucune donnée</em></p>"
    movers_html      = html_table(movers, max_rows=200)
    bd_html          = html_table(bd, max_rows=400)
    topm_html        = html_table(topm, max_rows=400)
    ctry_html        = html_table(ctry, max_rows=200)
    watch_html       = html_table(watch, max_rows=400)
    new_html         = html_table(new_df, max_rows=200)
    gone_html        = html_table(gone_df, max_rows=200)
    buckets_html     = html_table(buckets, max_rows=50)
    mo_all_html      = html_table(mo_all, max_rows=1000)
    mo_recent_html   = html_table(mo_recent, max_rows=300)

    # Page
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
{kpi_html}

---

## Historique des KPIs hebdo (tous les runs)
{kpi_hist_html}

---

## Gros mouvements de prix (Δ% ≥ {ALERT_PCT*100:.0f}% ou Δ€ ≥ {ALERT_EUR:.0f}€)
{movers_html}

---

## Meilleures **dates à réserver** (prix mini par destination)
{bd_html}

---

## Top offres par **mois** (les moins chères)
{topm_html}

---

## **Watchlist** — départs proches / presque confirmés
{watch_html}

---

## Nouvelles **destinations** du run
{new_html}

## Destinations **disparues** vs run précédent
{gone_html}

---

## Répartition par **tranches de prix**
{buckets_html}

---

## KPIs mensuels
