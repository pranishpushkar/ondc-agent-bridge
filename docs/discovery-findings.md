# Discovery findings: ONDC pre-prod, first contact

**Date:** 21 Nov 2026
**Environment:** ONDC pre-prod (staging has been retired by ONDC)
**Buyer app:** `ondc.pranishpushkar.com`, domain ONDC:RET10 (grocery) and RET11–RET15, cities Bengaluru (`std:080`) and Hyderabad (`std:040`)
**Tool:** [`discovery/ondc_probe.py`](../discovery/ondc_probe.py)
**Evidence:** raw captures under [`captures/`](../captures/), field report in [`captures/contract-report.md`](../captures/contract-report.md)

This document records what real ONDC sellers actually send, as opposed to what the spec says, and what each finding means for the bridge.

---

## 1. Registration and identity

- The ONDC portal (portal.ondc.org) handled registry subscription for pre-prod. After the pre-prod "Add new subscription" request, our subscriber was `SUBSCRIBED` in the registry for all six chosen domains. Our own site-verification / `/on_subscribe` flow was not needed.
- The portal generates the key pair and the unique key id (UKID) and issues them once as `keys.json`: Ed25519 signing key (64-byte libsodium format), X25519 encryption key (DER), UKID, subscriber id and URLs. The probe reads this file directly (`--keys`).
- The registry's open `/lookup` is closed to unregistered callers (pre-prod returned HTTP 403). Lookups need the signed `/v2.0/lookup`, which worked once subscribed.
- Callback URL: `https://ondc.pranishpushkar.com/` via a named Cloudflare Tunnel to the probe on the developer's machine. Sellers call `/<action>` under it (e.g. `/on_search`).

**For the bridge:** the network identity (subscriber id, UKID, keys) is issued by the portal; the bridge must load it rather than generate its own. Every registry call is signed.

## 2. The registry is not a list of working sellers

| | Bengaluru (`std:080`) | Hyderabad (`std:040`) |
|---|---|---|
| RET10 seller apps registered | 394 | 378 |
| In both lists | 377 | 377 |
| Registered with city `*` (all of India) | – | 373 of 378 |

- Registered entries include major platforms (Paytm, Snapdeal, Shiprocket, magicpin, ShopClues, Jio/Fynd, More Retail, HUL, Nestlé via Shopalyst), seller-tech platforms hosting many shops (Adya, thesellerapp, Protean adaptors, SellerSetu), ONDC's own test sellers (`seller-app-preprod-v2.ondc.org`, `pramaan.ondc.org`, `workbench.ondc.tech`, `gcr-bpp*.ondc.org`), and clear junk (`google.com`, `wa.me`, `test.abc.com`, `exapmle.com`, a bare IP, temporary ngrok URLs, a few `UNSUBSCRIBED`).
- City registration is meaningless in practice: almost every seller app claims every city.

**For the bridge:** do not route by registry city. Learn real coverage from responses (see §5) and keep a per-seller health record.

## 3. Search: who answers, and how

| Run | Query | City | Callbacks | Seller apps |
|---|---|---|---|---|
| 1 | milk | Bengaluru | 5 (lost: see gzip below) | – |
| 2 | milk | Bengaluru | 5 | 3 |
| 3 | rice | Hyderabad | 0 | 0 |

Run 2 sellers: `stageapi.lekhha.com` (2 stores), `sellerpreprod.orderbazaar.in` (2 stores), `ondcseller-staging.costbo.com` (1 store). All replies arrived ~0.6 s after the search.

Findings:

1. **Response rate is tiny:** 3 of 394 registered seller apps replied.
2. **One callback per store, not per seller app.** Multi-store platforms send several `on_search` callbacks for one search, each with one provider.
3. **Sellers ignore the search text.** A search for "milk" returned jam, chicken, rice and masala; only one dairy store was relevant. Sellers appear to return whole catalogues.
4. **Sellers do not filter by location.** One OrderBazaar store is in Kayarambedu, Tamil Nadu, yet answered a Bengaluru search.
5. **Hyderabad got nothing.** Sellers that claim Hyderabad in the registry (including the three above) did not answer, because their stores are elsewhere.

