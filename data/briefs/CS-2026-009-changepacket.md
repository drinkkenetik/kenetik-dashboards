# ChangePacket — CS-2026-009
## BWR Post-Purchase Flow — Endurance Training Bundle Protocol

**Created:** 2026-03-18
**Execution Owner:** Katie
**Target Build Date:** 2026-03-19
**Surface:** Klaviyo
**Status:** Ready to build

---

## Pre-Build Checklist

- [ ] Confirm BWR discount code is active and tracking in Shopify
- [ ] Verify variant ID `9180100985051` (Endurance Training Bundle) is correct
- [ ] Check how many BWR bundle purchases have occurred since Mar 5 (for retroactive Day 0 send)
- [ ] Confirm Devon has reviewed science claims content for Emails 2, 4, 5 (HARD GATE — do not activate science emails without Devon approval)

---

## 1. Segment Build

**Segment Name:** `BWR Bundle Purchasers — 2026`

**Conditions:**
- Placed Order where:
  - Discount Code = `BWR`
  - AND Items contain product with variant ID = `9180100985051`
- Dynamic segment (new purchasers enter automatically)

**Estimated size:** 75–150 over campaign window (Mar 5 – May 3)

---

## 2. Flow Configuration

**Flow Name:** `BWR Post-Purchase Protocol Flow`

**Trigger:** Placed Order
- Filter: Discount Code = `BWR` AND Item variant ID = `9180100985051`

**Suppression:**
- Suppress from generic welcome series while in this flow
- Re-enter standard flows after flow completion or May 3 (BWR event date), whichever is later

**Flow Timeline:** Mar 5 → May 3, 2026 (~52 days / ~7.5 weeks from first purchaser)

---

## 3. Message Sequence — Build Order

### Email 1 — Day 0 (immediate post-purchase)
**Subject line suggestion:** "Your BWR Prep Starts Now"
**Content:**
- Welcome to the endurance athlete community
- What's in the bundle: Cans (daily post-exercise recovery), Shots (pre-sleep + race day), Water Bottle (hydration during training)
- Set expectation: "Over the next 8 weeks, we're sending you a science-backed Kenetik protocol designed to peak at BWR"
- CTA: Read the protocol overview
**Claims tier:** Tier 0 (no science claims) ✅ Can go live immediately

### Email 2 — Day 3
**Subject line suggestion:** "The Science Behind Your Protocol"
**Content:**
- Reference Robberechts et al. (2026) study findings
- Protocol: 1 can post-exercise (12g ketones), 1 shot before sleep (10g ketones) on training days
- **⚠️ CLAIMS GATE:** Must use Tier A qualified language only. "A 2026 study in The Journal of Physiology found that post-exercise ketone supplementation during an 8-week periodized endurance program..." Do NOT imply Kenetik was the product studied.
- CTA: Save your protocol schedule
**Claims tier:** Tier A — REQUIRES DEVON APPROVAL before activation

### Email 3 — Day 10 (~Week 2)
**Subject line suggestion:** "Weeks 1–2: Building the Foundation"
**Content:**
- Protocol check-in: consistency with post-exercise can + pre-sleep shot
- Dose timing tips: Within 30 min post-exercise; 30 min before bed
- Format pairing: Cans for post-ride, Shots for nightstand
- Quick FAQ: taste tips, mixing with recovery shake, hydration
**Claims tier:** Tier 0 (product usage, no science claims) ✅ Can go live immediately

### Email 4 — Day 21 (~Week 3)
**Subject line suggestion:** "The Adaptation Window Is Open"
**Content:**
- Reference study: At 3-week mark, measurable changes in both groups — supplementation starts to separate
- Encourage consistency: the compounding effect
- Reorder check + CTA: Reorder link to bundle or individual formats
**Claims tier:** Tier A — REQUIRES DEVON APPROVAL before activation

