---
title: RoadPrice — Accueil
---

# RoadPrice — synthèse

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/simple-datatables@9.0.3/dist/style.min.css">
<script src="https://cdn.jsdelivr.net/npm/simple-datatables@9.0.3"></script>
<style>
.dataTable-wrapper, .dataTable-wrapper .dataTable-container { background: transparent !important; border: 0 !important; box-shadow: none !important; padding: 0 !important; }
.dataTable-top, .dataTable-bottom { background: transparent !important; border: none !important; box-shadow: none !important; padding: .25rem 0 !important; }
.dataTable-info, .dataTable-pagination, .dataTable-dropdown, .dataTable-search { margin: .35rem 0 !important; font-size: .95rem !important; }
.dataTable-pagination a { border-radius: .4rem !important; }
.table-wrapper { overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 0 0 1.25rem 0; }
</style>
<script>
(function() {
  const ready = (fn) => {
    if (document.readyState !== "loading") requestAnimationFrame(fn);
    else document.addEventListener("DOMContentLoaded", () => requestAnimationFrame(fn));
  };
  const euroToNumber = (txt) => {
    if (!txt) return null;
    const s = String(txt).replace(/\s/g, "").replace("€","").replace(/\u00A0/g,"").replace(",",".");
    const v = parseFloat(s); return isNaN(v) ? null : v;
  };
  ready(() => {
    const tables = document.querySelectorAll("table.rp-table");
    tables.forEach((tbl, tIndex) => {
      try {
        const dt = new simpleDatatables.DataTable(tbl, {
          searchable: true, fixedHeight: false,
          perPage: 25, perPageSelect: [10, 25, 50, 100],
          labels: { placeholder: "Rechercher…", perPage: "{select} lignes par page", noRows: "Aucune donnée", info: "Affiche {start}–{end} sur {rows} lignes" },
        });
        try {
          dt.columns().each((idx) => {
            const header = tbl.tHead && tbl.tHead.rows && tbl.tHead.rows[0] && tbl.tHead.rows[0].cells ? tbl.tHead.rows[0].cells[idx] : null;
            if (!header) return;
            const htxt = (header.textContent || "").toLowerCase();
            const isMoney = /(€|price|prix|delta_abs)/.test(htxt);
            const isPct   = /(pct|%)/.test(htxt);
            if (isMoney || isPct) {
              dt.columns().sort(idx, (a, b) => {
                const ta = a.replace(/<[^>]*>/g, "");
                const tb = b.replace(/<[^>]*>/g, "");
                const na = isPct ? parseFloat(ta.replace("%","").replace(",",".")) : euroToNumber(ta);
                const nb = isPct ? parseFloat(tb.replace("%","").replace(",",".")) : euroToNumber(tb);
                if (na == null && nb == null) return 0;
                if (na == null) return -1;
                if (nb == null) return 1;
                return na - nb;
              });
            }
          });
        } catch(e) { console.warn("Sorter setup error on table", tIndex, e); }
      } catch (e) { console.warn("DataTable init failed on table", tIndex, e); }
    });
  });
})();
</script>

