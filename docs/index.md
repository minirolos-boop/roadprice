---
title: RoadPrice — Évolutions tarifaires
---


<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/simple-datatables@9.0.3/dist/style.min.css">
<script src="https://cdn.jsdelivr.net/npm/simple-datatables@9.0.3"></script>
<style>
/* neutraliser l'encapsulation par défaut du plugin */
.dataTable-wrapper, .dataTable-wrapper .dataTable-container { background: transparent !important; border: 0 !important; box-shadow: none !important; padding: 0 !important; }
.dataTable-top, .dataTable-bottom { background: transparent !important; border: none !important; box-shadow: none !important; padding: .25rem 0 !important; }
.dataTable-info, .dataTable-pagination, .dataTable-dropdown, .dataTable-search { margin: .35rem 0 !important; font-size: .95rem !important; }
.dataTable-pagination a { border-radius: .4rem !important; }

/* wrapper scroll horizontal */
.table-wrapper { overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 0 0 1.25rem 0; }

/* table style "ancien design" */
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


# RoadPrice — Évolutions tarifaires

**Dernier run : `2025-08-29` — 142 voyages disponibles**  
_Historique : **2025-08-29** → **2025-08-29** (1 runs)._  
_Build : 2025-08-29 16:46 UTC_

> Astuce : utilise la recherche au-dessus de chaque tableau et clique sur les en-têtes pour trier.

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
      <td>2025-08-29</td>
      <td>449,00 €</td>
      <td>3 499,00 €</td>
      <td>1 285,96 €</td>
      <td>1 149,00 €</td>
      <td>499,00 €</td>
      <td>3 299,00 €</td>
      <td>1 317,91 €</td>
      <td>1 099,00 €</td>
      <td>40.0</td>
      <td>590.0</td>
      <td>158.195652</td>
      <td>125.0</td>
      <td>5.0</td>
      <td>20.0</td>
      <td>12.102174</td>
      <td>12.1</td>
      <td>142</td>
      <td>46</td>
      <td>32.4%</td>
      <td>{"2025-08": 1, "2025-09": 38, "2025-10": 28, "2025-11": 24, "2025-12": 13, "2026-01": 4, "2026-02": 7, "2026-03": 9, "2026-04": 6, "2026-05": 3, "2026-06": 3, "2026-07": 2, "2026-08": 2, "2026-11": 1, "2026-12": 1}</td>
    </tr>
  </tbody>
</table>
</div>

---

## Changements de prix (même date)
Départs identiques (même `best_tour_id`) dont le prix a changé entre les deux derniers runs.  
Seuil d’affichage paramétré côté collecte : |Δ€| ≥ **0**.

<p><em>Aucune donnée</em></p>

---

## Gros mouvements de prix
Critères : Δ% ≥ **10%** ou Δ€ ≥ **150€**

<p><em>Aucune donnée</em></p>

---

