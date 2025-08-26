# summarize.py — Génère un site multi-pages (Jekyll) dans docs/
# Pages : index.md, weekly.md, monthly.md, best-dates.md, countries.md, watchlist.md

from pathlib import Path
from datetime import datetime, timezone
import os
import sqlite3
import pandas as pd

DOCS = Path("docs")
DB = Path("data/weroad.db")

# Fichiers de sortie
OUT_INDEX     = DOCS / "index.md"
OUT_WEEKLY    = DOCS / "weekly.md"
OUT_MONTHLY   = DOCS / "monthly.md"
OUT_BEST      = DOCS / "best-dates.md"
OUT_COUNTRIES = DOCS / "countries.md"
OUT_WATCH     = DOCS / "watchlist.md"

# Paramètres
RECENT_MONTHS = 24
ALERT_PCT = float(os.getenv("ALERT_PCT", "0.10"))
ALERT_EUR = float(os.getenv("ALERT_EUR", "150"))

# ---------------------- Utils / Rendu ----------------------
def ensure_dirs():
    (DOCS / "_includes").mkdir(parents=True, exist_ok=True)
    (DOCS / "assets" / "css").mkdir(parents=True, exist_ok=True)

def safe_sql(conn, q, params=()):
    try:
        return pd.read_sql_query(q, conn, params=params)
    except Exception:
        return pd.DataFrame()

def choose_url_col(df: pd.DataFrame) -> pd.Series:
    for c in ("url_curr", "url", "url_prev"):
        if c in df.columns:
            s = df[c].copy()
            s.name = "url"
            return s
    return pd.Series([None] * len(df), index=df.index, name="url")

def linkify_url_col(df: pd.DataFrame):
    if "url" in df.columns:
        df["url"] = df["url"].map(lambda u: f"<a target='_blank' href='{u}'>🔗 voir</a>" if pd.notna(u) and str(u) != "" else "")
    return df

def style_status_badge(v: str) -> str:
    if v is None: return ""
    v = str(v).upper().strip()
    m = {
        "ALMOST_CONFIRMED": "<span class='rp-badge almost'>ALMOST</span>",
        "CONFIRMED":        "<span class='rp-badge confirmed'>CONFIRMED</span>",
        "GUARANTEED":       "<span class='rp-badge guaranteed'>GUARANTEED</span>",
        "ON_SALE":          "<span class='rp-badge on-sale'>ON SALE</span>",
        "WAITING_LIST":     "<span class='rp-badge default'>WAITING</span>",
        "PLANNED":          "<span class='rp-badge on-sale'>PLANNED</span>",
        "SOLD_OUT":         "<span class='rp-badge default'>SOLD OUT</span>",
    }
    return m.get(v, f"<span class='rp-badge default'>{v}</span>")

def decorate_movement(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty or "movement" not in df.columns:
        return df
    m = df["movement"].fillna("=")
    cls = m.map(lambda x: "up" if x == "↑" else ("down" if x == "↓" else "equal"))
    out = df.copy()
    out["movement"] = [f"<code class='{c}'>{s}</code>" for c, s in zip(cls, m)]
    return out

def html_table(df: pd.DataFrame, max_rows=50) -> str:
    """
    Table HTML (pandas.to_html) + formats (€/%), sans casser les cellules déjà HTML.
    Enveloppée par .table-wrapper pour le scroll horizontal.
    """
    if df is None or df.empty:
        return "<p><em>Aucune donnée</em></p>"
    df = df.copy().head(max_rows)

    def has_html(s: pd.Series) -> bool:
        return s.dtype == "object" and s.astype(str).str.contains("<", regex=False).any()

    # formater % si pas déjà stylé
    pct_cols = [c for c in df.columns if c.endswith("_pct") or c in ("delta_pct", "promo_share_pct")]
    for c in pct_cols:
        if c in df.columns and not has_html(df[c]):
            df[c] = df[c].map(lambda v: f"{v*100:.1f}%" if pd.notna(v) else "")

    # formater montants si pas déjà stylé
    money_cols = [c for c in df.columns if any(k in c for k in ["price", "prix", "delta_abs"])]
    for c in money_cols:
        if c in df.columns and not has_html(df[c]):
            df[c] = df[c].map(lambda v: f"{v:,.2f} €".replace(",", " ").replace(".", ",") if pd.notna(v) else "")

    return "<div class='table-wrapper'>\n" + df.to_html(index=False, classes="rp-table", escape=False) + "\n</div>"

def write_page(path: Path, title: str, body_html: str):
    nav = "{% include nav.html %}"
    content = f"""---
title: {title}
---

{nav}

{body_html}
"""
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path}")

