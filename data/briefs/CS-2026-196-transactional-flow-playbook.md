# Transactional Flow Playbook — WML 6→12 Migration Notices

Goal: notify **all** affected subscribers (including the ~9+ non-consented in A and anyone in B/C) in one mechanism, as transactional email, so consent status doesn't gate delivery. Reuses the templates already built.

> Connector limitation: flows can't be created via the Klaviyo MCP connector, so these steps are done in the Klaviyo UI. Templates already exist and are reusable: A=`Vxw9At`, B=`XH5iFp`, C=`SxEr3B`, D=`Wr2dhC`.

## Key constraints (read first)

1. **List-triggered flows fire only on new additions.** The 86 are already on lists A/B/C, so they won't trigger retroactively. Build each flow against a NEW trigger list and upload the members *after* the flow is live + approved.
2. **Transactional status for a list-triggered flow requires a Klaviyo Support request** (self-serve transactional is metric-triggered flows only). Approval typically ~1 business day. The flow won't send until approved.
3. **Content must stay strictly transactional** — no coupons, no product pushes, no marketing CTAs, no sign-up/subscribe links. Our copy already qualifies (account-management link + preferences/unsubscribe only).
4. Once approved, transactional sends reach all profiles regardless of marketing consent, **except** hard-bounced, 7x soft-bounced, or prior-spam-complaint profiles.

## Build steps (repeat per segment: A, B, C — and D when ready)

1. **Create fresh trigger lists** (do not reuse the current A/B/C lists, since their members are already added): e.g. `WML 6→12 FLOW-A`, `FLOW-B`, `FLOW-C`. Leave empty for now.
2. **Create a flow** for each, trigger = "When someone is added to list → FLOW-A" (etc.).
3. Add a **time delay of 0** (immediate) or a small smart delay if you prefer; add one **Email action**.
4. In the email, **load the existing template** (A→`Vxw9At`, B→`XH5iFp`, C→`SxEr3B`). Set sender **Katie at Kenetik / katie.s@drinkkenetik.com**, reply-to `katie.s@drinkkenetik.com` (Gorgias-linked).
5. **Flow filters:** set "Only send to profiles once" so re-adds don't double-send. No additional consent filter needed once transactional.
6. **Mark the email transactional** in the message settings. For a list-triggered flow this will prompt a Support submission — submit it (wording below).
7. **Wait for approval** (~1 business day). Editing content after approval removes transactional status, so finalize copy first.

## After approval — trigger the send

1. Confirm the flow is **Live**.
2. **Upload the segment CSV into its matching FLOW list** (`klaviyo_segment_A/B/C_emails.csv`). The add-to-list event fires the transactional email to every uploaded profile, consent-independent.
3. Spot-check the flow's recipient activity to confirm all members received (compare to 67 / 3 / 6).

## Segment D (8 error-charge subs)

Same pattern with template `Wr2dhC` (FLOW-D + `klaviyo_segment_D_emails.csv`), but these subs also need a payment fix. Decide whether to send the notice now (informs them + payment-update CTA) or after individually resolving — the email itself is a valid transactional dunning notice.

## Klaviyo Support request wording (copy-paste)

> Hi — I'd like to request transactional status for the email message(s) in these list-triggered flows: [FLOW-A, FLOW-B, FLOW-C]. These are one-time operational notices to existing paying subscribers about a change to their active subscription: we are retiring the Watermelon Lime 6-pack and migrating each subscriber to the 12-pack at the same volume and price over time. The emails contain only subscription/account information (what changed, billing impact, a link to their account, and standard preferences/unsubscribe). No promotional content, coupons, product recommendations, or sign-up links. Please review for transactional approval. Thank you.

## Timing tradeoff

The flow reaches everyone but only after ~1 business day of approval. If the billing change is imminent, consider sending campaign A/B/C now (covers the 58 + consented in B/C immediately) and using the transactional flow only for the skipped/non-consented + Segment D. Either path is fine; the flow-only path is cleaner but slower.
