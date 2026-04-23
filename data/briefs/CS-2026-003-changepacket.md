# CHANGEPACKET: CS-2026-003
## SMS-First Flash Sale Channel Strategy

**A/B Test Execution Brief | Brain Awareness Week 2nd Send | March 19, 2026**

---

| Field | Value |
|---|---|
| ChangeSet ID | CS-2026-003 |
| Surface | Klaviyo (Email + SMS) |
| Owner | Katie + Nick |
| Risk Level | Medium |
| Send Date | **March 19, 2026** |
| Measurement | 7-day attribution window (through March 26) |

---

## Objective

Test whether SMS-first sequencing (SMS fires first, email follows 2 hours later) captures more total flash sale revenue than email-only. SMS drives 24x higher click-through rates, but email drives 69% higher revenue per recipient ($0.27 vs $0.16) and higher AOV ($82.90 vs $63.90). The hypothesis is that sequencing captures both urgency-driven SMS buyers and higher-value email buyers.

---

## A/B Test Design

Split the SMS-eligible + email-eligible overlap audience into three equal cells (~7,000 each). Each cell receives a different channel treatment for the BAW flash sale 2nd send.

| Cell | Size | Treatment | Purpose |
|---|---|---|---|
| A (Control) | ~7,000 | Email-only | Current approach baseline |
| B | ~7,000 | SMS-only | Isolate SMS conversion value |
| **C (Test)** | ~7,000 | **SMS first → Email 2hr later** | Test sequencing hypothesis |

---

## Klaviyo Setup Instructions

### Step 1: Create Audience Segments

1. Create a master segment of profiles that are both SMS-consented AND email-subscribed. This is your test universe (~21,000 based on current list sizes of ~14,828 SMS / ~27,890 email).
2. Randomly split this master segment into 3 equal groups using Klaviyo's random sample feature or manual list splitting. Label them: "CS003-CellA", "CS003-CellB", "CS003-CellC".
3. Verify each cell has ~7,000 profiles and there is zero overlap between cells.

### Step 2: Configure Campaigns

**Cell A (Email-Only):**
- Create email campaign targeting CS003-CellA segment
- Use standard flash sale creative and copy
- UTM: `utm_campaign=baw-flash-cs003&utm_content=cellA`
- Send time: Standard flash sale send time

**Cell B (SMS-Only):**
- Create SMS campaign targeting CS003-CellB segment
- Same flash sale offer, adapted for SMS format
- UTM: `utm_campaign=baw-flash-cs003&utm_content=cellB`
- Send time: Same as Cell A
- **IMPORTANT: Exclude CS003-CellB from the email campaign entirely**

**Cell C (SMS First → Email 2hr Delay):**
- Create SMS campaign targeting CS003-CellC segment — fires at standard send time
- Create email campaign targeting CS003-CellC segment — scheduled **2 hours AFTER** SMS send
- UTM (SMS): `utm_campaign=baw-flash-cs003&utm_content=cellC-sms`
- UTM (Email): `utm_campaign=baw-flash-cs003&utm_content=cellC-email`

### Step 3: UTM Parameters

All links in all campaigns must include these UTM parameters for proper attribution. This is critical given the ongoing attribution remediation work (CS-2026-025).

| Parameter | Value |
|---|---|
| utm_source | klaviyo |
| utm_medium | sms or email (match the channel) |
| utm_campaign | baw-flash-cs003 |
| utm_content | cellA / cellB / cellC-sms / cellC-email |

---

## Guardrails & Monitoring

| Guardrail | Threshold | Action if Breached |
|---|---|---|
| SMS unsubscribe rate | **1.0% per send (HARD CAP)** | Immediately reduce SMS frequency. Flag Katie. |
| Email unsubscribe rate | < 0.3% per send | Monitor only — no action unless 2x threshold. |
| Cell size imbalance | > 10% variance | Rebalance before send or note in measurement. |

**Current SMS unsub baseline: 0.97%** — only 3 basis points from the hard cap. Monitor per-cell unsub rates in real time during the first hour after send.

---

## Measurement Plan

**Measurement window:** 7 days from send date (March 19–26, 2026)
**Statistical significance required:** 95% confidence

### Primary Success Metric

**Cell C (SMS+Email) total revenue > Cell A (Email-only) total revenue at 95% confidence.**

### Metrics to Track Per Cell

| Metric | Cell A Target | Cell B Target | Cell C Target |
|---|---|---|---|
| Total revenue | Baseline | Track | **> Cell A** |
| Revenue per recipient (RPR) | ~$0.27 | ~$0.16 | Track |
| Average order value (AOV) | ~$82.90 | ~$63.90 | Track |
| Click-through rate | ~1.14% | ~26.93% | Track both |
| Conversion rate | ~0.32% | ~0.24% | Track |
| Unsub rate | < 0.3% | < 1.0% | < 1.0% SMS |

### Secondary Learning Questions

1. Do SMS and email attract different buyer types? (Compare AOV differential between Cell B and Cell C-email portion.)
2. Does the 2-hour delay email in Cell C cannibalize SMS conversions, or does it capture incremental buyers?
3. What is the conversion timing pattern? (Do SMS conversions happen within the first 2 hours before the email fires?)

---

## Rollback Plan

**Fully reversible.** If any issues arise during or after the test, revert to email-primary allocation for the next flash sale. No structural changes to undo.

- **Time to rollback:** Immediate — next campaign simply uses email-primary
- **Who executes rollback:** Katie
- **Trigger:** SMS unsub rate exceeds 1.0%, or critical delivery issues

---

## Approvals

| Approver | Role | Status | Date |
|---|---|---|---|
| Katie | CEM / Execution Owner | ✅ Approved | 2026-03-13 |
| Nick | Marketing | Informed | 2026-03-18 |

---

## Timeline

- **Today (Mar 18):** Build segments and configure campaigns in Klaviyo
- **Mar 19:** Send BAW 2nd flash sale with 3-cell A/B structure
- **Mar 19 (first hour):** Monitor SMS unsub rates per cell in real time
- **Mar 26:** Measurement window closes — pull results and determine winner
