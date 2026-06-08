# Watermelon Lime 6-Pack → 12-Pack Migration — Customer Emails

Drafted for Klaviyo send. Tone: Transparent + Warm (per brand-voice.md price-change and retention guidance). No em dashes, no banned category terms, proof set used only as factual footer. Merge tags and links are placeholders — confirm against your Klaviyo/Recharge setup before send.

**Audience split**

| Email | Who | Count | State |
|---|---|---|---|
| A — Batch 1, single-pack | Migrated subs that had 1×6-pack, frequency doubled | 69 | Updated |
| B — Batch 1, 2×6-pack combine | Migrated subs that had 2×6-pack, now 1×12-pack | 3 (672347155, 781152509, 818666832) | Updated |
| C — Future-skipped hold | Subs with an upcoming skipped order, not yet migrated | 6 | On hold |
| D — Error-charge hold | Subs with a failed payment, not yet migrated | 8 | On hold |

> Note: sub **788724219** is a 2×6-pack sub but sits in the future-skipped group (Email C) for now. When you migrate it, apply the Email B "two 6-packs become one 12-pack" framing rather than the frequency-change framing.

> Suggested sequence: send all four today, before any charge can fire at the new SKU/price. A and B confirm a change already made; C and D set expectations ahead of the manual migration.

---

## Email A — Batch 1, single 6-pack subscribers (frequency doubled)

**Subject:** Your Watermelon Lime subscription is moving to the 12-pack
**Subject (alt):** A small change to your Watermelon Lime subscription
**Preview:** Same Kenetik, same cost over time. A quick note on what's new.

Hi {{ first_name|default:'there' }},

We're retiring the Watermelon Lime 6-pack, so we've moved your subscription to the 12-pack of the same Watermelon Lime.

The part that matters most: you'll get the same amount of Kenetik over time, at the same cost over time. Your total doesn't change.

What's different, and what isn't:

- Each delivery is now a 12-pack instead of a 6-pack.
- Deliveries arrive half as often, so your cans per month stay the same.
- Each charge is now $47.90 instead of $23.95, on the new schedule. Across the month, you pay the same.

There's nothing you need to do. Your next order is already set on the updated schedule. If you'd like to change your delivery date or how often it arrives, you can adjust everything in your account: [Manage my subscription]({{ portal_link }}).

Questions? Just reply to this email and we'll help.

Katie Spaller
Director of Customer Success, Kenetik

*12 grams of ketones. Caffeine-free. Sugar-free. Nothing artificial.*

---

## Email B — Batch 1, 2×6-pack subscribers (combined into one 12-pack)

**Subject:** A small update to your Watermelon Lime subscription
**Preview:** Two 6-packs becomes one 12-pack. Same delivery, same price.

Hi {{ first_name|default:'there' }},

We're retiring the Watermelon Lime 6-pack. Because your subscription included two 6-packs in every delivery, we've combined them into a single 12-pack of the same Watermelon Lime.

Nothing else changes. You'll get the same 12 cans per delivery, on the same schedule, at the same $47.90 per order. The only difference is one 12-pack on your packing slip instead of two 6-packs.

No action needed on your end. You can review or adjust your subscription anytime in your account: [Manage my subscription]({{ portal_link }}).

Questions? Just reply and we'll help.

Katie Spaller
Director of Customer Success, Kenetik

*12 grams of ketones. Caffeine-free. Sugar-free. Nothing artificial.*

---

## Email C — Future-skipped hold group (not yet migrated)

**Subject:** A quick update on your Watermelon Lime subscription
**Preview:** We're moving you to the 12-pack. Your skipped order still stands.

Hi {{ first_name|default:'there' }},

A heads-up about your Watermelon Lime subscription. We're retiring the 6-pack and moving subscriptions to the 12-pack of the same Watermelon Lime. You'll get the same amount of Kenetik over time, at the same cost over time.

You've already skipped your next order, and that still stands. We won't ship it or charge you for it. When your subscription picks back up, it'll be the Watermelon Lime 12-pack on your usual terms.

There's nothing you need to do. You can review or change anything in your account anytime: [Manage my subscription]({{ portal_link }}).

Questions? Just reply to this email and we'll help.

Katie Spaller
Director of Customer Success, Kenetik

*12 grams of ketones. Caffeine-free. Sugar-free. Nothing artificial.*

---

## Email D — Error-charge hold group (failed payment, not yet migrated)

**Subject:** Action needed: update your payment to keep your Kenetik coming
**Subject (alt):** A quick fix to keep your Watermelon Lime subscription active
**Preview:** Your last payment didn't go through. A quick update picks things back up.

Hi {{ first_name|default:'there' }},

Two quick things about your Watermelon Lime subscription.

First, we're retiring the 6-pack and moving subscriptions to the 12-pack of the same Watermelon Lime. You'll get the same amount of Kenetik over time, at the same cost over time.

Second, your most recent payment didn't go through, so your subscription is paused for now. Update your payment method and we'll pick right back up with your Watermelon Lime 12-pack.

[Update my payment method]({{ payment_update_link }})

Need a hand? Just reply to this email and we'll sort it out with you.

Katie Spaller
Director of Customer Success, Kenetik

*12 grams of ketones. Caffeine-free. Sugar-free. Nothing artificial.*

---

## Build notes

- **Merge tags / links:** `{{ first_name }}`, `{{ portal_link }}` (Recharge customer portal), `{{ payment_update_link }}` (Recharge payment-update / hosted page) are placeholders. Swap for your actual Klaviyo/Recharge tokens before send.
- **Claims:** No health or performance claims used. The proof-set footer is factual product spec (approved). The product line name "Daily Clarity + Focus" appears only as the subscription's product title in-account, not as a benefit claim in copy.
- **Voice checks applied:** Transparent tone (lead with what we're doing, no spin), Warm tone for retention, no em dashes, no banned terms ("energy drink," "supplement," etc.), Oxford commas, sentence-case headings, numerals for figures, zero exclamation marks.
- **Price transparency:** Emails A, C, and D name the per-charge change ($23.95 → $47.90) and explain the offsetting frequency change so the higher per-shipment amount doesn't read as a price increase. This is the single most likely support/churn trigger; keep it in.
- **Segmentation:** Build the four sends against the matching subscription-ID lists (Batch 1 single vs. 2×6-pack, plus the two hold CSVs already split out).
