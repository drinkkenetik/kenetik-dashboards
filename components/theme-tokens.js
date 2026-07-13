/* ============================================================
   VENDORED COPY — canonical source is kenetik-growth-system:
     portal/components/theme-tokens.js
   Kept in sync manually (same pattern as the P5-T4 nav vendoring).
   Do NOT edit here; change it in KGS and re-copy. Vendored for
   Phase 6A (design-system unification), 2026-07-13.
   ============================================================ */
/* [P6A-T1] Shared chart tokens — one visual language for every portal chart.
   Exposes the chart palette + Chart.js defaults so all surfaces' charts match
   the Board Intelligence Portal (the reference surface). Colors are READ from
   the CSS custom properties in components/portal-theme.css (single source of
   truth) with hard fallbacks, so this file never re-declares a hex the theme
   owns. Presentation only — NO chart data/series logic lives here.

   Usage:
     <link rel="stylesheet" href="components/portal-theme.css">
     <script src="components/theme-tokens.js"></script>
     ...
     KTOKENS.applyChartDefaults(Chart);      // once, after Chart.js loads
     new Chart(ctx, { data: { datasets:[{ borderColor: KTOKENS.palette.blue, ... }] }});

   Self-contained (no build step); safe to vendor into kenetik-dashboards. */
(function (root) {
  var css = (typeof getComputedStyle === 'function' && typeof document !== 'undefined')
    ? getComputedStyle(document.documentElement) : null;
  var tok = function (name, fallback) {
    var v = css ? (css.getPropertyValue(name) || '').trim() : '';
    return v || fallback;
  };

  // Palette — mirrors the board portal COLORS map (P5-T1), token-sourced.
  var palette = {
    blue:       tok('--blue', '#2E6BE6'),
    berry:      tok('--berry', '#D0148C'),
    violet:     tok('--violet', '#7A2BD0'),
    ok:         tok('--ok', '#1FA463'),
    attn:       tok('--attn', '#F5821F'),
    bad:        tok('--bad', '#E0322B'),
    pineapple:  tok('--pineapple', '#FBB11B'),
    muted:      tok('--muted', '#9A9BA6'),
    deep:       tok('--deep', '#1E1230'),
    ink:        tok('--ink', '#16161D'),
    line:       tok('--line', 'rgba(20,20,32,.12)')
  };

  // Ordered series colors for multi-series charts (matches board portal order).
  var series = [palette.blue, palette.berry, palette.violet, palette.ok,
                palette.attn, palette.pineapple, palette.bad, palette.muted];

  // Chart.js global defaults so fonts/grids/tooltips are consistent everywhere.
  function applyChartDefaults(Chart) {
    if (!Chart || !Chart.defaults) return;
    var d = Chart.defaults;
    d.font = d.font || {};
    d.font.family = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";
    d.font.size = 12;
    d.color = palette.ink;
    if (d.plugins && d.plugins.legend && d.plugins.legend.labels) {
      d.plugins.legend.labels.color = palette.ink;
      d.plugins.legend.labels.boxWidth = 12;
      d.plugins.legend.labels.usePointStyle = true;
    }
    if (d.plugins && d.plugins.tooltip) {
      var t = d.plugins.tooltip;
      t.backgroundColor = palette.deep;
      t.titleColor = '#fff'; t.bodyColor = '#fff';
      t.cornerRadius = 8; t.padding = 10; t.displayColors = true;
    }
    if (d.scale && d.scale.grid) d.scale.grid.color = palette.line;
    if (d.scales) { /* Chart v3+ reads per-axis grid from options; left to callers */ }
  }

  root.KTOKENS = { palette: palette, series: series, applyChartDefaults: applyChartDefaults };
})(typeof window !== 'undefined' ? window : this);