def to_month(s):
    try:
        return pd.to_datetime(s).strftime("%Y-%m")
    except Exception:
        return None

# ---------------------- Analyses ----------------------
def best_dates(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=["destination_label", "price_eur"]).copy()
    if base.empty: return pd.DataFrame()
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
    if "sales_status" in out.columns:
        out["sales_status"] = out["sales_status"].map(style_status_badge)
    out = linkify_url_col(out)
    return out

def cheapest_by_month(df: pd.DataFrame, top_n=15) -> pd.DataFrame:
    tmp = df.dropna(subset=["best_starting_date","price_eur"]).copy()
    if tmp.empty: return pd.DataFrame()
    tmp["month_depart"] = tmp["best_starting_date"].map(to_month)
    tmp = tmp.dropna(subset=["month_depart"])
    tmp["rk"] = tmp.groupby("month_depart")["price_eur"].rank(method="first")
    out = tmp[tmp["rk"] <= top_n].sort_values(["month_depart","price_eur"])[[
        "month_depart","destination_label","title","country_name",
        "price_eur","discount_pct","sales_status","best_starting_date","url"
    ]]
    out.rename(columns={"price_eur":"price_eur_min_month"}, inplace=True)
    if "sales_status" in out.columns:
        out["sales_status"] = out["sales_status"].map(style_status_badge)
    out = linkify_url_col(out)
    return out.reset_index(drop=True)

def country_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return pd.DataFrame()
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
    if df.empty: return pd.DataFrame()
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
    x = x[cols].reset_index(drop=True)
    if "sales_status" in x.columns:
        x["sales_status"] = x["sales_status"].map(style_status_badge)
    x = linkify_url_col(x)
    return x

def big_movers(wk_diff: pd.DataFrame, pct_threshold=ALERT_PCT, abs_threshold=ALERT_EUR) -> pd.DataFrame:
    if wk_diff.empty: return pd.DataFrame()
    x = wk_diff.copy()
    # Sécurisation numérique
    for c in ("delta_pct","delta_abs","price_eur_prev","price_eur_curr"):
        if c in x.columns:
            x[c] = pd.to_numeric(x[c], errors="coerce")
    x["flag"] = (x["delta_pct"].abs() > pct_threshold) | (x["delta_abs"].abs() > abs_threshold)
    cols = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url"]
    cols = [c for c in cols if c in x.columns]
    out = x[x["flag"]].sort_values(["delta_pct","delta_abs"], ascending=[False, False])[cols].reset_index(drop=True)
    # Δ% en pourcentage coloré (span) + mouvement coloré + lien URL
    if "delta_pct" in out.columns:
        out["delta_pct"] = out["delta_pct"].map(lambda v: "" if pd.isna(v) else (f"<span class='rp-delta-pos'>+{v:.1%}</span>" if v>0 else (f"<span class='rp-delta-neg'>{v:.1%}</span>" if v<0 else "<span class='rp-delta-eq'>0%</span>")))
    out = decorate_movement(out)
    out = linkify_url_col(out)
    return out