### Email 5 — Day 35 (~Week 5)
**Subject line suggestion:** "Intensification Phase — This Is Where It Counts"
**Content:**
- Reference study: Second 4-week mesocycle is where KE group pulled ahead
- Training intensity increasing — recovery matters more
- Reorder urgency CTA
**Claims tier:** Tier A — REQUIRES DEVON APPROVAL before activation

### Email 6 — Day 42 (~Week 6)
**Subject line suggestion:** "2 Weeks to BWR — Taper Smart"
**Content:**
- Taper protocol: training volume drops but maintain Kenetik protocol
- Reference study: Even during taper, supplementation group maintained performance edge
- Race prep checklist: gear, nutrition plan, Kenetik supply for race week
- CTA: Final reorder window for pre-race delivery
**Claims tier:** Tier A (light reference) — Bundle with Devon review of Emails 2/4/5

### SMS — Day 49 (May 1, race eve)
**Content:** "8 weeks of prep. Tomorrow you ride. Trust the work. See you at BWR. 🏁"
**Claims tier:** Tier 0 ✅ Can go live immediately

### Email 7 — Day 49 (~Race Week)
**Subject line suggestion:** "Your BWR Race Day Protocol"
**Content:**
- Race day Kenetik plan:
  - Morning: 1 can with breakfast (2–3 hours before start)
  - During: 1 shot at feed zone / midpoint
  - Post-race: 1 can within 30 min of finishing + 1 shot before sleep
- Water bottle: filled and on the bike
- Good luck message
**Claims tier:** Tier 0 (product usage) ✅ Can go live immediately

### Email 8 — Day 56 (post-race)
**Subject line suggestion:** "What's Next — Keep the Momentum"
**Content:**
- Congratulations on BWR
- Recovery protocol: Continue post-exercise + pre-sleep routine through recovery week
- Light study reference: adaptations continued building through week 8 and beyond
- Subscription CTA: "Lock in your protocol at the best price"
- Community: Share BWR story (social tag, review prompt)
**Claims tier:** Tier A (light) — Bundle with Devon review

---

## 4. Recommended Build Strategy

Given the Devon claims gate on Emails 2, 4, 5, 6, 8:

**Phase 1 — Go live immediately (Mar 19):**
- Build full flow structure with all 8 emails + 1 SMS
- ACTIVATE: Email 1 (Day 0), Email 3 (Day 10), SMS (Day 49), Email 7 (Day 49)
- SET TO DRAFT: Emails 2, 4, 5, 6, 8 (pending Devon review)
- This ensures Day 0 and Day 10 emails fire on schedule while science content awaits approval

**Phase 2 — After Devon approval:**
- Activate Emails 2, 4, 5, 6, 8
- No disruption to flow timing — Klaviyo will queue based on each recipient's entry date

**Retroactive sends:**
- After flow goes live, identify all BWR purchasers from Mar 5 to Mar 19
- Manually send Email 1 to anyone who purchased before flow activation
- For purchasers >3 days old, consider sending Email 1 + Email 2 (if Devon approved) in quick succession
- For purchasers >10 days old, send compressed catch-up (Emails 1+3 or custom catch-up message)

---

## 5. Measurement Setup

| Metric | Target | Attribution Window |
|---|---|---|
| Flow open rate | >45% | 7-day, min 75 sends |
| Flow click rate | >4% | 7-day, min 75 sends |
| Reorder rate (flow recipients) | >12% | 52-day (full protocol window) |
| Subscription conversion | >4% | 60-day |
| Revenue per recipient | >$8 | 60-day |

**Measurement window:** 60 days from first send
**Note:** Small cohort (75-150). Directional pilot — not powered for statistical significance.

---

## 6. Rollback Plan

- Disable flow in Klaviyo (set to Draft/Manual status)
- Time to rollback: <5 minutes
- No customer-facing impact beyond stopping future sends

---

## 7. Post-Build Confirmation

After building and activating the flow, return to `/changeset-execute CS-2026-009` to:
1. Confirm publish with Klaviyo flow ID
2. Update tracker to `published` status
3. Start measurement clock
4. Send post-publish Slack notification
