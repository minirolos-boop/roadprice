---
title: RoadPrice — Accueil
---

# RoadPrice — synthèse

<!-- Simple-DataTables (CDN) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/simple-datatables@9.0.3/dist/style.min.css">
<script src="https://cdn.jsdelivr.net/npm/simple-datatables@9.0.3"></script>

<style>
/* Supprimer l'aspect "carte/rectangle" du wrapper Simple-DataTables */
.dataTable-wrapper,
.dataTable-wrapper .dataTable-container { background: transparent !important; border: 0 !important; box-shadow: none !important; padding: 0 !important; }
.dataTable-top, .dataTable-bottom { background: transparent !important; border: none !important; box-shadow: none !important; padding: .25rem 0 !important; }
.dataTable-info, .dataTable-pagination, .dataTable-dropdown, .dataTable-search { margin: .35rem 0 !important; font-size: .95rem !important; }
.dataTable-pagination a { border-radius: .4rem !important; }

/* Conserver le scroll horizontal du conteneur .table-wrapper */
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
    const v = parseFloat(s);
    return isNaN(v) ? null : v;
  };

  ready(() => {
    const tables = document.querySelectorAll("table.rp-table");
    tables.forEach((tbl, tIndex) => {
      try {
        const dt = new simpleDatatables.DataTable(tbl, {
          searchable: true,
          fixedHeight: false,
          perPage: 25,
          perPageSelect: [10, 25, 50, 100],
          labels: {
            placeholder: "Rechercher…",
            perPage: "{select} lignes par page",
            noRows: "Aucune donnée",
            info: "Affiche {start}–{end} sur {rows} lignes",
          },
        });

        // tri custom € / %
        try {
          dt.columns().each((idx) => {
            const header = tbl.tHead && tbl.tHead.rows && tbl.tHead.rows[0] && tbl.tHead.rows[0].cells
              ? tbl.tHead.rows[0].cells[idx] : null;
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
        } catch(e) {
          console.warn("Sorter setup error on table", tIndex, e);
        }
      } catch (e) {
        console.warn("DataTable init failed on table", tIndex, e);
      }
    });
  });
})();
</script>

