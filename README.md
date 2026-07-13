# Kenetik Growth System — Dashboards

Public GitHub Pages surfaces mirroring live data from the private
`kenetik-growth-system` repo. Every deployed surface here must be registered
in that repo's `architecture/reporting/surface-registry.md` (+ `.json`) —
`validate-dashboard.yml`'s surface-registry gate fails the build otherwise.

## Dashboards

- **[ChangeSet Dashboard](changeset-dashboard.html)** — ChangeSet pipeline: tracker statuses, work queue, impact rollup.
- **[Website Experiment Dashboard](website-experiment-dashboard.html)** — Auto-optimize experiment state, Clarity snapshots, website-state trends.
- **[Kenetik Network Viewer](kenetik-network-viewer.html)** — Mermaid network diagrams of KGS roles/processes (`pending-retirement-decision` — Devon to decide).

**Retired 2026-07-13:** the KGS Virtual Team Dashboard (`kenetik-growth-system-dashboard.html`) — Devon's call, the underlying 12-role/98-process framing is obsolete. Removed from `surface-registry.md`/`.json` and this repo; its validator (`validate-dashboard.py`) and pre-commit hook (`install-hooks.sh`) removed with it. `system-state.json` / `system-state-definitions.json` are left in the repo (orphaned — no remaining reader) pending Devon's call on whether to delete them too.

## How This Stays Updated

- ChangeSet Dashboard data syncs via `sync-tracker-to-dashboards.yml` (source repo).
- Website Experiment Dashboard data syncs via `sync-clarity-to-dashboards.yml` / `sync-website-state-to-dashboards.yml` (source repo).
- `surface-registry.json` here is a pure sync target mirrored from `kenetik-growth-system`'s `architecture/reporting/surface-registry.json` — never edit it directly in this repo.
- The source of truth for all of the above lives in the private `kenetik-growth-system` repo; this public repo mirrors only the rendered dashboards and their data.
