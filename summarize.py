# summarize.py — Génère plusieurs pages Markdown dans docs/
# - Page d'accueil + 7 sous-pages : same-date, movers, best-dates, top-by-month, watchlist, kpi-weekly, kpi-monthly, countries
# - Tri/recherche/pagination via Simple-DataTables (injecté sur chaque page)
# - Pourcentages normalisés (>1 => /100)
# - Liens WeRoad corrects (url + url_precise)
# - Section same-date basée sur best_tour_id (avec seuil SAME_DATE_MIN_EUR si fourni)
# - Affiche sur l'accueil le nombre de voyages disponibles (len(df_curr))
# - Aucun badge externe (suppression des shields)

from pathlib import Path
from datetime import datetime, timezone
import os
import sqlite3
import pandas as pd
import html

DOCS = Path("docs")
DB = Path("data/weroad.db")

# Réglages
RECENT_MONTHS = 24
ALERT_PCT = float(os.getenv("ALERT_PCT", "0.10"))     # 10%
ALERT_EUR = float(os.getenv("ALERT_EUR", "150"))      # 150 €
SAME_DATE_MIN_EUR = float(os.getenv("SAME_DATE_MIN_EUR", "0.0"))

# ---------------- Assets (Simple-DataTables + style anti-"rectangle") ----------------
ASSETS = """
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/simple-datatables@9.0.3/dist/style.min.css">
<script src="https://cdn.jsdelivr.net/npm/simple-datatables@9.0.3"></script>
<style>
.dataTable-wrapper, .dataTable-wrapper .dataTable-container { background: transparent !important; border: 0 !important; box-shadow: none !important; padding: 0 !important; }
.dataTable-top, .dataTable-bottom { background: transparent !important; border: none !important; box-shadow: none !important; padding: .25rem 0 !important; }
.dataTable-info, .dataTable-pagination, .dataTable-dropdown, .dataTable-search { margin: .35rem 0 !important; font-size: .95rem !important; }
.dataTable-pagination a { border-radius: .4rem !important; }
.table-wrapper { overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 0 0 1.25rem 0; }

/* tables .rp-table (reprend le style “ancien design”) */
.rp-table { width: 100%; border-collapse: collapse; margin: 0.25rem 0 1.25rem 0; font-variant-numeric: tabular-nums; font-size: 0.95rem; background: #fff; }
.rp-table thead th { background: #f6f8fa; border-bottom: 2px solid #d0d7de; text-align: left; padding: .6rem .7rem; position: sticky; top: 0; z-index: 1; }
.rp-table td { padding: .55rem .7rem; border-bottom: 1px solid #e5e7eb; vertical-align: top; white-space: nowrap; }
.rp-table tbody tr:hover { background: #fafbfc; }
.rp-table a { text-decoration: none; color: #0969da; font-weight: 500; }
.rp-table a:hover { text-decoration: underline; }

/* badges + variations */
.rp-badge { display:inline-block; padding:.25em .6em; font-size:.8rem; font-weight:600; border-radius:.4em; color:#fff; line-height:1.2; white-space:nowrap; }
.rp-badge.almost{background:#d97706;} .rp-badge.confirmed{background:#2da44e;} .rp-badge.guaranteed{background:#1f6feb;} .rp-badge.on-sale{background:#8250df;} .rp-badge.default{background:#6e7781;}
code.up{color:#d73a49;font-weight:600;} code.down{color:#2da44e;font-weight:600;} code.equal{color:#57606a;}
</style>
<script>
(function() {
  const ready = (fn) => {
    if (document.readyState !== "loading") requestAnimationFrame(fn);
    else document.addEventListener("DOMContentLoaded", () => requestAnimationFrame(fn));
  };
  const euroToNumber = (txt) => {
    if (!txt) return null;
    const s = String(txt).replace(/\\s/g,"").replace("€","").replace(/\\u00A0/g,"").replace(",",".");
    const v = parseFloat(s); return isNaN(v) ? null : v;
  };
  ready(() => {
    document.querySelectorAll("table.rp-table").forEach((tbl, i) => {
      try {
        const dt = new simpleDatatables.DataTable(tbl, {
          searchable: true, fixedHeight: false,
          perPage: 25, perPageSelect: [10,25,50,100],
          labels: { placeholder: "Rechercher…", perPage: "{select} lignes par page", noRows: "Aucune donnée", info: "Affiche {start}–{end} sur {rows} lignes" },
        });
        try {
          dt.columns().each((idx) => {
            const header = tbl.tHead?.rows?.[0]?.cells?.[idx]; if (!header) return;
            const htxt = (header.textContent || "").toLowerCase();
            const isMoney = /(€|price|prix|delta_abs)/.test(htxt);
            const isPct   = /(pct|%)/.test(htxt);
            if (isMoney || isPct) {
              dt.columns().sort(idx, (a,b) => {
                const ta = a.replace(/<[^>]*>/g,""), tb = b.replace(/<[^>]*>/g,"");
                const na = isPct ? parseFloat(ta.replace("%","").replace(",",".")) : euroToNumber(ta);
                const nb = isPct ? parseFloat(tb.replace("%","").replace(",",".")) : euroToNumber(tb);
                if (na==null && nb==null) return 0; if (na==null) return -1; if (nb==null) return 1; return na - nb;
              });
            }
          });
        } catch(e) { console.warn("Sorter setup error", i, e); }
      } catch(e) { console.warn("DataTable init failed", i, e); }
    });
  });
})();
</script>
"""