## Meilleures dates à réserver (prix mini par destination)
<div class='table-wrapper'>
<table border="1" class="dataframe rp-table">
  <thead>
    <tr style="text-align: right;">
      <th>destination_label</th>
      <th>country_name</th>
      <th>title</th>
      <th>best_price_eur</th>
      <th>base_price_at_best</th>
      <th>discount_value_eur</th>
      <th>discount_pct</th>
      <th>sales_status</th>
      <th>date_debut</th>
      <th>date_fin</th>
      <th>url_precise</th>
      <th>url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Afrique du Sud</td>
      <td>Afrique du Sud</td>
      <td>Afrique du Sud 360° : du Cap au safari dans le parc national Kruger</td>
      <td>1 899,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge default'>WAITING</span></td>
      <td>2025-09-08</td>
      <td>2025-09-20</td>
      <td>https://www.weroad.fr/destinations/afrique-du-sud-cap-safari-parc-kruger/3485c3c9-e940-42ea-84ec-8f0379d93a8b</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/afrique-du-sud-cap-safari-parc-kruger/3485c3c9-e940-42ea-84ec-8f0379d93a8b'>🔗</a></td>
    </tr>
    <tr>
      <td>Albanie</td>
      <td>Albanie</td>
      <td>Albanie Express Winter : histoire, nature et aventure</td>
      <td>549,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-04-05</td>
      <td>2026-04-10</td>
      <td>https://www.weroad.fr/destinations/albanie-express-hiver/b480d1d1-d49c-4b3c-939d-b41c7c3aa1a9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/albanie-express-hiver/b480d1d1-d49c-4b3c-939d-b41c7c3aa1a9'>🔗</a></td>
    </tr>
    <tr>
      <td>Allemagne</td>
      <td>Allemagne</td>
      <td>Berlin Express</td>
      <td>599,00 €</td>
      <td>699,00 €</td>
      <td>100.0</td>
      <td>14.3%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-18</td>
      <td>2025-12-22</td>
      <td>https://www.weroad.fr/destinations/allemagne-berlin-express-tour-weroadx/e5d6c677-81fc-44be-abbf-d9589f0ebf6d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/allemagne-berlin-express-tour-weroadx/e5d6c677-81fc-44be-abbf-d9589f0ebf6d'>🔗</a></td>
    </tr>
    <tr>
      <td>Argentine</td>
      <td>Argentine</td>
      <td>Argentine et Brésil : une aventure sud-américaine authentique</td>
      <td>1 899,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-01-24</td>
      <td>2026-02-01</td>
      <td>https://www.weroad.fr/destinations/argentine-bresil-360/c40313b7-250c-4aaa-a9ec-cf5155b39a03</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/argentine-bresil-360/c40313b7-250c-4aaa-a9ec-cf5155b39a03'>🔗</a></td>
    </tr>
    <tr>
      <td>Patagonie</td>
      <td>Argentine</td>
      <td>Patagonie Trekking : aventure à travers l’Argentine et le Chili</td>
      <td>2 999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-24</td>
      <td>2025-12-06</td>
      <td>https://www.weroad.fr/destinations/patagonie-360/4d4d6956-9089-4a57-8988-9869cccc3a40</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/patagonie-360/4d4d6956-9089-4a57-8988-9869cccc3a40'>🔗</a></td>
    </tr>
    <tr>
      <td>Australie</td>
      <td>Australie</td>
      <td>Australie : Road Trip de Sydney à Brisbane</td>
      <td>2 019,00 €</td>
      <td>2 299,00 €</td>
      <td>280.0</td>
      <td>12.2%</td>
      <td><span class='rp-badge default'>SOLD&nbsp;OUT</span></td>
      <td>2025-09-21</td>
      <td>2025-10-04</td>
      <td>https://www.weroad.fr/destinations/australie-de-sydney-a-brisbane/71ad43cc-f00f-4060-b3ab-db20c2cf8759</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/australie-de-sydney-a-brisbane/71ad43cc-f00f-4060-b3ab-db20c2cf8759'>🔗</a></td>
    </tr>
    <tr>
      <td>Autriche</td>
      <td>Autriche</td>
      <td>Autriche Ski & Snowboard Express : neige et sport à Kitzbühel</td>
      <td>799,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-26</td>
      <td>2025-11-30</td>
      <td>https://www.weroad.fr/destinations/autriche-kitzbuhel-ski-snowboard/0b5412fb-f73d-421d-9976-c29ec0aa81a0</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/autriche-kitzbuhel-ski-snowboard/0b5412fb-f73d-421d-9976-c29ec0aa81a0'>🔗</a></td>
    </tr>
    <tr>
      <td>Belgique</td>
      <td>Belgique</td>
      <td>Bruxelles et Amsterdam : Entre culture, saveurs et découverte</td>
      <td>789,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-11</td>
      <td>2025-11-16</td>
      <td>https://www.weroad.fr/destinations/bruxelles-amsterdam-express-culture/0e2cf4a6-3b15-41d9-aeb9-843c1e541f70</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bruxelles-amsterdam-express-culture/0e2cf4a6-3b15-41d9-aeb9-843c1e541f70'>🔗</a></td>
    </tr>
    <tr>
      <td>Belize</td>
      <td>Belize</td>
      <td>Belize 360° : jungles luxuriantes, plages paradisiaques et Blue Hole</td>
      <td>1 499,00 €</td>
      <td>1 599,00 €</td>
      <td>100.0</td>
      <td>6.3%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-17</td>
      <td>2025-10-25</td>
      <td>https://www.weroad.fr/destinations/belize-jungles-plages-blue-hole/b1d4305d-a377-46ed-b533-dad5169b092e</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/belize-jungles-plages-blue-hole/b1d4305d-a377-46ed-b533-dad5169b092e'>🔗</a></td>
    </tr>
    <tr>
      <td>Chili & Bolivie</td>
      <td>Bolivie</td>
      <td>Bolivie & Chili : de Santiago à La Paz</td>
      <td>2 499,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-01</td>
      <td>2025-11-12</td>
      <td>https://www.weroad.fr/destinations/bolivie-et-chili-360/1ff089b7-7105-4750-a027-f101e4ff4ad1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bolivie-et-chili-360/1ff089b7-7105-4750-a027-f101e4ff4ad1'>🔗</a></td>
    </tr>
    <tr>
      <td>Brésil</td>
      <td>Brésil</td>
      <td>Brésil Beach Life : jungle, mer et amour</td>
      <td>1 599,00 €</td>
      <td>1 699,00 €</td>
      <td>100.0</td>
      <td>5.9%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-10-17</td>
      <td>2025-10-26</td>
      <td>https://www.weroad.fr/destinations/bresil-mer-plage-foret-rio-de-janeiro/8c9a0abb-bb94-41b6-9cd0-ca0ae9490e12</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bresil-mer-plage-foret-rio-de-janeiro/8c9a0abb-bb94-41b6-9cd0-ca0ae9490e12'>🔗</a></td>
    </tr>
    <tr>
      <td>Bulgarie</td>
      <td>Bulgarie</td>
      <td>Bulgarie Ski Express : Bansko entre pistes, spa et fête !</td>
      <td>699,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-12-23</td>
      <td>2026-12-28</td>
      <td>https://www.weroad.fr/destinations/bulgarie-ski-express-bansko/8832ad88-d827-4684-8b3d-eb733e544d51</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bulgarie-ski-express-bansko/8832ad88-d827-4684-8b3d-eb733e544d51'>🔗</a></td>
    </tr>
    <tr>
      <td>Cambodge</td>
      <td>Cambodge</td>
      <td>Laos et Cambodge : Sur les routes des temples d’Indochine</td>
      <td>1 900,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-03-20</td>
      <td>2026-03-31</td>
      <td>https://www.weroad.fr/destinations/laos-cambodge-routes-temples-indochine/3a3d0763-6567-4060-b7cc-eb9ab1b3c06d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/laos-cambodge-routes-temples-indochine/3a3d0763-6567-4060-b7cc-eb9ab1b3c06d'>🔗</a></td>
    </tr>
    <tr>
      <td>Canada</td>
      <td>Canada</td>
      <td>Canada de l’Est : Montréal, Toronto et les chutes du Niagara</td>
      <td>1 389,00 €</td>
      <td>1 699,00 €</td>
      <td>310.0</td>
      <td>18.2%</td>
      <td><span class='rp-badge default'>ALMOST_FULL</span></td>
      <td>2025-09-19</td>
      <td>2025-09-26</td>
      <td>https://www.weroad.fr/destinations/canada-quebec-montreal-toronto-niagara/5d4bdd04-4236-45bf-9c2f-2b87f5f173aa</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/canada-quebec-montreal-toronto-niagara/5d4bdd04-4236-45bf-9c2f-2b87f5f173aa'>🔗</a></td>
    </tr>
    <tr>
      <td>Cap-Vert</td>
      <td>Cap-Vert</td>
      <td>Cap Vert : Santiago, Fogo et Boa Vista</td>
      <td>1 599,00 €</td>
      <td>1 699,00 €</td>
      <td>100.0</td>
      <td>5.9%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-01</td>
      <td>2025-11-10</td>
      <td>https://www.weroad.fr/destinations/cap-vert-beach-life-santiago-fogo-boa-vista/9cc7c7bb-6537-403c-a60c-87b268b6005d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/cap-vert-beach-life-santiago-fogo-boa-vista/9cc7c7bb-6537-403c-a60c-87b268b6005d'>🔗</a></td>
    </tr>
    <tr>
      <td>Chili et Bolivie</td>
      <td>Chili</td>
      <td>Chili et Bolivie : Aventure dans le Salar d'Uyuni</td>
      <td>1 999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-10-24</td>
      <td>2025-11-04</td>
      <td>https://www.weroad.fr/destinations/chili-bolivie-aventure-salar-uyuni/55233722-d5d2-4477-89d5-a2115d31530c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/chili-bolivie-aventure-salar-uyuni/55233722-d5d2-4477-89d5-a2115d31530c'>🔗</a></td>
    </tr>
    <tr>
      <td>Chine</td>
      <td>Chine</td>
      <td>Chine 360° : Pékin, Shanghai et la Grande Muraille</td>
      <td>1 899,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-04-18</td>
      <td>2026-04-29</td>
      <td>https://www.weroad.fr/destinations/chine/b05e8889-941d-4e19-b2b2-7658732fe70a</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/chine/b05e8889-941d-4e19-b2b2-7658732fe70a'>🔗</a></td>
    </tr>
    <tr>
      <td>Colombie</td>
      <td>Colombie</td>
      <td>Colombie 360° : Bogota, Medellin, Carthagène et parc Tayrona</td>
      <td>2 199,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-01</td>
      <td>2025-11-12</td>
      <td>https://www.weroad.fr/destinations/colombie-360/c0331d34-29c3-4b21-9ccf-7bdedc3449b5</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/colombie-360/c0331d34-29c3-4b21-9ccf-7bdedc3449b5'>🔗</a></td>
    </tr>
    <tr>
      <td>Corée du Sud</td>
      <td>Corée du Sud</td>
      <td>Corée du Sud 360° : entre tradition et modernité</td>
      <td>1 499,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge default'>ALMOST_FULL</span></td>
      <td>2025-10-18</td>
      <td>2025-10-27</td>
      <td>https://www.weroad.fr/destinations/coree-du-sud-360/d1db200e-8ac8-40ad-88d3-04c78aff3fc2</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/coree-du-sud-360/d1db200e-8ac8-40ad-88d3-04c78aff3fc2'>🔗</a></td>
    </tr>
    <tr>
      <td>Costa Rica</td>
      <td>Costa Rica</td>
      <td>Costa Rica 360° : pura vida parmi les forêts tropicales</td>
      <td>1 799,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-11-22</td>
      <td>2026-12-04</td>
      <td>https://www.weroad.fr/destinations/costa-rica-360/885085c8-d0ef-4cbe-a1c0-ad233f9423e5</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/costa-rica-360/885085c8-d0ef-4cbe-a1c0-ad233f9423e5'>🔗</a></td>
    </tr>
    <tr>
      <td>Cuba</td>
      <td>Cuba</td>
      <td>Cuba 360°: au rythme de la salsa de la Havane à Trinidad</td>
      <td>969,00 €</td>
      <td>1 099,00 €</td>
      <td>130.0</td>
      <td>11.8%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-20</td>
      <td>2025-10-01</td>
      <td>https://www.weroad.fr/destinations/cuba-360/f632605e-d0f9-473b-a118-34113dce67c0</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/cuba-360/f632605e-d0f9-473b-a118-34113dce67c0'>🔗</a></td>
    </tr>
    <tr>
      <td>Barcelone & Costa Brava</td>
      <td>Espagne</td>
      <td>Barcelone & Costa Brava Beach Life</td>
      <td>1 299,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-10-29</td>
      <td>2025-11-04</td>
      <td>https://www.weroad.fr/destinations/barcelone-costa-brava-360/821e1e1e-bdcb-442a-bf67-d1423fd2b452</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/barcelone-costa-brava-360/821e1e1e-bdcb-442a-bf67-d1423fd2b452'>🔗</a></td>
    </tr>
    <tr>
      <td>Espagne</td>
      <td>Espagne</td>
      <td>Fuerteventura Surf : aventure à la découverte de l'île</td>
      <td>999,00 €</td>
      <td>1 099,00 €</td>
      <td>100.0</td>
      <td>9.1%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-07-25</td>
      <td>2026-08-01</td>
      <td>https://www.weroad.fr/destinations/fuerteventura-surf-weroadx/317f930c-e5c9-4fe2-8ff8-f8731e8196ab</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/fuerteventura-surf-weroadx/317f930c-e5c9-4fe2-8ff8-f8731e8196ab'>🔗</a></td>
    </tr>
    <tr>
      <td>Gran Canaria</td>
      <td>Espagne</td>
      <td>Gran Canaria Beach Life Express : l’île du soleil</td>
      <td>599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-01</td>
      <td>2025-10-05</td>
      <td>https://www.weroad.fr/destinations/gran-canaria-express-ile-soleil/9f57e3fc-c9ae-44d0-9483-f13ecadbfb94</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/gran-canaria-express-ile-soleil/9f57e3fc-c9ae-44d0-9483-f13ecadbfb94'>🔗</a></td>
    </tr>
    <tr>
      <td>Îles Canaries</td>
      <td>Espagne</td>
      <td>Fuerteventura et Lanzarote  360° : entre plages et volcans</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-28</td>
      <td>2026-01-04</td>
      <td>https://www.weroad.fr/destinations/fuerteventura-lanzarote-plages-volcans/433a927c-fec3-4f68-be9c-45e2b5cfcfcb</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/fuerteventura-lanzarote-plages-volcans/433a927c-fec3-4f68-be9c-45e2b5cfcfcb'>🔗</a></td>
    </tr>
    <tr>
      <td>Pays Baltes</td>
      <td>Estonie</td>
      <td>Pays Baltes : Tallinn, Riga et Vilnius</td>
      <td>899,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-25</td>
      <td>2025-11-01</td>
      <td>https://www.weroad.fr/destinations/pays-baltes-tallinn-riga-vilnius/4233778c-476f-4887-8f15-6c0bcda166ca</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/pays-baltes-tallinn-riga-vilnius/4233778c-476f-4887-8f15-6c0bcda166ca'>🔗</a></td>
    </tr>
    <tr>
      <td>Finlande</td>
      <td>Finlande</td>
      <td>Laponie finlandaise : à la recherche des aurores boréales</td>
      <td>1 549,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-01-23</td>
      <td>2026-01-28</td>
      <td>https://www.weroad.fr/destinations/laponie-finlandaise/3197a02f-7b14-4dea-8e82-acdb48bae7da</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/laponie-finlandaise/3197a02f-7b14-4dea-8e82-acdb48bae7da'>🔗</a></td>
    </tr>
    <tr>
      <td>Auvergne</td>
      <td>France</td>
      <td>Auvergne Express : à la découverte du Sancy</td>
      <td>549,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-07-28</td>
      <td>2026-08-01</td>
      <td>https://www.weroad.fr/destinations/auvergne-express/d7f1381f-4b84-4268-a52f-699c450ca721</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/auvergne-express/d7f1381f-4b84-4268-a52f-699c450ca721'>🔗</a></td>
    </tr>
    <tr>
      <td>Bordeaux</td>
      <td>France</td>
      <td>Bordeaux Express : de la Dune du Pilat à la pointe du Cap-Ferret</td>
      <td>899,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-06-27</td>
      <td>2026-07-01</td>
      <td>https://www.weroad.fr/destinations/bordeaux-dune-du-pilat/b202dfa7-62bd-4a24-a4d1-cf7eafb1d031</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bordeaux-dune-du-pilat/b202dfa7-62bd-4a24-a4d1-cf7eafb1d031'>🔗</a></td>
    </tr>
    <tr>
      <td>Bourgogne</td>
      <td>France</td>
      <td>Bourgogne Express : sur la route des Grands Crus</td>
      <td>599,00 €</td>
      <td>649,00 €</td>
      <td>50.0</td>
      <td>7.7%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-03</td>
      <td>2025-12-07</td>
      <td>https://www.weroad.fr/destinations/bourgogne-express-route-grand-crus/a7cdffcd-8b37-4239-b0c0-4fca95ebb9b4</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bourgogne-express-route-grand-crus/a7cdffcd-8b37-4239-b0c0-4fca95ebb9b4'>🔗</a></td>
    </tr>
    <tr>
      <td>Bretagne</td>
      <td>France</td>
      <td>Bretagne Sud Beach Life : Quiberon et Belle-île-en-Mer</td>
      <td>679,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-08-08</td>
      <td>2026-08-12</td>
      <td>https://www.weroad.fr/destinations/bretagne-quiberon-belle-ile/02a71e36-0af9-4567-9cf2-238b0da67e7f</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bretagne-quiberon-belle-ile/02a71e36-0af9-4567-9cf2-238b0da67e7f'>🔗</a></td>
    </tr>
    <tr>
      <td>France</td>
      <td>France</td>
      <td>Méditerranée Beach Life Express : Montpellier, Sète et Camargue</td>
      <td>599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-30</td>
      <td>2025-11-03</td>
      <td>https://www.weroad.fr/destinations/mediterranee-express-montpellier-sete-camargue/dc5c957d-9752-4248-bdcd-e0df79513b15</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/mediterranee-express-montpellier-sete-camargue/dc5c957d-9752-4248-bdcd-e0df79513b15'>🔗</a></td>
    </tr>
    <tr>
      <td>Normandie</td>
      <td>France</td>
      <td>Normandie 360° : Châteaux, Falaises et Mont Saint-Michel</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-06-19</td>
      <td>2026-06-25</td>
      <td>https://www.weroad.fr/destinations/normandie-360-mont-saint-michel/0bd9b86b-5e44-4a90-8fb3-0156567fe1d9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/normandie-360-mont-saint-michel/0bd9b86b-5e44-4a90-8fb3-0156567fe1d9'>🔗</a></td>
    </tr>
    <tr>
      <td>Corfou</td>
      <td>Grèce</td>
      <td>Corfou Beach Life : plage et découverte des îles</td>
      <td>739,00 €</td>
      <td>899,00 €</td>
      <td>160.0</td>
      <td>17.8%</td>
      <td><span class='rp-badge default'>ALMOST_FULL</span></td>
      <td>2025-09-14</td>
      <td>2025-09-21</td>
      <td>https://www.weroad.fr/destinations/corfou-360/9d44fecc-3467-4a0f-b668-c1cd49f0e9c3</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/corfou-360/9d44fecc-3467-4a0f-b668-c1cd49f0e9c3'>🔗</a></td>
    </tr>
    <tr>
      <td>Crète</td>
      <td>Grèce</td>
      <td>Crète Beach Life</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-25</td>
      <td>2025-11-01</td>
      <td>https://www.weroad.fr/destinations/crete-beach-life/02afa47c-512f-4310-afd1-26407a5449a1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/crete-beach-life/02afa47c-512f-4310-afd1-26407a5449a1'>🔗</a></td>
    </tr>
    <tr>
      <td>Grecia</td>
      <td>Grèce</td>
      <td>Grèce 360: Athènes, les Météores et le Péloponnèse</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge default'>SOLD&nbsp;OUT</span></td>
      <td>2025-09-14</td>
      <td>2025-09-21</td>
      <td>https://www.weroad.fr/destinations/grece-360-athenes-meteores-peloponnese/57cacbf8-6ddd-4c2c-a68c-82eb85b4c3ed</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/grece-360-athenes-meteores-peloponnese/57cacbf8-6ddd-4c2c-a68c-82eb85b4c3ed'>🔗</a></td>
    </tr>
    <tr>
      <td>Guatemala</td>
      <td>Guatemala</td>
      <td>Guatemala 360° : Voyage au pays des volcans, nature sauvage et cultures anciennes</td>
      <td>1 699,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-04-09</td>
      <td>2026-04-20</td>
      <td>https://www.weroad.fr/destinations/guatemala-volcans-nature-cultures-anciennes/63bb2f26-bd1b-42c0-a675-00df9455154e</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/guatemala-volcans-nature-cultures-anciennes/63bb2f26-bd1b-42c0-a675-00df9455154e'>🔗</a></td>
    </tr>
    <tr>
      <td>Géorgie</td>
      <td>Géorgie</td>
      <td>Georgie Ski & Snowboard Express : dans les montagnes du Caucase</td>
      <td>899,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-28</td>
      <td>2026-01-02</td>
      <td>https://www.weroad.fr/destinations/georgie-caucase-ski-snowboard/bacb86c1-cfdb-4691-893b-593ddd94b1a9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/georgie-caucase-ski-snowboard/bacb86c1-cfdb-4691-893b-593ddd94b1a9'>🔗</a></td>
    </tr>
    <tr>
      <td>Hongrie</td>
      <td>Hongrie</td>
      <td>Budapest Express</td>
      <td>599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-07</td>
      <td>2025-11-11</td>
      <td>https://www.weroad.fr/destinations/budapest-express/997c4112-821d-42d3-8295-05400366e503</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/budapest-express/997c4112-821d-42d3-8295-05400366e503'>🔗</a></td>
    </tr>
    <tr>
      <td>Hungary</td>
      <td>Hongrie</td>
      <td>Prague, Vienne et Budapest : édition Marchés de Noël</td>
      <td>949,00 €</td>
      <td>999,00 €</td>
      <td>50.0</td>
      <td>5.0%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-06</td>
      <td>2025-12-12</td>
      <td>https://www.weroad.fr/destinations/prague-budapest-marches-noel-weroadx/3cce12b1-62f4-49ef-9931-4dced2893755</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/prague-budapest-marches-noel-weroadx/3cce12b1-62f4-49ef-9931-4dced2893755'>🔗</a></td>
    </tr>
    <tr>
      <td>Inde</td>
      <td>Inde</td>
      <td>Inde : du Rajasthan au Taj Mahal</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-10-12</td>
      <td>2025-10-20</td>
      <td>https://www.weroad.fr/destinations/inde-rajasthan-taj-mahal/e39b83ce-32a1-4f98-8d35-e6437f87c7c1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/inde-rajasthan-taj-mahal/e39b83ce-32a1-4f98-8d35-e6437f87c7c1'>🔗</a></td>
    </tr>
    <tr>
      <td>INDONÉSIE</td>
      <td>Indonésie</td>
      <td>Bali 360° : entre rizières, temples et plages paradisiaques</td>
      <td>779,00 €</td>
      <td>949,00 €</td>
      <td>170.0</td>
      <td>17.9%</td>
      <td><span class='rp-badge default'>ALMOST_FULL</span></td>
      <td>2025-09-07</td>
      <td>2025-09-14</td>
      <td>https://www.weroad.fr/destinations/bali-360/9656aacd-dbf2-4707-aa9a-53da2f5f87fb</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bali-360/9656aacd-dbf2-4707-aa9a-53da2f5f87fb'>🔗</a></td>
    </tr>
    <tr>
      <td>Indonesie</td>
      <td>Indonésie</td>
      <td>Indonésie d'île en île : Bali, Lembongan et Gili</td>
      <td>899,00 €</td>
      <td>1 099,00 €</td>
      <td>200.0</td>
      <td>18.2%</td>
      <td><span class='rp-badge default'>SOLD&nbsp;OUT</span></td>
      <td>2025-09-05</td>
      <td>2025-09-14</td>
      <td>https://www.weroad.fr/destinations/indonesie-bali-lombok-java-nusa-penida/d0b065fd-904f-4676-97d6-44355c8075bb</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/indonesie-bali-lombok-java-nusa-penida/d0b065fd-904f-4676-97d6-44355c8075bb'>🔗</a></td>
    </tr>
    <tr>
      <td>Indonésie</td>
      <td>Indonésie</td>
      <td>Bali et Gili : ambiance tropicale et eau turquoise</td>
      <td>889,00 €</td>
      <td>949,00 €</td>
      <td>60.0</td>
      <td>6.3%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-21</td>
      <td>2025-11-29</td>
      <td>https://www.weroad.fr/destinations/bali-gili-indonesie-tropicale-eau-turquoise/cf7b2440-b096-49db-93bc-a63d02147298</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bali-gili-indonesie-tropicale-eau-turquoise/cf7b2440-b096-49db-93bc-a63d02147298'>🔗</a></td>
    </tr>
    <tr>
      <td>Irlande</td>
      <td>Irlande</td>
      <td>Irlande Express : Dublin, Galway et au Connemara</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-02-03</td>
      <td>2026-02-08</td>
      <td>https://www.weroad.fr/destinations/irlande-express-tour-dublin-galway-connemara-weroadx/a5843663-f32e-4882-ab04-d8f741753d22</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/irlande-express-tour-dublin-galway-connemara-weroadx/a5843663-f32e-4882-ab04-d8f741753d22'>🔗</a></td>
    </tr>
    <tr>
      <td>Islande</td>
      <td>Islande</td>
      <td>Islande Express : un aperçu de l'île de glace et de feu</td>
      <td>899,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-03-11</td>
      <td>2026-03-15</td>
      <td>https://www.weroad.fr/destinations/islande-express/d898ced6-2b42-4c17-b767-4a831b07989c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/islande-express/d898ced6-2b42-4c17-b767-4a831b07989c'>🔗</a></td>
    </tr>
    <tr>
      <td>Dolomites</td>
      <td>Italie</td>
      <td>Dolomites 360° et Lac de Braies</td>
      <td>919,00 €</td>
      <td>1 049,00 €</td>
      <td>130.0</td>
      <td>12.4%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-27</td>
      <td>2025-10-04</td>
      <td>https://www.weroad.fr/destinations/dolomites/cd862058-7484-4ee5-b21b-7152baf7951f</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/dolomites/cd862058-7484-4ee5-b21b-7152baf7951f'>🔗</a></td>
    </tr>
    <tr>
      <td>Italie</td>
      <td>Italie</td>
      <td>Italie Ski & Snowboard Express : les montagnes de Sestrières dans les Alpes</td>
      <td>799,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-26</td>
      <td>2025-11-30</td>
      <td>https://www.weroad.fr/destinations/sestrieres-italie-ski-snowboard/d1280ff0-9371-4d62-bd54-f50a6526b313</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/sestrieres-italie-ski-snowboard/d1280ff0-9371-4d62-bd54-f50a6526b313'>🔗</a></td>
    </tr>
    <tr>
      <td>Naples & la côte Amalfitaine</td>
      <td>Italie</td>
      <td>Naples et la côte Amalfitaine Express</td>
      <td>519,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge default'>ALMOST_FULL</span></td>
      <td>2025-09-17</td>
      <td>2025-09-21</td>
      <td>https://www.weroad.fr/destinations/naples-cote-amalfitaine/b1ddad19-7b00-494e-9704-5558c46f7999</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/naples-cote-amalfitaine/b1ddad19-7b00-494e-9704-5558c46f7999'>🔗</a></td>
    </tr>
    <tr>
      <td>Sicile</td>
      <td>Italie</td>
      <td>Sicile Beach Life : de Palerme À San Vito entre mer et temples</td>
      <td>1 199,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-04</td>
      <td>2025-10-11</td>
      <td>https://www.weroad.fr/destinations/sicile-palerme-san-vito/52eddb48-7798-4b5c-8798-3fc4656441e9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/sicile-palerme-san-vito/52eddb48-7798-4b5c-8798-3fc4656441e9'>🔗</a></td>
    </tr>
    <tr>
      <td>Japon</td>
      <td>Japon</td>
      <td>Japon 360° : découverte de Tokyo, Kyoto, Hiroshima et Osaka</td>
      <td>1 499,00 €</td>
      <td>1 799,00 €</td>
      <td>300.0</td>
      <td>16.7%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-26</td>
      <td>2025-10-06</td>
      <td>https://www.weroad.fr/destinations/japon-360/a5da9bc1-f6ff-48ee-bd83-c7e58a0752c9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/japon-360/a5da9bc1-f6ff-48ee-bd83-c7e58a0752c9'>🔗</a></td>
    </tr>
    <tr>
      <td>Jordanie</td>
      <td>Jordanie</td>
      <td>Jordanie 360° : Petra, Amman et Wadi Rum</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge default'>SOLD&nbsp;OUT</span></td>
      <td>2025-09-22</td>
      <td>2025-09-29</td>
      <td>https://www.weroad.fr/destinations/jordanie-360/8ebabc2b-e374-462d-b424-a73c9f775a23</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/jordanie-360/8ebabc2b-e374-462d-b424-a73c9f775a23'>🔗</a></td>
    </tr>
    <tr>
      <td>Kenya</td>
      <td>Kenya</td>
      <td>Kenya : au cœur de l'Afrique entre safaris, plages et villages locaux</td>
      <td>1 789,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-19</td>
      <td>2025-10-28</td>
      <td>https://www.weroad.fr/destinations/kenya-afrique-safari-plage-village/c38a5ff2-25f2-4033-b1f3-829713cef607</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kenya-afrique-safari-plage-village/c38a5ff2-25f2-4033-b1f3-829713cef607'>🔗</a></td>
    </tr>
    <tr>
      <td>Kirghizistan</td>
      <td>Kirghizistan</td>
      <td>Kirghizistan Winter : entre lacs gelés et culture nomade</td>
      <td>1 049,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-28</td>
      <td>2026-01-05</td>
      <td>https://www.weroad.fr/destinations/kirghizistan-winter/8fd3b586-dd7b-4f85-837d-64830c233a1c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kirghizistan-winter/8fd3b586-dd7b-4f85-837d-64830c233a1c'>🔗</a></td>
    </tr>
    <tr>
      <td>Malaisie</td>
      <td>Malaisie</td>
      <td>Malaisie : nature sauvage et îles paradisiaques</td>
      <td>1 105,00 €</td>
      <td>1 299,00 €</td>
      <td>194.0</td>
      <td>14.9%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-03-29</td>
      <td>2026-04-09</td>
      <td>https://www.weroad.fr/destinations/malaisie-nature-ile/c37b0913-06fc-4049-8953-3b73e3430880</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/malaisie-nature-ile/c37b0913-06fc-4049-8953-3b73e3430880'>🔗</a></td>
    </tr>
    <tr>
      <td>Maldives</td>
      <td>Maldives</td>
      <td>Maldives Beach Life BackPack : snorkeling et détente à Maafushi</td>
      <td>1 179,00 €</td>
      <td>1 249,00 €</td>
      <td>70.0</td>
      <td>5.6%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-02-22</td>
      <td>2026-03-01</td>
      <td>https://www.weroad.fr/destinations/maldives-beach-life-detente-snorkeling-maafushi/15a96831-47c3-478e-9183-c6619e40cb18</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maldives-beach-life-detente-snorkeling-maafushi/15a96831-47c3-478e-9183-c6619e40cb18'>🔗</a></td>
    </tr>
    <tr>
      <td>Malte</td>
      <td>Malte</td>
      <td>Malte Beach Life Express : Voyage sur les îles de Malte, Gozo et Comino</td>
      <td>759,00 €</td>
      <td>799,00 €</td>
      <td>40.0</td>
      <td>5.0%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-19</td>
      <td>2025-09-24</td>
      <td>https://www.weroad.fr/destinations/malte-express-gozo-comino/562901ce-50c2-426f-9b47-479ea882d372</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/malte-express-gozo-comino/562901ce-50c2-426f-9b47-479ea882d372'>🔗</a></td>
    </tr>
    <tr>
      <td>Maroc</td>
      <td>Maroc</td>
      <td>Maroc : Trekking au Mont Toubkal</td>
      <td>479,00 €</td>
      <td>599,00 €</td>
      <td>120.0</td>
      <td>20.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-27</td>
      <td>2025-10-01</td>
      <td>https://www.weroad.fr/destinations/maroc-trekking-mount-toubkal/4310fa36-bb29-48fb-856e-359806887f88</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maroc-trekking-mount-toubkal/4310fa36-bb29-48fb-856e-359806887f88'>🔗</a></td>
    </tr>
    <tr>
      <td>Maurice</td>
      <td>Maurice</td>
      <td>Île Maurice Beach Life : Road trip entre plages paradisiaques et aventure locale</td>
      <td>1 149,00 €</td>
      <td>1 329,00 €</td>
      <td>180.0</td>
      <td>13.5%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-14</td>
      <td>2025-09-21</td>
      <td>https://www.weroad.fr/destinations/ile-maurice-beach-life-road-trip-plages-aventure/1e66c621-1836-46e2-abeb-5ffe000ba6c8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/ile-maurice-beach-life-road-trip-plages-aventure/1e66c621-1836-46e2-abeb-5ffe000ba6c8'>🔗</a></td>
    </tr>
    <tr>
      <td>Mexique</td>
      <td>Mexique</td>
      <td>Mexique Beach Life : de Cancun à Isla Mujeres, plage et détente</td>
      <td>1 399,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-03-03</td>
      <td>2026-03-10</td>
      <td>https://www.weroad.fr/destinations/mexique-yucatan-beach-life/cfcca156-1834-4bd3-83ae-e3c429ab3ee2</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/mexique-yucatan-beach-life/cfcca156-1834-4bd3-83ae-e3c429ab3ee2'>🔗</a></td>
    </tr>
    <tr>
      <td>Namibie</td>
      <td>Namibie</td>
      <td>Namibie 360°</td>
      <td>2 299,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-05-03</td>
      <td>2026-05-13</td>
      <td>https://www.weroad.fr/destinations/namibie/f8882a9a-fd70-466d-8dc9-f0f6ce0838ae</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/namibie/f8882a9a-fd70-466d-8dc9-f0f6ce0838ae'>🔗</a></td>
    </tr>
    <tr>
      <td>Nicaragua</td>
      <td>Nicaragua</td>
      <td>Nicaragua 360° : aventure au pays des lacs et des volcans</td>
      <td>1 429,00 €</td>
      <td>1 649,00 €</td>
      <td>220.0</td>
      <td>13.3%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-01-20</td>
      <td>2026-01-31</td>
      <td>https://www.weroad.fr/destinations/nicaragua-aventure-lacs-volcans/6581d368-826f-46c2-a893-664aa3666c3f</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/nicaragua-aventure-lacs-volcans/6581d368-826f-46c2-a893-664aa3666c3f'>🔗</a></td>
    </tr>
    <tr>
      <td>Norvège</td>
      <td>Norvège</td>
      <td>Norvège : chasse aux aurores boréales aux îles Lofoten</td>
      <td>1 449,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-29</td>
      <td>2026-01-04</td>
      <td>https://www.weroad.fr/destinations/norvege-lofoten-aurore-boreales/0f479dd1-e9b6-40ec-9576-8eed660fa474</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/norvege-lofoten-aurore-boreales/0f479dd1-e9b6-40ec-9576-8eed660fa474'>🔗</a></td>
    </tr>
    <tr>
      <td>Nouvelle-Zélande</td>
      <td>Nouvelle-Zélande</td>
      <td>Nouvelle-Zélande 360°: sur la route d'Auckland jusqu'à Queenstown</td>
      <td>2 549,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-18</td>
      <td>2025-12-01</td>
      <td>https://www.weroad.fr/destinations/nouvelle-zelande-360/71f6cafe-68e7-4353-8896-7abffce8ad52</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/nouvelle-zelande-360/71f6cafe-68e7-4353-8896-7abffce8ad52'>🔗</a></td>
    </tr>
    <tr>
      <td>Népal</td>
      <td>Népal</td>
      <td>Népal 360° : entre les temples de Katmandou et les sommets de l'Annapurna</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-10-27</td>
      <td>2025-11-04</td>
      <td>https://www.weroad.fr/destinations/nepal/178e3708-674a-4eee-b56b-6cbdde73a7f7</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/nepal/178e3708-674a-4eee-b56b-6cbdde73a7f7'>🔗</a></td>
    </tr>
    <tr>
      <td>Oman</td>
      <td>Oman</td>
      <td>Oman 360°</td>
      <td>1 149,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-07</td>
      <td>2025-11-15</td>
      <td>https://www.weroad.fr/destinations/oman/77ce635f-0502-479d-afc6-6b51f8f4d033</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/oman/77ce635f-0502-479d-afc6-6b51f8f4d033'>🔗</a></td>
    </tr>
    <tr>
      <td>Ouzbékistan</td>
      <td>Ouzbékistan</td>
      <td>Ouzbékistan 360° Summer</td>
      <td>899,00 €</td>
      <td>1 099,00 €</td>
      <td>200.0</td>
      <td>18.2%</td>
      <td><span class='rp-badge default'>WAITING</span></td>
      <td>2025-09-21</td>
      <td>2025-09-29</td>
      <td>https://www.weroad.fr/destinations/ouzbekistan-tachkent-samarkand-360/83f3e4d5-0674-4453-b714-7cfb349bab8c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/ouzbekistan-tachkent-samarkand-360/83f3e4d5-0674-4453-b714-7cfb349bab8c'>🔗</a></td>
    </tr>
    <tr>
      <td>Panamá</td>
      <td>Panamá</td>
      <td>Panama Beach Life : d’îles en îles des San Blas à Bocas del Toro</td>
      <td>1 566,00 €</td>
      <td>1 649,00 €</td>
      <td>83.0</td>
      <td>5.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-26</td>
      <td>2026-01-04</td>
      <td>https://www.weroad.fr/destinations/panama-beach-life-san-blas-bocas-del-toro/ca12031b-f919-40f6-b4e4-6c93e8c50516</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/panama-beach-life-san-blas-bocas-del-toro/ca12031b-f919-40f6-b4e4-6c93e8c50516'>🔗</a></td>
    </tr>
    <tr>
      <td>Philippines</td>
      <td>Philippines</td>
      <td>Philippines 360° : Bohol, Coron & Palawan</td>
      <td>2 099,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-02</td>
      <td>2025-12-14</td>
      <td>https://www.weroad.fr/destinations/philippines-360/24433f78-1729-4032-a40b-c8310e85563c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/philippines-360/24433f78-1729-4032-a40b-c8310e85563c'>🔗</a></td>
    </tr>
    <tr>
      <td>Portugal</td>
      <td>Portugal</td>
      <td>Portugal Express</td>
      <td>699,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-10-04</td>
      <td>2025-10-08</td>
      <td>https://www.weroad.fr/destinations/portugal-express/4fac448c-b7e1-4c52-9265-632cf8912065</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/portugal-express/4fac448c-b7e1-4c52-9265-632cf8912065'>🔗</a></td>
    </tr>
    <tr>
      <td>Pérou</td>
      <td>Pérou</td>
      <td>Pérou 360° : Machu Picchu, montagne arc-en-ciel et lac Titicaca</td>
      <td>1 529,00 €</td>
      <td>1 699,00 €</td>
      <td>170.0</td>
      <td>10.0%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-29</td>
      <td>2025-10-10</td>
      <td>https://www.weroad.fr/destinations/perou-360/16c0ac74-1577-4752-b63d-1a081063cbd3</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/perou-360/16c0ac74-1577-4752-b63d-1a081063cbd3'>🔗</a></td>
    </tr>
    <tr>
      <td>Romania</td>
      <td>Roumanie</td>
      <td>Transylvanie Express : Road Trip dans le pays du Comte Dracula</td>
      <td>449,00 €</td>
      <td>499,00 €</td>
      <td>50.0</td>
      <td>10.0%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-17</td>
      <td>2025-09-21</td>
      <td>https://www.weroad.fr/destinations/transylvanie-express-route-comte-dracula/8a2982d2-c24c-4361-8101-f6a4fbb9e5ef</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/transylvanie-express-route-comte-dracula/8a2982d2-c24c-4361-8101-f6a4fbb9e5ef'>🔗</a></td>
    </tr>
    <tr>
      <td>Écosse</td>
      <td>Royaume-Uni</td>
      <td>Écosse Express : Édimbourg et les Highlands comme un local</td>
      <td>849,00 €</td>
      <td>899,00 €</td>
      <td>50.0</td>
      <td>5.6%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-08</td>
      <td>2025-10-12</td>
      <td>https://www.weroad.fr/destinations/Ecosse-express-edimbourg-highlands/f9928125-64ec-4fbb-aa0f-d830fc9f913c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/Ecosse-express-edimbourg-highlands/f9928125-64ec-4fbb-aa0f-d830fc9f913c'>🔗</a></td>
    </tr>
    <tr>
      <td>Réunion</td>
      <td>Réunion</td>
      <td>L'île de La Réunion : entre cirques, volcan et plages</td>
      <td>1 390,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-15</td>
      <td>2025-12-22</td>
      <td>https://www.weroad.fr/destinations/ile-reunion-cirques-volcan-plages/1d152290-dbfc-413e-baee-48ddcd2a4ffb</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/ile-reunion-cirques-volcan-plages/1d152290-dbfc-413e-baee-48ddcd2a4ffb'>🔗</a></td>
    </tr>
    <tr>
      <td>Slovénie</td>
      <td>Slovénie</td>
      <td>Slovénie 360°</td>
      <td>1 049,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge default'>ALMOST_FULL</span></td>
      <td>2025-09-23</td>
      <td>2025-09-28</td>
      <td>https://www.weroad.fr/destinations/slovenie-360/51571407-697c-4137-bd98-6a5a32404bff</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/slovenie-360/51571407-697c-4137-bd98-6a5a32404bff'>🔗</a></td>
    </tr>
    <tr>
      <td>Sri Lanka</td>
      <td>Sri Lanka</td>
      <td>Sri Lanka 360° Summer</td>
      <td>899,00 €</td>
      <td>999,00 €</td>
      <td>100.0</td>
      <td>10.0%</td>
      <td><span class='rp-badge default'>SOLD&nbsp;OUT</span></td>
      <td>2025-09-01</td>
      <td>2025-09-12</td>
      <td>https://www.weroad.fr/destinations/sri-lanka-360-ete/cd29383d-b82d-4c3b-a062-052b18c87d3f</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/sri-lanka-360-ete/cd29383d-b82d-4c3b-a062-052b18c87d3f'>🔗</a></td>
    </tr>
    <tr>
      <td>Suisse</td>
      <td>Suisse</td>
      <td>Suisse Express : aventure en train au coeur des Alpes entre lacs et montagnes</td>
      <td>949,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-22</td>
      <td>2025-10-26</td>
      <td>https://www.weroad.fr/destinations/suisse-express-alpes-lacs-montagnes/28df726d-d517-4b7c-8072-a9c1ff638411</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/suisse-express-alpes-lacs-montagnes/28df726d-d517-4b7c-8072-a9c1ff638411'>🔗</a></td>
    </tr>
    <tr>
      <td>Suède</td>
      <td>Suède</td>
      <td>Laponie suédoise : chasse aux aurores boréales à Luleå</td>
      <td>1 549,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-30</td>
      <td>2026-01-03</td>
      <td>https://www.weroad.fr/destinations/suede-lulea-laponie/914ba73f-ceab-4cd8-92f4-f966f0ed37db</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/suede-lulea-laponie/914ba73f-ceab-4cd8-92f4-f966f0ed37db'>🔗</a></td>
    </tr>
    <tr>
      <td>Sénégal</td>
      <td>Sénégal</td>
      <td>Sénégal :  Roadtrip entre terre et fleuve</td>
      <td>2 050,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-04-16</td>
      <td>2026-04-25</td>
      <td>https://www.weroad.fr/destinations/senegal-entre-terre-et-fleuve/dfd20650-8ed4-4f16-8209-26479258f025</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/senegal-entre-terre-et-fleuve/dfd20650-8ed4-4f16-8209-26479258f025'>🔗</a></td>
    </tr>
    <tr>
      <td>Tanzanie</td>
      <td>Tanzanie</td>
      <td>Kilimandjaro Expedition: Lemosho route and Safari</td>
      <td>3 499,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-26</td>
      <td>2026-01-05</td>
      <td>https://www.weroad.fr/destinations/kilimandjaro-trekking-lemosho-route-safari/2cf26f9c-b039-4e59-939c-4666e92acd44</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kilimandjaro-trekking-lemosho-route-safari/2cf26f9c-b039-4e59-939c-4666e92acd44'>🔗</a></td>
    </tr>
    <tr>
      <td>Tchéquie</td>
      <td>Tchéquie</td>
      <td>Europe centrale : Prague, Vienne et Budapest en train</td>
      <td>849,00 €</td>
      <td>899,00 €</td>
      <td>50.0</td>
      <td>5.6%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-11</td>
      <td>2025-10-17</td>
      <td>https://www.weroad.fr/destinations/europe-prague-vienne-budapest-weroadx/ee1e9275-45f4-4120-a2b4-0dedbe5d3d65</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/europe-prague-vienne-budapest-weroadx/ee1e9275-45f4-4120-a2b4-0dedbe5d3d65'>🔗</a></td>
    </tr>
    <tr>
      <td>Thailande</td>
      <td>Thaïlande</td>
      <td>Thaïlande 360° Summer</td>
      <td>1 249,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge default'>WAITING</span></td>
      <td>2025-09-11</td>
      <td>2025-09-22</td>
      <td>https://www.weroad.fr/destinations/thailande-360-ete/e3f05c52-64db-42c9-a457-8b25c6fb177e</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/thailande-360-ete/e3f05c52-64db-42c9-a457-8b25c6fb177e'>🔗</a></td>
    </tr>
    <tr>
      <td>Thaïlande</td>
      <td>Thaïlande</td>
      <td>Thaïlande Beach Life Winter : Phuket, Krabi et Koh Lanta</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-03-10</td>
      <td>2026-03-19</td>
      <td>https://www.weroad.fr/destinations/thailande-plage-hiver/43ad04b5-307e-4067-aeb3-b0f66415d4ad</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/thailande-plage-hiver/43ad04b5-307e-4067-aeb3-b0f66415d4ad'>🔗</a></td>
    </tr>
    <tr>
      <td>Tunisie</td>
      <td>Tunisie</td>
      <td>Tunisie Express : Djerba, Un mélange de détente et cultures.</td>
      <td>789,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-15</td>
      <td>2025-10-19</td>
      <td>https://www.weroad.fr/destinations/tunisie-express-djerba-detente-culture/a36141f8-fe71-4213-9468-4434f3e031b6</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/tunisie-express-djerba-detente-culture/a36141f8-fe71-4213-9468-4434f3e031b6'>🔗</a></td>
    </tr>
    <tr>
      <td>Istanbul</td>
      <td>Turquie</td>
      <td>Istanbul Express</td>
      <td>599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-04-28</td>
      <td>2026-05-02</td>
      <td>https://www.weroad.fr/destinations/istanbul-express/3d770660-8db7-4454-b2c0-a6e0b4230788</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/istanbul-express/3d770660-8db7-4454-b2c0-a6e0b4230788'>🔗</a></td>
    </tr>
    <tr>
      <td>Istanbul & Cappadoce</td>
      <td>Turquie</td>
      <td>Turquie : un voyage d'Istanbul à la Cappadoce</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-16</td>
      <td>2025-11-23</td>
      <td>https://www.weroad.fr/destinations/istanbul-cappadoce/295a0250-7839-4f8b-9e28-a52e6de7a8a3</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/istanbul-cappadoce/295a0250-7839-4f8b-9e28-a52e6de7a8a3'>🔗</a></td>
    </tr>
    <tr>
      <td>Turquie</td>
      <td>Turquie</td>
      <td>Turquie 360° : Istanbul, Cappadoce et Éphèse</td>
      <td>1 349,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-03-21</td>
      <td>2026-03-29</td>
      <td>https://www.weroad.fr/destinations/turquie-istanbul-cappadoce-ephese/a587c038-116a-4db7-9945-9a45e50c9ead</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/turquie-istanbul-cappadoce-ephese/a587c038-116a-4db7-9945-9a45e50c9ead'>🔗</a></td>
    </tr>
    <tr>
      <td>Vietnam</td>
      <td>Viêt Nam</td>
      <td>Vietnam 360° : de Hanoï à Hô Chi Minh</td>
      <td>959,00 €</td>
      <td>1 199,00 €</td>
      <td>240.0</td>
      <td>20.0%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-19</td>
      <td>2025-10-01</td>
      <td>https://www.weroad.fr/destinations/vietnam/a1eb2771-a671-4f45-8838-1bb93cebf42a</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/vietnam/a1eb2771-a671-4f45-8838-1bb93cebf42a'>🔗</a></td>
    </tr>
    <tr>
      <td>Égypte</td>
      <td>Égypte</td>
      <td>Egypte Express: Le Caire et les Pyramides</td>
      <td>499,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-05</td>
      <td>2025-12-09</td>
      <td>https://www.weroad.fr/destinations/le-caire-express-egypt/bfe5c5e8-2c20-4761-9093-e5941d18325c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/le-caire-express-egypt/bfe5c5e8-2c20-4761-9093-e5941d18325c'>🔗</a></td>
    </tr>
    <tr>
      <td>Émirats Arabes Unis</td>
      <td>Émirats arabes unis</td>
      <td>Émirats Arabes Unis 360° : Dubaï, Abou Dabi et le désert</td>
      <td>1 199,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-10-17</td>
      <td>2025-10-23</td>
      <td>https://www.weroad.fr/destinations/dubai-abou-dhabi-desert/ea5c696d-41ec-4831-8b2e-65f6d10205f1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/dubai-abou-dhabi-desert/ea5c696d-41ec-4831-8b2e-65f6d10205f1'>🔗</a></td>
    </tr>
    <tr>
      <td>Équateur</td>
      <td>Équateur</td>
      <td>Équateur & Galapagos 360° : entre Andes, Amazonie et îles enchantées</td>
      <td>2 709,00 €</td>
      <td>3 299,00 €</td>
      <td>590.0</td>
      <td>17.9%</td>
      <td><span class='rp-badge default'>SOLD&nbsp;OUT</span></td>
      <td>2025-09-05</td>
      <td>2025-09-19</td>
      <td>https://www.weroad.fr/destinations/equateur-galapogos-amazonie/7e4307e1-1821-426e-bcaa-ccb4120a2a56</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/equateur-galapogos-amazonie/7e4307e1-1821-426e-bcaa-ccb4120a2a56'>🔗</a></td>
    </tr>
    <tr>
      <td>Équateur & Amazonie</td>
      <td>Équateur</td>
      <td>Équateur & Amazonie Expedition</td>
      <td>1 299,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-25</td>
      <td>2025-11-04</td>
      <td>https://www.weroad.fr/destinations/equateur-et-amazonie/89e92461-4baa-44bf-b886-18280e75526d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/equateur-et-amazonie/89e92461-4baa-44bf-b886-18280e75526d'>🔗</a></td>
    </tr>
    <tr>
      <td>Floride</td>
      <td>États-Unis d'Amérique</td>
      <td>Floride 360° : Orlando, Miami et Key West</td>
      <td>1 479,00 €</td>
      <td>1 799,00 €</td>
      <td>320.0</td>
      <td>17.8%</td>
      <td><span class='rp-badge default'>ALMOST_FULL</span></td>
      <td>2025-09-07</td>
      <td>2025-09-16</td>
      <td>https://www.weroad.fr/destinations/floride/18a6b821-33fc-4b9e-809a-22a2ce8264da</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/floride/18a6b821-33fc-4b9e-809a-22a2ce8264da'>🔗</a></td>
    </tr>
    <tr>
      <td>New York</td>
      <td>États-Unis d'Amérique</td>
      <td>New York 360° : à la découverte de Manhattan, Brooklyn et Harlem</td>
      <td>819,00 €</td>
      <td>999,00 €</td>
      <td>180.0</td>
      <td>18.0%</td>
      <td><span class='rp-badge default'>ALMOST_FULL</span></td>
      <td>2025-09-14</td>
      <td>2025-09-19</td>
      <td>https://www.weroad.fr/destinations/new-york/b570f3fe-55dc-4dad-a15b-48718a0ef8e8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/new-york/b570f3fe-55dc-4dad-a15b-48718a0ef8e8'>🔗</a></td>
    </tr>
    <tr>
      <td>Route 66</td>
      <td>États-Unis d'Amérique</td>
      <td>États-Unis : Road Trip sur la route 66 de Chicago à Los Angeles</td>
      <td>1 899,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-10-18</td>
      <td>2025-11-01</td>
      <td>https://www.weroad.fr/destinations/road-trip-route-66-chicago-los-angeles/9f58586f-b92a-455d-a8e1-d404f1abdb85</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/road-trip-route-66-chicago-los-angeles/9f58586f-b92a-455d-a8e1-d404f1abdb85'>🔗</a></td>
    </tr>
    <tr>
      <td>États-Unis</td>
      <td>États-Unis d'Amérique</td>
      <td>Far West 360° : Los Angeles, Las Vegas et les grands parcs américains</td>
      <td>1 599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-10-26</td>
      <td>2025-11-06</td>
      <td>https://www.weroad.fr/destinations/far-west-360/737ac5d4-4aa4-4ea0-8689-996f9835ca89</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/far-west-360/737ac5d4-4aa4-4ea0-8689-996f9835ca89'>🔗</a></td>
    </tr>
  </tbody>