![run](https://img.shields.io/badge/run-2025-08-26-blue) ![build](https://img.shields.io/badge/build-2025-08-26 20:37 UTC-success)

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

## Changements de prix (même date) — dernier vs précédent
<p><em>Aucune donnée</em></p>

---

## Gros mouvements de prix (Δ% ≥ 10% ou Δ€ ≥ 150€) — sur le panier “meilleur prix par destination”
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/afrique-du-sud-cap-safari-parc-kruger'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/albanie-express-hiver'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/allemagne-berlin-express-tour-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/argentine-bresil-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/patagonie-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/australie-de-sydney-a-brisbane'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/autriche-kitzbuhel-ski-snowboard'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bruxelles-amsterdam-express-culture'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/belize-jungles-plages-blue-hole'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bolivie-et-chili-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bresil-mer-plage-foret-rio-de-janeiro'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bulgarie-ski-express-bansko'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/laos-cambodge-routes-temples-indochine'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/canada-quebec-montreal-toronto-niagara'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/cap-vert-beach-life-santiago-fogo-boa-vista'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/chili-bolivie-aventure-salar-uyuni'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/chine'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/colombie-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/coree-du-sud-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/costa-rica-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/cuba-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/barcelone-costa-brava-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/fuerteventura-surf-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/gran-canaria-express-ile-soleil'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/fuerteventura-lanzarote-plages-volcans'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/pays-baltes-tallinn-riga-vilnius'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/laponie-finlandaise'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/auvergne-express'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bordeaux-dune-du-pilat'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bourgogne-express-route-grand-crus'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bretagne-quiberon-belle-ile'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/mediterranee-express-montpellier-sete-camargue'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/corfou-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/crete-beach-life'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/grece-360-athenes-meteores-peloponnese'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/guatemala-volcans-nature-cultures-anciennes'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/georgie-caucase-ski-snowboard'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/budapest-express'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/prague-budapest-marches-noel-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/inde-rajasthan-taj-mahal'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bali-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/indonesie-bali-lombok-java-nusa-penida'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bali-gili-indonesie-tropicale-eau-turquoise'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/irlande-express-tour-dublin-galway-connemara-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/islande-express'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/dolomites'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/italie-carnaval-venise-masques-aperitivo'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/naples-cote-amalfitaine'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/pouilles-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/sardaigne'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/sicile-favignana-san-vito-lo-capo-zingaro'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/japon-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/jordanie-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/kazakhstan-almaty-turkestan-desert-4x4'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/kenya-afrique-safari-plage-village'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/kirghizistan-winter'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/malaisie-nature-ile'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/maldives-beach-life-detente-snorkeling-maafushi'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/malte-express-gozo-comino'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/maroc-trekking-mount-toubkal'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/ile-maurice-beach-life-road-trip-plages-aventure'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/mexique-yucatan-beach-life'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/namibie'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/nicaragua-aventure-lacs-volcans'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/norvege-lofoten-aurore-boreales'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/nouvelle-zelande-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/nepal'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/oman'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/ouzbekistan-tachkent-samarkand-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/panama-beach-life-san-blas-bocas-del-toro'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/philippines-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/madere-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/portugal-express'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/portugal-algarve-lisbonne'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/perou-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/transylvanie-express-route-comte-dracula'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/Ecosse-express-edimbourg-highlands'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/ile-reunion-cirques-volcan-plages'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/slovenie-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/sri-lanka-360-ete'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/suisse-express-alpes-lacs-montagnes'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/suede-lulea-laponie'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/senegal-entre-terre-et-fleuve'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/kilimandjaro-trekking-lemosho-route-safari'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/europe-prague-vienne-budapest-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/thailande-360-ete'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/thailande-plage-hiver'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/tunisie-express-djerba-detente-culture'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/istanbul-express'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/istanbul-cappadoce'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/turquie-istanbul-cappadoce-ephese'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/vietnam-backpack'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/le-caire-express-egypt'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/dubai-abou-dhabi-desert'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/equateur-galapogos-amazonie'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/equateur-et-amazonie'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/floride'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/new-york'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/road-trip-route-66-chicago-los-angeles'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/far-west-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/islande-expedition'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/islande-360-ete'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/transylvanie-express-route-comte-dracula'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/maroc-trekking-mount-toubkal'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/naples-cote-amalfitaine'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/maroc-marrakech-essaouira-desert'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/istanbul-express'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/albanie-tirana-plages-sud'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/malte-express-gozo-comino'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/maroc-marrakech-fes-rabat-desert'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/corfou-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/maroc'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/new-york'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/Ecosse-express-edimbourg-highlands'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/jordanie-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/sri-lanka-360-ete'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/indonesie-bali-lombok-java-nusa-penida'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/budapest-express'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/tunisie-express-djerba-detente-culture'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/europe-prague-vienne-budapest-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/chateaux-loire-express-blois-amboise-tours'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/pays-baltes-tallinn-riga-vilnius'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/suisse-express-alpes-lacs-montagnes'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/rome-chianti-florence-luques-pise'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/nepal'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/fuerteventura-lanzarote-plages-volcans'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/ibiza-formentera-baleares'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/maroc-surf-ocean-desert'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/sicile-palerme-san-vito'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/dubai-abou-dhabi-desert'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/barcelone-costa-brava-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/islande-aurores-boreales'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/albanie-express-hiver'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bourgogne-express-route-grand-crus'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/portugal-express'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/paris-disneyland-express-entre-culture-vasion-et-magie'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bruxelles-amsterdam-express-culture'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/alpe-d-huez-express-ski-snowboard'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/autriche-kitzbuhel-ski-snowboard'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bali-gili-indonesie-tropicale-eau-turquoise'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/sri-lanka-360-hiver'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/oman'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/jordanie-trekking'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/equateur-et-amazonie'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/inde-rajasthan-agra-varanasi'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/indonesie-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/mexique-yucatan-maya'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/le-caire-express-egypt'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/allemagne-berlin-express-tour-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bulgarie-ski-express-bansko'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/georgie-caucase-ski-snowboard'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/prague-budapest-marches-noel-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/ile-reunion-cirques-volcan-plages'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/norvege-lofoten-aurore-boreales'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/suede-lulea-laponie'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/panama-beach-life-san-blas-bocas-del-toro'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/kilimandjaro-trekking-lemosho-route-safari'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/thailande-plage-hiver'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/mexique-yucatan-beach-life'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/nicaragua-aventure-lacs-volcans'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/laponie-finlandaise'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/italie-carnaval-venise-masques-aperitivo'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/fuerteventura-surf-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/ouzbekistan-hiver'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/maldives-beach-life-detente-snorkeling-maafushi'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/ile-maurice-beach-life-road-trip-plages-aventure'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/thailande-360-hiver'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/japon-ski-snowboard'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bresil-carnaval-rio-salvador-fiesta-plages'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/islande-express'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bordeaux-dune-du-pilat'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/irlande-express-tour-dublin-galway-connemara-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/vietnam-backpack'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/malaisie-nature-ile'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/thailande-hiver-expedition'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/irlande-tour-saint-patrick'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/laos-cambodge-routes-temples-indochine'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/mediterranee-express-montpellier-sete-camargue'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/nepal-trekking'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/maldives-tour-plages-paradisiaques-dauphins-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/turquie-istanbul-cappadoce-ephese'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/usa-rock-n-drive'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/acores-sao-miguel-faial-terceira'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/philippines-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/cote-azur-express-france-nice-monaco'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bali-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/thailande-ete-expedition'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/gran-canaria-express-ile-soleil'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bretagne-quiberon-belle-ile'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/namibie'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/auvergne-express'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/costa-rica-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/chine'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/istanbul-express'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/istanbul-cappadoce'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/albanie-tirana-plages-sud'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/Ecosse-express-edimbourg-highlands'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/inde-rajasthan-taj-mahal'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/sardaigne'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/maroc-trekking-mount-toubkal'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/naples-cote-amalfitaine'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/pouilles-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/new-york'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/kirghizistan-winter'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/portugal-algarve-lisbonne'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/sicile-palerme-san-vito'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/europe-prague-vienne-budapest-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/fuerteventura-lanzarote-plages-volcans'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/kazakhstan-almaty-turkestan-desert-4x4'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/chili-bolivie-aventure-salar-uyuni'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/ibiza-formentera-baleares'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/tunisie-express-djerba-detente-culture'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/belize-jungles-plages-blue-hole'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/colombie-aventure-amazonie-caraibes-san-andres'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/turquie-on-the-road'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/cap-vert-beach-life-santiago-fogo-boa-vista'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/suisse-express-alpes-lacs-montagnes'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/pays-baltes-tallinn-riga-vilnius'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/budapest-express'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/islande-aurores-boreales'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/senegal-entre-terre-et-fleuve'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/mexique-yucatan-maya'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/paris-disneyland-express-entre-culture-vasion-et-magie'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/chine-pekin-hong-kong-grande-muraille-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/jordanie-trekking'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/mexique-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/kenya-afrique-safari-plage-village'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/colombie-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/prague-budapest-marches-noel-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/ile-reunion-cirques-volcan-plages'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/allemagne-berlin-express-tour-weroadx'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/kilimandjaro-trekking-lemosho-route-safari'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/panama-beach-life-san-blas-bocas-del-toro'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/norvege-lofoten-aurore-boreales'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/nicaragua-aventure-lacs-volcans'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bresil-carnaval-rio-salvador-fiesta-plages'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/italie-carnaval-venise-masques-aperitivo'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/laos-cambodge-routes-temples-indochine'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/malaisie-nature-ile'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/mediterranee-express-montpellier-sete-camargue'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/turquie-istanbul-cappadoce-ephese'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/acores-sao-miguel-faial-terceira'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/cote-azur-express-france-nice-monaco'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/jordanie-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/thailande-360-ete'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/maroc-marrakech-fes-rabat-desert'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/egypte-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/transylvanie-express-route-comte-dracula'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/maroc'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/malte-express-gozo-comino'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/vietnam'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/cuba-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/maroc-marrakech-essaouira-desert'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/japon-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/dolomites'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/guatemala-volcans-nature-cultures-anciennes'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bresil-mer-plage-foret-rio-de-janeiro'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/nepal'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/far-west-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/patagonie-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/inde-rajasthan-agra-varanasi'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/bolivie-et-chili-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/oman'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/floride'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/indonesie-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/nouvelle-zelande-360'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/equateur-et-amazonie'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/vietnam-cambodge'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/sri-lanka-360-hiver'>🔗</a></td>
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
      <td><a target='_blank' href='https://www.weroad.fr/voyages/maldives-beach-life-detente-snorkeling-maafushi'>🔗</a></td>
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
