# KGS Learning Log (v2.1.1)

Record of everything the KGS has learned from team feedback, ChangeSet outcomes, and operational signals. Active entries maintained by Process 3.8; acted-on entries archived weekly. Index layer enables bandwidth-aware reads across all consumers.

## Files

- `cross-surface-pm.json` — The learning log. Contains an `index` (fast-read summaries), `entries` (active learnings), and `archived_entries` (codified learnings preserved for audit).
- `pdp-atc.md` — Surface-specific experiment log for PDP Add-to-Cart optimization (written by the autonomous optimization loop, independent of the learning log).

## Structure of cross-surface-pm.json

```
config              — evidence thresholds, archive policy, synthesis cadence
index[]             — one line per learning (~150 chars): id, summary, domain, status, date
                      READ THIS for daily synthesis and contradiction checks
entries[]           — full detail for active (un-acted) learnings
                      READ THIS for Process 3.8 weekly review and skill file proposals
archived_entries[]  — full detail for codified learnings (action_taken populated, live ≥7 days)
                      READ THIS only during monthly calibration audits
```

**Read discipline:** Daily synthesis reads the index only. Process 3.8 reads entries (active) for weekly review. Monthly calibration reads all arrays for staleness and closed-loop checks.

**Documented `archived_reason` values** (2026-07-11): `acted_on` (action_taken populated ≥7d — the normal codified path, archived by the weekly cron), `expired_unactioned` (>90d, no action — Q1 policy), `closed_without_measurement` (no-learning lifecycle CS closes, archived on write), `merged_into_L-NNN` (consolidation judge absorbed the entry), `resolved_wont_act` (a human ruled via `🚫 L-NNN <reason>` that no action is warranted — resolution-without-action is a legitimate closure; the reply is preserved in `resolution_note`).

**Write discipline:** Writers append a new entry to `entries` AND a corresponding one-line summary to `index` (status: "active"). Process 3.8 moves acted-on entries from `entries` to `archived_entries` and updates index status to "archived".

## How It Works

**Signal capture (daily, during pipeline run):**
Synthesis Step 9a-9c scans Slack and domain briefs for learning signals — team corrections, contradictions, consistent outperformance, cross-domain convergence. Signals are formatted as `LEARNING SIGNAL:` blocks in the synthesis output.

**Signal write (daily, Task B orchestrator):**
Task B Step 5b parses `LEARNING SIGNAL:` blocks from the synthesis output, constructs entries with proper field mappings, and writes them to `cross-surface-pm.json` (both `entries` and `index` arrays). This is the actual write path — synthesis captures signals, Task B commits them.

**ChangeSet outcome capture (on every close):**
Every ChangeSet close — whether auto-closed by the sweep or manually closed — appends a `changeset_outcome` entry and index line. This is a universal writeback, not variance-gated. Closes with >20% variance ALSO emit a separate `LEARNING SIGNAL` for cross-domain synthesis, but the baseline outcome entry is written regardless. See `/changeset-lifecycle-sweep` Step 3C and `brain/kenetik-brain/references/system-architecture.md` §2 for rationale.

**Weekly consolidation + synthesis (Fridays, Process 3.8):**
Step 0 consolidates the log: merges related entries, archives acted-on entries (live ≥7 days with action_taken populated), prunes evidence bloat (>200 chars → source pointers), flags contradictions. Then reviews active entries, clusters them, and proposes skill file updates through the governance path (Rapid / Regular / Governance).

**Skeptical retrieval principle:**
Learning log entries are working hypotheses, not established truth. If fresh domain data directly contradicts a logged learning, the contradiction takes precedence and is flagged as a new signal. The log informs decisions; it does not override data.

## Entry Types

- `skill_update` — Decision rules destined for skill files
- `process_change` — Operational instruction changes (may become ChangeSets)
- `threshold_calibration` — Numeric tuning that requires measurement before commit
- `changeset_outcome` — Auto-appended when any ChangeSet closes (includes outcome_class and variance_pct)

## Domain Field Convention

The `domain` field is free-text. Writers should use one of the recommended values when possible:
`paid-media`, `content`, `lifecycle`, `website`, `campaigns`, `operations`, `cross-surface`.

New values can emerge as the system evolves (e.g., "amazon" when that channel activates).

Each department's instruction file defines which domain keywords it matches on — that's the
authoritative routing. Readers use keyword/contains matching, not exact equality, so entries
with non-standard domains still get picked up if they contain relevant terms.

## Writing Evidence

Evidence fields should be 1-2 sentences plus a source pointer. Do not duplicate session handoff narratives or Slack thread contents — point to where the detail lives.

Good: `"Fix C restructuring tree requires ATC + checkout rate at campaign level. Polar has these (infra spec §4.1). See session-handoff-2026-04-02."`

Bad: a 3-line forensic narrative copying information from the session handoff.

## Governed By