</table>
</div>

---

## Top offres par mois (les moins chères)
<div class='table-wrapper'>
<table border="1" class="dataframe rp-table">
  <thead>
    <tr style="text-align: right;">
      <th>month_depart</th>
      <th>destination_label</th>
      <th>title</th>
      <th>country_name</th>
      <th>price_eur_min_month</th>
      <th>discount_pct</th>
      <th>sales_status</th>
      <th>best_starting_date</th>
      <th>url_precise</th>
      <th>url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2025-08</td>
      <td>Islande</td>
      <td>Islande Expédition : sur l'île de glace et de feu sous une tente</td>
      <td>Islande</td>
      <td>999,00 €</td>
      <td></td>
      <td><span class='rp-badge default'>WAITING</span></td>
      <td>2025-08-31</td>
      <td>https://www.weroad.fr/destinations/islande-expedition/5f3339d6-7b58-4a8f-a3cc-6b6194015a03</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/islande-expedition/5f3339d6-7b58-4a8f-a3cc-6b6194015a03'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Romania</td>
      <td>Transylvanie Express : Road Trip dans le pays du Comte Dracula</td>
      <td>Roumanie</td>
      <td>449,00 €</td>
      <td>10.0%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-17</td>
      <td>https://www.weroad.fr/destinations/transylvanie-express-route-comte-dracula/8a2982d2-c24c-4361-8101-f6a4fbb9e5ef</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/transylvanie-express-route-comte-dracula/8a2982d2-c24c-4361-8101-f6a4fbb9e5ef'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Maroc</td>
      <td>Maroc : Trekking au Mont Toubkal</td>
      <td>Maroc</td>
      <td>479,00 €</td>
      <td>20.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-27</td>
      <td>https://www.weroad.fr/destinations/maroc-trekking-mount-toubkal/4310fa36-bb29-48fb-856e-359806887f88</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maroc-trekking-mount-toubkal/4310fa36-bb29-48fb-856e-359806887f88'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Naples & la côte Amalfitaine</td>
      <td>Naples et la côte Amalfitaine Express</td>
      <td>Italie</td>
      <td>519,00 €</td>
      <td></td>
      <td><span class='rp-badge default'>ALMOST_FULL</span></td>
      <td>2025-09-17</td>
      <td>https://www.weroad.fr/destinations/naples-cote-amalfitaine/b1ddad19-7b00-494e-9704-5558c46f7999</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/naples-cote-amalfitaine/b1ddad19-7b00-494e-9704-5558c46f7999'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Maroc</td>
      <td>Maroc Express : Marrakech, Essaouira et le désert</td>
      <td>Maroc</td>
      <td>529,00 €</td>
      <td>18.5%</td>
      <td><span class='rp-badge default'>ALMOST_FULL</span></td>
      <td>2025-09-01</td>
      <td>https://www.weroad.fr/destinations/maroc-marrakech-essaouira-desert/6d8880ec-825a-48eb-8ac5-647d09249450</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maroc-marrakech-essaouira-desert/6d8880ec-825a-48eb-8ac5-647d09249450'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Albanie</td>
      <td>Albanie 360° : Tirana et les plages du sud</td>
      <td>Albanie</td>
      <td>639,00 €</td>
      <td>20.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-23</td>
      <td>https://www.weroad.fr/destinations/albanie-tirana-plages-sud/d117ece9-bd9e-494a-bae7-281d52d89619</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/albanie-tirana-plages-sud/d117ece9-bd9e-494a-bae7-281d52d89619'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Maroc</td>
      <td>Maroc 360° : Marrakech, Fès, Rabat et le désert</td>
      <td>Maroc</td>
      <td>659,00 €</td>
      <td>12.0%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-12</td>
      <td>https://www.weroad.fr/destinations/maroc-marrakech-fes-rabat-desert/2e17500f-c6fb-4880-949e-390fd175f648</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maroc-marrakech-fes-rabat-desert/2e17500f-c6fb-4880-949e-390fd175f648'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Maroc</td>
      <td>Maroc 360° : du désert aux villes des mille et une nuits</td>
      <td>Maroc</td>
      <td>699,00 €</td>
      <td>12.5%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-30</td>
      <td>https://www.weroad.fr/destinations/maroc/61788514-5980-4778-8e12-ab4be26e5b60</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maroc/61788514-5980-4778-8e12-ab4be26e5b60'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Corfou</td>
      <td>Corfou Beach Life : plage et découverte des îles</td>
      <td>Grèce</td>
      <td>739,00 €</td>
      <td>17.8%</td>
      <td><span class='rp-badge default'>ALMOST_FULL</span></td>
      <td>2025-09-14</td>
      <td>https://www.weroad.fr/destinations/corfou-360/9d44fecc-3467-4a0f-b668-c1cd49f0e9c3</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/corfou-360/9d44fecc-3467-4a0f-b668-c1cd49f0e9c3'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Malte</td>
      <td>Malte Beach Life Express : Voyage sur les îles de Malte, Gozo et Comino</td>
      <td>Malte</td>
      <td>759,00 €</td>
      <td>5.0%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-19</td>
      <td>https://www.weroad.fr/destinations/malte-express-gozo-comino/562901ce-50c2-426f-9b47-479ea882d372</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/malte-express-gozo-comino/562901ce-50c2-426f-9b47-479ea882d372'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>INDONÉSIE</td>
      <td>Bali 360° : entre rizières, temples et plages paradisiaques</td>
      <td>Indonésie</td>
      <td>779,00 €</td>
      <td>17.9%</td>
      <td><span class='rp-badge default'>ALMOST_FULL</span></td>
      <td>2025-09-07</td>
      <td>https://www.weroad.fr/destinations/bali-360/9656aacd-dbf2-4707-aa9a-53da2f5f87fb</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bali-360/9656aacd-dbf2-4707-aa9a-53da2f5f87fb'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>France</td>
      <td>Côte d’Azur Express : Nice, Monaco et leurs trésors</td>
      <td>France</td>
      <td>789,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-09-24</td>
      <td>https://www.weroad.fr/destinations/cote-azur-express-france-nice-monaco/320ecf62-5f53-43fd-9cad-6602cd2ff294</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/cote-azur-express-france-nice-monaco/320ecf62-5f53-43fd-9cad-6602cd2ff294'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>New York</td>
      <td>New York 360° : à la découverte de Manhattan, Brooklyn et Harlem</td>
      <td>États-Unis d'Amérique</td>
      <td>819,00 €</td>
      <td>18.0%</td>
      <td><span class='rp-badge default'>ALMOST_FULL</span></td>
      <td>2025-09-14</td>
      <td>https://www.weroad.fr/destinations/new-york/b570f3fe-55dc-4dad-a15b-48718a0ef8e8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/new-york/b570f3fe-55dc-4dad-a15b-48718a0ef8e8'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Italie</td>
      <td>Italie: Rome, le Chianti, Florence, Luques et Pise</td>
      <td>Italie</td>
      <td>859,00 €</td>
      <td>18.1%</td>
      <td><span class='rp-badge default'>WAITING</span></td>
      <td>2025-09-06</td>
      <td>https://www.weroad.fr/destinations/rome-chianti-florence-luques-pise/7c9246eb-81f5-4f79-9aab-6a8e335ddcda</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/rome-chianti-florence-luques-pise/7c9246eb-81f5-4f79-9aab-6a8e335ddcda'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Sri Lanka</td>
      <td>Sri Lanka 360° Summer</td>
      <td>Sri Lanka</td>
      <td>899,00 €</td>
      <td>10.0%</td>
      <td><span class='rp-badge default'>SOLD&nbsp;OUT</span></td>
      <td>2025-09-01</td>
      <td>https://www.weroad.fr/destinations/sri-lanka-360-ete/cd29383d-b82d-4c3b-a062-052b18c87d3f</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/sri-lanka-360-ete/cd29383d-b82d-4c3b-a062-052b18c87d3f'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Indonesie</td>
      <td>Indonésie d'île en île : Bali, Lembongan et Gili</td>
      <td>Indonésie</td>
      <td>899,00 €</td>
      <td>18.2%</td>
      <td><span class='rp-badge default'>SOLD&nbsp;OUT</span></td>
      <td>2025-09-05</td>
      <td>https://www.weroad.fr/destinations/indonesie-bali-lombok-java-nusa-penida/d0b065fd-904f-4676-97d6-44355c8075bb</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/indonesie-bali-lombok-java-nusa-penida/d0b065fd-904f-4676-97d6-44355c8075bb'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Gran Canaria</td>
      <td>Gran Canaria Beach Life Express : l’île du soleil</td>
      <td>Espagne</td>
      <td>599,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-01</td>
      <td>https://www.weroad.fr/destinations/gran-canaria-express-ile-soleil/9f57e3fc-c9ae-44d0-9483-f13ecadbfb94</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/gran-canaria-express-ile-soleil/9f57e3fc-c9ae-44d0-9483-f13ecadbfb94'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>France</td>
      <td>Méditerranée Beach Life Express : Montpellier, Sète et Camargue</td>
      <td>France</td>
      <td>599,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-30</td>
      <td>https://www.weroad.fr/destinations/mediterranee-express-montpellier-sete-camargue/dc5c957d-9752-4248-bdcd-e0df79513b15</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/mediterranee-express-montpellier-sete-camargue/dc5c957d-9752-4248-bdcd-e0df79513b15'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Portugal</td>
      <td>Portugal Express</td>
      <td>Portugal</td>
      <td>699,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-10-04</td>
      <td>https://www.weroad.fr/destinations/portugal-express/4fac448c-b7e1-4c52-9265-632cf8912065</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/portugal-express/4fac448c-b7e1-4c52-9265-632cf8912065'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Tunisie</td>
      <td>Tunisie Express : Djerba, Un mélange de détente et cultures.</td>
      <td>Tunisie</td>
      <td>789,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-15</td>
      <td>https://www.weroad.fr/destinations/tunisie-express-djerba-detente-culture/a36141f8-fe71-4213-9468-4434f3e031b6</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/tunisie-express-djerba-detente-culture/a36141f8-fe71-4213-9468-4434f3e031b6'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Écosse</td>
      <td>Écosse Express : Édimbourg et les Highlands comme un local</td>
      <td>Royaume-Uni</td>
      <td>849,00 €</td>
      <td>5.6%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-08</td>
      <td>https://www.weroad.fr/destinations/Ecosse-express-edimbourg-highlands/f9928125-64ec-4fbb-aa0f-d830fc9f913c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/Ecosse-express-edimbourg-highlands/f9928125-64ec-4fbb-aa0f-d830fc9f913c'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Tchéquie</td>
      <td>Europe centrale : Prague, Vienne et Budapest en train</td>
      <td>Tchéquie</td>
      <td>849,00 €</td>
      <td>5.6%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-11</td>
      <td>https://www.weroad.fr/destinations/europe-prague-vienne-budapest-weroadx/ee1e9275-45f4-4120-a2b4-0dedbe5d3d65</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/europe-prague-vienne-budapest-weroadx/ee1e9275-45f4-4120-a2b4-0dedbe5d3d65'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>France</td>
      <td>Châteaux de la Loire Express : entre Blois, Amboise et Tours</td>
      <td>France</td>
      <td>899,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-10-18</td>
      <td>https://www.weroad.fr/destinations/chateaux-loire-express-blois-amboise-tours/7e1b847d-3a09-4e7a-b59d-fd565fa3f764</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/chateaux-loire-express-blois-amboise-tours/7e1b847d-3a09-4e7a-b59d-fd565fa3f764'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Pays Baltes</td>
      <td>Pays Baltes : Tallinn, Riga et Vilnius</td>
      <td>Estonie</td>
      <td>899,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-25</td>
      <td>https://www.weroad.fr/destinations/pays-baltes-tallinn-riga-vilnius/4233778c-476f-4887-8f15-6c0bcda166ca</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/pays-baltes-tallinn-riga-vilnius/4233778c-476f-4887-8f15-6c0bcda166ca'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Suisse</td>
      <td>Suisse Express : aventure en train au coeur des Alpes entre lacs et montagnes</td>
      <td>Suisse</td>
      <td>949,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-22</td>
      <td>https://www.weroad.fr/destinations/suisse-express-alpes-lacs-montagnes/28df726d-d517-4b7c-8072-a9c1ff638411</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/suisse-express-alpes-lacs-montagnes/28df726d-d517-4b7c-8072-a9c1ff638411'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Crète</td>
      <td>Crète Beach Life</td>
      <td>Grèce</td>
      <td>999,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-25</td>
      <td>https://www.weroad.fr/destinations/crete-beach-life/02afa47c-512f-4310-afd1-26407a5449a1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/crete-beach-life/02afa47c-512f-4310-afd1-26407a5449a1'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Népal</td>
      <td>Népal 360° : entre les temples de Katmandou et les sommets de l'Annapurna</td>
      <td>Népal</td>
      <td>999,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-10-27</td>
      <td>https://www.weroad.fr/destinations/nepal/178e3708-674a-4eee-b56b-6cbdde73a7f7</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/nepal/178e3708-674a-4eee-b56b-6cbdde73a7f7'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Inde</td>
      <td>Inde : du Rajasthan au Taj Mahal</td>
      <td>Inde</td>
      <td>999,00 €</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-10-12</td>
      <td>https://www.weroad.fr/destinations/inde-rajasthan-taj-mahal/e39b83ce-32a1-4f98-8d35-e6437f87c7c1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/inde-rajasthan-taj-mahal/e39b83ce-32a1-4f98-8d35-e6437f87c7c1'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Maroc</td>
      <td>Maroc Surf : Entre océan et désert à Agadir</td>
      <td>Maroc</td>
      <td>1 099,00 €</td>
      <td>12.0%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-10-04</td>
      <td>https://www.weroad.fr/destinations/maroc-surf-ocean-desert/665e3872-06c6-4ca7-b2c6-b2c127e42410</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maroc-surf-ocean-desert/665e3872-06c6-4ca7-b2c6-b2c127e42410'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Espagne</td>
      <td>Ibiza et Formentera Beach Life : aventure aux Baléares</td>
      <td>Espagne</td>
      <td>1 099,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-10-26</td>
      <td>https://www.weroad.fr/destinations/ibiza-formentera-baleares/aad9bc1e-d226-4d9c-a410-411aeed2da89</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/ibiza-formentera-baleares/aad9bc1e-d226-4d9c-a410-411aeed2da89'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Sicile</td>
      <td>Sicile Beach Life : de Palerme À San Vito entre mer et temples</td>
      <td>Italie</td>
      <td>1 199,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-04</td>
      <td>https://www.weroad.fr/destinations/sicile-palerme-san-vito/52eddb48-7798-4b5c-8798-3fc4656441e9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/sicile-palerme-san-vito/52eddb48-7798-4b5c-8798-3fc4656441e9'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Hongrie</td>
      <td>Budapest Express</td>
      <td>Hongrie</td>
      <td>599,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-07</td>
      <td>https://www.weroad.fr/destinations/budapest-express/997c4112-821d-42d3-8295-05400366e503</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/budapest-express/997c4112-821d-42d3-8295-05400366e503'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>France</td>
      <td>Paris & Disneyland Express: entre culture, évasion et magie</td>
      <td>France</td>
      <td>699,00 €</td>
      <td>12.5%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-07</td>
      <td>https://www.weroad.fr/destinations/paris-disneyland-express-entre-culture-vasion-et-magie/9c88a53e-1f9b-4f26-946a-ee08ef9172ac</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/paris-disneyland-express-entre-culture-vasion-et-magie/9c88a53e-1f9b-4f26-946a-ee08ef9172ac'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Belgique</td>
      <td>Bruxelles et Amsterdam : Entre culture, saveurs et découverte</td>
      <td>Belgique</td>
      <td>789,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-11</td>
      <td>https://www.weroad.fr/destinations/bruxelles-amsterdam-express-culture/0e2cf4a6-3b15-41d9-aeb9-843c1e541f70</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bruxelles-amsterdam-express-culture/0e2cf4a6-3b15-41d9-aeb9-843c1e541f70'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>France</td>
      <td>Alpe d'Huez Express : ski et snowboard dans les Alpes françaises</td>
      <td>France</td>
      <td>799,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-26</td>
      <td>https://www.weroad.fr/destinations/alpe-d-huez-express-ski-snowboard/8c28b30f-0cc3-459c-8914-238125bdb537</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/alpe-d-huez-express-ski-snowboard/8c28b30f-0cc3-459c-8914-238125bdb537'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Autriche</td>
      <td>Autriche Ski & Snowboard Express : neige et sport à Kitzbühel</td>
      <td>Autriche</td>
      <td>799,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-26</td>
      <td>https://www.weroad.fr/destinations/autriche-kitzbuhel-ski-snowboard/0b5412fb-f73d-421d-9976-c29ec0aa81a0</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/autriche-kitzbuhel-ski-snowboard/0b5412fb-f73d-421d-9976-c29ec0aa81a0'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Italie</td>
      <td>Italie Ski & Snowboard Express : les montagnes de Sestrières dans les Alpes</td>
      <td>Italie</td>
      <td>799,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-26</td>
      <td>https://www.weroad.fr/destinations/sestrieres-italie-ski-snowboard/d1280ff0-9371-4d62-bd54-f50a6526b313</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/sestrieres-italie-ski-snowboard/d1280ff0-9371-4d62-bd54-f50a6526b313'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Indonésie</td>
      <td>Bali et Gili : ambiance tropicale et eau turquoise</td>
      <td>Indonésie</td>
      <td>889,00 €</td>
      <td>6.3%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-21</td>
      <td>https://www.weroad.fr/destinations/bali-gili-indonesie-tropicale-eau-turquoise/cf7b2440-b096-49db-93bc-a63d02147298</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bali-gili-indonesie-tropicale-eau-turquoise/cf7b2440-b096-49db-93bc-a63d02147298'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Autriche</td>
      <td>Autriche Ski & Snowboard Express : sport et détente à Sölden</td>
      <td>Autriche</td>
      <td>899,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-26</td>
      <td>https://www.weroad.fr/destinations/autriche-solden-ski-snowboard/38faed8a-ee1c-477d-b49d-678b7d88bee5</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/autriche-solden-ski-snowboard/38faed8a-ee1c-477d-b49d-678b7d88bee5'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Istanbul & Cappadoce</td>
      <td>Turquie : un voyage d'Istanbul à la Cappadoce</td>
      <td>Turquie</td>
      <td>999,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-16</td>
      <td>https://www.weroad.fr/destinations/istanbul-cappadoce/295a0250-7839-4f8b-9e28-a52e6de7a8a3</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/istanbul-cappadoce/295a0250-7839-4f8b-9e28-a52e6de7a8a3'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Sri Lanka</td>
      <td>Sri Lanka 360° Winter</td>
      <td>Sri Lanka</td>
      <td>1 099,00 €</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-28</td>
      <td>https://www.weroad.fr/destinations/sri-lanka-360-hiver/70ff426d-905e-4e91-99e1-f5bfffe14768</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/sri-lanka-360-hiver/70ff426d-905e-4e91-99e1-f5bfffe14768'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Oman</td>
      <td>Oman 360°</td>
      <td>Oman</td>
      <td>1 149,00 €</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-07</td>
      <td>https://www.weroad.fr/destinations/oman/77ce635f-0502-479d-afc6-6b51f8f4d033</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/oman/77ce635f-0502-479d-afc6-6b51f8f4d033'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Jordanie</td>
      <td>Jordanie Trekking</td>
      <td>Jordanie</td>
      <td>1 249,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-15</td>
      <td>https://www.weroad.fr/destinations/jordanie-trekking/08ab2340-2115-4c98-8b7a-c18643dfad8d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/jordanie-trekking/08ab2340-2115-4c98-8b7a-c18643dfad8d'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Inde</td>
      <td>Inde 360° : Rajasthan, Agra et Varanasi</td>
      <td>Inde</td>
      <td>1 299,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-16</td>
      <td>https://www.weroad.fr/destinations/inde-rajasthan-agra-varanasi/c0470ad0-6f49-4d15-8369-feaadee1710c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/inde-rajasthan-agra-varanasi/c0470ad0-6f49-4d15-8369-feaadee1710c'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Indonésie</td>
      <td>Indonésie 360° : Java, Bali et Gili</td>
      <td>Indonésie</td>
      <td>1 349,00 €</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-15</td>
      <td>https://www.weroad.fr/destinations/indonesie-360/0c2b49fa-d541-43a4-9c97-8a4ad1f8af3b</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/indonesie-360/0c2b49fa-d541-43a4-9c97-8a4ad1f8af3b'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Islande</td>
      <td>Islande : à la poursuite des aurores boréales</td>
      <td>Islande</td>
      <td>1 449,00 €</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-14</td>
      <td>https://www.weroad.fr/destinations/islande-aurores-boreales/4c76cd50-42c1-42e0-81c7-9eba938eee99</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/islande-aurores-boreales/4c76cd50-42c1-42e0-81c7-9eba938eee99'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Égypte</td>
      <td>Egypte Express: Le Caire et les Pyramides</td>
      <td>Égypte</td>
      <td>499,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-05</td>
      <td>https://www.weroad.fr/destinations/le-caire-express-egypt/bfe5c5e8-2c20-4761-9093-e5941d18325c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/le-caire-express-egypt/bfe5c5e8-2c20-4761-9093-e5941d18325c'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Bourgogne</td>
      <td>Bourgogne Express : sur la route des Grands Crus</td>
      <td>France</td>
      <td>599,00 €</td>
      <td>7.7%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-03</td>
      <td>https://www.weroad.fr/destinations/bourgogne-express-route-grand-crus/a7cdffcd-8b37-4239-b0c0-4fca95ebb9b4</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bourgogne-express-route-grand-crus/a7cdffcd-8b37-4239-b0c0-4fca95ebb9b4'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Allemagne</td>
      <td>Berlin Express</td>
      <td>Allemagne</td>
      <td>599,00 €</td>
      <td>14.3%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-18</td>
      <td>https://www.weroad.fr/destinations/allemagne-berlin-express-tour-weroadx/e5d6c677-81fc-44be-abbf-d9589f0ebf6d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/allemagne-berlin-express-tour-weroadx/e5d6c677-81fc-44be-abbf-d9589f0ebf6d'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Géorgie</td>
      <td>Georgie Ski & Snowboard Express : dans les montagnes du Caucase</td>
      <td>Géorgie</td>
      <td>899,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-28</td>
      <td>https://www.weroad.fr/destinations/georgie-caucase-ski-snowboard/bacb86c1-cfdb-4691-893b-593ddd94b1a9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/georgie-caucase-ski-snowboard/bacb86c1-cfdb-4691-893b-593ddd94b1a9'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Hungary</td>
      <td>Prague, Vienne et Budapest : édition Marchés de Noël</td>
      <td>Hongrie</td>
      <td>949,00 €</td>
      <td>5.0%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-06</td>
      <td>https://www.weroad.fr/destinations/prague-budapest-marches-noel-weroadx/3cce12b1-62f4-49ef-9931-4dced2893755</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/prague-budapest-marches-noel-weroadx/3cce12b1-62f4-49ef-9931-4dced2893755'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Îles Canaries</td>
      <td>Fuerteventura et Lanzarote  360° : entre plages et volcans</td>
      <td>Espagne</td>
      <td>999,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-28</td>
      <td>https://www.weroad.fr/destinations/fuerteventura-lanzarote-plages-volcans/433a927c-fec3-4f68-be9c-45e2b5cfcfcb</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/fuerteventura-lanzarote-plages-volcans/433a927c-fec3-4f68-be9c-45e2b5cfcfcb'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Kirghizistan</td>
      <td>Kirghizistan Winter : entre lacs gelés et culture nomade</td>
      <td>Kirghizistan</td>
      <td>1 049,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-28</td>
      <td>https://www.weroad.fr/destinations/kirghizistan-winter/8fd3b586-dd7b-4f85-837d-64830c233a1c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kirghizistan-winter/8fd3b586-dd7b-4f85-837d-64830c233a1c'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Réunion</td>
      <td>L'île de La Réunion : entre cirques, volcan et plages</td>
      <td>Réunion</td>
      <td>1 390,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-15</td>
      <td>https://www.weroad.fr/destinations/ile-reunion-cirques-volcan-plages/1d152290-dbfc-413e-baee-48ddcd2a4ffb</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/ile-reunion-cirques-volcan-plages/1d152290-dbfc-413e-baee-48ddcd2a4ffb'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Norvège</td>
      <td>Norvège : chasse aux aurores boréales aux îles Lofoten</td>
      <td>Norvège</td>
      <td>1 449,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-29</td>
      <td>https://www.weroad.fr/destinations/norvege-lofoten-aurore-boreales/0f479dd1-e9b6-40ec-9576-8eed660fa474</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/norvege-lofoten-aurore-boreales/0f479dd1-e9b6-40ec-9576-8eed660fa474'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Suède</td>
      <td>Laponie suédoise : chasse aux aurores boréales à Luleå</td>
      <td>Suède</td>
      <td>1 549,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-30</td>
      <td>https://www.weroad.fr/destinations/suede-lulea-laponie/914ba73f-ceab-4cd8-92f4-f966f0ed37db</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/suede-lulea-laponie/914ba73f-ceab-4cd8-92f4-f966f0ed37db'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Panamá</td>
      <td>Panama Beach Life : d’îles en îles des San Blas à Bocas del Toro</td>
      <td>Panamá</td>
      <td>1 566,00 €</td>
      <td>5.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-26</td>
      <td>https://www.weroad.fr/destinations/panama-beach-life-san-blas-bocas-del-toro/ca12031b-f919-40f6-b4e4-6c93e8c50516</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/panama-beach-life-san-blas-bocas-del-toro/ca12031b-f919-40f6-b4e4-6c93e8c50516'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Philippines</td>
      <td>Philippines 360° : Bohol, Coron & Palawan</td>
      <td>Philippines</td>
      <td>2 099,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-02</td>
      <td>https://www.weroad.fr/destinations/philippines-360/24433f78-1729-4032-a40b-c8310e85563c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/philippines-360/24433f78-1729-4032-a40b-c8310e85563c'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Tanzanie</td>
      <td>Kilimandjaro Expedition: Lemosho route and Safari</td>
      <td>Tanzanie</td>
      <td>3 499,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-26</td>
      <td>https://www.weroad.fr/destinations/kilimandjaro-trekking-lemosho-route-safari/2cf26f9c-b039-4e59-939c-4666e92acd44</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kilimandjaro-trekking-lemosho-route-safari/2cf26f9c-b039-4e59-939c-4666e92acd44'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Vietnam</td>
      <td>Vietnam 360° Backpack : de Hanoï à Hô Chi Minh</td>
      <td>Viêt Nam</td>
      <td>1 049,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-01-23</td>
      <td>https://www.weroad.fr/destinations/vietnam-backpack/693c19b0-7e1c-475f-8aeb-2a4039833bf8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/vietnam-backpack/693c19b0-7e1c-475f-8aeb-2a4039833bf8'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Nicaragua</td>
      <td>Nicaragua 360° : aventure au pays des lacs et des volcans</td>
      <td>Nicaragua</td>
      <td>1 429,00 €</td>
      <td>13.3%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-01-20</td>
      <td>https://www.weroad.fr/destinations/nicaragua-aventure-lacs-volcans/6581d368-826f-46c2-a893-664aa3666c3f</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/nicaragua-aventure-lacs-volcans/6581d368-826f-46c2-a893-664aa3666c3f'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Finlande</td>
      <td>Laponie finlandaise : à la recherche des aurores boréales</td>
      <td>Finlande</td>
      <td>1 549,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-01-23</td>
      <td>https://www.weroad.fr/destinations/laponie-finlandaise/3197a02f-7b14-4dea-8e82-acdb48bae7da</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/laponie-finlandaise/3197a02f-7b14-4dea-8e82-acdb48bae7da'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Argentine</td>
      <td>Argentine et Brésil : une aventure sud-américaine authentique</td>
      <td>Argentine</td>
      <td>1 899,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-01-24</td>
      <td>https://www.weroad.fr/destinations/argentine-bresil-360/c40313b7-250c-4aaa-a9ec-cf5155b39a03</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/argentine-bresil-360/c40313b7-250c-4aaa-a9ec-cf5155b39a03'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Italie</td>
      <td>Italie : Carnaval de Venise : Masques, féérie & aperitivo</td>
      <td>Italie</td>
      <td>949,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-02-12</td>
      <td>https://www.weroad.fr/destinations/italie-carnaval-venise-masques-aperitivo/9d104808-b7d6-4ebe-b63a-6338d095d374</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/italie-carnaval-venise-masques-aperitivo/9d104808-b7d6-4ebe-b63a-6338d095d374'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Irlande</td>
      <td>Irlande Express : Dublin, Galway et au Connemara</td>
      <td>Irlande</td>
      <td>999,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-02-03</td>
      <td>https://www.weroad.fr/destinations/irlande-express-tour-dublin-galway-connemara-weroadx/a5843663-f32e-4882-ab04-d8f741753d22</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/irlande-express-tour-dublin-galway-connemara-weroadx/a5843663-f32e-4882-ab04-d8f741753d22'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Ouzbékistan</td>
      <td>Ouzbékistan 360° Winter</td>
      <td>Ouzbékistan</td>
      <td>1 149,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-02-23</td>
      <td>https://www.weroad.fr/destinations/ouzbekistan-hiver/ec6387ab-c26c-4658-b57f-53d8c609906e</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/ouzbekistan-hiver/ec6387ab-c26c-4658-b57f-53d8c609906e'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Maldives</td>
      <td>Maldives Beach Life BackPack : snorkeling et détente à Maafushi</td>
      <td>Maldives</td>
      <td>1 179,00 €</td>
      <td>5.6%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-02-22</td>
      <td>https://www.weroad.fr/destinations/maldives-beach-life-detente-snorkeling-maafushi/15a96831-47c3-478e-9183-c6619e40cb18</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maldives-beach-life-detente-snorkeling-maafushi/15a96831-47c3-478e-9183-c6619e40cb18'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Thaïlande</td>
      <td>Thaïlande Backpack Winter : Bangkok, Krabi et les îles Phi Phi</td>
      <td>Thaïlande</td>
      <td>1 249,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-02-07</td>
      <td>https://www.weroad.fr/destinations/thailande-hiver-expedition/febe99be-1ee6-4b6a-b673-1a81e33cec47</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/thailande-hiver-expedition/febe99be-1ee6-4b6a-b673-1a81e33cec47'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Japon</td>
      <td>Japon ski & snowboard : de Tokyo aux montagnes de Nagano</td>
      <td>Japon</td>
      <td>2 099,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-02-22</td>
      <td>https://www.weroad.fr/destinations/japon-ski-snowboard/5f816e11-0b35-400b-95f1-0925692dc2f0</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/japon-ski-snowboard/5f816e11-0b35-400b-95f1-0925692dc2f0'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Brésil</td>
      <td>Brésil : Double Carnaval à Rio & Salvador, Fiesta & plages</td>
      <td>Brésil</td>
      <td>2 929,00 €</td>
      <td>5.2%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-02-11</td>
      <td>https://www.weroad.fr/destinations/bresil-carnaval-rio-salvador-fiesta-plages/9fa3f4b0-0b21-45fb-9fbb-de6e846e1247</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bresil-carnaval-rio-salvador-fiesta-plages/9fa3f4b0-0b21-45fb-9fbb-de6e846e1247'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Islande</td>
      <td>Islande Express : un aperçu de l'île de glace et de feu</td>
      <td>Islande</td>
      <td>899,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-03-11</td>
      <td>https://www.weroad.fr/destinations/islande-express/d898ced6-2b42-4c17-b767-4a831b07989c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/islande-express/d898ced6-2b42-4c17-b767-4a831b07989c'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Thaïlande</td>
      <td>Thaïlande Beach Life Winter : Phuket, Krabi et Koh Lanta</td>
      <td>Thaïlande</td>
      <td>999,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-03-10</td>
      <td>https://www.weroad.fr/destinations/thailande-plage-hiver/43ad04b5-307e-4067-aeb3-b0f66415d4ad</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/thailande-plage-hiver/43ad04b5-307e-4067-aeb3-b0f66415d4ad'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Malaisie</td>
      <td>Malaisie : nature sauvage et îles paradisiaques</td>
      <td>Malaisie</td>
      <td>1 105,00 €</td>
      <td>14.9%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-03-29</td>
      <td>https://www.weroad.fr/destinations/malaisie-nature-ile/c37b0913-06fc-4049-8953-3b73e3430880</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/malaisie-nature-ile/c37b0913-06fc-4049-8953-3b73e3430880'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Maldives</td>
      <td>Maldives Beach Life : aventure et découverte locale à Dharavandhoo</td>
      <td>Maldives</td>
      <td>1 299,00 €</td>
      <td>7.1%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-03-22</td>
      <td>https://www.weroad.fr/destinations/maldives-tour-plages-paradisiaques-dauphins-weroadx/7367ecaf-276d-4474-bba2-dd45a27b54b3</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maldives-tour-plages-paradisiaques-dauphins-weroadx/7367ecaf-276d-4474-bba2-dd45a27b54b3'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Irlande</td>
      <td>Irlande: Édition la Saint-Patrick</td>
      <td>Irlande</td>
      <td>1 299,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-03-13</td>
      <td>https://www.weroad.fr/destinations/irlande-tour-saint-patrick/db8c4b49-3180-41dd-af15-28a720c78422</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/irlande-tour-saint-patrick/db8c4b49-3180-41dd-af15-28a720c78422'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Turquie</td>
      <td>Turquie 360° : Istanbul, Cappadoce et Éphèse</td>
      <td>Turquie</td>
      <td>1 349,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-03-21</td>
      <td>https://www.weroad.fr/destinations/turquie-istanbul-cappadoce-ephese/a587c038-116a-4db7-9945-9a45e50c9ead</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/turquie-istanbul-cappadoce-ephese/a587c038-116a-4db7-9945-9a45e50c9ead'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Mexique</td>
      <td>Mexique Beach Life : de Cancun à Isla Mujeres, plage et détente</td>
      <td>Mexique</td>
      <td>1 399,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-03-03</td>
      <td>https://www.weroad.fr/destinations/mexique-yucatan-beach-life/cfcca156-1834-4bd3-83ae-e3c429ab3ee2</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/mexique-yucatan-beach-life/cfcca156-1834-4bd3-83ae-e3c429ab3ee2'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Thaïlande</td>
      <td>Thaïlande 360° Winter : Bangkok, Chiang Mai et les îles Phi Phi</td>
      <td>Thaïlande</td>
      <td>1 699,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-03-08</td>
      <td>https://www.weroad.fr/destinations/thailande-360-hiver/87f91532-4322-4edc-8af6-7545b5ee4f37</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/thailande-360-hiver/87f91532-4322-4edc-8af6-7545b5ee4f37'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Cambodge</td>
      <td>Laos et Cambodge : Sur les routes des temples d’Indochine</td>
      <td>Cambodge</td>
      <td>1 900,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-03-20</td>
      <td>https://www.weroad.fr/destinations/laos-cambodge-routes-temples-indochine/3a3d0763-6567-4060-b7cc-eb9ab1b3c06d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/laos-cambodge-routes-temples-indochine/3a3d0763-6567-4060-b7cc-eb9ab1b3c06d'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Albanie</td>
      <td>Albanie Express Winter : histoire, nature et aventure</td>
      <td>Albanie</td>
      <td>549,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-04-05</td>
      <td>https://www.weroad.fr/destinations/albanie-express-hiver/b480d1d1-d49c-4b3c-939d-b41c7c3aa1a9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/albanie-express-hiver/b480d1d1-d49c-4b3c-939d-b41c7c3aa1a9'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Istanbul</td>
      <td>Istanbul Express</td>
      <td>Turquie</td>
      <td>599,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-04-28</td>
      <td>https://www.weroad.fr/destinations/istanbul-express/3d770660-8db7-4454-b2c0-a6e0b4230788</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/istanbul-express/3d770660-8db7-4454-b2c0-a6e0b4230788'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Guatemala</td>
      <td>Guatemala 360° : Voyage au pays des volcans, nature sauvage et cultures anciennes</td>
      <td>Guatemala</td>
      <td>1 699,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-04-09</td>
      <td>https://www.weroad.fr/destinations/guatemala-volcans-nature-cultures-anciennes/63bb2f26-bd1b-42c0-a675-00df9455154e</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/guatemala-volcans-nature-cultures-anciennes/63bb2f26-bd1b-42c0-a675-00df9455154e'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>États-Unis</td>
      <td>Usa Rock'n Drive : d'Atlanta à la Nouvelle-Orléans en passant par Nashville et Memphis</td>
      <td>États-Unis d'Amérique</td>
      <td>1 699,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-04-24</td>
      <td>https://www.weroad.fr/destinations/usa-rock-n-drive/07449856-21ed-40f5-8a9e-e3806a9c3574</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/usa-rock-n-drive/07449856-21ed-40f5-8a9e-e3806a9c3574'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Chine</td>
      <td>Chine 360° : Pékin, Shanghai et la Grande Muraille</td>
      <td>Chine</td>
      <td>1 899,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-04-18</td>
      <td>https://www.weroad.fr/destinations/chine/b05e8889-941d-4e19-b2b2-7658732fe70a</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/chine/b05e8889-941d-4e19-b2b2-7658732fe70a'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Sénégal</td>
      <td>Sénégal :  Roadtrip entre terre et fleuve</td>
      <td>Sénégal</td>
      <td>2 050,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-04-16</td>
      <td>https://www.weroad.fr/destinations/senegal-entre-terre-et-fleuve/dfd20650-8ed4-4f16-8209-26479258f025</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/senegal-entre-terre-et-fleuve/dfd20650-8ed4-4f16-8209-26479258f025'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>Népal</td>
      <td>Népal Trekking :  de Pokhara au camp de base de l'Annapurna</td>
      <td>Népal</td>
      <td>1 019,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-05-10</td>
      <td>https://www.weroad.fr/destinations/nepal-trekking/f2c8048b-a3c9-417c-a6f9-94099345ed4a</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/nepal-trekking/f2c8048b-a3c9-417c-a6f9-94099345ed4a'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>Portugal</td>
      <td>Açores 360° : au coeur de l'archipel, de São Miguel à Faial et Terceira</td>
      <td>Portugal</td>
      <td>1 699,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-05-01</td>
      <td>https://www.weroad.fr/destinations/acores-sao-miguel-faial-terceira/84b78f91-1db0-4e65-80b6-235d0a1562bf</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/acores-sao-miguel-faial-terceira/84b78f91-1db0-4e65-80b6-235d0a1562bf'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>Namibie</td>
      <td>Namibie 360°</td>
      <td>Namibie</td>
      <td>2 299,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-05-03</td>
      <td>https://www.weroad.fr/destinations/namibie/f8882a9a-fd70-466d-8dc9-f0f6ce0838ae</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/namibie/f8882a9a-fd70-466d-8dc9-f0f6ce0838ae'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>Bordeaux</td>
      <td>Bordeaux Express : de la Dune du Pilat à la pointe du Cap-Ferret</td>
      <td>France</td>
      <td>899,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-06-27</td>
      <td>https://www.weroad.fr/destinations/bordeaux-dune-du-pilat/b202dfa7-62bd-4a24-a4d1-cf7eafb1d031</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bordeaux-dune-du-pilat/b202dfa7-62bd-4a24-a4d1-cf7eafb1d031'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>Normandie</td>
      <td>Normandie 360° : Châteaux, Falaises et Mont Saint-Michel</td>
      <td>France</td>
      <td>999,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-06-19</td>
      <td>https://www.weroad.fr/destinations/normandie-360-mont-saint-michel/0bd9b86b-5e44-4a90-8fb3-0156567fe1d9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/normandie-360-mont-saint-michel/0bd9b86b-5e44-4a90-8fb3-0156567fe1d9'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>Thaïlande</td>
      <td>Thaïlande Beach Life Summer : de Bangkok à Koh Tao et Koh Samui</td>
      <td>Thaïlande</td>
      <td>1 199,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-06-21</td>
      <td>https://www.weroad.fr/destinations/thailande-ete-expedition/3fc78f4a-d22d-4465-9f15-e20c98932305</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/thailande-ete-expedition/3fc78f4a-d22d-4465-9f15-e20c98932305'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-07</td>
      <td>Auvergne</td>
      <td>Auvergne Express : à la découverte du Sancy</td>
      <td>France</td>
      <td>549,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-07-28</td>
      <td>https://www.weroad.fr/destinations/auvergne-express/d7f1381f-4b84-4268-a52f-699c450ca721</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/auvergne-express/d7f1381f-4b84-4268-a52f-699c450ca721'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-07</td>
      <td>Espagne</td>
      <td>Fuerteventura Surf : aventure à la découverte de l'île</td>
      <td>Espagne</td>
      <td>999,00 €</td>
      <td>9.1%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-07-25</td>
      <td>https://www.weroad.fr/destinations/fuerteventura-surf-weroadx/317f930c-e5c9-4fe2-8ff8-f8731e8196ab</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/fuerteventura-surf-weroadx/317f930c-e5c9-4fe2-8ff8-f8731e8196ab'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-08</td>
      <td>Bretagne</td>
      <td>Bretagne Sud Beach Life : Quiberon et Belle-île-en-Mer</td>
      <td>France</td>
      <td>679,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-08-08</td>
      <td>https://www.weroad.fr/destinations/bretagne-quiberon-belle-ile/02a71e36-0af9-4567-9cf2-238b0da67e7f</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bretagne-quiberon-belle-ile/02a71e36-0af9-4567-9cf2-238b0da67e7f'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-08</td>
      <td>Kirghizistan</td>
      <td>Kirghizistan Actif : chevaux, yourtes et rando</td>
      <td>Kirghizistan</td>
      <td>1 490,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-08-28</td>
      <td>https://www.weroad.fr/destinations/kirghizistan-actif-trekking-chevaux-weroadx/d436331b-8e23-4bde-92cc-d3aeefe79952</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kirghizistan-actif-trekking-chevaux-weroadx/d436331b-8e23-4bde-92cc-d3aeefe79952'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-11</td>
      <td>Costa Rica</td>
      <td>Costa Rica 360° : pura vida parmi les forêts tropicales</td>
      <td>Costa Rica</td>
      <td>1 799,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-11-22</td>
      <td>https://www.weroad.fr/destinations/costa-rica-360/885085c8-d0ef-4cbe-a1c0-ad233f9423e5</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/costa-rica-360/885085c8-d0ef-4cbe-a1c0-ad233f9423e5'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-12</td>
      <td>Bulgarie</td>
      <td>Bulgarie Ski Express : Bansko entre pistes, spa et fête !</td>
      <td>Bulgarie</td>
      <td>699,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-12-23</td>
      <td>https://www.weroad.fr/destinations/bulgarie-ski-express-bansko/8832ad88-d827-4684-8b3d-eb733e544d51</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bulgarie-ski-express-bansko/8832ad88-d827-4684-8b3d-eb733e544d51'>🔗</a></td>
    </tr>
  </tbody>