def new_vs_gone(df_curr: pd.DataFrame, df_prev: pd.DataFrame | None):
    if df_prev is None or df_prev.empty or df_curr.empty:
        return pd.DataFrame(), pd.DataFrame()
    curr = set(df_curr["destination_label"].dropna().unique())
    prev = set(df_prev["destination_label"].dropna().unique())
    new_labels  = curr - prev
    gone_labels = prev - curr

    new = df_curr[df_curr["destination_label"].isin(new_labels)].copy()
    if not new.empty:
        idx = new.groupby("destination_label")["price_eur"].idxmin()
        new = new.loc[idx, ["destination_label","country_name","title","price_eur","discount_pct","best_starting_date","url"]]
        new = new.sort_values(["country_name","destination_label"]).reset_index(drop=True)
        new = linkify_url_col(new)

    gone = df_prev[df_prev["destination_label"].isin(gone_labels)].copy()
    if not gone.empty:
        idx2 = gone.groupby("destination_label")["price_eur"].idxmin()
        gone = gone.loc[idx2, ["destination_label","country_name","title","price_eur","best_starting_date","url"]]
        gone.rename(columns={"price_eur":"last_seen_price_eur","best_starting_date":"last_seen_date"}, inplace=True)
        gone = gone.sort_values(["country_name","destination_label"]).reset_index(drop=True)
        gone = linkify_url_col(gone)

    return new, gone

def price_buckets(df: pd.DataFrame):
    if df.empty: return pd.DataFrame()
    bins   = [0, 800, 1000, 1200, 1500, 2000, 3000, 99999]
    labels = ["<800", "800–999", "1000–1199", "1200–1499", "1500–1999", "2000–2999", "≥3000"]
    x = df.dropna(subset=["price_eur"]).copy()
    x["bucket"] = pd.cut(x["price_eur"], bins=bins, labels=labels, right=False)
    out = x["bucket"].value_counts().reindex(labels, fill_value=0).reset_index()
    out.columns = ["tranche_prix", "nb_offres"]
    return out