- Performance Memory Architecture Build Spec v1.0 (authoritative reference)
- Operations Intelligence spec §9 (System Learning Protocol)
- Creative Intelligence spec §6.8 (Two-Path Learning Architecture — Path 2)

## Implemented By

- `cgo-daily-pipeline/config/synthesis-instructions.md` — Step 9a-9c (signal detection + formatting)
- `cgo-daily-pipeline/config/task-b-synthesis.md` — Step 5b (signal write to JSON)
- `kenetik-growth-system/commands/synthesize-learnings.md` — Process 3.8 (weekly consolidation + synthesis)
- `scripts/pm_maintain.py` — the deterministic Friday passes run by `.github/workflows/pm-weekly-cron.yml`: `outcomes` (one `changeset_outcome` entry per closed ChangeSet), `graduate` (DL-T8 wedge-insight graduation — rules in `scripts/insight_graduation.py`; a paid-media hypothesis CONFIRMED at its measured close, or a wedge dossier conclusion past this store's own `config.evidence_thresholds` bar, becomes a `skill_update` entry with `source_type: "wedge_insight"`), `actions` (citation collector), `archive` (Q1 policy) and `candidates` (proposals for the judge above). Every write goes through `scripts/pm_write_gate.py`.
- `kenetik-growth-system/commands/changeset-lifecycle-sweep.md` — Step 3C (baseline `changeset_outcome` entry on every close, including manual closes since last sweep)
- `kenetik-growth-system/commands/changeset-measurement.md` — Step 8 (variance-based `LEARNING SIGNAL` emission when |variance| > 20%)
- `kenetik-growth-system/commands/monthly-calibration.md` — Section 3 (monthly validation)

## What Does NOT Go Here

Raw metrics (→ paid-media-state.json, Polar), creative performance scores (→ Moe's weekly synthesis at `cgo-logs/queues/performance-memory.json`), ChangeSet tracker entries (→ tracker.json), experiment raw results (→ results.tsv). Only interpretive insights belong in the learning log.

## Design Principle: Two Layers, Not One

Raw performance data stays in domain-specific stores — Larry's social PM, website experiment TSVs, Polar paid media metrics, Klaviyo email metrics. Each domain owns its data and uses it for domain-specific decisions.

The Learning Log sits above those. It captures *what we learned* (surprises, corrections, cross-domain insights), not *what we measured*. Process 3.8 is the governor between the two layers — it reads the Learning Log and proposes skill file updates when evidence accumulates. No raw data goes directly into skill files without synthesis.

## Design Principle: Bandwidth Awareness

The context window is a scarce resource. The Learning Log is structured so that consumers load only what they need:

- **Daily synthesis** reads the `index` array (~150 chars per learning) to check for contradictions and deduplication. It never needs full evidence narratives during the pipeline run.
- **Process 3.8** reads `entries` (active only) for weekly proposals. It skips `archived_entries` — those learnings are already codified in skill files.
- **Monthly calibration** is the only process that reads all arrays, for staleness review and closed-loop validation.

If the Learning Log grows beyond ~50 active entries, revisit whether the index is still sufficient for daily synthesis or whether domain-scoped filtering is needed.

## Signal Flow

How a learning moves from origin to skill file update. File paths at each stage.

### 1. Signal Capture (daily)

| Source | Where it happens | What triggers it |
|---|---|---|
| Team corrections | `cgo-daily-pipeline/config/synthesis-instructions.md` Step 9a | Slack messages containing ❌, "actually", "wrong", "stop", "don't" |
| Domain brief contradictions | Step 9b | A domain brief contradicts yesterday's brief or a current skill file rule |
| DATA_UNAVAILABLE flags | Step 9b | A domain reports missing data that another domain expected |
| Consistent outperformance | Step 9b | A strategy meets or exceeds targets for 4+ consecutive weeks |
| Cross-domain convergence | Step 9b | Same trend in 3+ domain briefs on the same day |
| ChangeSet close (baseline) | `kenetik-growth-system/commands/changeset-lifecycle-sweep.md` Step 3C | Every close — writes baseline `changeset_outcome` entry regardless of variance |
| ChangeSet variance (learning) | `kenetik-growth-system/commands/changeset-measurement.md` Step 8 | >20% variance from projection — additionally emits a `LEARNING SIGNAL` for synthesis |

**Before capturing:** Synthesis reads the `index` array (not full entries) from `cross-surface-pm.json` to check for duplicates and corroboration. If a signal matches an existing index entry, it's noted as evidence bump rather than a new signal.

Signals are formatted as `LEARNING SIGNAL:` blocks in the synthesis output (Step 9c).

### 1b. Signal Write (daily, Task B orchestrator)

`cgo-daily-pipeline/config/task-b-synthesis.md` Step 5b

Task B parses the `LEARNING SIGNAL:` blocks from synthesis output and writes them to `cross-surface-pm.json`:
- Finds the highest L-NNN in the index, increments for new entries
- Maps Step 9c fields → entry fields (Source→source, Signal→learning, Type→type, Domain→domain, Confidence→confidence, Root cause→evidence, Target→target)
- Infers `source_type`: team_feedback (from Slack), operational_signal (from domain brief), domain_contradiction (brief conflicts)
- Appends to both `entries` and `index` arrays
- Pushes independently (if synthesis contains `LEARNING SIGNALS: 0 new today.` — skips this step)

All signals land in → `data/performance-memory/cross-surface-pm.json` (entry + index line)

### 2. Weekly Consolidation + Synthesis (Fridays)

`kenetik-growth-system/commands/synthesize-learnings.md` (Process 3.8)

**Step 0 — Consolidate:** Merge related entries, archive acted-on entries, prune evidence bloat, flag contradictions.

**Then:** Read active entries. Cluster related learnings. Route proposals through three tiers:
- **Rapid** (≤2 business days): Wording fixes, threshold nudges within guardrails
- **Regular** (next weekly review): New rules, removed rules, process changes
- **Governance** (monthly calibration): Cross-role changes, guardrail adjustments

Publishes "How I Got Smarter" report to Slack with ❌ feedback path.

### 3. Monthly Validation

`kenetik-growth-system/commands/monthly-calibration.md` Section 3 (Learning System Health)

- Did last month's learnings improve outcomes? (closed-loop check)
- Stale entries older than 90 days — still valid?
- Evidence quality — are anecdotal signals reaching moderate confidence without corroboration?

### 4. Domain-Specific Stores (separate layer)

These are NOT the Learning Log. They hold raw performance data used for domain-specific decisions.

| Store | Path | Owner |
|---|---|---|
| Weekly social synthesis | `cgo-logs/queues/performance-memory.json` | Moe |
| Website experiment results | `data/performance-memory/pdp-atc.md` + `pdp-atc-results.tsv` | Website optimization loop |

Domain stores feed the Learning Log only through synthesis (Step 9) when a domain-specific pattern becomes a cross-domain insight.

## Known Gaps and Weaknesses (as of 2026-04-05)

Evaluated against the system's intention: maximize autonomous learning rate.

**1. ~~Two parallel learning store specifications.~~** RESOLVED 2026-04-04. Learning Record Log references across 6 files consolidated to point to this Learning Log.

**2. The system learns mostly from failures, not from consistent success.** Both signal sources are reactive — >20% ChangeSet variance catches surprises, Slack corrections catch errors. Consistent positive performance never generates a signal. The system should also capture "what to keep doing," not just "what to stop doing wrong."

**3. No cross-domain pattern detection across domain-specific stores.** If the same trend appears across Larry's social PM, paid media, and website experiments simultaneously, nothing aggregates that. The Learning Log only captures what synthesis or humans happen to notice.

**4. Process 3.8 weekly batch creates a minimum ~7-10 day learning-to-action delay.** Larry's auto-apply (≤100% hook weight changes) is the only sub-week path. The weekly cadence is appropriate for the current volume. Revisit if volume grows and rapid-tier items are waiting unnecessarily.

**5. ~~No closed-loop validation that learnings improved outcomes.~~** PARTIALLY ADDRESSED 2026-04-05. Skeptical retrieval principle means fresh data contradicting a learning generates a signal. Monthly calibration checks whether skill file updates improved outcomes. Full closed-loop (automated tracking of post-update performance) remains a gap.

**6. Evidence thresholds are count-based, not quality-weighted.** Moderate threshold refined to require 3 entries from 2+ independent sources (not just 3 entries). Monthly calibration reviews whether low-quality signals are reaching moderate confidence without corroboration.

**7. "How I Got Smarter" report has no structured feedback path.** If the CGO disagrees with a learning, the correction depends on a Slack message with keywords that Step 9a catches the next day. A structured "flag as wrong" mechanism would close this loop faster.

**8. ~~No learning expiration or confidence decay.~~** ADDRESSED 2026-04-05. Process 3.8 weekly consolidation archives acted-on entries. Monthly calibration reviews entries older than 90 days for staleness.

**9. Moe's creative synthesis is siloed to social data.** Moe does the most sophisticated pattern analysis in the system but only sees Larry's Sprout Social data. Other domains lack an equivalent analytical layer.

**10. No direct Larry → Learning Log path (by design).** Larry's social patterns enter the Learning Log only through synthesis when they represent cross-domain insight. Monitor whether synthesis is actually catching important social learnings like the TikTok direct-benefit reversal.

**11. ~~Log grows without consolidation (append-only).~~** ADDRESSED 2026-04-05. v2.1 replaces append-only constraint with weekly consolidation in Process 3.8 (merge related entries, archive acted-on, prune evidence bloat). Index layer provides bandwidth-aware reads.

**12. ~~No explicit write path from synthesis to JSON.~~** ADDRESSED 2026-04-05. Synthesis instructions captured learning signals in output text but the Task B orchestrator had no step to write them to `cross-surface-pm.json`. Step 5b now handles the full write path with field mapping, ID generation, and independent push.