</table>
</div>

---

## Watchlist — départs proches / confirmés
ALMOST / CONFIRMED / GUARANTEED
<div class='table-wrapper'>
<table border="1" class="dataframe rp-table">
  <thead>
    <tr style="text-align: right;">
      <th>sales_status</th>
      <th>best_starting_date</th>
      <th>best_ending_date</th>
      <th>title</th>
      <th>destination_label</th>
      <th>country_name</th>
      <th>price_eur</th>
      <th>discount_pct</th>
      <th>seatsToConfirm</th>
      <th>maxPax</th>
      <th>weroadersCount</th>
      <th>url_precise</th>
      <th>url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-23</td>
      <td>2025-09-30</td>
      <td>Albanie 360° : Tirana et les plages du sud</td>
      <td>Albanie</td>
      <td>Albanie</td>
      <td>639,00 €</td>
      <td>20.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/albanie-tirana-plages-sud/d117ece9-bd9e-494a-bae7-281d52d89619</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/albanie-tirana-plages-sud/d117ece9-bd9e-494a-bae7-281d52d89619'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-27</td>
      <td>2025-10-01</td>
      <td>Maroc : Trekking au Mont Toubkal</td>
      <td>Maroc</td>
      <td>Maroc</td>
      <td>479,00 €</td>
      <td>20.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/maroc-trekking-mount-toubkal/4310fa36-bb29-48fb-856e-359806887f88</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maroc-trekking-mount-toubkal/4310fa36-bb29-48fb-856e-359806887f88'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-01</td>
      <td>2025-10-05</td>
      <td>Gran Canaria Beach Life Express : l’île du soleil</td>
      <td>Gran Canaria</td>
      <td>Espagne</td>
      <td>599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/gran-canaria-express-ile-soleil/9f57e3fc-c9ae-44d0-9483-f13ecadbfb94</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/gran-canaria-express-ile-soleil/9f57e3fc-c9ae-44d0-9483-f13ecadbfb94'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-04</td>
      <td>2025-10-11</td>
      <td>Sicile Beach Life : de Palerme À San Vito entre mer et temples</td>
      <td>Sicile</td>
      <td>Italie</td>
      <td>1 199,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>11.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/sicile-palerme-san-vito/52eddb48-7798-4b5c-8798-3fc4656441e9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/sicile-palerme-san-vito/52eddb48-7798-4b5c-8798-3fc4656441e9'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-08</td>
      <td>2025-10-12</td>
      <td>Écosse Express : Édimbourg et les Highlands comme un local</td>
      <td>Écosse</td>
      <td>Royaume-Uni</td>
      <td>849,00 €</td>
      <td>5.6%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/Ecosse-express-edimbourg-highlands/f9928125-64ec-4fbb-aa0f-d830fc9f913c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/Ecosse-express-edimbourg-highlands/f9928125-64ec-4fbb-aa0f-d830fc9f913c'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-11</td>
      <td>2025-10-17</td>
      <td>Europe centrale : Prague, Vienne et Budapest en train</td>
      <td>Tchéquie</td>
      <td>Tchéquie</td>
      <td>849,00 €</td>
      <td>5.6%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/europe-prague-vienne-budapest-weroadx/ee1e9275-45f4-4120-a2b4-0dedbe5d3d65</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/europe-prague-vienne-budapest-weroadx/ee1e9275-45f4-4120-a2b4-0dedbe5d3d65'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-15</td>
      <td>2025-10-19</td>
      <td>Tunisie Express : Djerba, Un mélange de détente et cultures.</td>
      <td>Tunisie</td>
      <td>Tunisie</td>
      <td>789,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/tunisie-express-djerba-detente-culture/a36141f8-fe71-4213-9468-4434f3e031b6</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/tunisie-express-djerba-detente-culture/a36141f8-fe71-4213-9468-4434f3e031b6'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-17</td>
      <td>2025-10-25</td>
      <td>Belize 360° : jungles luxuriantes, plages paradisiaques et Blue Hole</td>
      <td>Belize</td>
      <td>Belize</td>
      <td>1 499,00 €</td>
      <td>6.3%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/belize-jungles-plages-blue-hole/b1d4305d-a377-46ed-b533-dad5169b092e</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/belize-jungles-plages-blue-hole/b1d4305d-a377-46ed-b533-dad5169b092e'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-17</td>
      <td>2025-10-29</td>
      <td>Colombie Expedition : aventure de l'Amazonie aux Caraïbes de San Andrés</td>
      <td>Colombie</td>
      <td>Colombie</td>
      <td>2 299,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/colombie-aventure-amazonie-caraibes-san-andres/ed317950-357c-45de-8890-43ca8e9f67b5</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/colombie-aventure-amazonie-caraibes-san-andres/ed317950-357c-45de-8890-43ca8e9f67b5'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-18</td>
      <td>2025-10-24</td>
      <td>Turquie on the road: entre Cappadoce et sa riche culture</td>
      <td>Turquie</td>
      <td>Turquie</td>
      <td>1 699,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/turquie-on-the-road/7f33ff07-3755-4f2c-9adc-3b3aa8e131c0</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/turquie-on-the-road/7f33ff07-3755-4f2c-9adc-3b3aa8e131c0'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-19</td>
      <td>2025-10-28</td>
      <td>Kenya : au cœur de l'Afrique entre safaris, plages et villages locaux</td>
      <td>Kenya</td>
      <td>Kenya</td>
      <td>1 789,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/kenya-afrique-safari-plage-village/c38a5ff2-25f2-4033-b1f3-829713cef607</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kenya-afrique-safari-plage-village/c38a5ff2-25f2-4033-b1f3-829713cef607'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-22</td>
      <td>2025-10-26</td>
      <td>Suisse Express : aventure en train au coeur des Alpes entre lacs et montagnes</td>
      <td>Suisse</td>
      <td>Suisse</td>
      <td>949,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/suisse-express-alpes-lacs-montagnes/28df726d-d517-4b7c-8072-a9c1ff638411</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/suisse-express-alpes-lacs-montagnes/28df726d-d517-4b7c-8072-a9c1ff638411'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-25</td>
      <td>2025-11-01</td>
      <td>Pays Baltes : Tallinn, Riga et Vilnius</td>
      <td>Pays Baltes</td>
      <td>Estonie</td>
      <td>899,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/pays-baltes-tallinn-riga-vilnius/4233778c-476f-4887-8f15-6c0bcda166ca</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/pays-baltes-tallinn-riga-vilnius/4233778c-476f-4887-8f15-6c0bcda166ca'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-25</td>
      <td>2025-11-01</td>
      <td>Crète Beach Life</td>
      <td>Crète</td>
      <td>Grèce</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/crete-beach-life/02afa47c-512f-4310-afd1-26407a5449a1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/crete-beach-life/02afa47c-512f-4310-afd1-26407a5449a1'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-25</td>
      <td>2025-11-04</td>
      <td>Équateur & Amazonie Expedition</td>
      <td>Équateur & Amazonie</td>
      <td>Équateur</td>
      <td>1 299,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/equateur-et-amazonie/89e92461-4baa-44bf-b886-18280e75526d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/equateur-et-amazonie/89e92461-4baa-44bf-b886-18280e75526d'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-30</td>
      <td>2025-11-03</td>
      <td>Méditerranée Beach Life Express : Montpellier, Sète et Camargue</td>
      <td>France</td>
      <td>France</td>
      <td>599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/mediterranee-express-montpellier-sete-camargue/dc5c957d-9752-4248-bdcd-e0df79513b15</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/mediterranee-express-montpellier-sete-camargue/dc5c957d-9752-4248-bdcd-e0df79513b15'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-01</td>
      <td>2025-11-12</td>
      <td>Colombie 360° : Bogota, Medellin, Carthagène et parc Tayrona</td>
      <td>Colombie</td>
      <td>Colombie</td>
      <td>2 199,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/colombie-360/c0331d34-29c3-4b21-9ccf-7bdedc3449b5</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/colombie-360/c0331d34-29c3-4b21-9ccf-7bdedc3449b5'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-03</td>
      <td>2025-11-15</td>
      <td>Mexique 360° : à la découverte du Yucatán des Mayas</td>
      <td>Mexique</td>
      <td>Mexique</td>
      <td>1 549,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/mexique-yucatan-maya/42832fc4-b316-4127-a357-aa4e125dfd94</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/mexique-yucatan-maya/42832fc4-b316-4127-a357-aa4e125dfd94'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-07</td>
      <td>2025-11-11</td>
      <td>Paris & Disneyland Express: entre culture, évasion et magie</td>
      <td>France</td>
      <td>France</td>
      <td>699,00 €</td>
      <td>12.5%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/paris-disneyland-express-entre-culture-vasion-et-magie/9c88a53e-1f9b-4f26-946a-ee08ef9172ac</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/paris-disneyland-express-entre-culture-vasion-et-magie/9c88a53e-1f9b-4f26-946a-ee08ef9172ac'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-12</td>
      <td>2025-11-23</td>
      <td>Chine : de Pékin à Hong Kong en passant une nuit inoubliable sur la Grande Muraille</td>
      <td>Chine</td>
      <td>Chine</td>
      <td>1 899,00 €</td>
      <td>9.5%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/chine-pekin-hong-kong-grande-muraille-weroadx/2acbb677-7ac2-46d1-8fff-94f8d833afb3</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/chine-pekin-hong-kong-grande-muraille-weroadx/2acbb677-7ac2-46d1-8fff-94f8d833afb3'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-15</td>
      <td>2025-11-22</td>
      <td>Jordanie Trekking</td>
      <td>Jordanie</td>
      <td>Jordanie</td>
      <td>1 249,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/jordanie-trekking/08ab2340-2115-4c98-8b7a-c18643dfad8d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/jordanie-trekking/08ab2340-2115-4c98-8b7a-c18643dfad8d'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-16</td>
      <td>2025-11-23</td>
      <td>Turquie : un voyage d'Istanbul à la Cappadoce</td>
      <td>Istanbul & Cappadoce</td>
      <td>Turquie</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/istanbul-cappadoce/295a0250-7839-4f8b-9e28-a52e6de7a8a3</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/istanbul-cappadoce/295a0250-7839-4f8b-9e28-a52e6de7a8a3'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-17</td>
      <td>2025-11-30</td>
      <td>Mexique 360° : Mexico, Oaxaca, Chiapas et le Yucatan</td>
      <td>Mexique</td>
      <td>Mexique</td>
      <td>1 599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/mexique-360/91ae642f-ad03-4066-b721-1ee4eda5e3b2</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/mexique-360/91ae642f-ad03-4066-b721-1ee4eda5e3b2'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-24</td>
      <td>2025-12-06</td>
      <td>Patagonie Trekking : aventure à travers l’Argentine et le Chili</td>
      <td>Patagonie</td>
      <td>Argentine</td>
      <td>2 999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/patagonie-360/4d4d6956-9089-4a57-8988-9869cccc3a40</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/patagonie-360/4d4d6956-9089-4a57-8988-9869cccc3a40'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-15</td>
      <td>2025-12-22</td>
      <td>L'île de La Réunion : entre cirques, volcan et plages</td>
      <td>Réunion</td>
      <td>Réunion</td>
      <td>1 390,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/ile-reunion-cirques-volcan-plages/1d152290-dbfc-413e-baee-48ddcd2a4ffb</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/ile-reunion-cirques-volcan-plages/1d152290-dbfc-413e-baee-48ddcd2a4ffb'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-26</td>
      <td>2026-01-05</td>
      <td>Kilimandjaro Expedition: Lemosho route and Safari</td>
      <td>Tanzanie</td>
      <td>Tanzanie</td>
      <td>3 499,00 €</td>
      <td></td>
      <td>2.0</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/kilimandjaro-trekking-lemosho-route-safari/2cf26f9c-b039-4e59-939c-4666e92acd44</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kilimandjaro-trekking-lemosho-route-safari/2cf26f9c-b039-4e59-939c-4666e92acd44'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-26</td>
      <td>2026-01-04</td>
      <td>Panama Beach Life : d’îles en îles des San Blas à Bocas del Toro</td>
      <td>Panamá</td>
      <td>Panamá</td>
      <td>1 566,00 €</td>
      <td>5.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/panama-beach-life-san-blas-bocas-del-toro/ca12031b-f919-40f6-b4e4-6c93e8c50516</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/panama-beach-life-san-blas-bocas-del-toro/ca12031b-f919-40f6-b4e4-6c93e8c50516'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-29</td>
      <td>2026-01-04</td>
      <td>Norvège : chasse aux aurores boréales aux îles Lofoten</td>
      <td>Norvège</td>
      <td>Norvège</td>
      <td>1 449,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/norvege-lofoten-aurore-boreales/0f479dd1-e9b6-40ec-9576-8eed660fa474</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/norvege-lofoten-aurore-boreales/0f479dd1-e9b6-40ec-9576-8eed660fa474'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-01-20</td>
      <td>2026-01-31</td>
      <td>Nicaragua 360° : aventure au pays des lacs et des volcans</td>
      <td>Nicaragua</td>
      <td>Nicaragua</td>
      <td>1 429,00 €</td>
      <td>13.3%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/nicaragua-aventure-lacs-volcans/6581d368-826f-46c2-a893-664aa3666c3f</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/nicaragua-aventure-lacs-volcans/6581d368-826f-46c2-a893-664aa3666c3f'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-01-23</td>
      <td>2026-02-01</td>
      <td>Vietnam 360° Backpack : de Hanoï à Hô Chi Minh</td>
      <td>Vietnam</td>
      <td>Viêt Nam</td>
      <td>1 049,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/vietnam-backpack/693c19b0-7e1c-475f-8aeb-2a4039833bf8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/vietnam-backpack/693c19b0-7e1c-475f-8aeb-2a4039833bf8'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-02-11</td>
      <td>2026-02-19</td>
      <td>Brésil : Double Carnaval à Rio & Salvador, Fiesta & plages</td>
      <td>Brésil</td>
      <td>Brésil</td>
      <td>2 929,00 €</td>
      <td>5.2%</td>
      <td>1.0</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/bresil-carnaval-rio-salvador-fiesta-plages/9fa3f4b0-0b21-45fb-9fbb-de6e846e1247</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bresil-carnaval-rio-salvador-fiesta-plages/9fa3f4b0-0b21-45fb-9fbb-de6e846e1247'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-02-12</td>
      <td>2026-02-16</td>
      <td>Italie : Carnaval de Venise : Masques, féérie & aperitivo</td>
      <td>Italie</td>
      <td>Italie</td>
      <td>949,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/italie-carnaval-venise-masques-aperitivo/9d104808-b7d6-4ebe-b63a-6338d095d374</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/italie-carnaval-venise-masques-aperitivo/9d104808-b7d6-4ebe-b63a-6338d095d374'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-02-22</td>
      <td>2026-03-01</td>
      <td>Maldives Beach Life BackPack : snorkeling et détente à Maafushi</td>
      <td>Maldives</td>
      <td>Maldives</td>
      <td>1 179,00 €</td>
      <td>5.6%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/maldives-beach-life-detente-snorkeling-maafushi/15a96831-47c3-478e-9183-c6619e40cb18</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maldives-beach-life-detente-snorkeling-maafushi/15a96831-47c3-478e-9183-c6619e40cb18'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-03-03</td>
      <td>2026-03-10</td>
      <td>Mexique Beach Life : de Cancun à Isla Mujeres, plage et détente</td>
      <td>Mexique</td>
      <td>Mexique</td>
      <td>1 399,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/mexique-yucatan-beach-life/cfcca156-1834-4bd3-83ae-e3c429ab3ee2</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/mexique-yucatan-beach-life/cfcca156-1834-4bd3-83ae-e3c429ab3ee2'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-03-20</td>
      <td>2026-03-31</td>
      <td>Laos et Cambodge : Sur les routes des temples d’Indochine</td>
      <td>Cambodge</td>
      <td>Cambodge</td>
      <td>1 900,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/laos-cambodge-routes-temples-indochine/3a3d0763-6567-4060-b7cc-eb9ab1b3c06d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/laos-cambodge-routes-temples-indochine/3a3d0763-6567-4060-b7cc-eb9ab1b3c06d'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-03-29</td>
      <td>2026-04-09</td>
      <td>Malaisie : nature sauvage et îles paradisiaques</td>
      <td>Malaisie</td>
      <td>Malaisie</td>
      <td>1 105,00 €</td>
      <td>14.9%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/malaisie-nature-ile/c37b0913-06fc-4049-8953-3b73e3430880</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/malaisie-nature-ile/c37b0913-06fc-4049-8953-3b73e3430880'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-04-09</td>
      <td>2026-04-20</td>
      <td>Guatemala 360° : Voyage au pays des volcans, nature sauvage et cultures anciennes</td>
      <td>Guatemala</td>
      <td>Guatemala</td>
      <td>1 699,00 €</td>
      <td></td>
      <td>2.0</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/guatemala-volcans-nature-cultures-anciennes/63bb2f26-bd1b-42c0-a675-00df9455154e</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/guatemala-volcans-nature-cultures-anciennes/63bb2f26-bd1b-42c0-a675-00df9455154e'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-04-16</td>
      <td>2026-04-25</td>
      <td>Sénégal :  Roadtrip entre terre et fleuve</td>
      <td>Sénégal</td>
      <td>Sénégal</td>
      <td>2 050,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/senegal-entre-terre-et-fleuve/dfd20650-8ed4-4f16-8209-26479258f025</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/senegal-entre-terre-et-fleuve/dfd20650-8ed4-4f16-8209-26479258f025'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-04-28</td>
      <td>2026-05-02</td>
      <td>Istanbul Express</td>
      <td>Istanbul</td>
      <td>Turquie</td>
      <td>599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/istanbul-express/3d770660-8db7-4454-b2c0-a6e0b4230788</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/istanbul-express/3d770660-8db7-4454-b2c0-a6e0b4230788'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-05-01</td>
      <td>2026-05-11</td>
      <td>Açores 360° : au coeur de l'archipel, de São Miguel à Faial et Terceira</td>
      <td>Portugal</td>
      <td>Portugal</td>
      <td>1 699,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>9.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/acores-sao-miguel-faial-terceira/84b78f91-1db0-4e65-80b6-235d0a1562bf</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/acores-sao-miguel-faial-terceira/84b78f91-1db0-4e65-80b6-235d0a1562bf'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-05-03</td>
      <td>2026-05-13</td>
      <td>Namibie 360°</td>
      <td>Namibie</td>
      <td>Namibie</td>
      <td>2 299,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>13.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/namibie/f8882a9a-fd70-466d-8dc9-f0f6ce0838ae</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/namibie/f8882a9a-fd70-466d-8dc9-f0f6ce0838ae'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-08-28</td>
      <td>2026-09-07</td>
      <td>Kirghizistan Actif : chevaux, yourtes et rando</td>
      <td>Kirghizistan</td>
      <td>Kirghizistan</td>
      <td>1 490,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/kirghizistan-actif-trekking-chevaux-weroadx/d436331b-8e23-4bde-92cc-d3aeefe79952</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kirghizistan-actif-trekking-chevaux-weroadx/d436331b-8e23-4bde-92cc-d3aeefe79952'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-12</td>
      <td>2025-09-19</td>
      <td>Maroc 360° : Marrakech, Fès, Rabat et le désert</td>
      <td>Maroc</td>
      <td>Maroc</td>
      <td>659,00 €</td>
      <td>12.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/maroc-marrakech-fes-rabat-desert/2e17500f-c6fb-4880-949e-390fd175f648</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maroc-marrakech-fes-rabat-desert/2e17500f-c6fb-4880-949e-390fd175f648'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-14</td>
      <td>2025-09-21</td>
      <td>Île Maurice Beach Life : Road trip entre plages paradisiaques et aventure locale</td>
      <td>Maurice</td>
      <td>Maurice</td>
      <td>1 149,00 €</td>
      <td>13.5%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/ile-maurice-beach-life-road-trip-plages-aventure/1e66c621-1836-46e2-abeb-5ffe000ba6c8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/ile-maurice-beach-life-road-trip-plages-aventure/1e66c621-1836-46e2-abeb-5ffe000ba6c8'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-17</td>
      <td>2025-09-21</td>
      <td>Transylvanie Express : Road Trip dans le pays du Comte Dracula</td>
      <td>Romania</td>
      <td>Roumanie</td>
      <td>449,00 €</td>
      <td>10.0%</td>
      <td>NaN</td>
      <td>11.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/transylvanie-express-route-comte-dracula/8a2982d2-c24c-4361-8101-f6a4fbb9e5ef</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/transylvanie-express-route-comte-dracula/8a2982d2-c24c-4361-8101-f6a4fbb9e5ef'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-19</td>
      <td>2025-09-24</td>
      <td>Malte Beach Life Express : Voyage sur les îles de Malte, Gozo et Comino</td>
      <td>Malte</td>
      <td>Malte</td>
      <td>759,00 €</td>
      <td>5.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/malte-express-gozo-comino/562901ce-50c2-426f-9b47-479ea882d372</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/malte-express-gozo-comino/562901ce-50c2-426f-9b47-479ea882d372'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-19</td>
      <td>2025-10-01</td>
      <td>Vietnam 360° : de Hanoï à Hô Chi Minh</td>
      <td>Vietnam</td>
      <td>Viêt Nam</td>
      <td>959,00 €</td>
      <td>20.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/vietnam/a1eb2771-a671-4f45-8838-1bb93cebf42a</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/vietnam/a1eb2771-a671-4f45-8838-1bb93cebf42a'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-20</td>
      <td>2025-10-01</td>
      <td>Cuba 360°: au rythme de la salsa de la Havane à Trinidad</td>
      <td>Cuba</td>
      <td>Cuba</td>
      <td>969,00 €</td>
      <td>11.8%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/cuba-360/f632605e-d0f9-473b-a118-34113dce67c0</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/cuba-360/f632605e-d0f9-473b-a118-34113dce67c0'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-26</td>
      <td>2025-10-06</td>
      <td>Japon 360° : découverte de Tokyo, Kyoto, Hiroshima et Osaka</td>
      <td>Japon</td>
      <td>Japon</td>
      <td>1 499,00 €</td>
      <td>16.7%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/japon-360/a5da9bc1-f6ff-48ee-bd83-c7e58a0752c9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/japon-360/a5da9bc1-f6ff-48ee-bd83-c7e58a0752c9'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-27</td>
      <td>2025-10-04</td>
      <td>Dolomites 360° et Lac de Braies</td>
      <td>Dolomites</td>
      <td>Italie</td>
      <td>919,00 €</td>
      <td>12.4%</td>
      <td>NaN</td>
      <td>7.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/dolomites/cd862058-7484-4ee5-b21b-7152baf7951f</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/dolomites/cd862058-7484-4ee5-b21b-7152baf7951f'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-27</td>
      <td>2025-10-07</td>
      <td>Malaisie : de Kuala Lumpur à Bornéo</td>
      <td>Malaisie</td>
      <td>Malaisie</td>
      <td>1 599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/malaisie-kuala-lumpur-borneo/c9aa87e8-3250-409f-b1dc-a334ddd342ee</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/malaisie-kuala-lumpur-borneo/c9aa87e8-3250-409f-b1dc-a334ddd342ee'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-29</td>
      <td>2025-10-10</td>
      <td>Pérou 360° : Machu Picchu, montagne arc-en-ciel et lac Titicaca</td>
      <td>Pérou</td>
      <td>Pérou</td>
      <td>1 529,00 €</td>
      <td>10.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/perou-360/16c0ac74-1577-4752-b63d-1a081063cbd3</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/perou-360/16c0ac74-1577-4752-b63d-1a081063cbd3'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-30</td>
      <td>2025-10-08</td>
      <td>Maroc 360° : du désert aux villes des mille et une nuits</td>
      <td>Maroc</td>
      <td>Maroc</td>
      <td>699,00 €</td>
      <td>12.5%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/maroc/61788514-5980-4778-8e12-ab4be26e5b60</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maroc/61788514-5980-4778-8e12-ab4be26e5b60'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-10-12</td>
      <td>2025-10-20</td>
      <td>Inde : du Rajasthan au Taj Mahal</td>
      <td>Inde</td>
      <td>Inde</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/inde-rajasthan-taj-mahal/e39b83ce-32a1-4f98-8d35-e6437f87c7c1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/inde-rajasthan-taj-mahal/e39b83ce-32a1-4f98-8d35-e6437f87c7c1'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-10-17</td>
      <td>2025-10-26</td>
      <td>Brésil Beach Life : jungle, mer et amour</td>
      <td>Brésil</td>
      <td>Brésil</td>
      <td>1 599,00 €</td>
      <td>5.9%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/bresil-mer-plage-foret-rio-de-janeiro/8c9a0abb-bb94-41b6-9cd0-ca0ae9490e12</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bresil-mer-plage-foret-rio-de-janeiro/8c9a0abb-bb94-41b6-9cd0-ca0ae9490e12'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-10-18</td>
      <td>2025-11-01</td>
      <td>États-Unis : Road Trip sur la route 66 de Chicago à Los Angeles</td>
      <td>Route 66</td>
      <td>États-Unis d'Amérique</td>
      <td>1 899,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/road-trip-route-66-chicago-los-angeles/9f58586f-b92a-455d-a8e1-d404f1abdb85</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/road-trip-route-66-chicago-los-angeles/9f58586f-b92a-455d-a8e1-d404f1abdb85'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-10-26</td>
      <td>2025-11-06</td>
      <td>Far West 360° : Los Angeles, Las Vegas et les grands parcs américains</td>
      <td>États-Unis</td>
      <td>États-Unis d'Amérique</td>
      <td>1 599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/far-west-360/737ac5d4-4aa4-4ea0-8689-996f9835ca89</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/far-west-360/737ac5d4-4aa4-4ea0-8689-996f9835ca89'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-01</td>
      <td>2025-11-12</td>
      <td>Bolivie & Chili : de Santiago à La Paz</td>
      <td>Chili & Bolivie</td>
      <td>Bolivie</td>
      <td>2 499,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/bolivie-et-chili-360/1ff089b7-7105-4750-a027-f101e4ff4ad1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bolivie-et-chili-360/1ff089b7-7105-4750-a027-f101e4ff4ad1'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-07</td>
      <td>2025-11-15</td>
      <td>Oman 360°</td>
      <td>Oman</td>
      <td>Oman</td>
      <td>1 149,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/oman/77ce635f-0502-479d-afc6-6b51f8f4d033</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/oman/77ce635f-0502-479d-afc6-6b51f8f4d033'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-14</td>
      <td>2025-11-21</td>
      <td>Islande : à la poursuite des aurores boréales</td>
      <td>Islande</td>
      <td>Islande</td>
      <td>1 449,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/islande-aurores-boreales/4c76cd50-42c1-42e0-81c7-9eba938eee99</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/islande-aurores-boreales/4c76cd50-42c1-42e0-81c7-9eba938eee99'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-15</td>
      <td>2025-11-27</td>
      <td>Indonésie 360° : Java, Bali et Gili</td>
      <td>Indonésie</td>
      <td>Indonésie</td>
      <td>1 349,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/indonesie-360/0c2b49fa-d541-43a4-9c97-8a4ad1f8af3b</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/indonesie-360/0c2b49fa-d541-43a4-9c97-8a4ad1f8af3b'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-18</td>
      <td>2025-12-01</td>
      <td>Nouvelle-Zélande 360°: sur la route d'Auckland jusqu'à Queenstown</td>
      <td>Nouvelle-Zélande</td>
      <td>Nouvelle-Zélande</td>
      <td>2 549,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/nouvelle-zelande-360/71f6cafe-68e7-4353-8896-7abffce8ad52</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/nouvelle-zelande-360/71f6cafe-68e7-4353-8896-7abffce8ad52'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-21</td>
      <td>2025-12-05</td>
      <td>Vietnam & Cambodge</td>
      <td>Vietnam</td>
      <td>Viêt Nam</td>
      <td>1 849,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/vietnam-cambodge/2918d031-dfc8-4d3d-a912-2e981e0c1bb2</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/vietnam-cambodge/2918d031-dfc8-4d3d-a912-2e981e0c1bb2'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-28</td>
      <td>2025-12-09</td>
      <td>Sri Lanka 360° Winter</td>
      <td>Sri Lanka</td>
      <td>Sri Lanka</td>
      <td>1 099,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/sri-lanka-360-hiver/70ff426d-905e-4e91-99e1-f5bfffe14768</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/sri-lanka-360-hiver/70ff426d-905e-4e91-99e1-f5bfffe14768'>🔗</a></td>
    </tr>
  </tbody>