# ---------------- utilitaires rendu ----------------
def ensure_docs():
    DOCS.mkdir(parents=True, exist_ok=True)

def safe_sql(conn, q, params=()):
    try:
        return pd.read_sql_query(q, conn, params=params)
    except Exception:
        return pd.DataFrame()

def to_month(s):
    try:
        return pd.to_datetime(s).strftime("%Y-%m")
    except Exception:
        return None

def choose_url_col(df: pd.DataFrame) -> pd.Series:
    # priorité: url_precise (date) > url_curr > url (globale) > url_prev
    for c in ("url_precise", "url_curr", "url", "url_prev"):
        if c in df.columns:
            s = df[c].copy(); s.name = "url"; return s
    return pd.Series([None] * len(df), index=df.index, name="url")

def linkify_url_col(df: pd.DataFrame, prefer_precise=False):
    if prefer_precise and "url_precise" in df.columns:
        df = df.copy()
        df["url"] = df["url_precise"]
    elif "url" not in df.columns:
        df["url"] = choose_url_col(df)
    if "url" in df.columns:
        df["url"] = df["url"].map(lambda u: f"<a target='_blank' href='{u}'>🔗</a>" if pd.notna(u) and str(u).strip() else "")
    return df

def style_status_badge(v: str) -> str:
    if v is None: return ""
    v = str(v).upper().strip()
    m = {
        "ALMOST_CONFIRMED": "<span class='rp-badge almost'>ALMOST</span>",
        "CONFIRMED":        "<span class='rp-badge confirmed'>CONFIRMED</span>",
        "GUARANTEED":       "<span class='rp-badge guaranteed'>GUARANTEED</span>",
        "ON_SALE":          "<span class='rp-badge on-sale'>ON&nbsp;SALE</span>",
        "WAITING_LIST":     "<span class='rp-badge default'>WAITING</span>",
        "PLANNED":          "<span class='rp-badge on-sale'>PLANNED</span>",
        "SOLD_OUT":         "<span class='rp-badge default'>SOLD&nbsp;OUT</span>",
    }
    return m.get(v, f"<span class='rp-badge default'>{html.escape(v)}</span>")

