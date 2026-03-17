# Kenetik Growth System — Dashboards

Live operational dashboards for the Kenetik Growth System. Auto-published via GitHub Pages whenever a process is built or a status is updated.

## Dashboards

- **[KGS System Dashboard](kenetik-growth-system-dashboard.html)** — Full system state: process statuses, infrastructure connections, build patterns
- **[Marketing & Content Calendar](marketing-calendar-dashboard.html)** — Campaign timeline, content calendar, content mix targets, platform cadence, inline editing
- **[ChangeSet Dashboard](changeset-dashboard.html)** — ChangeSet pipeline status and tracking
- **[Network Viewer](kenetik-network-viewer.html)** — KGS process network visualization

## How This Stays Updated

Dashboard updates are pushed automatically at the end of every `/build` and `/update-status` session in the Kenetik Growth System plugin. The source of truth lives in the private `kenetik-growth-system` repo; this public repo mirrors only the rendered dashboards.

### Marketing Calendar Data

The marketing calendar dashboard loads data from `data/marketing-calendar-data.json`. To update:
1. Export the Google Sheet as .xlsx
2. Run the conversion (or update the JSON manually)
3. Commit the updated JSON to the `data/` folder