</table>
</div>

---

## KPIs hebdo — Historique des runs
<div class='table-wrapper'>
<table border="1" class="dataframe rp-table">
  <thead>
    <tr style="text-align: right;">
      <th>run_date</th>
      <th>price_eur_min</th>
      <th>price_eur_med</th>
      <th>price_eur_avg</th>
      <th>count_total</th>
      <th>count_promos</th>
      <th>promo_share_pct</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2025-08-29</td>
      <td>449,00 €</td>
      <td>1 149,00 €</td>
      <td>1 285,96 €</td>
      <td>142</td>
      <td>46</td>
      <td>32.4%</td>
    </tr>
  </tbody>
</table>
</div>

---

## KPIs mensuels — Vue complète
<div class='table-wrapper'>
<table border="1" class="dataframe rp-table">
  <thead>
    <tr style="text-align: right;">
      <th>month</th>
      <th>destination_label</th>
      <th>prix_min</th>
      <th>prix_avg</th>
      <th>nb_depart</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2025-08</td>
      <td>Islande</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Afrique du Sud</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Albanie</td>
      <td>639,00 €</td>
      <td>639,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Australie</td>
      <td>2 019,00 €</td>
      <td>2 019,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Brésil</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Canada</td>
      <td>1 389,00 €</td>
      <td>1 839,50 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Corfou</td>
      <td>739,00 €</td>
      <td>739,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Cuba</td>
      <td>969,00 €</td>
      <td>969,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Dolomites</td>
      <td>919,00 €</td>
      <td>919,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Floride</td>
      <td>1 479,00 €</td>
      <td>1 479,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>France</td>
      <td>789,00 €</td>
      <td>789,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Grecia</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>INDONÉSIE</td>
      <td>779,00 €</td>
      <td>779,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Indonesie</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Indonésie</td>
      <td>1 609,00 €</td>
      <td>1 609,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Islande</td>
      <td>1 799,00 €</td>
      <td>1 799,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Italie</td>
      <td>859,00 €</td>
      <td>859,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Japon</td>
      <td>1 499,00 €</td>
      <td>1 499,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Jordanie</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Kenya</td>
      <td>2 299,00 €</td>
      <td>2 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Malaisie</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Malte</td>
      <td>759,00 €</td>
      <td>759,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Maroc</td>
      <td>479,00 €</td>
      <td>591,50 €</td>
      <td>4</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Maurice</td>
      <td>1 149,00 €</td>
      <td>1 149,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Naples & la côte Amalfitaine</td>
      <td>519,00 €</td>
      <td>519,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>New York</td>
      <td>819,00 €</td>
      <td>819,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Ouzbékistan</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Pérou</td>
      <td>1 529,00 €</td>
      <td>1 529,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Romania</td>
      <td>449,00 €</td>
      <td>449,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Slovénie</td>
      <td>1 049,00 €</td>
      <td>1 049,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Sri Lanka</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Thailande</td>
      <td>1 249,00 €</td>
      <td>1 249,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Vietnam</td>
      <td>959,00 €</td>
      <td>959,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Égypte</td>
      <td>1 079,00 €</td>
      <td>1 079,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Équateur</td>
      <td>2 709,00 €</td>
      <td>2 709,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Barcelone & Costa Brava</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Belize</td>
      <td>1 499,00 €</td>
      <td>1 499,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Brésil</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Chili et Bolivie</td>
      <td>1 999,00 €</td>
      <td>1 999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Colombie</td>
      <td>2 299,00 €</td>
      <td>2 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Corée du Sud</td>
      <td>1 499,00 €</td>
      <td>1 499,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Crète</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Espagne</td>
      <td>1 099,00 €</td>
      <td>1 099,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>France</td>
      <td>599,00 €</td>
      <td>749,00 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Gran Canaria</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Inde</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Kenya</td>
      <td>1 789,00 €</td>
      <td>1 789,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Maroc</td>
      <td>1 099,00 €</td>
      <td>1 099,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Népal</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Pays Baltes</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Portugal</td>
      <td>699,00 €</td>
      <td>699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Route 66</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Sicile</td>
      <td>1 199,00 €</td>
      <td>1 199,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Suisse</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Suède</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Tchéquie</td>
      <td>849,00 €</td>
      <td>849,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Tunisie</td>
      <td>789,00 €</td>
      <td>789,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Turquie</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Écosse</td>
      <td>849,00 €</td>
      <td>849,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Émirats Arabes Unis</td>
      <td>1 199,00 €</td>
      <td>1 199,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Équateur & Amazonie</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>États-Unis</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Autriche</td>
      <td>799,00 €</td>
      <td>849,00 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Belgique</td>
      <td>789,00 €</td>
      <td>789,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Cap-Vert</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Chili & Bolivie</td>
      <td>2 499,00 €</td>
      <td>2 499,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Chine</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Colombie</td>
      <td>2 199,00 €</td>
      <td>2 199,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>France</td>
      <td>699,00 €</td>
      <td>749,00 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Hongrie</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Inde</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Indonésie</td>
      <td>889,00 €</td>
      <td>1 119,00 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Islande</td>
      <td>1 449,00 €</td>
      <td>1 449,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Istanbul & Cappadoce</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Italie</td>
      <td>799,00 €</td>
      <td>799,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Jordanie</td>
      <td>1 249,00 €</td>
      <td>1 249,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Mexique</td>
      <td>1 549,00 €</td>
      <td>1 574,00 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Nouvelle-Zélande</td>
      <td>2 549,00 €</td>
      <td>2 549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Oman</td>
      <td>1 149,00 €</td>
      <td>1 149,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Patagonie</td>
      <td>2 999,00 €</td>
      <td>2 999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Sri Lanka</td>
      <td>1 099,00 €</td>
      <td>1 099,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Vietnam</td>
      <td>1 849,00 €</td>
      <td>1 849,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Allemagne</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Bourgogne</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Géorgie</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Hungary</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Kirghizistan</td>
      <td>1 049,00 €</td>
      <td>1 049,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Norvège</td>
      <td>1 449,00 €</td>
      <td>1 449,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Panamá</td>
      <td>1 566,00 €</td>
      <td>1 566,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Philippines</td>
      <td>2 099,00 €</td>
      <td>2 099,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Réunion</td>
      <td>1 390,00 €</td>
      <td>1 390,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Suède</td>
      <td>1 549,00 €</td>
      <td>1 549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Tanzanie</td>
      <td>3 499,00 €</td>
      <td>3 499,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Égypte</td>
      <td>499,00 €</td>
      <td>499,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Îles Canaries</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Argentine</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Finlande</td>
      <td>1 549,00 €</td>
      <td>1 549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Nicaragua</td>
      <td>1 429,00 €</td>
      <td>1 429,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Vietnam</td>
      <td>1 049,00 €</td>
      <td>1 049,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Brésil</td>
      <td>2 929,00 €</td>
      <td>2 929,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Irlande</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Italie</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Japon</td>
      <td>2 099,00 €</td>
      <td>2 099,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Maldives</td>
      <td>1 179,00 €</td>
      <td>1 179,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Ouzbékistan</td>
      <td>1 149,00 €</td>
      <td>1 149,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Thaïlande</td>
      <td>1 249,00 €</td>
      <td>1 249,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Cambodge</td>
      <td>1 900,00 €</td>
      <td>1 900,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Irlande</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Islande</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Malaisie</td>
      <td>1 105,00 €</td>
      <td>1 105,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Maldives</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Mexique</td>
      <td>1 399,00 €</td>
      <td>1 399,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Thaïlande</td>
      <td>999,00 €</td>
      <td>1 349,00 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Turquie</td>
      <td>1 349,00 €</td>
      <td>1 349,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Albanie</td>
      <td>549,00 €</td>
      <td>549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Chine</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Guatemala</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Istanbul</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Sénégal</td>
      <td>2 050,00 €</td>
      <td>2 050,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>États-Unis</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>Namibie</td>
      <td>2 299,00 €</td>
      <td>2 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>Népal</td>
      <td>1 019,00 €</td>
      <td>1 019,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>Portugal</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>Bordeaux</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>Normandie</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>Thaïlande</td>
      <td>1 199,00 €</td>
      <td>1 199,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-07</td>
      <td>Auvergne</td>
      <td>549,00 €</td>
      <td>549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-07</td>
      <td>Espagne</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-08</td>
      <td>Bretagne</td>
      <td>679,00 €</td>
      <td>679,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-08</td>
      <td>Kirghizistan</td>
      <td>1 490,00 €</td>
      <td>1 490,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-11</td>
      <td>Costa Rica</td>
      <td>1 799,00 €</td>
      <td>1 799,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-12</td>
      <td>Bulgarie</td>
      <td>699,00 €</td>
      <td>699,00 €</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

