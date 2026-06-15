# Performance Memory — pdp-atc

> Auto-updated by the autonomous optimization loop after each experiment cycle.
> This file accumulates patterns the agent has learned about what works and what doesn't
> on the Product Detail Page for Add-to-Cart rate optimization.
>
> **Do not edit manually** — the agent appends to this file after each keep/discard decision.
> Devon reviews patterns during the monthly calibration ceremony (Process 1.3).

## Surface Info

- **Surface**: pdp-atc (Product Detail Page — Add to Cart Rate)
- **Primary metric**: add_to_cart_rate (higher is better)
- **Measurement window**: 7 days
- **Minimum sample**: 100 sessions per arm
- **Started**: 2026-05-12 (Cycle 1 — paused_for_review on tier-2 CVR breach)
- **Total cycles**: 2
- **Cumulative lift**: 0.0%

## Winning Patterns

_(No patterns recorded yet. The agent will add entries here after each KEEP decision.)_

<!-- Format for entries:
- [Cycle N] Pattern description (lift: +X.X%, p: 0.XXX, date: YYYY-MM-DD)
-->

## Losing Patterns

### Losing patterns log

- [Cycle 1] Subscription-first buy-box default + option reorder (one-time → subscription anchoring). ATC rate +5.7% (control 8.97% → variant 9.48%, p(variant>control)=0.79, below 95% keep). CVR -19.2% guardrail tier-2 breach (control 2.34% → variant 1.89%) — paused for Katie review. Insight: subscription-first lifts top-of-funnel buy-button engagement but cannibalizes downstream conversion — pure ATC isn't enough to justify the CVR drag at this presentation strength. Sample: 6,455 control / 2,752 variant sessions over 9.3 days (date: 2026-05-12)
- [Cycle 2] Reorder buy-box Subscribe & Save above One-time WITHOUT preselect (one-time stays default `checked`). ATC -14.3% (control 9.49% -> variant 8.14%) and CVR -25.7% (control 3.52% -> variant 2.62%) — tier-1 guardrail breach. Hypothesis that reorder alone (no forced default) would lift ATC without cycle-1 CVR cannibalization is DISPROVED: ordering Subscribe & Save first suppressed both ATC and conversion. Sample: 5,227 control / 2,446 variant sessions (date: 2026-06-15). Manual preemptive revert (Stage-1 alert-only).


<!-- Format for entries:
- [Cycle N] Pattern description (lift: -X.X%, p: 0.XXX, date: YYYY-MM-DD)
-->

## Emergency Reverts

- [Cycle 2] pdp-atc-002 (CS-2026-154): tier-1 CVR guardrail breach (-25.7% vs control, threshold -20%). Stage-1 alert_only so cron did not auto-revert (revert_enabled=false); Katie manually removed the variant from auto-optimize-config.liquid (PR merged) and set state.json phase measuring->idle. (date: 2026-06-15)

<!-- Format for entries:
- [Cycle N] What happened, which guardrail tripped, what was reverted (date: YYYY-MM-DD)
-->

## Open Questions

- Does moving the review carousel above the product description improve ATC?
- Benefit-first vs. feature-first headline copy — which converts better?
- Does subscription value prop placement (above vs. below ATC button) affect attach rate?
- Impact of social proof density (star rating only vs. stars + review count + recent review snippet)
- Video on PDP: help or hurt ATC rate?
- Urgency/scarcity messaging: trust-builder or trust-breaker for this audience?
- Section ordering above fold: image gallery first vs. product info first on mobile

## Cross-Surface Insights

_(Patterns that may apply to other surfaces will be noted here and appended to the KGS Learning Log at `data/performance-memory/cross-surface-pm.json` — add to both `entries` and `index` arrays.)_