**For the bridge:** the bridge must (a) merge per-store callbacks within a time window, (b) do its own relevance filtering and ranking before showing results to an agent, (c) check serviceability itself, and (d) treat "no answer" as normal.

## 4. Transport details not in the spec

| | `on_search` (3 seller apps) | `on_select` (Lekhha) |
|---|---|---|
| Compression | gzip (`Content-Encoding: gzip`) | none |
| Signature computed over | the **compressed** bytes | the JSON body |
| HTTP client | `Go-http-client/2.0` (identical for all three) | `axios/1.7.7` |
| Sync response to our request | plain ACK | ACK echoing the full `context` |

- The probe's first run crashed on the gzip bodies (`UnicodeDecodeError`); the receiver now decompresses and verifies signatures against both forms.
- Identical client and compression across three unrelated sellers suggests `on_search` passes through a shared relay, while `on_select` comes straight from the seller. Unconfirmed.

**For the bridge:** the callback receiver must accept gzip and plain bodies and verify the signature over the raw bytes as received, falling back to the decompressed body. All callbacks in these runs had valid signatures.

## 5. Catalogue (`on_search`) contract

- All replies: `core_version` `1.2.0`, the same 12 context fields, catalogue keys `bpp/descriptor`, `bpp/fulfillments`, `bpp/providers`.
- Item fields common to all sellers: `id`, `descriptor`, `price`, `quantity`, `category_id`, `location_id`, `fulfillment_id`, `time`, `tags`, `@ondc/org/time_to_ship`, `@ondc/org/available_on_cod`, `@ondc/org/returnable`, `@ondc/org/cancellable`, `@ondc/org/return_window`, `@ondc/org/seller_pickup_return`, `@ondc/org/contact_details_consumer_care`, `@ondc/org/statutory_reqs_packaged_commodities`.
- Optional extras seen: provider `offers`, `creds`, `rating`; item `parent_item_id`, `recommended`, `rating`, `@ondc/org/statutory_reqs_prepackaged_food`.
- 221 distinct field paths and 15 tag groups (`serviceability`, `timing`, `veg_nonveg`, `bpp_terms`, `benefit`, `qualifier`, `config`, …). Full list in the contract report.
- Store location is given per provider: GPS, area code, street address.

**Data quality problems:**

| Problem | Example |
|---|---|
| Prices are strings in mixed formats | `"464"`, `"1380.0"`, `"71.20"` |
| Stock is a placeholder | `available.count` is `"99"` everywhere |
| Obvious typos | MRP ₹15,000 against a price of ₹1,400 |
| Nonsense items | "Milk orange" at ₹535 |
| Inconsistent durations | `time_to_ship`: `PT60M`, `PT1H`, `P1D`, `P1DT1H10M`, `P0DT0H5M` |

**For the bridge:** normalise money to integer minor units and durations to seconds at the edge; never trust catalogue stock or price for checkout.

## 6. Quote (`on_select`) contract

Request: 2 × Butter from Lekhha Provider A, delivery to Koramangala (560034).
Result: **₹308.28**, `Serviceable`, delivery in 15 minutes (`@ondc/org/TAT` `P0DT0H15M`), category "Immediate Delivery". The breakup adds up exactly:

| Line | `@ondc/org/title_type` | ₹ |
|---|---|---|
| Butter × 2 (₹110.00 each) | item | 220.00 |
| Tax on item | tax | 28.60 |
| Discount | discount | −29.84 |
| Delivery charges | delivery | 44.00 |
| Tax on delivery | tax | 4.84 |
| Packing charges | packing | 33.00 |
| Tax on packing | tax | 3.30 |
| Convenience fee | misc | 3.71 |
| Tax on convenience fee | tax | 0.67 |
| **Total** | | **308.28** |

Differences from the catalogue for the same item:

| | Catalogue (`on_search`) | Quote (`on_select`) |
|---|---|---|
| Unit price | ₹109.38 | ₹110.00 |
| Quantity limit | 99 available | maximum 23 |
| Time | ship in 5 min | deliver in 15 min |