### KPIs mensuels — Aperçu 24 derniers mois
<div class='table-wrapper'>
<table border="1" class="dataframe rp-table">
  <thead>
    <tr style="text-align: right;">
      <th>month</th>
      <th>destination_label</th>
      <th>prix_min</th>
      <th>prix_avg</th>
      <th>nb_depart</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2025-08</td>
      <td>Islande</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Afrique du Sud</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Albanie</td>
      <td>639,00 €</td>
      <td>639,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Australie</td>
      <td>2 019,00 €</td>
      <td>2 019,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Brésil</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Canada</td>
      <td>1 389,00 €</td>
      <td>1 839,50 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Corfou</td>
      <td>739,00 €</td>
      <td>739,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Cuba</td>
      <td>969,00 €</td>
      <td>969,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Dolomites</td>
      <td>919,00 €</td>
      <td>919,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Floride</td>
      <td>1 479,00 €</td>
      <td>1 479,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>France</td>
      <td>789,00 €</td>
      <td>789,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Grecia</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>INDONÉSIE</td>
      <td>779,00 €</td>
      <td>779,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Indonesie</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Indonésie</td>
      <td>1 609,00 €</td>
      <td>1 609,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Islande</td>
      <td>1 799,00 €</td>
      <td>1 799,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Italie</td>
      <td>859,00 €</td>
      <td>859,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Japon</td>
      <td>1 499,00 €</td>
      <td>1 499,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Jordanie</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Kenya</td>
      <td>2 299,00 €</td>
      <td>2 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Malaisie</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Malte</td>
      <td>759,00 €</td>
      <td>759,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Maroc</td>
      <td>479,00 €</td>
      <td>591,50 €</td>
      <td>4</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Maurice</td>
      <td>1 149,00 €</td>
      <td>1 149,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Naples & la côte Amalfitaine</td>
      <td>519,00 €</td>
      <td>519,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>New York</td>
      <td>819,00 €</td>
      <td>819,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Ouzbékistan</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Pérou</td>
      <td>1 529,00 €</td>
      <td>1 529,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Romania</td>
      <td>449,00 €</td>
      <td>449,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Slovénie</td>
      <td>1 049,00 €</td>
      <td>1 049,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Sri Lanka</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Thailande</td>
      <td>1 249,00 €</td>
      <td>1 249,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Vietnam</td>
      <td>959,00 €</td>
      <td>959,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Égypte</td>
      <td>1 079,00 €</td>
      <td>1 079,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Équateur</td>
      <td>2 709,00 €</td>
      <td>2 709,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Barcelone & Costa Brava</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Belize</td>
      <td>1 499,00 €</td>
      <td>1 499,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Brésil</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Chili et Bolivie</td>
      <td>1 999,00 €</td>
      <td>1 999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Colombie</td>
      <td>2 299,00 €</td>
      <td>2 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Corée du Sud</td>
      <td>1 499,00 €</td>
      <td>1 499,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Crète</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Espagne</td>
      <td>1 099,00 €</td>
      <td>1 099,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>France</td>
      <td>599,00 €</td>
      <td>749,00 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Gran Canaria</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Inde</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Kenya</td>
      <td>1 789,00 €</td>
      <td>1 789,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Maroc</td>
      <td>1 099,00 €</td>
      <td>1 099,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Népal</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Pays Baltes</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Portugal</td>
      <td>699,00 €</td>
      <td>699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Route 66</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Sicile</td>
      <td>1 199,00 €</td>
      <td>1 199,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Suisse</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Suède</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Tchéquie</td>
      <td>849,00 €</td>
      <td>849,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Tunisie</td>
      <td>789,00 €</td>
      <td>789,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Turquie</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Écosse</td>
      <td>849,00 €</td>
      <td>849,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Émirats Arabes Unis</td>
      <td>1 199,00 €</td>
      <td>1 199,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Équateur & Amazonie</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>États-Unis</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Autriche</td>
      <td>799,00 €</td>
      <td>849,00 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Belgique</td>
      <td>789,00 €</td>
      <td>789,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Cap-Vert</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Chili & Bolivie</td>
      <td>2 499,00 €</td>
      <td>2 499,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Chine</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Colombie</td>
      <td>2 199,00 €</td>
      <td>2 199,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>France</td>
      <td>699,00 €</td>
      <td>749,00 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Hongrie</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Inde</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Indonésie</td>
      <td>889,00 €</td>
      <td>1 119,00 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Islande</td>
      <td>1 449,00 €</td>
      <td>1 449,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Istanbul & Cappadoce</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Italie</td>
      <td>799,00 €</td>
      <td>799,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Jordanie</td>
      <td>1 249,00 €</td>
      <td>1 249,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Mexique</td>
      <td>1 549,00 €</td>
      <td>1 574,00 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Nouvelle-Zélande</td>
      <td>2 549,00 €</td>
      <td>2 549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Oman</td>
      <td>1 149,00 €</td>
      <td>1 149,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Patagonie</td>
      <td>2 999,00 €</td>
      <td>2 999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Sri Lanka</td>
      <td>1 099,00 €</td>
      <td>1 099,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Vietnam</td>
      <td>1 849,00 €</td>
      <td>1 849,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Allemagne</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Bourgogne</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Géorgie</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Hungary</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Kirghizistan</td>
      <td>1 049,00 €</td>
      <td>1 049,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Norvège</td>
      <td>1 449,00 €</td>
      <td>1 449,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Panamá</td>
      <td>1 566,00 €</td>
      <td>1 566,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Philippines</td>
      <td>2 099,00 €</td>
      <td>2 099,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Réunion</td>
      <td>1 390,00 €</td>
      <td>1 390,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Suède</td>
      <td>1 549,00 €</td>
      <td>1 549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Tanzanie</td>
      <td>3 499,00 €</td>
      <td>3 499,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Égypte</td>
      <td>499,00 €</td>
      <td>499,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Îles Canaries</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Argentine</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Finlande</td>
      <td>1 549,00 €</td>
      <td>1 549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Nicaragua</td>
      <td>1 429,00 €</td>
      <td>1 429,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Vietnam</td>
      <td>1 049,00 €</td>
      <td>1 049,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Brésil</td>
      <td>2 929,00 €</td>
      <td>2 929,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Irlande</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Italie</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Japon</td>
      <td>2 099,00 €</td>
      <td>2 099,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Maldives</td>
      <td>1 179,00 €</td>
      <td>1 179,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Ouzbékistan</td>
      <td>1 149,00 €</td>
      <td>1 149,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Thaïlande</td>
      <td>1 249,00 €</td>
      <td>1 249,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Cambodge</td>
      <td>1 900,00 €</td>
      <td>1 900,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Irlande</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Islande</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Malaisie</td>
      <td>1 105,00 €</td>
      <td>1 105,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Maldives</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Mexique</td>
      <td>1 399,00 €</td>
      <td>1 399,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Thaïlande</td>
      <td>999,00 €</td>
      <td>1 349,00 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Turquie</td>
      <td>1 349,00 €</td>
      <td>1 349,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Albanie</td>
      <td>549,00 €</td>
      <td>549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Chine</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Guatemala</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Istanbul</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>Sénégal</td>
      <td>2 050,00 €</td>
      <td>2 050,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>États-Unis</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>Namibie</td>
      <td>2 299,00 €</td>
      <td>2 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>Népal</td>
      <td>1 019,00 €</td>
      <td>1 019,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>Portugal</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>Bordeaux</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>Normandie</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>Thaïlande</td>
      <td>1 199,00 €</td>
      <td>1 199,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-07</td>
      <td>Auvergne</td>
      <td>549,00 €</td>
      <td>549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-07</td>
      <td>Espagne</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-08</td>
      <td>Bretagne</td>
      <td>679,00 €</td>
      <td>679,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-08</td>
      <td>Kirghizistan</td>
      <td>1 490,00 €</td>
      <td>1 490,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-11</td>
      <td>Costa Rica</td>
      <td>1 799,00 €</td>
      <td>1 799,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-12</td>
      <td>Bulgarie</td>
      <td>699,00 €</td>
      <td>699,00 €</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

