// docs/assets/js/enhance-tables.js
document.addEventListener("DOMContentLoaded", () => {
  // convertir "1 234,56 €" -> 1234.56 pour tri numérique
  const euroToNumber = (txt) => {
    if (!txt) return null;
    const s = String(txt).replace(/\s/g, "").replace("€", "").replace(/\u00A0/g, "").replace(",", ".");
    const v = parseFloat(s);
    return isNaN(v) ? null : v;
  };

  document.querySelectorAll("table.rp-table").forEach((tbl) => {
    const dt = new simpleDatatables.DataTable(tbl, {
      searchable: true,
      // IMPORTANT: on désactive la hauteur fixe pour éviter le "cadre" avec scroll interne
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

    // Ajoute une classe sur le wrapper pour pouvoir désactiver le style "carte"
    const wrapper = tbl.closest(".dataTable-wrapper");
    if (wrapper) wrapper.classList.add("rp-dt-unstyled");

    // Règles de tri personnalisées pour colonnes € et %
    dt.columns().each((idx) => {
      const header = tbl.tHead?.rows?.[0]?.cells?.[idx];
      if (!header) return;
      const htxt = header.textContent.toLowerCase();
      const isMoney = /(€|price|prix|delta_abs)/.test(htxt);
      const isPct   = /(pct|%)/.test(htxt);

      if (isMoney || isPct) {
        dt.columns().sort(idx, (a, b) => {
          // supprime éventuelles balises html (badges, liens)
          const ta = a.replace(/<[^>]*>/g, "");
          const tb = b.replace(/<[^>]*>/g, "");
          const na = isPct ? parseFloat(ta.replace("%", "").replace(",", ".")) : euroToNumber(ta);
          const nb = isPct ? parseFloat(tb.replace("%", "").replace(",", ".")) : euroToNumber(tb);
          if (na == null && nb == null) return 0;
          if (na == null) return -1;
          if (nb == null) return 1;
          return na - nb;
        });
      }
    });
  });
});
