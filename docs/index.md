---
title: RoadPrice — Accueil
---


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
    const s = String(txt).replace(/\s/g,"").replace("€","").replace(/\u00A0/g,"").replace(",",".");
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

<div style="margin:0 0 1rem 0; font-size:.95rem;"><strong>Accueil</strong> | <a href="./same-date.md">Changements (même date)</a> | <a href="./movers.md">Gros mouvements</a> | <a href="./best-dates.md">Meilleures dates</a> | <a href="./top-by-month.md">Top par mois</a> | <a href="./watchlist.md">Watchlist</a> | <a href="./kpi-weekly.md">KPIs hebdo</a> | <a href="./kpi-monthly.md">KPIs mensuels</a> | <a href="./countries.md">Pays</a></div>
<div style="margin:0 0 1rem 0; color:#57606a;">Build: 2025-08-27 08:49 UTC</div>

# RoadPrice — Accueil

**Dernier run : `2025-08-27` — 141 voyages disponibles**  
_Historique : **2025-08-27** → **2025-08-27** (1 runs)._

- **Changements (même date)** : variations de prix pour un *même départ* (clé `best_tour_id`) entre les deux derniers runs.
- **Gros mouvements** : variations fortes sur le panier “meilleur prix par destination”.
- **Meilleures dates** : prix minimum par destination au run courant.
- **Top par mois** : meilleures offres mensuelles.
- **Watchlist** : départs ALMOST/CONFIRMED/GUARANTEED.
- **KPIs** : historiques hebdo et mensuels.
- **Pays** : synthèse par pays.

---

## KPIs clés (dernier run)
<div class='table-wrapper'>
<table border="1" class="dataframe rp-table">
  <thead>
    <tr style="text-align: right;">
      <th>run_date</th>
      <th>price_eur_min</th>
      <th>price_eur_max</th>
      <th>price_eur_avg</th>
      <th>price_eur_med</th>
      <th>base_price_eur_min</th>
      <th>base_price_eur_max</th>
      <th>base_price_eur_avg</th>
      <th>base_price_eur_med</th>
      <th>discount_value_eur_min</th>
      <th>discount_value_eur_max</th>
      <th>discount_value_eur_avg</th>
      <th>discount_value_eur_med</th>
      <th>discount_pct_min</th>
      <th>discount_pct_max</th>
      <th>discount_pct_avg</th>
      <th>discount_pct_med</th>
      <th>count_total</th>
      <th>count_promos</th>
      <th>promo_share_pct</th>
      <th>depart_by_month</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2025-08-27</td>
      <td>469,00 €</td>
      <td>3 499,00 €</td>
      <td>1 286,79 €</td>
      <td>1 149,00 €</td>
      <td>499,00 €</td>
      <td>3 299,00 €</td>
      <td>1 281,83 €</td>
      <td>1 099,00 €</td>
      <td>30.0</td>
      <td>590.0</td>
      <td>158.245283</td>
      <td>130.0</td>
      <td>5.0</td>
      <td>20.0</td>
      <td>12.371698</td>
      <td>11.8</td>
      <td>141</td>
      <td>53</td>
      <td>37.6%</td>
      <td>{"2025-08": 2, "2025-09": 44, "2025-10": 26, "2025-11": 22, "2025-12": 13, "2026-01": 5, "2026-02": 5, "2026-03": 9, "2026-04": 2, "2026-05": 5, "2026-06": 1, "2026-07": 1, "2026-09": 2, "2026-10": 3, "2026-12": 1}</td>
    </tr>
  </tbody>
</table>
</div>

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