# ---------------------- Main (multi-pages) ----------------------
def main():
    ensure_dirs()

    if not DB.exists():
        OUT_INDEX.write_text("# RoadPrice\n\n_Base SQLite absente : `data/weroad.db`_", encoding="utf-8")
        return

    conn = sqlite3.connect(DB)
    try:
        # Période
        runs = safe_sql(conn, "SELECT DISTINCT run_date FROM weekly_kpis ORDER BY run_date")
        if runs.empty:
            OUT_INDEX.write_text("# RoadPrice\n\n_Aucune donnée_", encoding="utf-8")
            return
        last = runs["run_date"].iloc[-1]
        prev = runs["run_date"].iloc[-2] if len(runs) > 1 else None
        start_run = runs["run_date"].iloc[0]
        end_run   = runs["run_date"].iloc[-1]

        # Snapshots
        df_curr = safe_sql(conn, "SELECT * FROM snapshots WHERE run_date = ?", (last,))
        df_prev = safe_sql(conn, "SELECT * FROM snapshots WHERE run_date = ?", (prev,)) if prev else pd.DataFrame()
        if not df_curr.empty and "sales_status" in df_curr.columns:
            df_curr["sales_status"] = df_curr["sales_status"].map(style_status_badge)
        df_curr = linkify_url_col(df_curr)

        # KPIs
        kpi_last = safe_sql(conn, "SELECT * FROM weekly_kpis WHERE run_date = ?", (last,))
        kpi_hist = safe_sql(conn, "SELECT run_date, price_eur_min, price_eur_med, price_eur_avg, count_total, count_promos, promo_share_pct FROM weekly_kpis ORDER BY run_date")

        # Weekly diff
        wd = safe_sql(conn, "SELECT * FROM weekly_diff WHERE run_date = ?", (last,))
        if not wd.empty:
            wd["url"] = choose_url_col(wd)
            wd = wd[ [c for c in ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url"] if c in wd.columns] ]

        # Mensuel
        mo_all = safe_sql(conn, "SELECT month, destination_label, prix_min, prix_avg, nb_depart FROM monthly_kpis ORDER BY month, destination_label")
        mo_recent = pd.DataFrame()
        if not mo_all.empty:
            months = sorted(mo_all["month"].dropna().unique())
            keep = months[-RECENT_MONTHS:] if len(months) > RECENT_MONTHS else months
            mo_recent = mo_all[mo_all["month"].isin(keep)].copy()

        # Analyses actionnables
        bd      = best_dates(df_curr)
        topm    = cheapest_by_month(df_curr, top_n=15)
        ctry    = country_summary(df_curr)
        watch   = promo_watchlist(df_curr)
        movers  = big_movers(wd, ALERT_PCT, ALERT_EUR) if not wd.empty else pd.DataFrame()
        new_df, gone_df = new_vs_gone(df_curr, df_prev)
        buckets = price_buckets(df_curr)

    finally:
        conn.close()

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    badges = f"![run](https://img.shields.io/badge/run-{last}-blue) ![build](https://img.shields.io/badge/build-{ts}-success)"
    coverage = f"_Historique : **{start_run}** → **{end_run}** ({len(runs)} runs)._"

    # --------- Page : Accueil ---------
    body_index = f"""
# RoadPrice — synthèse
{badges}

{coverage}

**Accès rapide :**  
- [Analyse hebdo](./weekly.html) — KPIs, gros mouvements, nouvelles/disparues  
- [Meilleures dates](./best-dates.html) — prix mini par destination + top par mois  
- [Watchlist](./watchlist.html) — ALMOST/CONFIRMED/GAURANTEED  
- [Mensuel](./monthly.html) — KPIs par mois  
- [Pays](./countries.html) — synthèse par pays

## KPIs clés (dernier run)
{html_table(kpi_last, max_rows=1)}

## Répartition des offres par tranches de prix
{html_table(buckets, max_rows=50)}
"""
    write_page(OUT_INDEX, "RoadPrice — Accueil", body_index)

    # --------- Page : Hebdo ---------
    movers_html = html_table(movers, max_rows=250)
    new_html    = html_table(new_df, max_rows=200)
    gone_html   = html_table(gone_df, max_rows=200)
    kpi_hist_html = html_table(kpi_hist, max_rows=1000)

    body_weekly = f"""
# Analyse hebdo

**Dernier run :** `{last}`  
Seuils d'alerte : Δ% ≥ **{ALERT_PCT*100:.0f}%**, Δ€ ≥ **{ALERT_EUR:.0f}€**

## Gros mouvements de prix
{movers_html}

## Nouvelles destinations (vs précédent)
{new_html}

## Destinations disparues (vs précédent)
{gone_html}

## KPIs — Historique des runs
{kpi_hist_html}
"""
    write_page(OUT_WEEKLY, "RoadPrice — Hebdo", body_weekly)

    # --------- Page : Meilleures dates ---------
    body_best = f"""
# Meilleures dates à réserver

## Prix mini par destination (meilleure date)
{html_table(bd, max_rows=800)}

## Top offres par mois (les moins chères)
{html_table(topm, max_rows=800)}
"""
    write_page(OUT_BEST, "RoadPrice — Best dates", body_best)

    # --------- Page : Watchlist ---------
    body_watch = f"""
# Watchlist (départs confirmés / presque confirmés)

{html_table(watch, max_rows=800)}
"""
    write_page(OUT_WATCH, "RoadPrice — Watchlist", body_watch)

    # --------- Page : Mensuel ---------
    body_monthly = f"""
# KPIs mensuels

## Vue complète (toutes années)
{html_table(mo_all, max_rows=2000)}

## Aperçu {RECENT_MONTHS} derniers mois
{html_table(mo_recent, max_rows=1000)}
"""
    write_page(OUT_MONTHLY, "RoadPrice — Mensuel", body_monthly)

    # --------- Page : Pays ---------
    body_countries = f"""
# Synthèse par pays
{html_table(ctry, max_rows=1000)}
"""
    write_page(OUT_COUNTRIES, "RoadPrice — Pays", body_countries)


if __name__ == "__main__":
    main()