def decorate_movement(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty or "movement" not in df.columns:
        return df
    m = df["movement"].fillna("=")
    cls = m.map(lambda x: "up" if x == "↑" else ("down" if x == "↓" else "equal"))
    out = df.copy()
    out["movement"] = [f"<code class='{c}'>{s}</code>" for c, s in zip(cls, m)]
    return out

def html_table(df: pd.DataFrame, max_rows=200) -> str:
    """Table HTML stylable via .rp-table. Normalise *_pct (>1 => /100)."""
    if df is None or df.empty:
        return "<p><em>Aucune donnée</em></p>"
    df = df.copy().head(max_rows)

    def has_html(s: pd.Series) -> bool:
        return s.dtype == "object" and s.astype(str).str.contains("<", regex=False).any()

    # Pourcentages
    pct_cols = [c for c in df.columns if c.endswith("_pct") or c in ("delta_pct", "promo_share_pct")]
    for c in pct_cols:
        if c in df.columns and not has_html(df[c]):
            def fmt_pct(v):
                if pd.isna(v): return ""
                try:
                    vv = float(v)
                    if vv > 1: vv = vv / 100.0
                    return f"{vv:.1%}"
                except Exception:
                    return ""
            df[c] = df[c].map(fmt_pct)

    # Montants €
    money_cols = [c for c in df.columns if any(k in c for k in ["price", "prix", "delta_abs"])]
    for c in money_cols:
        if c in df.columns and not has_html(df[c]):
            df[c] = df[c].map(lambda v: f"{v:,.2f} €".replace(",", " ").replace(".", ",") if pd.notna(v) else "")

    return "<div class='table-wrapper'>\n" + df.to_html(index=False, classes="rp-table", escape=False) + "\n</div>"

# ---------------- nav + wrappers ----------------
PAGES = [
    ("index.md",        "Accueil"),
    ("same-date.md",    "Changements (même date)"),
    ("movers.md",       "Gros mouvements"),
    ("best-dates.md",   "Meilleures dates"),
    ("top-by-month.md", "Top par mois"),
    ("watchlist.md",    "Watchlist"),
    ("kpi-weekly.md",   "KPIs hebdo"),
    ("kpi-monthly.md",  "KPIs mensuels"),
    ("countries.md",    "Pays"),
]

def nav_bar(active: str) -> str:
    items = []
    for fn, label in PAGES:
        if fn == active:
            items.append(f"<strong>{label}</strong>")
        else:
            items.append(f"<a href=\"./{fn}\">{label}</a>")
    return " | ".join(items)

def page_wrap(front_title: str, active_file: str, body_html: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = f"""---
title: RoadPrice — {front_title}
---

{ASSETS}
<div style="margin:0 0 1rem 0; font-size:.95rem;">{nav_bar(active_file)}</div>
<div style="margin:0 0 1rem 0; color:#57606a;">Build: {ts}</div>
"""
    return header + body_html + "\n"

# ---------------- analyses (structures) ----------------
def best_dates(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=["destination_label", "price_eur"]).copy()
    if base.empty: return pd.DataFrame()
    idx = base.groupby("destination_label")["price_eur"].idxmin()
    out = base.loc[idx, [
        "destination_label","country_name","title","price_eur","base_price_eur",
        "discount_value_eur","discount_pct","sales_status",
        "best_starting_date","best_ending_date","url_precise","url"
    ]].sort_values(["country_name","destination_label"]).reset_index(drop=True)
    out.rename(columns={
        "price_eur":"best_price_eur",
        "base_price_eur":"base_price_at_best",
        "best_starting_date":"date_debut",
        "best_ending_date":"date_fin"
    }, inplace=True)
    out["sales_status"] = out["sales_status"].map(style_status_badge)
    out = linkify_url_col(out, prefer_precise=True)
    return out

def cheapest_by_month(df: pd.DataFrame, top_n=15) -> pd.DataFrame:
    tmp = df.dropna(subset=["best_starting_date","price_eur"]).copy()
    if tmp.empty: return pd.DataFrame()
    tmp["month_depart"] = tmp["best_starting_date"].map(to_month)
    tmp = tmp.dropna(subset=["month_depart"])
    tmp["rk"] = tmp.groupby("month_depart")["price_eur"].rank(method="first")
    out = tmp[tmp["rk"] <= top_n].sort_values(["month_depart","price_eur"])[[
        "month_depart","destination_label","title","country_name",
        "price_eur","discount_pct","sales_status","best_starting_date","url_precise","url"
    ]]
    out.rename(columns={"price_eur":"price_eur_min_month"}, inplace=True)
    out["sales_status"] = out["sales_status"].map(style_status_badge)
    out = linkify_url_col(out, prefer_precise=True)
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
    x = x.sort_values(by=["sales_status","best_starting_date","seatsToConfirm","price_eur"],
                      ascending=[True, True, True, True], na_position="last")
    cols = ["sales_status","best_starting_date","best_ending_date","title","destination_label","country_name",
            "price_eur","discount_pct","seatsToConfirm","maxPax","weroadersCount","url_precise","url"]
    x = x[cols].reset_index(drop=True)
    x["sales_status"] = x["sales_status"].map(style_status_badge)
    x = linkify_url_col(x, prefer_precise=True)
    return x

def big_movers(wd: pd.DataFrame) -> pd.DataFrame:
    if wd.empty: return pd.DataFrame()
    x = wd.copy()
    for c in ("delta_pct","delta_abs","price_eur_prev","price_eur_curr"):
        if c in x.columns:
            x[c] = pd.to_numeric(x[c], errors="coerce")
    x["flag"] = (x["delta_pct"].abs() > ALERT_PCT) | (x["delta_abs"].abs() > ALERT_EUR)
    cols = ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url","url_precise"]
    cols = [c for c in cols if c in x.columns]
    out = x[x["flag"]].sort_values(["delta_pct","delta_abs"], ascending=[False, False])[cols].reset_index(drop=True)
    out = decorate_movement(out)
    out = linkify_url_col(out, prefer_precise=False)
    return out

# ---------------- main ----------------
def main():
    ensure_docs()
    if not DB.exists():
        (DOCS / "index.md").write_text("# RoadPrice\n\n_Base SQLite absente : `data/weroad.db`_", encoding="utf-8")
        return

    conn = sqlite3.connect(DB)
    try:
        runs = safe_sql(conn, "SELECT DISTINCT run_date FROM weekly_kpis ORDER BY run_date")
        if runs.empty:
            (DOCS / "index.md").write_text("# RoadPrice\n\n_Aucune donnée disponible_", encoding="utf-8")
            return

        last = runs["run_date"].iloc[-1]
        prev = runs["run_date"].iloc[-2] if len(runs) > 1 else None

        # Snapshots courant / précédent
        df_curr = safe_sql(conn, "SELECT * FROM snapshots WHERE run_date = ?", (last,))
        df_prev = safe_sql(conn, "SELECT * FROM snapshots WHERE run_date = ?", (prev,)) if prev else pd.DataFrame()

        # Nombre total d'offres du run courant
        nb_offres = len(df_curr)

        # KPIs
        kpi_last = safe_sql(conn, "SELECT * FROM weekly_kpis WHERE run_date = ?", (last,))
        kpi_hist = safe_sql(conn,
            "SELECT run_date, price_eur_min, price_eur_med, price_eur_avg, count_total, count_promos, promo_share_pct "
            "FROM weekly_kpis ORDER BY run_date"
        )

        # Weekly diff (movers base)
        wd = safe_sql(conn, "SELECT * FROM weekly_diff WHERE run_date = ?", (last,))
        if not wd.empty:
            wd["url"] = choose_url_col(wd)
            wd = wd[[c for c in ["destination_label","title_curr","price_eur_prev","price_eur_curr","delta_abs","delta_pct","movement","url","url_precise"] if c in wd.columns]]

        # Same-date changes (dernier run) — déjà filtrés au run par SAME_DATE_MIN_EUR
        same_date = safe_sql(conn,
            "SELECT best_tour_id, slug, title, destination_label, country_name, best_starting_date, "
            "price_eur_prev, price_eur_curr, delta_abs, delta_pct, movement, sales_status, url_precise, url "
            "FROM same_date_diff WHERE run_date = ? "
            "ORDER BY ABS(delta_abs) DESC, ABS(delta_pct) DESC, best_starting_date",
            (last,)
        )
        if not same_date.empty:
            same_date = linkify_url_col(same_date, prefer_precise=True)

        # Mensuel
        mo_all = safe_sql(conn, "SELECT month, destination_label, prix_min, prix_avg, nb_depart FROM monthly_kpis ORDER BY month, destination_label")
        mo_recent = pd.DataFrame()
        if not mo_all.empty:
            months = sorted(mo_all["month"].dropna().unique())
            keep = months[-RECENT_MONTHS:] if len(months) > RECENT_MONTHS else months
            mo_recent = mo_all[mo_all["month"].isin(keep)].copy()

        # Dérivés
        bd      = best_dates(df_curr)
        topm    = cheapest_by_month(df_curr, top_n=15)
        ctry    = country_summary(df_curr)
        watch   = promo_watchlist(df_curr)
        movers  = big_movers(wd) if not wd.empty else pd.DataFrame()

        # Couverture
        start_run = runs["run_date"].iloc[0]
        end_run   = last
        coverage  = f"_Historique : **{start_run}** → **{end_run}** ({len(runs)} runs)._"

    finally:
        conn.close()

    # --- Écriture des pages ---
    # Accueil
    home = f"""
# RoadPrice — Accueil

**Dernier run : `{end_run}` — {nb_offres} voyages disponibles**  
{coverage}

- **Changements (même date)** : variations de prix pour un *même départ* (clé `best_tour_id`) entre les deux derniers runs.
- **Gros mouvements** : variations fortes sur le panier “meilleur prix par destination”.
- **Meilleures dates** : prix minimum par destination au run courant.
- **Top par mois** : meilleures offres mensuelles.
- **Watchlist** : départs ALMOST/CONFIRMED/GUARANTEED.
- **KPIs** : historiques hebdo et mensuels.
- **Pays** : synthèse par pays.

---

## KPIs clés (dernier run)
{html_table(kpi_last, max_rows=1)}

---

## Lien rapides
- [Changements (même date)](./same-date.md)
- [Gros mouvements](./movers.md)
- [Meilleures dates](./best-dates.md)
- [Top par mois](./top-by-month.md)
- [Watchlist](./watchlist.md)
- [KPIs hebdo](./kpi-weekly.md)
- [KPIs mensuels](./kpi-monthly.md)
- [Pays](./countries.md)
"""
    (DOCS / "index.md").write_text(page_wrap("Accueil", "index.md", home), encoding="utf-8")

    # Same-date
    same_body = f"""
# Changements de prix (même date)
Seuil d’affichage : |Δ€| ≥ **{SAME_DATE_MIN_EUR:.0f}**

{html_table(same_date, max_rows=1500)}
"""
    (DOCS / "same-date.md").write_text(page_wrap("Changements (même date)", "same-date.md", same_body), encoding="utf-8")

    # Movers
    movers_body = f"""
# Gros mouvements de prix
Critères : Δ% ≥ **{ALERT_PCT*100:.0f}%** ou Δ€ ≥ **{ALERT_EUR:.0f}€**

{html_table(movers, max_rows=800)}
"""
    (DOCS / "movers.md").write_text(page_wrap("Gros mouvements", "movers.md", movers_body), encoding="utf-8")

    # Best dates
    bd_body = f"""
# Meilleures dates à réserver
Prix minimum par destination (run courant).

{html_table(bd, max_rows=2000)}
"""
    (DOCS / "best-dates.md").write_text(page_wrap("Meilleures dates", "best-dates.md", bd_body), encoding="utf-8")

    # Top by month
    topm_body = f"""
# Top offres par mois
Les offres les moins chères par mois.

{html_table(topm, max_rows=2000)}
"""
    (DOCS / "top-by-month.md").write_text(page_wrap("Top par mois", "top-by-month.md", topm_body), encoding="utf-8")

    # Watchlist
    watch_body = f"""
# Watchlist — départs proches / confirmés
ALMOST / CONFIRMED / GUARANTEED.

{html_table(watch, max_rows=2000)}
"""
    (DOCS / "watchlist.md").write_text(page_wrap("Watchlist", "watchlist.md", watch_body), encoding="utf-8")

    # KPI weekly
    kpiw_body = f"""
# KPIs hebdo — Historique des runs
{html_table(kpi_hist, max_rows=5000)}
"""
    (DOCS / "kpi-weekly.md").write_text(page_wrap("KPIs hebdo", "kpi-weekly.md", kpiw_body), encoding="utf-8")

    # KPI monthly
    kpim_body = f"""
# KPIs mensuels — Vue complète
{html_table(mo_all, max_rows=5000)}

## Aperçu {RECENT_MONTHS} derniers mois
{html_table(mo_recent, max_rows=2000)}
"""
    (DOCS / "kpi-monthly.md").write_text(page_wrap("KPIs mensuels", "kpi-monthly.md", kpim_body), encoding="utf-8")

    # Countries
    countries_body = f"""
# Pays — synthèse
{html_table(ctry, max_rows=3000)}
"""
    (DOCS / "countries.md").write_text(page_wrap("Pays", "countries.md", countries_body), encoding="utf-8")

    print("Wrote multi-pages in docs/")
    

if __name__ == "__main__":
    main()