![run](https://img.shields.io/badge/run-2025-08-26-blue) ![build](https://img.shields.io/badge/build-2025-08-26 21:04 UTC-success)

_Historique : **2025-08-26** → **2025-08-26** (1 runs)._

**Astuce :** utilisez la **recherche** au-dessus de chaque tableau, et cliquez sur les **entêtes** pour trier.

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
      <td>2025-08-26</td>
      <td>469,00 €</td>
      <td>3 499,00 €</td>
      <td>1 288,17 €</td>
      <td>1 149,00 €</td>
      <td>499,00 €</td>
      <td>3 299,00 €</td>
      <td>1 276,25 €</td>
      <td>1 099,00 €</td>
      <td>30.0</td>
      <td>590.0</td>
      <td>150.72549</td>
      <td>130.0</td>
      <td>5.0</td>
      <td>20.0</td>
      <td>11.537255</td>
      <td>11.7</td>
      <td>145</td>
      <td>51</td>
      <td>35.2%</td>
      <td>{"2025-08": 2, "2025-09": 46, "2025-10": 26, "2025-11": 25, "2025-12": 10, "2026-01": 4, "2026-02": 8, "2026-03": 8, "2026-04": 1, "2026-05": 6, "2026-06": 3, "2026-07": 3, "2026-09": 1, "2026-10": 1, "2026-11": 1}</td>
    </tr>
  </tbody>
</table>
</div>

---

## Changements de prix (même date) — dernier vs précédent  (seuil: |Δ€| ≥ 0)
<p><em>Aucune donnée</em></p>

---

## Gros mouvements de prix (Δ% ≥ 10% ou Δ€ ≥ 150€)
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
      <td>2025-11-02</td>
      <td>2025-11-07</td>
      <td>https://www.weroad.fr/destinations/albanie-express-hiver/d1f93401-4d46-45aa-b657-214d5cc1ca4c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/albanie-express-hiver/d1f93401-4d46-45aa-b657-214d5cc1ca4c'>🔗</a></td>
    </tr>
    <tr>
      <td>Allemagne</td>
      <td>Allemagne</td>
      <td>Berlin Express</td>
      <td>649,00 €</td>
      <td>699,00 €</td>
      <td>50.0</td>
      <td>7.2%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
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
      <td><span class='rp-badge default'>WAITING</span></td>
      <td>2025-09-07</td>
      <td>2025-09-15</td>
      <td>https://www.weroad.fr/destinations/argentine-bresil-360/e6576e71-bb5e-4654-8395-479132600efd</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/argentine-bresil-360/e6576e71-bb5e-4654-8395-479132600efd'>🔗</a></td>
    </tr>
    <tr>
      <td>Patagonie</td>
      <td>Argentine</td>
      <td>Patagonie Trekking : aventure à travers l’Argentine et le Chili</td>
      <td>2 999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-10-28</td>
      <td>2025-11-09</td>
      <td>https://www.weroad.fr/destinations/patagonie-360/5857150e-6900-42bc-9490-3341afa4190e</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/patagonie-360/5857150e-6900-42bc-9490-3341afa4190e'>🔗</a></td>
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
      <td>890,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-23</td>
      <td>2025-12-28</td>
      <td>https://www.weroad.fr/destinations/bulgarie-ski-express-bansko/fe4a35e2-a5ee-47a5-b200-b1ca9e303e6d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bulgarie-ski-express-bansko/fe4a35e2-a5ee-47a5-b200-b1ca9e303e6d'>🔗</a></td>
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
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-19</td>
      <td>2025-10-28</td>
      <td>https://www.weroad.fr/destinations/cap-vert-beach-life-santiago-fogo-boa-vista/8b1e7e50-5a70-42f4-9885-6b4b762ceee8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/cap-vert-beach-life-santiago-fogo-boa-vista/8b1e7e50-5a70-42f4-9885-6b4b762ceee8'>🔗</a></td>
    </tr>
    <tr>
      <td>Chili et Bolivie</td>
      <td>Chili</td>
      <td>Chili et Bolivie : Aventure dans le Salar d'Uyuni</td>
      <td>1 999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-11</td>
      <td>2025-10-22</td>
      <td>https://www.weroad.fr/destinations/chili-bolivie-aventure-salar-uyuni/5514e1b5-d1c9-47a0-9bd9-918d9189cfe4</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/chili-bolivie-aventure-salar-uyuni/5514e1b5-d1c9-47a0-9bd9-918d9189cfe4'>🔗</a></td>
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
      <td>2026-11-20</td>
      <td>2026-12-01</td>
      <td>https://www.weroad.fr/destinations/chine/a01b1a11-a4b5-4767-b6d8-6d28e6c532b9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/chine/a01b1a11-a4b5-4767-b6d8-6d28e6c532b9'>🔗</a></td>
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
      <td>2025-11-23</td>
      <td>2025-12-04</td>
      <td>https://www.weroad.fr/destinations/colombie-360/16b572f8-f3b9-4e9c-9404-fb8c77dd80ab</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/colombie-360/16b572f8-f3b9-4e9c-9404-fb8c77dd80ab'>🔗</a></td>
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
      <td>2026-10-20</td>
      <td>2026-11-01</td>
      <td>https://www.weroad.fr/destinations/costa-rica-360/24c10910-4182-45e8-876a-370ccd2f1dff</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/costa-rica-360/24c10910-4182-45e8-876a-370ccd2f1dff'>🔗</a></td>
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
      <td>2026-02-14</td>
      <td>2026-02-21</td>
      <td>https://www.weroad.fr/destinations/fuerteventura-surf-weroadx/f6fde568-0c8e-4e19-8820-61d5b5b313e1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/fuerteventura-surf-weroadx/f6fde568-0c8e-4e19-8820-61d5b5b313e1'>🔗</a></td>
    </tr>
    <tr>
      <td>Gran Canaria</td>
      <td>Espagne</td>
      <td>Gran Canaria Beach Life Express : l’île du soleil</td>
      <td>599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-07-08</td>
      <td>2026-07-12</td>
      <td>https://www.weroad.fr/destinations/gran-canaria-express-ile-soleil/683f12d0-d741-45d3-80d9-8c7d2032290b</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/gran-canaria-express-ile-soleil/683f12d0-d741-45d3-80d9-8c7d2032290b'>🔗</a></td>
    </tr>
    <tr>
      <td>Îles Canaries</td>
      <td>Espagne</td>
      <td>Fuerteventura et Lanzarote  360° : entre plages et volcans</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-11</td>
      <td>2025-10-18</td>
      <td>https://www.weroad.fr/destinations/fuerteventura-lanzarote-plages-volcans/67e0eec3-90ff-4856-9dce-57691558b87d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/fuerteventura-lanzarote-plages-volcans/67e0eec3-90ff-4856-9dce-57691558b87d'>🔗</a></td>
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
      <td>2026-09-28</td>
      <td>2026-10-02</td>
      <td>https://www.weroad.fr/destinations/auvergne-express/ec34a251-229a-4b5d-be8c-855439805fa5</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/auvergne-express/ec34a251-229a-4b5d-be8c-855439805fa5'>🔗</a></td>
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
      <td>2026-03-07</td>
      <td>2026-03-11</td>
      <td>https://www.weroad.fr/destinations/bordeaux-dune-du-pilat/a23dc152-3886-4500-baa5-15933d8c2266</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bordeaux-dune-du-pilat/a23dc152-3886-4500-baa5-15933d8c2266'>🔗</a></td>
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
      <td>2025-11-19</td>
      <td>2025-11-23</td>
      <td>https://www.weroad.fr/destinations/bourgogne-express-route-grand-crus/dc2f4b00-102c-4305-9f1b-f18851bd24ca</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bourgogne-express-route-grand-crus/dc2f4b00-102c-4305-9f1b-f18851bd24ca'>🔗</a></td>
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
      <td>2026-07-25</td>
      <td>2026-07-29</td>
      <td>https://www.weroad.fr/destinations/bretagne-quiberon-belle-ile/5d5bea6a-d9c1-4759-884a-c3b5cae8e31c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bretagne-quiberon-belle-ile/5d5bea6a-d9c1-4759-884a-c3b5cae8e31c'>🔗</a></td>
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
      <td>2026-04-03</td>
      <td>2026-04-07</td>
      <td>https://www.weroad.fr/destinations/mediterranee-express-montpellier-sete-camargue/cb56f7b5-be01-40e8-a7de-e5daaa3c881d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/mediterranee-express-montpellier-sete-camargue/cb56f7b5-be01-40e8-a7de-e5daaa3c881d'>🔗</a></td>
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
      <td><span class='rp-badge default'>WAITING</span></td>
      <td>2025-09-13</td>
      <td>2025-09-20</td>
      <td>https://www.weroad.fr/destinations/crete-beach-life/151b04d2-e13f-421a-a398-abc9861657da</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/crete-beach-life/151b04d2-e13f-421a-a398-abc9861657da'>🔗</a></td>
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
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-10-01</td>
      <td>2025-10-12</td>
      <td>https://www.weroad.fr/destinations/guatemala-volcans-nature-cultures-anciennes/d474d722-e01f-4ed9-92c4-ae89a702a7f9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/guatemala-volcans-nature-cultures-anciennes/d474d722-e01f-4ed9-92c4-ae89a702a7f9'>🔗</a></td>
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
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-29</td>
      <td>2025-11-02</td>
      <td>https://www.weroad.fr/destinations/budapest-express/c2cdb0e5-7d03-447d-8cbe-c867b2e02c61</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/budapest-express/c2cdb0e5-7d03-447d-8cbe-c867b2e02c61'>🔗</a></td>
    </tr>
    <tr>
      <td>Hungary</td>
      <td>Hongrie</td>
      <td>Prague, Vienne et Budapest : édition Marchés de Noël</td>
      <td>949,00 €</td>
      <td>999,00 €</td>
      <td>50.0</td>
      <td>5.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-13</td>
      <td>2025-12-19</td>
      <td>https://www.weroad.fr/destinations/prague-budapest-marches-noel-weroadx/5f0863ec-25a3-42b2-9738-7bfb27a5e7ee</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/prague-budapest-marches-noel-weroadx/5f0863ec-25a3-42b2-9738-7bfb27a5e7ee'>🔗</a></td>
    </tr>
    <tr>
      <td>Inde</td>
      <td>Inde</td>
      <td>Inde : du Rajasthan au Taj Mahal</td>
      <td>949,00 €</td>
      <td>999,00 €</td>
      <td>50.0</td>
      <td>5.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-26</td>
      <td>2025-10-04</td>
      <td>https://www.weroad.fr/destinations/inde-rajasthan-taj-mahal/08c99925-1059-4f3a-9d34-a737157c5e11</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/inde-rajasthan-taj-mahal/08c99925-1059-4f3a-9d34-a737157c5e11'>🔗</a></td>
    </tr>
    <tr>
      <td>INDONÉSIE</td>
      <td>Indonésie</td>
      <td>Bali 360° : entre rizières, temples et plages paradisiaques</td>
      <td>849,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-06-03</td>
      <td>2026-06-10</td>
      <td>https://www.weroad.fr/destinations/bali-360/cc638763-0322-4393-bc0f-c6a217624507</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bali-360/cc638763-0322-4393-bc0f-c6a217624507'>🔗</a></td>
    </tr>
    <tr>
      <td>Indonesie</td>
      <td>Indonésie</td>
      <td>Indonésie d'île en île : Bali, Lembongan et Gili</td>
      <td>899,00 €</td>
      <td>1 099,00 €</td>
      <td>200.0</td>
      <td>18.2%</td>
      <td><span class='rp-badge default'>WAITING</span></td>
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
      <td>2026-03-03</td>
      <td>2026-03-08</td>
      <td>https://www.weroad.fr/destinations/irlande-express-tour-dublin-galway-connemara-weroadx/e0cd8b57-38b3-4c5b-86bc-d62707bc876b</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/irlande-express-tour-dublin-galway-connemara-weroadx/e0cd8b57-38b3-4c5b-86bc-d62707bc876b'>🔗</a></td>
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
      <td>Italie : Carnaval de Venise : Masques, féérie & aperitivo</td>
      <td>949,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-02-12</td>
      <td>2026-02-16</td>
      <td>https://www.weroad.fr/destinations/italie-carnaval-venise-masques-aperitivo/9d104808-b7d6-4ebe-b63a-6338d095d374</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/italie-carnaval-venise-masques-aperitivo/9d104808-b7d6-4ebe-b63a-6338d095d374'>🔗</a></td>
    </tr>
    <tr>
      <td>Naples & la côte Amalfitaine</td>
      <td>Italie</td>
      <td>Naples et la côte Amalfitaine Express</td>
      <td>489,00 €</td>
      <td>519,00 €</td>
      <td>30.0</td>
      <td>5.8%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-27</td>
      <td>2025-10-01</td>
      <td>https://www.weroad.fr/destinations/naples-cote-amalfitaine/d89f2758-79ec-4f9d-89c6-5bf9c0d317bc</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/naples-cote-amalfitaine/d89f2758-79ec-4f9d-89c6-5bf9c0d317bc'>🔗</a></td>
    </tr>
    <tr>
      <td>Pouilles</td>
      <td>Italie</td>
      <td>Pouilles 360°</td>
      <td>1 079,00 €</td>
      <td>1 349,00 €</td>
      <td>270.0</td>
      <td>20.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-27</td>
      <td>2025-10-04</td>
      <td>https://www.weroad.fr/destinations/pouilles-360/090b8ef2-dd13-4002-b1ef-9ec04e9a9907</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/pouilles-360/090b8ef2-dd13-4002-b1ef-9ec04e9a9907'>🔗</a></td>
    </tr>
    <tr>
      <td>Sardaigne</td>
      <td>Italie</td>
      <td>Sardaigne Beach Life : entre la Maddalena et la Costa Smeralda</td>
      <td>949,00 €</td>
      <td>999,00 €</td>
      <td>50.0</td>
      <td>5.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-26</td>
      <td>2025-10-03</td>
      <td>https://www.weroad.fr/destinations/sardaigne/5e78d21a-3663-46ac-b06f-518bb06c4cf7</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/sardaigne/5e78d21a-3663-46ac-b06f-518bb06c4cf7'>🔗</a></td>
    </tr>
    <tr>
      <td>Sicile</td>
      <td>Italie</td>
      <td>Sicile Beach Life : Favignana, San Vito lo Capo et la réserve de Zingaro</td>
      <td>949,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-09-12</td>
      <td>2025-09-19</td>
      <td>https://www.weroad.fr/destinations/sicile-favignana-san-vito-lo-capo-zingaro/ed3ff8f4-7f8d-4954-82d0-e24cc2d20fdf</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/sicile-favignana-san-vito-lo-capo-zingaro/ed3ff8f4-7f8d-4954-82d0-e24cc2d20fdf'>🔗</a></td>
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
      <td>899,00 €</td>
      <td>999,00 €</td>
      <td>100.0</td>
      <td>10.0%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-06</td>
      <td>2025-09-13</td>
      <td>https://www.weroad.fr/destinations/jordanie-360/afcab481-8862-453c-8b0b-df94fe52dce2</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/jordanie-360/afcab481-8862-453c-8b0b-df94fe52dce2'>🔗</a></td>
    </tr>
    <tr>
      <td>Kazakhstan</td>
      <td>Kazakhstan</td>
      <td>Kazakhstan 360° : Almaty, Turkestan et le désert de Mangystau en 4x4</td>
      <td>1 599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-11</td>
      <td>2025-10-19</td>
      <td>https://www.weroad.fr/destinations/kazakhstan-almaty-turkestan-desert-4x4/eb8f9a24-77ff-46e8-9d80-f2c28c5717b6</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kazakhstan-almaty-turkestan-desert-4x4/eb8f9a24-77ff-46e8-9d80-f2c28c5717b6'>🔗</a></td>
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
      <td>2025-11-23</td>
      <td>2025-12-02</td>
      <td>https://www.weroad.fr/destinations/kenya-afrique-safari-plage-village/47543c07-3a00-4029-913d-da11f9d9d789</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kenya-afrique-safari-plage-village/47543c07-3a00-4029-913d-da11f9d9d789'>🔗</a></td>
    </tr>
    <tr>
      <td>Kirghizistan</td>
      <td>Kirghizistan</td>
      <td>Kirghizistan Winter : entre lacs gelés et culture nomade</td>
      <td>1 049,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-28</td>
      <td>2025-10-06</td>
      <td>https://www.weroad.fr/destinations/kirghizistan-winter/541ca4fc-cf41-4cb7-9a5a-c599eb83b6f8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kirghizistan-winter/541ca4fc-cf41-4cb7-9a5a-c599eb83b6f8'>🔗</a></td>
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
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2026-02-08</td>
      <td>2026-02-15</td>
      <td>https://www.weroad.fr/destinations/maldives-beach-life-detente-snorkeling-maafushi/04c9b0b2-fc7f-4100-8174-58a62de3d2f6</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maldives-beach-life-detente-snorkeling-maafushi/04c9b0b2-fc7f-4100-8174-58a62de3d2f6'>🔗</a></td>
    </tr>
    <tr>
      <td>Malte</td>
      <td>Malte</td>
      <td>Malte Beach Life Express : Voyage sur les îles de Malte, Gozo et Comino</td>
      <td>639,00 €</td>
      <td>799,00 €</td>
      <td>160.0</td>
      <td>20.0%</td>
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
      <td>1 199,00 €</td>
      <td>1 329,00 €</td>
      <td>130.0</td>
      <td>9.8%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-02-22</td>
      <td>2026-03-01</td>
      <td>https://www.weroad.fr/destinations/ile-maurice-beach-life-road-trip-plages-aventure/16df8b33-89b1-43a4-ad3b-3cb1422e6475</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/ile-maurice-beach-life-road-trip-plages-aventure/16df8b33-89b1-43a4-ad3b-3cb1422e6475'>🔗</a></td>
    </tr>
    <tr>
      <td>Mexique</td>
      <td>Mexique</td>
      <td>Mexique Beach Life : de Cancun à Isla Mujeres, plage et détente</td>
      <td>1 399,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-01-03</td>
      <td>2026-01-10</td>
      <td>https://www.weroad.fr/destinations/mexique-yucatan-beach-life/0b25142d-a8c0-4876-b686-09a5a65c2bec</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/mexique-yucatan-beach-life/0b25142d-a8c0-4876-b686-09a5a65c2bec'>🔗</a></td>
    </tr>
    <tr>
      <td>Namibie</td>
      <td>Namibie</td>
      <td>Namibie 360°</td>
      <td>2 299,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-07-10</td>
      <td>2026-07-20</td>
      <td>https://www.weroad.fr/destinations/namibie/61f10893-a458-417d-a0ff-b8bc29bf418a</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/namibie/61f10893-a458-417d-a0ff-b8bc29bf418a'>🔗</a></td>
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
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-10-19</td>
      <td>2025-10-27</td>
      <td>https://www.weroad.fr/destinations/nepal/09858358-b277-4895-97c7-edb8b98ebe3e</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/nepal/09858358-b277-4895-97c7-edb8b98ebe3e'>🔗</a></td>
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
      <td>2026-05-10</td>
      <td>2026-05-22</td>
      <td>https://www.weroad.fr/destinations/philippines-360/d49cefea-e595-4b75-a68f-6dff13374c5a</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/philippines-360/d49cefea-e595-4b75-a68f-6dff13374c5a'>🔗</a></td>
    </tr>
    <tr>
      <td>Madère</td>
      <td>Portugal</td>
      <td>Madère 360° : l'île de la verdure et de l'aventure</td>
      <td>1 299,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-09-26</td>
      <td>2025-10-03</td>
      <td>https://www.weroad.fr/destinations/madere-360/34c660d6-804e-41f6-90bf-3cab644b7870</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/madere-360/34c660d6-804e-41f6-90bf-3cab644b7870'>🔗</a></td>
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
      <td>2025-11-06</td>
      <td>2025-11-10</td>
      <td>https://www.weroad.fr/destinations/portugal-express/5f928c79-9649-480e-9d9a-0bb5e3826de3</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/portugal-express/5f928c79-9649-480e-9d9a-0bb5e3826de3'>🔗</a></td>
    </tr>
    <tr>
      <td>le Portugal</td>
      <td>Portugal</td>
      <td>Portugal Beach Life : Lisbonne & Algarve</td>
      <td>1 119,00 €</td>
      <td>1 399,00 €</td>
      <td>280.0</td>
      <td>20.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-28</td>
      <td>2025-10-05</td>
      <td>https://www.weroad.fr/destinations/portugal-algarve-lisbonne/a8166e8a-3c9d-4ebe-9cb2-f8054daa5190</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/portugal-algarve-lisbonne/a8166e8a-3c9d-4ebe-9cb2-f8054daa5190'>🔗</a></td>
    </tr>
    <tr>
      <td>Pérou</td>
      <td>Pérou</td>
      <td>Pérou 360° : Machu Picchu, montagne arc-en-ciel et lac Titicaca</td>
      <td>1 699,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge default'>SOLD&nbsp;OUT</span></td>
      <td>2025-09-07</td>
      <td>2025-09-18</td>
      <td>https://www.weroad.fr/destinations/perou-360/1fbc1234-869a-4e05-8800-124e2b0432e3</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/perou-360/1fbc1234-869a-4e05-8800-124e2b0432e3'>🔗</a></td>
    </tr>
    <tr>
      <td>Romania</td>
      <td>Roumanie</td>
      <td>Transylvanie Express : Road Trip dans le pays du Comte Dracula</td>
      <td>469,00 €</td>
      <td>499,00 €</td>
      <td>30.0</td>
      <td>6.0%</td>
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
      <td>2025-09-25</td>
      <td>2025-09-29</td>
      <td>https://www.weroad.fr/destinations/Ecosse-express-edimbourg-highlands/6ff88504-1177-48bc-b5cc-932725dd1d79</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/Ecosse-express-edimbourg-highlands/6ff88504-1177-48bc-b5cc-932725dd1d79'>🔗</a></td>
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
      <td>1 950,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-02</td>
      <td>2025-11-11</td>
      <td>https://www.weroad.fr/destinations/senegal-entre-terre-et-fleuve/14011cbd-6e8f-4ca5-861c-5c389da9fbed</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/senegal-entre-terre-et-fleuve/14011cbd-6e8f-4ca5-861c-5c389da9fbed'>🔗</a></td>
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
      <td>1 099,00 €</td>
      <td>1 249,00 €</td>
      <td>150.0</td>
      <td>12.0%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
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
      <td>2026-01-15</td>
      <td>2026-01-24</td>
      <td>https://www.weroad.fr/destinations/thailande-plage-hiver/0aa75913-2a0b-4e4c-a3d9-fea3deb052a4</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/thailande-plage-hiver/0aa75913-2a0b-4e4c-a3d9-fea3deb052a4'>🔗</a></td>
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
      <td>569,00 €</td>
      <td>599,00 €</td>
      <td>30.0</td>
      <td>5.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-17</td>
      <td>2025-09-21</td>
      <td>https://www.weroad.fr/destinations/istanbul-express/78553c0f-2e64-4b94-bf07-152ba50a0bcb</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/istanbul-express/78553c0f-2e64-4b94-bf07-152ba50a0bcb'>🔗</a></td>
    </tr>
    <tr>
      <td>Istanbul & Cappadoce</td>
      <td>Turquie</td>
      <td>Turquie : un voyage d'Istanbul à la Cappadoce</td>
      <td>949,00 €</td>
      <td>999,00 €</td>
      <td>50.0</td>
      <td>5.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-19</td>
      <td>2025-09-26</td>
      <td>https://www.weroad.fr/destinations/istanbul-cappadoce/9f065672-d538-4d64-b27e-077f0e867b88</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/istanbul-cappadoce/9f065672-d538-4d64-b27e-077f0e867b88'>🔗</a></td>
    </tr>
    <tr>
      <td>Turquie</td>
      <td>Turquie</td>
      <td>Turquie 360° : Istanbul, Cappadoce et Éphèse</td>
      <td>1 349,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-05-01</td>
      <td>2026-05-09</td>
      <td>https://www.weroad.fr/destinations/turquie-istanbul-cappadoce-ephese/597a75fe-83b7-428f-8942-c5c5e6959ce1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/turquie-istanbul-cappadoce-ephese/597a75fe-83b7-428f-8942-c5c5e6959ce1'>🔗</a></td>
    </tr>
    <tr>
      <td>Vietnam</td>
      <td>Viêt Nam</td>
      <td>Vietnam 360° Backpack : de Hanoï à Hô Chi Minh</td>
      <td>1 049,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-03-07</td>
      <td>2026-03-16</td>
      <td>https://www.weroad.fr/destinations/vietnam-backpack/3fe8d53b-1989-4731-9c7c-30b8a01cd8f0</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/vietnam-backpack/3fe8d53b-1989-4731-9c7c-30b8a01cd8f0'>🔗</a></td>
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
      <td><span class='rp-badge default'>WAITING</span></td>
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
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-19</td>
      <td>2025-11-29</td>
      <td>https://www.weroad.fr/destinations/equateur-et-amazonie/cc3d1845-1f91-4944-9ee4-312a8ab36bf8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/equateur-et-amazonie/cc3d1845-1f91-4944-9ee4-312a8ab36bf8'>🔗</a></td>
    </tr>
    <tr>
      <td>Floride</td>
      <td>États-Unis d'Amérique</td>
      <td>Floride 360° : Orlando, Miami et Key West</td>
      <td>1 599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-09</td>
      <td>2025-11-18</td>
      <td>https://www.weroad.fr/destinations/floride/c763c529-259d-4aa7-a56d-eedb7277cd0d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/floride/c763c529-259d-4aa7-a56d-eedb7277cd0d'>🔗</a></td>
    </tr>
    <tr>
      <td>New York</td>
      <td>États-Unis d'Amérique</td>
      <td>New York 360° : à la découverte de Manhattan, Brooklyn et Harlem</td>
      <td>799,00 €</td>
      <td>999,00 €</td>
      <td>200.0</td>
      <td>20.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-28</td>
      <td>2025-10-03</td>
      <td>https://www.weroad.fr/destinations/new-york/be94222b-4570-4efc-abc5-e9fffca1ace0</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/new-york/be94222b-4570-4efc-abc5-e9fffca1ace0'>🔗</a></td>
    </tr>
    <tr>
      <td>Route 66</td>
      <td>États-Unis d'Amérique</td>
      <td>États-Unis : Road Trip sur la route 66 de Chicago à Los Angeles</td>
      <td>1 899,00 €</td>
      <td></td>
      <td>NaN</td>
      <td></td>
      <td><span class='rp-badge default'>SOLD&nbsp;OUT</span></td>
      <td>2025-09-12</td>
      <td>2025-09-26</td>
      <td>https://www.weroad.fr/destinations/road-trip-route-66-chicago-los-angeles/e6b8bddc-1bc1-4087-a6ba-dc460de73139</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/road-trip-route-66-chicago-los-angeles/e6b8bddc-1bc1-4087-a6ba-dc460de73139'>🔗</a></td>
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
      <td><span class='rp-badge default'>ALMOST_FULL</span></td>
      <td>2025-08-31</td>
      <td>https://www.weroad.fr/destinations/islande-expedition/5f3339d6-7b58-4a8f-a3cc-6b6194015a03</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/islande-expedition/5f3339d6-7b58-4a8f-a3cc-6b6194015a03'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-08</td>
      <td>Islande</td>
      <td>Islande 360° :  à la découverte de l'île de glace et de feu</td>
      <td>Islande</td>
      <td>1 479,00 €</td>
      <td>17.8%</td>
      <td><span class='rp-badge default'>SOLD&nbsp;OUT</span></td>
      <td>2025-08-29</td>
      <td>https://www.weroad.fr/destinations/islande-360-ete/383a8efe-d171-43f0-8c13-40ab3475ec83</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/islande-360-ete/383a8efe-d171-43f0-8c13-40ab3475ec83'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Romania</td>
      <td>Transylvanie Express : Road Trip dans le pays du Comte Dracula</td>
      <td>Roumanie</td>
      <td>469,00 €</td>
      <td>6.0%</td>
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
      <td>489,00 €</td>
      <td>5.8%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-27</td>
      <td>https://www.weroad.fr/destinations/naples-cote-amalfitaine/d89f2758-79ec-4f9d-89c6-5bf9c0d317bc</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/naples-cote-amalfitaine/d89f2758-79ec-4f9d-89c6-5bf9c0d317bc'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Maroc</td>
      <td>Maroc Express : Marrakech, Essaouira et le désert</td>
      <td>Maroc</td>
      <td>519,00 €</td>
      <td>20.0%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-23</td>
      <td>https://www.weroad.fr/destinations/maroc-marrakech-essaouira-desert/95e7a0a0-1110-4737-a411-b4b710b8dcd8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maroc-marrakech-essaouira-desert/95e7a0a0-1110-4737-a411-b4b710b8dcd8'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Istanbul</td>
      <td>Istanbul Express</td>
      <td>Turquie</td>
      <td>569,00 €</td>
      <td>5.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-17</td>
      <td>https://www.weroad.fr/destinations/istanbul-express/78553c0f-2e64-4b94-bf07-152ba50a0bcb</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/istanbul-express/78553c0f-2e64-4b94-bf07-152ba50a0bcb'>🔗</a></td>
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
      <td>Malte</td>
      <td>Malte Beach Life Express : Voyage sur les îles de Malte, Gozo et Comino</td>
      <td>Malte</td>
      <td>639,00 €</td>
      <td>20.0%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-19</td>
      <td>https://www.weroad.fr/destinations/malte-express-gozo-comino/562901ce-50c2-426f-9b47-479ea882d372</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/malte-express-gozo-comino/562901ce-50c2-426f-9b47-479ea882d372'>🔗</a></td>
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
      <td>Maroc</td>
      <td>Maroc 360° : du désert aux villes des mille et une nuits</td>
      <td>Maroc</td>
      <td>799,00 €</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-17</td>
      <td>https://www.weroad.fr/destinations/maroc/ac582f74-41af-464c-84e8-cb1ab505c18f</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maroc/ac582f74-41af-464c-84e8-cb1ab505c18f'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>New York</td>
      <td>New York 360° : à la découverte de Manhattan, Brooklyn et Harlem</td>
      <td>États-Unis d'Amérique</td>
      <td>799,00 €</td>
      <td>20.0%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-28</td>
      <td>https://www.weroad.fr/destinations/new-york/be94222b-4570-4efc-abc5-e9fffca1ace0</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/new-york/be94222b-4570-4efc-abc5-e9fffca1ace0'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Écosse</td>
      <td>Écosse Express : Édimbourg et les Highlands comme un local</td>
      <td>Royaume-Uni</td>
      <td>849,00 €</td>
      <td>5.6%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-25</td>
      <td>https://www.weroad.fr/destinations/Ecosse-express-edimbourg-highlands/6ff88504-1177-48bc-b5cc-932725dd1d79</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/Ecosse-express-edimbourg-highlands/6ff88504-1177-48bc-b5cc-932725dd1d79'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Jordanie</td>
      <td>Jordanie 360° : Petra, Amman et Wadi Rum</td>
      <td>Jordanie</td>
      <td>899,00 €</td>
      <td>10.0%</td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-06</td>
      <td>https://www.weroad.fr/destinations/jordanie-360/afcab481-8862-453c-8b0b-df94fe52dce2</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/jordanie-360/afcab481-8862-453c-8b0b-df94fe52dce2'>🔗</a></td>
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
      <td><span class='rp-badge default'>WAITING</span></td>
      <td>2025-09-05</td>
      <td>https://www.weroad.fr/destinations/indonesie-bali-lombok-java-nusa-penida/d0b065fd-904f-4676-97d6-44355c8075bb</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/indonesie-bali-lombok-java-nusa-penida/d0b065fd-904f-4676-97d6-44355c8075bb'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Hongrie</td>
      <td>Budapest Express</td>
      <td>Hongrie</td>
      <td>599,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-29</td>
      <td>https://www.weroad.fr/destinations/budapest-express/c2cdb0e5-7d03-447d-8cbe-c867b2e02c61</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/budapest-express/c2cdb0e5-7d03-447d-8cbe-c867b2e02c61'>🔗</a></td>
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
      <td>Italie</td>
      <td>Italie: Rome, le Chianti, Florence, Luques et Pise</td>
      <td>Italie</td>
      <td>999,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-10-26</td>
      <td>https://www.weroad.fr/destinations/rome-chianti-florence-luques-pise/bb439071-6ea1-4311-8017-092346b1aa36</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/rome-chianti-florence-luques-pise/bb439071-6ea1-4311-8017-092346b1aa36'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Népal</td>
      <td>Népal 360° : entre les temples de Katmandou et les sommets de l'Annapurna</td>
      <td>Népal</td>
      <td>999,00 €</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-10-19</td>
      <td>https://www.weroad.fr/destinations/nepal/09858358-b277-4895-97c7-edb8b98ebe3e</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/nepal/09858358-b277-4895-97c7-edb8b98ebe3e'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Îles Canaries</td>
      <td>Fuerteventura et Lanzarote  360° : entre plages et volcans</td>
      <td>Espagne</td>
      <td>999,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-11</td>
      <td>https://www.weroad.fr/destinations/fuerteventura-lanzarote-plages-volcans/67e0eec3-90ff-4856-9dce-57691558b87d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/fuerteventura-lanzarote-plages-volcans/67e0eec3-90ff-4856-9dce-57691558b87d'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Espagne</td>
      <td>Ibiza et Formentera Beach Life : aventure aux Baléares</td>
      <td>Espagne</td>
      <td>1 099,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-12</td>
      <td>https://www.weroad.fr/destinations/ibiza-formentera-baleares/3527020b-7f01-4028-a0c4-63035ed07ea9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/ibiza-formentera-baleares/3527020b-7f01-4028-a0c4-63035ed07ea9'>🔗</a></td>
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
      <td>2025-10</td>
      <td>Émirats Arabes Unis</td>
      <td>Émirats Arabes Unis 360° : Dubaï, Abou Dabi et le désert</td>
      <td>Émirats arabes unis</td>
      <td>1 199,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-10-17</td>
      <td>https://www.weroad.fr/destinations/dubai-abou-dhabi-desert/ea5c696d-41ec-4831-8b2e-65f6d10205f1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/dubai-abou-dhabi-desert/ea5c696d-41ec-4831-8b2e-65f6d10205f1'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Barcelone & Costa Brava</td>
      <td>Barcelone & Costa Brava Beach Life</td>
      <td>Espagne</td>
      <td>1 299,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-10-29</td>
      <td>https://www.weroad.fr/destinations/barcelone-costa-brava-360/821e1e1e-bdcb-442a-bf67-d1423fd2b452</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/barcelone-costa-brava-360/821e1e1e-bdcb-442a-bf67-d1423fd2b452'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Islande</td>
      <td>Islande : à la poursuite des aurores boréales</td>
      <td>Islande</td>
      <td>1 449,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-30</td>
      <td>https://www.weroad.fr/destinations/islande-aurores-boreales/7c8a9c13-6755-4bf5-921d-511c71054350</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/islande-aurores-boreales/7c8a9c13-6755-4bf5-921d-511c71054350'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Albanie</td>
      <td>Albanie Express Winter : histoire, nature et aventure</td>
      <td>Albanie</td>
      <td>549,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-02</td>
      <td>https://www.weroad.fr/destinations/albanie-express-hiver/d1f93401-4d46-45aa-b657-214d5cc1ca4c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/albanie-express-hiver/d1f93401-4d46-45aa-b657-214d5cc1ca4c'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Bourgogne</td>
      <td>Bourgogne Express : sur la route des Grands Crus</td>
      <td>France</td>
      <td>599,00 €</td>
      <td>7.7%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-19</td>
      <td>https://www.weroad.fr/destinations/bourgogne-express-route-grand-crus/dc2f4b00-102c-4305-9f1b-f18851bd24ca</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bourgogne-express-route-grand-crus/dc2f4b00-102c-4305-9f1b-f18851bd24ca'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Portugal</td>
      <td>Portugal Express</td>
      <td>Portugal</td>
      <td>699,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-11-06</td>
      <td>https://www.weroad.fr/destinations/portugal-express/5f928c79-9649-480e-9d9a-0bb5e3826de3</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/portugal-express/5f928c79-9649-480e-9d9a-0bb5e3826de3'>🔗</a></td>
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
      <td>Équateur & Amazonie</td>
      <td>Équateur & Amazonie Expedition</td>
      <td>Équateur</td>
      <td>1 299,00 €</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-19</td>
      <td>https://www.weroad.fr/destinations/equateur-et-amazonie/cc3d1845-1f91-4944-9ee4-312a8ab36bf8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/equateur-et-amazonie/cc3d1845-1f91-4944-9ee4-312a8ab36bf8'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Inde</td>
      <td>Inde 360° : Rajasthan, Agra et Varanasi</td>
      <td>Inde</td>
      <td>1 299,00 €</td>
      <td></td>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-01</td>
      <td>https://www.weroad.fr/destinations/inde-rajasthan-agra-varanasi/508c2831-dbf0-4b96-b9d5-ab7095a0f62b</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/inde-rajasthan-agra-varanasi/508c2831-dbf0-4b96-b9d5-ab7095a0f62b'>🔗</a></td>
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
      <td>Mexique</td>
      <td>Mexique 360° : à la découverte du Yucatán des Mayas</td>
      <td>Mexique</td>
      <td>1 549,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-03</td>
      <td>https://www.weroad.fr/destinations/mexique-yucatan-maya/42832fc4-b316-4127-a357-aa4e125dfd94</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/mexique-yucatan-maya/42832fc4-b316-4127-a357-aa4e125dfd94'>🔗</a></td>
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
      <td>Allemagne</td>
      <td>Berlin Express</td>
      <td>Allemagne</td>
      <td>649,00 €</td>
      <td>7.2%</td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-18</td>
      <td>https://www.weroad.fr/destinations/allemagne-berlin-express-tour-weroadx/e5d6c677-81fc-44be-abbf-d9589f0ebf6d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/allemagne-berlin-express-tour-weroadx/e5d6c677-81fc-44be-abbf-d9589f0ebf6d'>🔗</a></td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Bulgarie</td>
      <td>Bulgarie Ski Express : Bansko entre pistes, spa et fête !</td>
      <td>Bulgarie</td>
      <td>890,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2025-12-23</td>
      <td>https://www.weroad.fr/destinations/bulgarie-ski-express-bansko/fe4a35e2-a5ee-47a5-b200-b1ca9e303e6d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bulgarie-ski-express-bansko/fe4a35e2-a5ee-47a5-b200-b1ca9e303e6d'>🔗</a></td>
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
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-13</td>
      <td>https://www.weroad.fr/destinations/prague-budapest-marches-noel-weroadx/5f0863ec-25a3-42b2-9738-7bfb27a5e7ee</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/prague-budapest-marches-noel-weroadx/5f0863ec-25a3-42b2-9738-7bfb27a5e7ee'>🔗</a></td>
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
      <td>Thaïlande</td>
      <td>Thaïlande Beach Life Winter : Phuket, Krabi et Koh Lanta</td>
      <td>Thaïlande</td>
      <td>999,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-01-15</td>
      <td>https://www.weroad.fr/destinations/thailande-plage-hiver/0aa75913-2a0b-4e4c-a3d9-fea3deb052a4</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/thailande-plage-hiver/0aa75913-2a0b-4e4c-a3d9-fea3deb052a4'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Mexique</td>
      <td>Mexique Beach Life : de Cancun à Isla Mujeres, plage et détente</td>
      <td>Mexique</td>
      <td>1 399,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-01-03</td>
      <td>https://www.weroad.fr/destinations/mexique-yucatan-beach-life/0b25142d-a8c0-4876-b686-09a5a65c2bec</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/mexique-yucatan-beach-life/0b25142d-a8c0-4876-b686-09a5a65c2bec'>🔗</a></td>
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
      <td>Espagne</td>
      <td>Fuerteventura Surf : aventure à la découverte de l'île</td>
      <td>Espagne</td>
      <td>999,00 €</td>
      <td>9.1%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-02-14</td>
      <td>https://www.weroad.fr/destinations/fuerteventura-surf-weroadx/f6fde568-0c8e-4e19-8820-61d5b5b313e1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/fuerteventura-surf-weroadx/f6fde568-0c8e-4e19-8820-61d5b5b313e1'>🔗</a></td>
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
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2026-02-08</td>
      <td>https://www.weroad.fr/destinations/maldives-beach-life-detente-snorkeling-maafushi/04c9b0b2-fc7f-4100-8174-58a62de3d2f6</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maldives-beach-life-detente-snorkeling-maafushi/04c9b0b2-fc7f-4100-8174-58a62de3d2f6'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Maurice</td>
      <td>Île Maurice Beach Life : Road trip entre plages paradisiaques et aventure locale</td>
      <td>Maurice</td>
      <td>1 199,00 €</td>
      <td>9.8%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-02-22</td>
      <td>https://www.weroad.fr/destinations/ile-maurice-beach-life-road-trip-plages-aventure/16df8b33-89b1-43a4-ad3b-3cb1422e6475</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/ile-maurice-beach-life-road-trip-plages-aventure/16df8b33-89b1-43a4-ad3b-3cb1422e6475'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-02</td>
      <td>Thaïlande</td>
      <td>Thaïlande 360° Winter : Bangkok, Chiang Mai et les îles Phi Phi</td>
      <td>Thaïlande</td>
      <td>1 699,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-02-21</td>
      <td>https://www.weroad.fr/destinations/thailande-360-hiver/99b5e49e-0dbc-488b-b26f-ed8d56b9b3aa</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/thailande-360-hiver/99b5e49e-0dbc-488b-b26f-ed8d56b9b3aa'>🔗</a></td>
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
      <td>Bordeaux</td>
      <td>Bordeaux Express : de la Dune du Pilat à la pointe du Cap-Ferret</td>
      <td>France</td>
      <td>899,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-03-07</td>
      <td>https://www.weroad.fr/destinations/bordeaux-dune-du-pilat/a23dc152-3886-4500-baa5-15933d8c2266</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bordeaux-dune-du-pilat/a23dc152-3886-4500-baa5-15933d8c2266'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Irlande</td>
      <td>Irlande Express : Dublin, Galway et au Connemara</td>
      <td>Irlande</td>
      <td>999,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-03-03</td>
      <td>https://www.weroad.fr/destinations/irlande-express-tour-dublin-galway-connemara-weroadx/e0cd8b57-38b3-4c5b-86bc-d62707bc876b</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/irlande-express-tour-dublin-galway-connemara-weroadx/e0cd8b57-38b3-4c5b-86bc-d62707bc876b'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Vietnam</td>
      <td>Vietnam 360° Backpack : de Hanoï à Hô Chi Minh</td>
      <td>Viêt Nam</td>
      <td>1 049,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-03-07</td>
      <td>https://www.weroad.fr/destinations/vietnam-backpack/3fe8d53b-1989-4731-9c7c-30b8a01cd8f0</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/vietnam-backpack/3fe8d53b-1989-4731-9c7c-30b8a01cd8f0'>🔗</a></td>
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
      <td>Thaïlande</td>
      <td>Thaïlande Backpack Winter : Bangkok, Krabi et les îles Phi Phi</td>
      <td>Thaïlande</td>
      <td>1 249,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-03-05</td>
      <td>https://www.weroad.fr/destinations/thailande-hiver-expedition/7b9ecb87-8a57-472a-b61f-5cdcf8ab9d33</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/thailande-hiver-expedition/7b9ecb87-8a57-472a-b61f-5cdcf8ab9d33'>🔗</a></td>
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
      <td>France</td>
      <td>Méditerranée Beach Life Express : Montpellier, Sète et Camargue</td>
      <td>France</td>
      <td>599,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-04-03</td>
      <td>https://www.weroad.fr/destinations/mediterranee-express-montpellier-sete-camargue/cb56f7b5-be01-40e8-a7de-e5daaa3c881d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/mediterranee-express-montpellier-sete-camargue/cb56f7b5-be01-40e8-a7de-e5daaa3c881d'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>Népal</td>
      <td>Népal Trekking :  de Pokhara au camp de base de l'Annapurna</td>
      <td>Népal</td>
      <td>1 019,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-05-30</td>
      <td>https://www.weroad.fr/destinations/nepal-trekking/e4592ae4-0fd2-435c-b7e2-b49227eb1ce1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/nepal-trekking/e4592ae4-0fd2-435c-b7e2-b49227eb1ce1'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>Maldives</td>
      <td>Maldives Beach Life : aventure et découverte locale à Dharavandhoo</td>
      <td>Maldives</td>
      <td>1 299,00 €</td>
      <td>7.1%</td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-05-02</td>
      <td>https://www.weroad.fr/destinations/maldives-tour-plages-paradisiaques-dauphins-weroadx/1334bdff-066b-4d62-a883-ae514a869f20</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maldives-tour-plages-paradisiaques-dauphins-weroadx/1334bdff-066b-4d62-a883-ae514a869f20'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>Turquie</td>
      <td>Turquie 360° : Istanbul, Cappadoce et Éphèse</td>
      <td>Turquie</td>
      <td>1 349,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-05-01</td>
      <td>https://www.weroad.fr/destinations/turquie-istanbul-cappadoce-ephese/597a75fe-83b7-428f-8942-c5c5e6959ce1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/turquie-istanbul-cappadoce-ephese/597a75fe-83b7-428f-8942-c5c5e6959ce1'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>États-Unis</td>
      <td>Usa Rock'n Drive : d'Atlanta à la Nouvelle-Orléans en passant par Nashville et Memphis</td>
      <td>États-Unis d'Amérique</td>
      <td>1 699,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-05-29</td>
      <td>https://www.weroad.fr/destinations/usa-rock-n-drive/c7a1403c-b8fd-41c1-a1ab-f23bd497b6fe</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/usa-rock-n-drive/c7a1403c-b8fd-41c1-a1ab-f23bd497b6fe'>🔗</a></td>
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
      <td>Philippines</td>
      <td>Philippines 360° : Bohol, Coron & Palawan</td>
      <td>Philippines</td>
      <td>2 099,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-05-10</td>
      <td>https://www.weroad.fr/destinations/philippines-360/d49cefea-e595-4b75-a68f-6dff13374c5a</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/philippines-360/d49cefea-e595-4b75-a68f-6dff13374c5a'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>France</td>
      <td>Côte d’Azur Express : Nice, Monaco et leurs trésors</td>
      <td>France</td>
      <td>789,00 €</td>
      <td></td>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-06-24</td>
      <td>https://www.weroad.fr/destinations/cote-azur-express-france-nice-monaco/0361186f-ad97-4ac8-9ecd-db873c693a71</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/cote-azur-express-france-nice-monaco/0361186f-ad97-4ac8-9ecd-db873c693a71'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>INDONÉSIE</td>
      <td>Bali 360° : entre rizières, temples et plages paradisiaques</td>
      <td>Indonésie</td>
      <td>849,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-06-03</td>
      <td>https://www.weroad.fr/destinations/bali-360/cc638763-0322-4393-bc0f-c6a217624507</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bali-360/cc638763-0322-4393-bc0f-c6a217624507'>🔗</a></td>
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
      <td>Gran Canaria</td>
      <td>Gran Canaria Beach Life Express : l’île du soleil</td>
      <td>Espagne</td>
      <td>599,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-07-08</td>
      <td>https://www.weroad.fr/destinations/gran-canaria-express-ile-soleil/683f12d0-d741-45d3-80d9-8c7d2032290b</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/gran-canaria-express-ile-soleil/683f12d0-d741-45d3-80d9-8c7d2032290b'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-07</td>
      <td>Bretagne</td>
      <td>Bretagne Sud Beach Life : Quiberon et Belle-île-en-Mer</td>
      <td>France</td>
      <td>679,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-07-25</td>
      <td>https://www.weroad.fr/destinations/bretagne-quiberon-belle-ile/5d5bea6a-d9c1-4759-884a-c3b5cae8e31c</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/bretagne-quiberon-belle-ile/5d5bea6a-d9c1-4759-884a-c3b5cae8e31c'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-07</td>
      <td>Namibie</td>
      <td>Namibie 360°</td>
      <td>Namibie</td>
      <td>2 299,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-07-10</td>
      <td>https://www.weroad.fr/destinations/namibie/61f10893-a458-417d-a0ff-b8bc29bf418a</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/namibie/61f10893-a458-417d-a0ff-b8bc29bf418a'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-09</td>
      <td>Auvergne</td>
      <td>Auvergne Express : à la découverte du Sancy</td>
      <td>France</td>
      <td>549,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-09-28</td>
      <td>https://www.weroad.fr/destinations/auvergne-express/ec34a251-229a-4b5d-be8c-855439805fa5</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/auvergne-express/ec34a251-229a-4b5d-be8c-855439805fa5'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-10</td>
      <td>Costa Rica</td>
      <td>Costa Rica 360° : pura vida parmi les forêts tropicales</td>
      <td>Costa Rica</td>
      <td>1 799,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-10-20</td>
      <td>https://www.weroad.fr/destinations/costa-rica-360/24c10910-4182-45e8-876a-370ccd2f1dff</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/costa-rica-360/24c10910-4182-45e8-876a-370ccd2f1dff'>🔗</a></td>
    </tr>
    <tr>
      <td>2026-11</td>
      <td>Chine</td>
      <td>Chine 360° : Pékin, Shanghai et la Grande Muraille</td>
      <td>Chine</td>
      <td>1 899,00 €</td>
      <td></td>
      <td><span class='rp-badge on-sale'>PLANNED</span></td>
      <td>2026-11-20</td>
      <td>https://www.weroad.fr/destinations/chine/a01b1a11-a4b5-4767-b6d8-6d28e6c532b9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/chine/a01b1a11-a4b5-4767-b6d8-6d28e6c532b9'>🔗</a></td>
    </tr>
  </tbody>
</table>
</div>

---

## Watchlist — départs proches / confirmés
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
      <td>2025-09-17</td>
      <td>2025-09-21</td>
      <td>Istanbul Express</td>
      <td>Istanbul</td>
      <td>Turquie</td>
      <td>569,00 €</td>
      <td>5.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/istanbul-express/78553c0f-2e64-4b94-bf07-152ba50a0bcb</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/istanbul-express/78553c0f-2e64-4b94-bf07-152ba50a0bcb'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-19</td>
      <td>2025-09-26</td>
      <td>Turquie : un voyage d'Istanbul à la Cappadoce</td>
      <td>Istanbul & Cappadoce</td>
      <td>Turquie</td>
      <td>949,00 €</td>
      <td>5.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/istanbul-cappadoce/9f065672-d538-4d64-b27e-077f0e867b88</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/istanbul-cappadoce/9f065672-d538-4d64-b27e-077f0e867b88'>🔗</a></td>
    </tr>
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
      <td>2025-09-25</td>
      <td>2025-09-29</td>
      <td>Écosse Express : Édimbourg et les Highlands comme un local</td>
      <td>Écosse</td>
      <td>Royaume-Uni</td>
      <td>849,00 €</td>
      <td>5.6%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/Ecosse-express-edimbourg-highlands/6ff88504-1177-48bc-b5cc-932725dd1d79</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/Ecosse-express-edimbourg-highlands/6ff88504-1177-48bc-b5cc-932725dd1d79'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-26</td>
      <td>2025-10-04</td>
      <td>Inde : du Rajasthan au Taj Mahal</td>
      <td>Inde</td>
      <td>Inde</td>
      <td>949,00 €</td>
      <td>5.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/inde-rajasthan-taj-mahal/08c99925-1059-4f3a-9d34-a737157c5e11</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/inde-rajasthan-taj-mahal/08c99925-1059-4f3a-9d34-a737157c5e11'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-26</td>
      <td>2025-10-03</td>
      <td>Sardaigne Beach Life : entre la Maddalena et la Costa Smeralda</td>
      <td>Sardaigne</td>
      <td>Italie</td>
      <td>949,00 €</td>
      <td>5.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/sardaigne/5e78d21a-3663-46ac-b06f-518bb06c4cf7</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/sardaigne/5e78d21a-3663-46ac-b06f-518bb06c4cf7'>🔗</a></td>
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
      <td>2025-09-27</td>
      <td>2025-10-01</td>
      <td>Naples et la côte Amalfitaine Express</td>
      <td>Naples & la côte Amalfitaine</td>
      <td>Italie</td>
      <td>489,00 €</td>
      <td>5.8%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/naples-cote-amalfitaine/d89f2758-79ec-4f9d-89c6-5bf9c0d317bc</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/naples-cote-amalfitaine/d89f2758-79ec-4f9d-89c6-5bf9c0d317bc'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-27</td>
      <td>2025-10-04</td>
      <td>Pouilles 360°</td>
      <td>Pouilles</td>
      <td>Italie</td>
      <td>1 079,00 €</td>
      <td>20.0%</td>
      <td>NaN</td>
      <td>19.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/pouilles-360/090b8ef2-dd13-4002-b1ef-9ec04e9a9907</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/pouilles-360/090b8ef2-dd13-4002-b1ef-9ec04e9a9907'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-28</td>
      <td>2025-10-03</td>
      <td>New York 360° : à la découverte de Manhattan, Brooklyn et Harlem</td>
      <td>New York</td>
      <td>États-Unis d'Amérique</td>
      <td>799,00 €</td>
      <td>20.0%</td>
      <td>NaN</td>
      <td>11.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/new-york/be94222b-4570-4efc-abc5-e9fffca1ace0</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/new-york/be94222b-4570-4efc-abc5-e9fffca1ace0'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-28</td>
      <td>2025-10-06</td>
      <td>Kirghizistan Winter : entre lacs gelés et culture nomade</td>
      <td>Kirghizistan</td>
      <td>Kirghizistan</td>
      <td>1 049,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/kirghizistan-winter/541ca4fc-cf41-4cb7-9a5a-c599eb83b6f8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kirghizistan-winter/541ca4fc-cf41-4cb7-9a5a-c599eb83b6f8'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-09-28</td>
      <td>2025-10-05</td>
      <td>Portugal Beach Life : Lisbonne & Algarve</td>
      <td>le Portugal</td>
      <td>Portugal</td>
      <td>1 119,00 €</td>
      <td>20.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/portugal-algarve-lisbonne/a8166e8a-3c9d-4ebe-9cb2-f8054daa5190</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/portugal-algarve-lisbonne/a8166e8a-3c9d-4ebe-9cb2-f8054daa5190'>🔗</a></td>
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
      <td>2025-10-11</td>
      <td>2025-10-18</td>
      <td>Fuerteventura et Lanzarote  360° : entre plages et volcans</td>
      <td>Îles Canaries</td>
      <td>Espagne</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/fuerteventura-lanzarote-plages-volcans/67e0eec3-90ff-4856-9dce-57691558b87d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/fuerteventura-lanzarote-plages-volcans/67e0eec3-90ff-4856-9dce-57691558b87d'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-11</td>
      <td>2025-10-19</td>
      <td>Kazakhstan 360° : Almaty, Turkestan et le désert de Mangystau en 4x4</td>
      <td>Kazakhstan</td>
      <td>Kazakhstan</td>
      <td>1 599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/kazakhstan-almaty-turkestan-desert-4x4/eb8f9a24-77ff-46e8-9d80-f2c28c5717b6</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kazakhstan-almaty-turkestan-desert-4x4/eb8f9a24-77ff-46e8-9d80-f2c28c5717b6'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-11</td>
      <td>2025-10-22</td>
      <td>Chili et Bolivie : Aventure dans le Salar d'Uyuni</td>
      <td>Chili et Bolivie</td>
      <td>Chili</td>
      <td>1 999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>14.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/chili-bolivie-aventure-salar-uyuni/5514e1b5-d1c9-47a0-9bd9-918d9189cfe4</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/chili-bolivie-aventure-salar-uyuni/5514e1b5-d1c9-47a0-9bd9-918d9189cfe4'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-12</td>
      <td>2025-10-19</td>
      <td>Ibiza et Formentera Beach Life : aventure aux Baléares</td>
      <td>Espagne</td>
      <td>Espagne</td>
      <td>1 099,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/ibiza-formentera-baleares/3527020b-7f01-4028-a0c4-63035ed07ea9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/ibiza-formentera-baleares/3527020b-7f01-4028-a0c4-63035ed07ea9'>🔗</a></td>
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
      <td>Cap Vert : Santiago, Fogo et Boa Vista</td>
      <td>Cap-Vert</td>
      <td>Cap-Vert</td>
      <td>1 599,00 €</td>
      <td>5.9%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/cap-vert-beach-life-santiago-fogo-boa-vista/8b1e7e50-5a70-42f4-9885-6b4b762ceee8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/cap-vert-beach-life-santiago-fogo-boa-vista/8b1e7e50-5a70-42f4-9885-6b4b762ceee8'>🔗</a></td>
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
      <td>2025-10-29</td>
      <td>2025-11-02</td>
      <td>Budapest Express</td>
      <td>Hongrie</td>
      <td>Hongrie</td>
      <td>599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/budapest-express/c2cdb0e5-7d03-447d-8cbe-c867b2e02c61</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/budapest-express/c2cdb0e5-7d03-447d-8cbe-c867b2e02c61'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-10-30</td>
      <td>2025-11-06</td>
      <td>Islande : à la poursuite des aurores boréales</td>
      <td>Islande</td>
      <td>Islande</td>
      <td>1 449,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/islande-aurores-boreales/7c8a9c13-6755-4bf5-921d-511c71054350</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/islande-aurores-boreales/7c8a9c13-6755-4bf5-921d-511c71054350'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-02</td>
      <td>2025-11-11</td>
      <td>Sénégal :  Roadtrip entre terre et fleuve</td>
      <td>Sénégal</td>
      <td>Sénégal</td>
      <td>1 950,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/senegal-entre-terre-et-fleuve/14011cbd-6e8f-4ca5-861c-5c389da9fbed</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/senegal-entre-terre-et-fleuve/14011cbd-6e8f-4ca5-861c-5c389da9fbed'>🔗</a></td>
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
      <td>2025-11-23</td>
      <td>2025-12-02</td>
      <td>Kenya : au cœur de l'Afrique entre safaris, plages et villages locaux</td>
      <td>Kenya</td>
      <td>Kenya</td>
      <td>1 789,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/kenya-afrique-safari-plage-village/47543c07-3a00-4029-913d-da11f9d9d789</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/kenya-afrique-safari-plage-village/47543c07-3a00-4029-913d-da11f9d9d789'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-11-23</td>
      <td>2025-12-04</td>
      <td>Colombie 360° : Bogota, Medellin, Carthagène et parc Tayrona</td>
      <td>Colombie</td>
      <td>Colombie</td>
      <td>2 199,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/colombie-360/16b572f8-f3b9-4e9c-9404-fb8c77dd80ab</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/colombie-360/16b572f8-f3b9-4e9c-9404-fb8c77dd80ab'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2025-12-13</td>
      <td>2025-12-19</td>
      <td>Prague, Vienne et Budapest : édition Marchés de Noël</td>
      <td>Hungary</td>
      <td>Hongrie</td>
      <td>949,00 €</td>
      <td>5.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/prague-budapest-marches-noel-weroadx/5f0863ec-25a3-42b2-9738-7bfb27a5e7ee</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/prague-budapest-marches-noel-weroadx/5f0863ec-25a3-42b2-9738-7bfb27a5e7ee'>🔗</a></td>
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
      <td>2025-12-18</td>
      <td>2025-12-22</td>
      <td>Berlin Express</td>
      <td>Allemagne</td>
      <td>Allemagne</td>
      <td>649,00 €</td>
      <td>7.2%</td>
      <td>NaN</td>
      <td>11.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/allemagne-berlin-express-tour-weroadx/e5d6c677-81fc-44be-abbf-d9589f0ebf6d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/allemagne-berlin-express-tour-weroadx/e5d6c677-81fc-44be-abbf-d9589f0ebf6d'>🔗</a></td>
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
      <td>2026-04-03</td>
      <td>2026-04-07</td>
      <td>Méditerranée Beach Life Express : Montpellier, Sète et Camargue</td>
      <td>France</td>
      <td>France</td>
      <td>599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/mediterranee-express-montpellier-sete-camargue/cb56f7b5-be01-40e8-a7de-e5daaa3c881d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/mediterranee-express-montpellier-sete-camargue/cb56f7b5-be01-40e8-a7de-e5daaa3c881d'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge almost'>ALMOST</span></td>
      <td>2026-05-01</td>
      <td>2026-05-09</td>
      <td>Turquie 360° : Istanbul, Cappadoce et Éphèse</td>
      <td>Turquie</td>
      <td>Turquie</td>
      <td>1 349,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>17.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/turquie-istanbul-cappadoce-ephese/597a75fe-83b7-428f-8942-c5c5e6959ce1</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/turquie-istanbul-cappadoce-ephese/597a75fe-83b7-428f-8942-c5c5e6959ce1'>🔗</a></td>
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
      <td>2026-06-24</td>
      <td>2026-06-28</td>
      <td>Côte d’Azur Express : Nice, Monaco et leurs trésors</td>
      <td>France</td>
      <td>France</td>
      <td>789,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/cote-azur-express-france-nice-monaco/0361186f-ad97-4ac8-9ecd-db873c693a71</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/cote-azur-express-france-nice-monaco/0361186f-ad97-4ac8-9ecd-db873c693a71'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-06</td>
      <td>2025-09-13</td>
      <td>Jordanie 360° : Petra, Amman et Wadi Rum</td>
      <td>Jordanie</td>
      <td>Jordanie</td>
      <td>899,00 €</td>
      <td>10.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/jordanie-360/afcab481-8862-453c-8b0b-df94fe52dce2</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/jordanie-360/afcab481-8862-453c-8b0b-df94fe52dce2'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-11</td>
      <td>2025-09-22</td>
      <td>Thaïlande 360° Summer</td>
      <td>Thailande</td>
      <td>Thaïlande</td>
      <td>1 099,00 €</td>
      <td>12.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/thailande-360-ete/e3f05c52-64db-42c9-a457-8b25c6fb177e</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/thailande-360-ete/e3f05c52-64db-42c9-a457-8b25c6fb177e'>🔗</a></td>
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
      <td>2025-09-13</td>
      <td>2025-09-21</td>
      <td>Égypte 360° : des pyramides à la mer d'Hurgada</td>
      <td>Égypte</td>
      <td>Égypte</td>
      <td>1 079,00 €</td>
      <td>10.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/egypte-360/2d57b987-0463-465e-b916-636dd0cc50cf</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/egypte-360/2d57b987-0463-465e-b916-636dd0cc50cf'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-17</td>
      <td>2025-09-21</td>
      <td>Transylvanie Express : Road Trip dans le pays du Comte Dracula</td>
      <td>Romania</td>
      <td>Roumanie</td>
      <td>469,00 €</td>
      <td>6.0%</td>
      <td>NaN</td>
      <td>13.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/transylvanie-express-route-comte-dracula/8a2982d2-c24c-4361-8101-f6a4fbb9e5ef</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/transylvanie-express-route-comte-dracula/8a2982d2-c24c-4361-8101-f6a4fbb9e5ef'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-17</td>
      <td>2025-09-25</td>
      <td>Maroc 360° : du désert aux villes des mille et une nuits</td>
      <td>Maroc</td>
      <td>Maroc</td>
      <td>799,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/maroc/ac582f74-41af-464c-84e8-cb1ab505c18f</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maroc/ac582f74-41af-464c-84e8-cb1ab505c18f'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-09-19</td>
      <td>2025-09-24</td>
      <td>Malte Beach Life Express : Voyage sur les îles de Malte, Gozo et Comino</td>
      <td>Malte</td>
      <td>Malte</td>
      <td>639,00 €</td>
      <td>20.0%</td>
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
      <td>1 059,00 €</td>
      <td>11.7%</td>
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
      <td>2025-09-23</td>
      <td>2025-09-27</td>
      <td>Maroc Express : Marrakech, Essaouira et le désert</td>
      <td>Maroc</td>
      <td>Maroc</td>
      <td>519,00 €</td>
      <td>20.0%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/maroc-marrakech-essaouira-desert/95e7a0a0-1110-4737-a411-b4b710b8dcd8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maroc-marrakech-essaouira-desert/95e7a0a0-1110-4737-a411-b4b710b8dcd8'>🔗</a></td>
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
      <td>19.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/dolomites/cd862058-7484-4ee5-b21b-7152baf7951f</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/dolomites/cd862058-7484-4ee5-b21b-7152baf7951f'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-10-01</td>
      <td>2025-10-12</td>
      <td>Guatemala 360° : Voyage au pays des volcans, nature sauvage et cultures anciennes</td>
      <td>Guatemala</td>
      <td>Guatemala</td>
      <td>1 699,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/guatemala-volcans-nature-cultures-anciennes/d474d722-e01f-4ed9-92c4-ae89a702a7f9</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/guatemala-volcans-nature-cultures-anciennes/d474d722-e01f-4ed9-92c4-ae89a702a7f9'>🔗</a></td>
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
      <td>2025-10-19</td>
      <td>2025-10-27</td>
      <td>Népal 360° : entre les temples de Katmandou et les sommets de l'Annapurna</td>
      <td>Népal</td>
      <td>Népal</td>
      <td>999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/nepal/09858358-b277-4895-97c7-edb8b98ebe3e</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/nepal/09858358-b277-4895-97c7-edb8b98ebe3e'>🔗</a></td>
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
      <td>2025-10-28</td>
      <td>2025-11-09</td>
      <td>Patagonie Trekking : aventure à travers l’Argentine et le Chili</td>
      <td>Patagonie</td>
      <td>Argentine</td>
      <td>2 999,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/patagonie-360/5857150e-6900-42bc-9490-3341afa4190e</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/patagonie-360/5857150e-6900-42bc-9490-3341afa4190e'>🔗</a></td>
    </tr>
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2025-11-01</td>
      <td>2025-11-12</td>
      <td>Inde 360° : Rajasthan, Agra et Varanasi</td>
      <td>Inde</td>
      <td>Inde</td>
      <td>1 299,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/inde-rajasthan-agra-varanasi/508c2831-dbf0-4b96-b9d5-ab7095a0f62b</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/inde-rajasthan-agra-varanasi/508c2831-dbf0-4b96-b9d5-ab7095a0f62b'>🔗</a></td>
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
      <td>2025-11-09</td>
      <td>2025-11-18</td>
      <td>Floride 360° : Orlando, Miami et Key West</td>
      <td>Floride</td>
      <td>États-Unis d'Amérique</td>
      <td>1 599,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/floride/c763c529-259d-4aa7-a56d-eedb7277cd0d</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/floride/c763c529-259d-4aa7-a56d-eedb7277cd0d'>🔗</a></td>
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
      <td>2025-11-19</td>
      <td>2025-11-29</td>
      <td>Équateur & Amazonie Expedition</td>
      <td>Équateur & Amazonie</td>
      <td>Équateur</td>
      <td>1 299,00 €</td>
      <td></td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/equateur-et-amazonie/cc3d1845-1f91-4944-9ee4-312a8ab36bf8</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/equateur-et-amazonie/cc3d1845-1f91-4944-9ee4-312a8ab36bf8'>🔗</a></td>
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
    <tr>
      <td><span class='rp-badge confirmed'>CONFIRMED</span></td>
      <td>2026-02-08</td>
      <td>2026-02-15</td>
      <td>Maldives Beach Life BackPack : snorkeling et détente à Maafushi</td>
      <td>Maldives</td>
      <td>Maldives</td>
      <td>1 179,00 €</td>
      <td>5.6%</td>
      <td>NaN</td>
      <td>15.0</td>
      <td>None</td>
      <td>https://www.weroad.fr/destinations/maldives-beach-life-detente-snorkeling-maafushi/04c9b0b2-fc7f-4100-8174-58a62de3d2f6</td>
      <td><a target='_blank' href='https://www.weroad.fr/destinations/maldives-beach-life-detente-snorkeling-maafushi/04c9b0b2-fc7f-4100-8174-58a62de3d2f6'>🔗</a></td>
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
      <td>2025-08-26</td>
      <td>469,00 €</td>
      <td>1 149,00 €</td>
      <td>1 288,17 €</td>
      <td>145</td>
      <td>51</td>
      <td>35.2%</td>
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
      <td>1 239,00 €</td>
      <td>2</td>
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
      <td>Argentine</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
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
      <td>Crète</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
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
      <td>Grecia</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Inde</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
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
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Istanbul</td>
      <td>569,00 €</td>
      <td>569,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Istanbul & Cappadoce</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
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
      <td>899,00 €</td>
      <td>899,00 €</td>
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
      <td>Kirghizistan</td>
      <td>1 049,00 €</td>
      <td>1 269,50 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Madère</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Malaisie</td>
      <td>1 359,00 €</td>
      <td>1 359,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Malte</td>
      <td>639,00 €</td>
      <td>639,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Maroc</td>
      <td>479,00 €</td>
      <td>614,00 €</td>
      <td>4</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Naples & la côte Amalfitaine</td>
      <td>489,00 €</td>
      <td>489,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>New York</td>
      <td>799,00 €</td>
      <td>799,00 €</td>
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
      <td>Pouilles</td>
      <td>1 079,00 €</td>
      <td>1 079,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Pérou</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Romania</td>
      <td>469,00 €</td>
      <td>469,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Route 66</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Sardaigne</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Sicile</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
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
      <td>1 099,00 €</td>
      <td>1 099,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Vietnam</td>
      <td>1 059,00 €</td>
      <td>1 059,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>le Portugal</td>
      <td>1 119,00 €</td>
      <td>1 119,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Écosse</td>
      <td>849,00 €</td>
      <td>849,00 €</td>
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
      <td>Cap-Vert</td>
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
      <td>Espagne</td>
      <td>1 099,00 €</td>
      <td>1 099,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>France</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Guatemala</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Hongrie</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Islande</td>
      <td>1 449,00 €</td>
      <td>1 449,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Italie</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Kazakhstan</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
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
      <td>Patagonie</td>
      <td>2 999,00 €</td>
      <td>2 999,00 €</td>
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
      <td>Émirats Arabes Unis</td>
      <td>1 199,00 €</td>
      <td>1 199,00 €</td>
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
      <td>2025-10</td>
      <td>Îles Canaries</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Albanie</td>
      <td>549,00 €</td>
      <td>549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Autriche</td>
      <td>799,00 €</td>
      <td>799,00 €</td>
      <td>1</td>
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
      <td>Bourgogne</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
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
      <td>Floride</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
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
      <td>Jordanie</td>
      <td>1 249,00 €</td>
      <td>1 249,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Kenya</td>
      <td>1 789,00 €</td>
      <td>1 789,00 €</td>
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
      <td>Portugal</td>
      <td>699,00 €</td>
      <td>699,00 €</td>
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
      <td>Suède</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Sénégal</td>
      <td>1 950,00 €</td>
      <td>1 950,00 €</td>
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
      <td>2025-11</td>
      <td>Équateur & Amazonie</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Allemagne</td>
      <td>649,00 €</td>
      <td>649,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Bulgarie</td>
      <td>890,00 €</td>
      <td>890,00 €</td>
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
      <td>2026-01</td>
      <td>Finlande</td>
      <td>1 549,00 €</td>
      <td>1 549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Mexique</td>
      <td>1 399,00 €</td>
      <td>1 399,00 €</td>
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
      <td>Thaïlande</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
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
      <td>Espagne</td>
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
      <td>Maurice</td>
      <td>1 199,00 €</td>
      <td>1 199,00 €</td>
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
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Bordeaux</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
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
      <td>999,00 €</td>
      <td>1 149,00 €</td>
      <td>2</td>
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
      <td>Thaïlande</td>
      <td>1 249,00 €</td>
      <td>1 249,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Vietnam</td>
      <td>1 049,00 €</td>
      <td>1 049,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>France</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>Maldives</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
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
      <td>Philippines</td>
      <td>2 099,00 €</td>
      <td>2 099,00 €</td>
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
      <td>2026-05</td>
      <td>Turquie</td>
      <td>1 349,00 €</td>
      <td>1 349,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>États-Unis</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>France</td>
      <td>789,00 €</td>
      <td>789,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>INDONÉSIE</td>
      <td>849,00 €</td>
      <td>849,00 €</td>
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
      <td>Bretagne</td>
      <td>679,00 €</td>
      <td>679,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-07</td>
      <td>Gran Canaria</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-07</td>
      <td>Namibie</td>
      <td>2 299,00 €</td>
      <td>2 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-09</td>
      <td>Auvergne</td>
      <td>549,00 €</td>
      <td>549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-10</td>
      <td>Costa Rica</td>
      <td>1 799,00 €</td>
      <td>1 799,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-11</td>
      <td>Chine</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

## KPIs mensuels — Aperçu 24 derniers mois
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
      <td>1 239,00 €</td>
      <td>2</td>
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
      <td>Argentine</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
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
      <td>Crète</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
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
      <td>Grecia</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Inde</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
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
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Istanbul</td>
      <td>569,00 €</td>
      <td>569,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Istanbul & Cappadoce</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
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
      <td>899,00 €</td>
      <td>899,00 €</td>
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
      <td>Kirghizistan</td>
      <td>1 049,00 €</td>
      <td>1 269,50 €</td>
      <td>2</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Madère</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Malaisie</td>
      <td>1 359,00 €</td>
      <td>1 359,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Malte</td>
      <td>639,00 €</td>
      <td>639,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Maroc</td>
      <td>479,00 €</td>
      <td>614,00 €</td>
      <td>4</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Naples & la côte Amalfitaine</td>
      <td>489,00 €</td>
      <td>489,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>New York</td>
      <td>799,00 €</td>
      <td>799,00 €</td>
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
      <td>Pouilles</td>
      <td>1 079,00 €</td>
      <td>1 079,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Pérou</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Romania</td>
      <td>469,00 €</td>
      <td>469,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Route 66</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Sardaigne</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Sicile</td>
      <td>949,00 €</td>
      <td>949,00 €</td>
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
      <td>1 099,00 €</td>
      <td>1 099,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Vietnam</td>
      <td>1 059,00 €</td>
      <td>1 059,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>le Portugal</td>
      <td>1 119,00 €</td>
      <td>1 119,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-09</td>
      <td>Écosse</td>
      <td>849,00 €</td>
      <td>849,00 €</td>
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
      <td>Cap-Vert</td>
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
      <td>Espagne</td>
      <td>1 099,00 €</td>
      <td>1 099,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>France</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Guatemala</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Hongrie</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Islande</td>
      <td>1 449,00 €</td>
      <td>1 449,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Italie</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-10</td>
      <td>Kazakhstan</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
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
      <td>Patagonie</td>
      <td>2 999,00 €</td>
      <td>2 999,00 €</td>
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
      <td>Émirats Arabes Unis</td>
      <td>1 199,00 €</td>
      <td>1 199,00 €</td>
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
      <td>2025-10</td>
      <td>Îles Canaries</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Albanie</td>
      <td>549,00 €</td>
      <td>549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Autriche</td>
      <td>799,00 €</td>
      <td>799,00 €</td>
      <td>1</td>
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
      <td>Bourgogne</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
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
      <td>Floride</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
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
      <td>Jordanie</td>
      <td>1 249,00 €</td>
      <td>1 249,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Kenya</td>
      <td>1 789,00 €</td>
      <td>1 789,00 €</td>
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
      <td>Portugal</td>
      <td>699,00 €</td>
      <td>699,00 €</td>
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
      <td>Suède</td>
      <td>1 599,00 €</td>
      <td>1 599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-11</td>
      <td>Sénégal</td>
      <td>1 950,00 €</td>
      <td>1 950,00 €</td>
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
      <td>2025-11</td>
      <td>Équateur & Amazonie</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Allemagne</td>
      <td>649,00 €</td>
      <td>649,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2025-12</td>
      <td>Bulgarie</td>
      <td>890,00 €</td>
      <td>890,00 €</td>
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
      <td>2026-01</td>
      <td>Finlande</td>
      <td>1 549,00 €</td>
      <td>1 549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-01</td>
      <td>Mexique</td>
      <td>1 399,00 €</td>
      <td>1 399,00 €</td>
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
      <td>Thaïlande</td>
      <td>999,00 €</td>
      <td>999,00 €</td>
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
      <td>Espagne</td>
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
      <td>Maurice</td>
      <td>1 199,00 €</td>
      <td>1 199,00 €</td>
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
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Bordeaux</td>
      <td>899,00 €</td>
      <td>899,00 €</td>
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
      <td>999,00 €</td>
      <td>1 149,00 €</td>
      <td>2</td>
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
      <td>Thaïlande</td>
      <td>1 249,00 €</td>
      <td>1 249,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-03</td>
      <td>Vietnam</td>
      <td>1 049,00 €</td>
      <td>1 049,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-04</td>
      <td>France</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>Maldives</td>
      <td>1 299,00 €</td>
      <td>1 299,00 €</td>
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
      <td>Philippines</td>
      <td>2 099,00 €</td>
      <td>2 099,00 €</td>
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
      <td>2026-05</td>
      <td>Turquie</td>
      <td>1 349,00 €</td>
      <td>1 349,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-05</td>
      <td>États-Unis</td>
      <td>1 699,00 €</td>
      <td>1 699,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>France</td>
      <td>789,00 €</td>
      <td>789,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-06</td>
      <td>INDONÉSIE</td>
      <td>849,00 €</td>
      <td>849,00 €</td>
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
      <td>Bretagne</td>
      <td>679,00 €</td>
      <td>679,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-07</td>
      <td>Gran Canaria</td>
      <td>599,00 €</td>
      <td>599,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-07</td>
      <td>Namibie</td>
      <td>2 299,00 €</td>
      <td>2 299,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-09</td>
      <td>Auvergne</td>
      <td>549,00 €</td>
      <td>549,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-10</td>
      <td>Costa Rica</td>
      <td>1 799,00 €</td>
      <td>1 799,00 €</td>
      <td>1</td>
    </tr>
    <tr>
      <td>2026-11</td>
      <td>Chine</td>
      <td>1 899,00 €</td>
      <td>1 899,00 €</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>