---

## Pays — synthèse
<div class='table-wrapper'>
<table border="1" class="dataframe rp-table">
  <thead>
    <tr style="text-align: right;">
      <th>country_name</th>
      <th>nb_offres</th>
      <th>prix_min</th>
      <th>prix_med</th>
      <th>prix_moy</th>
      <th>taux_promos_pct</th>
      <th>rating_moy</th>
      <th>rating_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Roumanie</td>
      <td>1</td>
      <td>449,00 €</td>
      <td>449,00 €</td>
      <td>449,00 €</td>
      <td>100.0%</td>
      <td>4.800000</td>
      <td>507.0</td>
    </tr>
    <tr>
      <td>Albanie</td>
      <td>2</td>
      <td>549,00 €</td>
      <td>594,00 €</td>
      <td>594,00 €</td>
      <td>50.0%</td>
      <td>4.700000</td>
      <td>1619.0</td>
    </tr>
    <tr>
      <td>Allemagne</td>
      <td>1</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>100.0%</td>
      <td>5.000000</td>
      <td>1.0</td>
    </tr>
    <tr>
      <td>Maroc</td>
      <td>5</td>
      <td>479,00 €</td>
      <td>659,00 €</td>
      <td>693,00 €</td>
      <td>100.0%</td>
      <td>4.775000</td>
      <td>7638.0</td>
    </tr>
    <tr>
      <td>Bulgarie</td>
      <td>1</td>
      <td>699,00 €</td>
      <td>699,00 €</td>
      <td>699,00 €</td>
      <td>0.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>France</td>
      <td>10</td>
      <td>549,00 €</td>
      <td>744,00 €</td>
      <td>751,00 €</td>
      <td>20.0%</td>
      <td>4.675000</td>
      <td>198.0</td>
    </tr>
    <tr>
      <td>Malte</td>
      <td>1</td>
      <td>759,00 €</td>
      <td>759,00 €</td>
      <td>759,00 €</td>
      <td>100.0%</td>
      <td>4.600000</td>
      <td>102.0</td>
    </tr>
    <tr>
      <td>Hongrie</td>
      <td>2</td>
      <td>599,00 €</td>
      <td>774,00 €</td>
      <td>774,00 €</td>
      <td>50.0%</td>
      <td>4.700000</td>
      <td>13.0</td>
    </tr>
    <tr>
      <td>Belgique</td>
      <td>1</td>
      <td>789,00 €</td>
      <td>789,00 €</td>
      <td>789,00 €</td>
      <td>0.0%</td>
      <td>5.000000</td>
      <td>4.0</td>
    </tr>
    <tr>
      <td>Tunisie</td>
      <td>1</td>
      <td>789,00 €</td>
      <td>789,00 €</td>
      <td>789,00 €</td>
      <td>0.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>Égypte</td>
      <td>2</td>
      <td>499,00 €</td>
      <td>789,00 €</td>
      <td>789,00 €</td>
      <td>50.0%</td>
      <td>4.750000</td>
      <td>1024.0</td>
    </tr>
    <tr>
      <td>Royaume-Uni</td>
      <td>1</td>
      <td>849,00 €</td>
      <td>849,00 €</td>
      <td>849,00 €</td>
      <td>100.0%</td>
      <td>5.000000</td>
      <td>1.0</td>
    </tr>
    <tr>
      <td>Tchéquie</td>
      <td>1</td>
      <td>849,00 €</td>
      <td>849,00 €</td>
      <td>849,00 €</td>
      <td>100.0%</td>
      <td>5.000000</td>
      <td>8.0</td>
    </tr>
    <tr>
      <td>Autriche</td>
      <td>2</td>
      <td>799,00 €</td>
      <td>849,00 €</td>
      <td>849,00 €</td>
      <td>0.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>Italie</td>
      <td>6</td>
      <td>519,00 €</td>
      <td>889,00 €</td>
      <td>874,00 €</td>
      <td>33.3%</td>
      <td>4.675000</td>
      <td>2428.0</td>
    </tr>
    <tr>
      <td>Estonie</td>
      <td>1</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>0.0%</td>
      <td>4.700000</td>
      <td>279.0</td>
    </tr>
    <tr>
      <td>Géorgie</td>
      <td>1</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>0.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>Indonésie</td>
      <td>5</td>
      <td>779,00 €</td>
      <td>899,00 €</td>
      <td>1 105,00 €</td>
      <td>80.0%</td>
      <td>4.733333</td>
      <td>5324.0</td>
    </tr>
    <tr>
      <td>Suisse</td>
      <td>1</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
      <td>0.0%</td>
      <td>4.600000</td>
      <td>5.0</td>
    </tr>
    <tr>
      <td>Cuba</td>
      <td>1</td>
      <td>969,00 €</td>
      <td>969,00 €</td>
      <td>969,00 €</td>
      <td>100.0%</td>
      <td>4.700000</td>
      <td>4287.0</td>
    </tr>
    <tr>
      <td>Grèce</td>
      <td>3</td>
      <td>739,00 €</td>
      <td>999,00 €</td>
      <td>912,33 €</td>
      <td>33.3%</td>
      <td>4.666667</td>
      <td>3651.0</td>
    </tr>
    <tr>
      <td>Sri Lanka</td>
      <td>2</td>
      <td>899,00 €</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>50.0%</td>
      <td>4.750000</td>
      <td>1945.0</td>
    </tr>
    <tr>
      <td>Espagne</td>
      <td>5</td>
      <td>599,00 €</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>20.0%</td>
      <td>4.850000</td>
      <td>432.0</td>
    </tr>
    <tr>
      <td>Népal</td>
      <td>2</td>
      <td>999,00 €</td>
      <td>1 009,00 €</td>
      <td>1 009,00 €</td>
      <td>0.0%</td>
      <td>4.800000</td>
      <td>1405.0</td>
    </tr>
    <tr>
      <td>Ouzbékistan</td>
      <td>2</td>
      <td>899,00 €</td>
      <td>1 024,00 €</td>
      <td>1 024,00 €</td>
      <td>50.0%</td>
      <td>4.900000</td>
      <td>494.0</td>
    </tr>
    <tr>
      <td>Slovénie</td>
      <td>1</td>
      <td>1 049,00 €</td>
      <td>1 049,00 €</td>
      <td>1 049,00 €</td>
      <td>0.0%</td>
      <td>4.700000</td>
      <td>123.0</td>
    </tr>
    <tr>
      <td>Viêt Nam</td>
      <td>3</td>
      <td>959,00 €</td>
      <td>1 049,00 €</td>
      <td>1 285,67 €</td>
      <td>33.3%</td>
      <td>4.833333</td>
      <td>2449.0</td>
    </tr>
    <tr>
      <td>Jordanie</td>
      <td>2</td>
      <td>999,00 €</td>
      <td>1 124,00 €</td>
      <td>1 124,00 €</td>
      <td>0.0%</td>
      <td>4.850000</td>
      <td>8810.0</td>
    </tr>
    <tr>
      <td>Maurice</td>
      <td>1</td>
      <td>1 149,00 €</td>
      <td>1 149,00 €</td>
      <td>1 149,00 €</td>
      <td>100.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>Oman</td>
      <td>1</td>
      <td>1 149,00 €</td>
      <td>1 149,00 €</td>
      <td>1 149,00 €</td>
      <td>0.0%</td>
      <td>4.700000</td>
      <td>525.0</td>
    </tr>
    <tr>
      <td>Inde</td>
      <td>2</td>
      <td>999,00 €</td>
      <td>1 149,00 €</td>
      <td>1 149,00 €</td>
      <td>0.0%</td>
      <td>4.800000</td>
      <td>723.0</td>
    </tr>
    <tr>
      <td>Irlande</td>
      <td>2</td>
      <td>999,00 €</td>
      <td>1 149,00 €</td>
      <td>1 149,00 €</td>
      <td>0.0%</td>
      <td>4.000000</td>
      <td>1.0</td>
    </tr>
    <tr>
      <td>Turquie</td>
      <td>4</td>
      <td>599,00 €</td>
      <td>1 174,00 €</td>
      <td>1 161,50 €</td>
      <td>0.0%</td>
      <td>4.700000</td>
      <td>2564.0</td>
    </tr>
    <tr>
      <td>Émirats arabes unis</td>
      <td>1</td>
      <td>1 199,00 €</td>
      <td>1 199,00 €</td>
      <td>1 199,00 €</td>
      <td>0.0%</td>
      <td>4.700000</td>
      <td>323.0</td>
    </tr>
    <tr>
      <td>Portugal</td>
      <td>2</td>
      <td>699,00 €</td>
      <td>1 199,00 €</td>
      <td>1 199,00 €</td>
      <td>0.0%</td>
      <td>4.700000</td>
      <td>1169.0</td>
    </tr>
    <tr>
      <td>Islande</td>
      <td>4</td>
      <td>899,00 €</td>
      <td>1 224,00 €</td>
      <td>1 286,50 €</td>
      <td>0.0%</td>
      <td>4.800000</td>
      <td>7024.0</td>
    </tr>
    <tr>
      <td>Maldives</td>
      <td>2</td>
      <td>1 179,00 €</td>
      <td>1 239,00 €</td>
      <td>1 239,00 €</td>
      <td>100.0%</td>
      <td>5.000000</td>
      <td>26.0</td>
    </tr>
    <tr>
      <td>Thaïlande</td>
      <td>5</td>
      <td>999,00 €</td>
      <td>1 249,00 €</td>
      <td>1 279,00 €</td>
      <td>0.0%</td>
      <td>4.720000</td>
      <td>4365.0</td>
    </tr>
    <tr>
      <td>Kirghizistan</td>
      <td>2</td>
      <td>1 049,00 €</td>
      <td>1 269,50 €</td>
      <td>1 269,50 €</td>
      <td>0.0%</td>
      <td>5.000000</td>
      <td>2.0</td>
    </tr>
    <tr>
      <td>Malaisie</td>
      <td>2</td>
      <td>1 105,00 €</td>
      <td>1 352,00 €</td>
      <td>1 352,00 €</td>
      <td>50.0%</td>
      <td>4.800000</td>
      <td>204.0</td>
    </tr>
    <tr>
      <td>Réunion</td>
      <td>1</td>
      <td>1 390,00 €</td>
      <td>1 390,00 €</td>
      <td>1 390,00 €</td>
      <td>0.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>Nicaragua</td>
      <td>1</td>
      <td>1 429,00 €</td>
      <td>1 429,00 €</td>
      <td>1 429,00 €</td>
      <td>100.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>Norvège</td>
      <td>1</td>
      <td>1 449,00 €</td>
      <td>1 449,00 €</td>
      <td>1 449,00 €</td>
      <td>0.0%</td>
      <td>4.800000</td>
      <td>412.0</td>
    </tr>
    <tr>
      <td>Belize</td>
      <td>1</td>
      <td>1 499,00 €</td>
      <td>1 499,00 €</td>
      <td>1 499,00 €</td>
      <td>100.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>Corée du Sud</td>
      <td>1</td>
      <td>1 499,00 €</td>
      <td>1 499,00 €</td>
      <td>1 499,00 €</td>
      <td>0.0%</td>
      <td>4.700000</td>
      <td>240.0</td>
    </tr>
    <tr>
      <td>Pérou</td>
      <td>1</td>
      <td>1 529,00 €</td>
      <td>1 529,00 €</td>
      <td>1 529,00 €</td>
      <td>100.0%</td>
      <td>4.800000</td>
      <td>2545.0</td>
    </tr>
    <tr>
      <td>Mexique</td>
      <td>3</td>
      <td>1 399,00 €</td>
      <td>1 549,00 €</td>
      <td>1 515,67 €</td>
      <td>0.0%</td>
      <td>4.733333</td>
      <td>3200.0</td>
    </tr>
    <tr>
      <td>Finlande</td>
      <td>1</td>
      <td>1 549,00 €</td>
      <td>1 549,00 €</td>
      <td>1 549,00 €</td>
      <td>0.0%</td>
      <td>4.800000</td>
      <td>242.0</td>
    </tr>
    <tr>
      <td>Panamá</td>
      <td>1</td>
      <td>1 566,00 €</td>
      <td>1 566,00 €</td>
      <td>1 566,00 €</td>
      <td>100.0%</td>
      <td>4.500000</td>
      <td>4.0</td>
    </tr>
    <tr>
      <td>Suède</td>
      <td>2</td>
      <td>1 549,00 €</td>
      <td>1 574,00 €</td>
      <td>1 574,00 €</td>
      <td>0.0%</td>
      <td>4.850000</td>
      <td>1690.0</td>
    </tr>
    <tr>
      <td>États-Unis d'Amérique</td>
      <td>5</td>
      <td>819,00 €</td>
      <td>1 599,00 €</td>
      <td>1 499,00 €</td>
      <td>40.0%</td>
      <td>4.760000</td>
      <td>5327.0</td>
    </tr>
    <tr>
      <td>Cap-Vert</td>
      <td>1</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
      <td>100.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>Guatemala</td>
      <td>1</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>0.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>Costa Rica</td>
      <td>1</td>
      <td>1 799,00 €</td>
      <td>1 799,00 €</td>
      <td>1 799,00 €</td>
      <td>0.0%</td>
      <td>4.700000</td>
      <td>751.0</td>
    </tr>
    <tr>
      <td>Japon</td>
      <td>2</td>
      <td>1 499,00 €</td>
      <td>1 799,00 €</td>
      <td>1 799,00 €</td>
      <td>50.0%</td>
      <td>4.700000</td>
      <td>3256.0</td>
    </tr>
    <tr>
      <td>Canada</td>
      <td>2</td>
      <td>1 389,00 €</td>
      <td>1 839,50 €</td>
      <td>1 839,50 €</td>
      <td>50.0%</td>
      <td>4.850000</td>
      <td>64.0</td>
    </tr>
    <tr>
      <td>Afrique du Sud</td>
      <td>1</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>0.0%</td>
      <td>4.800000</td>
      <td>542.0</td>
    </tr>
    <tr>
      <td>Chine</td>
      <td>2</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>50.0%</td>
      <td>4.700000</td>
      <td>145.0</td>
    </tr>
    <tr>
      <td>Brésil</td>
      <td>3</td>
      <td>1 599,00 €</td>
      <td>1 899,00 €</td>
      <td>2 142,33 €</td>
      <td>66.7%</td>
      <td>4.750000</td>
      <td>248.0</td>
    </tr>
    <tr>
      <td>Cambodge</td>
      <td>1</td>
      <td>1 900,00 €</td>
      <td>1 900,00 €</td>
      <td>1 900,00 €</td>
      <td>0.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>Chili</td>
      <td>1</td>
      <td>1 999,00 €</td>
      <td>1 999,00 €</td>
      <td>1 999,00 €</td>
      <td>0.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>Équateur</td>
      <td>2</td>
      <td>1 299,00 €</td>
      <td>2 004,00 €</td>
      <td>2 004,00 €</td>
      <td>50.0%</td>
      <td>4.800000</td>
      <td>110.0</td>
    </tr>
    <tr>
      <td>Australie</td>
      <td>1</td>
      <td>2 019,00 €</td>
      <td>2 019,00 €</td>
      <td>2 019,00 €</td>
      <td>100.0%</td>
      <td>4.600000</td>
      <td>101.0</td>
    </tr>
    <tr>
      <td>Kenya</td>
      <td>2</td>
      <td>1 789,00 €</td>
      <td>2 044,00 €</td>
      <td>2 044,00 €</td>
      <td>50.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>Sénégal</td>
      <td>1</td>
      <td>2 050,00 €</td>
      <td>2 050,00 €</td>
      <td>2 050,00 €</td>
      <td>0.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>Philippines</td>
      <td>1</td>
      <td>2 099,00 €</td>
      <td>2 099,00 €</td>
      <td>2 099,00 €</td>
      <td>0.0%</td>
      <td>4.700000</td>
      <td>236.0</td>
    </tr>
    <tr>
      <td>Colombie</td>
      <td>2</td>
      <td>2 199,00 €</td>
      <td>2 249,00 €</td>
      <td>2 249,00 €</td>
      <td>0.0%</td>
      <td>4.700000</td>
      <td>926.0</td>
    </tr>
    <tr>
      <td>Namibie</td>
      <td>1</td>
      <td>2 299,00 €</td>
      <td>2 299,00 €</td>
      <td>2 299,00 €</td>
      <td>0.0%</td>
      <td>4.900000</td>
      <td>193.0</td>
    </tr>
    <tr>
      <td>Argentine</td>
      <td>2</td>
      <td>1 899,00 €</td>
      <td>2 449,00 €</td>
      <td>2 449,00 €</td>
      <td>0.0%</td>
      <td>4.800000</td>
      <td>491.0</td>
    </tr>
    <tr>
      <td>Bolivie</td>
      <td>1</td>
      <td>2 499,00 €</td>
      <td>2 499,00 €</td>
      <td>2 499,00 €</td>
      <td>0.0%</td>
      <td>4.900000</td>
      <td>53.0</td>
    </tr>
    <tr>
      <td>Nouvelle-Zélande</td>
      <td>1</td>
      <td>2 549,00 €</td>
      <td>2 549,00 €</td>
      <td>2 549,00 €</td>
      <td>0.0%</td>
      <td>4.600000</td>
      <td>35.0</td>
    </tr>
    <tr>
      <td>Tanzanie</td>
      <td>1</td>
      <td>3 499,00 €</td>
      <td>3 499,00 €</td>
      <td>3 499,00 €</td>
      <td>0.0%</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>
