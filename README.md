# Kenetik Growth System — Dashboards

Public GitHub Pages surfaces mirroring live data from the private
`kenetik-growth-system` repo. Every deployed surface here must be registered
in that repo's `architecture/reporting/surface-registry.md` (+ `.json`) —
`validate-dashboard.yml`'s surface-registry gate fails the build otherwise.

## Dashboards

- **[Creator Hub](creator-hub.html)** — public creator/ambassador landing page (fed by `data/creator-hub-data.json`, this repo's own).
- **[Kenetik Network Viewer](kenetik-network-viewer.html)** — Mermaid network diagrams of KGS roles/processes (`pending-retirement-decision` — Devon to decide).
- **[ChangeSet Dashboard](changeset-dashboard.html)** / **[Website Experiment Dashboard](website-experiment-dashboard.html)** — redirect stubs. Rebuilt in the `kenetik-growth-system` portal (`portal/changesets.html`, `portal/experiments.html`) and folded into the board-portal deploy (P7-T9). The github.io URLs still resolve.

**Retired 2026-07-13 (P7-T9):** the ChangeSet + Website-Experiment dashboards moved into the kgs portal; their cross-repo syncs (`sync-tracker-to-dashboards.yml`, `sync-website-state-to-dashboards.yml`, `sync-clarity-to-dashboards.yml`) are retired and the data they fed (`data/changeset-*.json`, `data/website-state.json`, `data/clarity/`, `data/auto-optimize/`, `data/briefs/`) was deleted from this repo (P7-T10) — git history is the archive.

**Retired 2026-07-13:** the KGS Virtual Team Dashboard (`kenetik-growth-system-dashboard.html`) — Devon's call, the underlying 12-role/98-process framing is obsolete. Removed from `surface-registry.md`/`.json` and this repo; its validator (`validate-dashboard.py`) and pre-commit hook (`install-hooks.sh`) removed with it. `system-state.json` / `system-state-definitions.json` are left in the repo (orphaned — no remaining reader) pending Devon's call on whether to delete them too.

## How This Stays Updated

- `surface-registry.json` here is a manual mirror of `kenetik-growth-system`'s canonical `architecture/reporting/surface-registry.json`. The automated mirror sync was retired P7-T9 — edit rows in kgs and re-copy; never edit them here.
- `creator-hub-data.json` is this repo's own (public creator landing page). The reporting surfaces that used to sync here now live in the kgs portal and read kgs-native files.
- The source of truth lives in the private `kenetik-growth-system` repo; this public repo now hosts only the redirect stubs, the creator hub, and the network viewer.