Seller terms (`bpp_terms` tags): `np_type` MSN, `collect_payment` **N**, `max_liability` 2, `max_liability_cap` 10000, `court_jurisdiction` Bengaluru, `delay_interest` 7, `accept_bap_terms` Y.

**For the bridge:**
- The `on_select` quote is the source of truth for price, limits and delivery promise; re-quote before checkout, and enforce the user's budget against the quote, not the catalogue.
- The breakup's title types map onto UCP checkout totals (subtotal, tax, discount, fulfillment, fees). This mapping is the core translation.
- `collect_payment: N` means the **buyer app collects payment** and settles with the seller later. Payment collection and settlement are the bridge's responsibility, which needs a decision early.

## 7. Final terms (`init` / `on_init`): the payment model

`init` sends billing and delivery details and asks for final terms. It places no order (only `confirm` does).

**What made `init` work** (all three sellers silently dropped our first attempts after ACKing):

- No `payment` block in `init`. ONDC's official RET10 example has none; the seller proposes terms in `on_init`.
- Every item must carry `quantity.count`. Some sellers omit quantity from `on_select` items (it appears only in the breakup, or nowhere), so the buyer app must carry it from its own `select`.
- Test buyer details in a realistic shape (ONDC's sample values).

After these fixes: **OrderBazaar and Costbo returned `on_init`; Lekhha never did** (silent on every attempt, including a fresh transaction). ACK means "received", not "accepted".

**Terms received:**

| | OrderBazaar | Costbo |
|---|---|---|
| `collected_by` | not stated | not stated |
| Payment type / status | `ON-ORDER` / `NOT-PAID` | not stated |
| Settlement basis / window | delivery / `P1D` | not stated |
| Withholding | ₹10.00 | not stated |
| Buyer-app finder fee | not stated | 3% (echoed our search offer) |
| Seller settlement account | NEFT, bank account + IFSC | NEFT, bank account + IFSC |
| Cancellation terms | none | ₹50 at any fulfilment state |
| Quote | ₹62 (item ₹62, delivery ₹0) | ₹280 (item ₹80 + convenience ₹100 + packing ₹100) |

**Conclusion on the payment model:** neither seller offers a payment link (`uri`), and both send their bank account for settlement as the `seller-app` counterparty. That is the buyer-app-collects model: **the bridge collects the buyer's money (prepaid, `ON-ORDER`), keeps its finder fee, and pays the seller within the settlement window after delivery**, minus any withholding. Combined with Lekhha's `collect_payment: N` (§6), all three live sellers expect the buyer app to collect.

**For the bridge:**
- Payment collection, holding funds through the settlement window, payouts to sellers' bank accounts, reconciliation and refunds are the bridge's job. This is the biggest scope and compliance decision in the project.
- Don't assume optional fields: `collected_by`, settlement window and cancellation terms were each missing from at least one seller. Fill gaps with network defaults and treat missing terms as a risk to show the user.
- Fees can dwarf the item: Costbo's ₹80 jam costs ₹280. The bridge should show agents the full landed cost and enforce budgets on the `on_init` total.
- `on_init` contains sellers' real bank details. Captures must stay in a private repo.

## 8. Open questions

1. Who sends the gzip `on_search` callbacks: the sellers themselves or a shared relay?
2. Do ONDC's own test sellers (`seller-app-preprod-v2.ondc.org`, `pramaan.ondc.org`) answer searches, and with cleaner data?
3. How stable is the response rate across times of day and queries (atta, rice, category searches)?
4. Why does Lekhha never answer `init`? (Seller-side issue, or a field only it requires.)
5. What does `confirm` require, and how does payment proof travel (`payment.status` PAID, transaction id)? Not probed: it places a real order.
6. Should the bridge register as an MSN-aware buyer app, given most live sellers are multi-store platforms?

## 9. Suggested next steps

- Repeat searches at different times and with several queries to measure the response rate properly.
- Probe ONDC's reference seller and Pramaan mocks directly.
- Draft the shared internal model (`Offer`, `Quote`, `QuoteLine`, `Store`, `Serviceability`) from §5 and §6.
- Decide how the bridge will collect and settle payments (§7) before designing checkout.
