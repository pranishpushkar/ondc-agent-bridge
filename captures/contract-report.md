# ONDC contract report

Generated 2026-11-20T19:36:01.803Z from `captures`.

## on_search

5 callbacks from 3 seller apps: ondcseller-staging.costbo.com, sellerpreprod.orderbazaar.in, stageapi.lekhha.com

| Seller app | Latency after request | Signature |
|---|---|---|
| ondcseller-staging.costbo.com | 0.6s | ok (over compressed body) |
| sellerpreprod.orderbazaar.in | 0.6s | ok (over compressed body) |
| sellerpreprod.orderbazaar.in | 0.6s | ok (over compressed body) |
| stageapi.lekhha.com | 0.6s | ok (over compressed body) |
| stageapi.lekhha.com | 0.6s | ok (over compressed body) |

| Field path | In callbacks | Types | Example |
|---|---|---|---|
| `$` | 5/5 | object |  |
| `context` | 5/5 | object |  |
| `context.action` | 5/5 | string | "on_search" |
| `context.bap_id` | 5/5 | string | "ondc.pranishpushkar.com" |
| `context.bap_uri` | 5/5 | string | "https://ondc.pranishpushkar.com" |
| `context.bpp_id` | 5/5 | string | "ondcseller-staging.costbo.com" |
| `context.bpp_uri` | 5/5 | string | "https://ondcseller-staging.costbo.com/ondc/v1/seller" |
| `context.city` | 5/5 | string | "std:080" |
| `context.core_version` | 5/5 | string | "1.2.0" |
| `context.country` | 5/5 | string | "IND" |
| `context.domain` | 5/5 | string | "ONDC:RET10" |
| `context.message_id` | 5/5 | string | "ba2c7a9f-9ccb-4eb8-b52d-741bf6a4e243" |
| `context.timestamp` | 5/5 | string | "2026-11-20T19:35:06.885Z" |
| `context.transaction_id` | 5/5 | string | "bac43bb8-f94d-4700-a8b0-f9a42bcc5775" |
| `message` | 5/5 | object |  |
| `message.catalog` | 5/5 | object |  |
| `message.catalog.bpp/descriptor` | 5/5 | object |  |
| `message.catalog.bpp/descriptor.images` | 5/5 | array |  |
| `message.catalog.bpp/descriptor.images[]` | 5/5 | string | "https://storage.googleapis.com/bodefaults/ondc/backend/COST |
| `message.catalog.bpp/descriptor.long_desc` | 5/5 | string | "Effortlessly manage Online and ONDC orders, WebStore, Integ |
| `message.catalog.bpp/descriptor.name` | 5/5 | string | "COSTBO SERVICES" |
| `message.catalog.bpp/descriptor.short_desc` | 5/5 | string | "Everything you need to make Online & ONDC sales happen" |
| `message.catalog.bpp/descriptor.symbol` | 5/5 | string | "https://storage.googleapis.com/bodefaults/ondc/backend/COST |
| `message.catalog.bpp/descriptor.tags` | 5/5 | array |  |
| `message.catalog.bpp/descriptor.tags[]` | 5/5 | object |  |
| `message.catalog.bpp/descriptor.tags[].code` | 5/5 | string | "bpp_terms" |
| `message.catalog.bpp/descriptor.tags[].list` | 5/5 | array |  |
| `message.catalog.bpp/descriptor.tags[].list[]` | 5/5 | object |  |
| `message.catalog.bpp/descriptor.tags[].list[].code` | 5/5 | string | "np_type" |
| `message.catalog.bpp/descriptor.tags[].list[].value` | 5/5 | string | "MSN" |
| `message.catalog.bpp/fulfillments` | 5/5 | array |  |
| `message.catalog.bpp/fulfillments[]` | 5/5 | object |  |
| `message.catalog.bpp/fulfillments[].contact` | 2/5 | object |  |
| `message.catalog.bpp/fulfillments[].contact.email` | 2/5 | string | "lekhha.04@yopmail.com" |
| `message.catalog.bpp/fulfillments[].contact.phone` | 2/5 | string | "9123450003" |
| `message.catalog.bpp/fulfillments[].id` | 5/5 | string | "F1" |
| `message.catalog.bpp/fulfillments[].type` | 5/5 | string | "Delivery" |
| `message.catalog.bpp/providers` | 5/5 | array |  |
| `message.catalog.bpp/providers[]` | 5/5 | object |  |
| `message.catalog.bpp/providers[].categories` | 5/5 | array |  |
| `message.catalog.bpp/providers[].categories[]` | 5/5 | object |  |
| `message.catalog.bpp/providers[].categories[].descriptor` | 5/5 | object |  |
| `message.catalog.bpp/providers[].categories[].descriptor.images` | 1/5 | array |  |
| `message.catalog.bpp/providers[].categories[].descriptor.images[]` | 1/5 | string | "/images/f5894680-c22c-11f1-add2-3b44957f6987/menu_image/259 |
| `message.catalog.bpp/providers[].categories[].descriptor.long_desc` | 1/5 | string | "Grocery" |
| `message.catalog.bpp/providers[].categories[].descriptor.name` | 5/5 | string | "very Berry  jam" |
| `message.catalog.bpp/providers[].categories[].descriptor.short_desc` | 1/5 | string | "Grocery" |
| `message.catalog.bpp/providers[].categories[].id` | 5/5 | string | "0a160d2cf41247f5a4e725dbddc77f14" |
| `message.catalog.bpp/providers[].categories[].parent_category_id` | 1/5 | string | "" |
| `message.catalog.bpp/providers[].categories[].tags` | 5/5 | array |  |
| `message.catalog.bpp/providers[].categories[].tags[]` | 5/5 | object |  |
| `message.catalog.bpp/providers[].categories[].tags[].code` | 5/5 | string | "type" |
| `message.catalog.bpp/providers[].categories[].tags[].list` | 5/5 | array |  |
| `message.catalog.bpp/providers[].categories[].tags[].list[]` | 5/5 | object |  |
| `message.catalog.bpp/providers[].categories[].tags[].list[].code` | 5/5 | string | "type" |
| `message.catalog.bpp/providers[].categories[].tags[].list[].value` | 5/5 | string | "variant_group" |
| `message.catalog.bpp/providers[].creds` | 2/5 | array |  |
| `message.catalog.bpp/providers[].creds[]` | 2/5 | object |  |
| `message.catalog.bpp/providers[].creds[].descriptor` | 2/5 | object |  |
| `message.catalog.bpp/providers[].creds[].descriptor.code` | 1/5 | string | "social sectors2" |
| `message.catalog.bpp/providers[].creds[].descriptor.name` | 1/5 | string | "test1" |
| `message.catalog.bpp/providers[].creds[].descriptor.short_desc` | 1/5 | string | "MSME Team TAG description2" |
| `message.catalog.bpp/providers[].creds[].id` | 2/5 | string | "TEAM51392" |
| `message.catalog.bpp/providers[].creds[].tags` | 2/5 | array |  |
| `message.catalog.bpp/providers[].creds[].tags[]` | 2/5 | object |  |
| `message.catalog.bpp/providers[].creds[].tags[].code` | 2/5 | string | "verification" |
| `message.catalog.bpp/providers[].creds[].tags[].list` | 2/5 | array |  |
| `message.catalog.bpp/providers[].creds[].tags[].list[]` | 2/5 | object |  |
| `message.catalog.bpp/providers[].creds[].tags[].list[].code` | 2/5 | string | "verify_url" |
| `message.catalog.bpp/providers[].creds[].tags[].list[].value` | 2/5 | string | "https://business.costbo.com" |
| `message.catalog.bpp/providers[].creds[].url` | 1/5 | string | "https://www.test1.com/url1" |
| `message.catalog.bpp/providers[].descriptor` | 5/5 | object |  |
| `message.catalog.bpp/providers[].descriptor.images` | 5/5 | array |  |
| `message.catalog.bpp/providers[].descriptor.images[]` | 5/5 | string | "https://storage.googleapis.com/bo3151920215/business/7bf9b5 |
| `message.catalog.bpp/providers[].descriptor.long_desc` | 5/5 | string | "Himachal Factory was started up in the year 2010, with the  |
| `message.catalog.bpp/providers[].descriptor.name` | 5/5 | string | "Himachal Factory" |
| `message.catalog.bpp/providers[].descriptor.short_desc` | 5/5 | string | "Himachal Factory" |
| `message.catalog.bpp/providers[].descriptor.symbol` | 5/5 | string | "https://storage.googleapis.com/bo3151920215/business/7bf9b5 |
| `message.catalog.bpp/providers[].fulfillments` | 5/5 | array |  |
| `message.catalog.bpp/providers[].fulfillments[]` | 5/5 | object |  |
| `message.catalog.bpp/providers[].fulfillments[].contact` | 5/5 | object |  |
| `message.catalog.bpp/providers[].fulfillments[].contact.email` | 5/5 | string | "ananth@gmail.com" |
| `message.catalog.bpp/providers[].fulfillments[].contact.phone` | 5/5 | string | "9845570111" |
| `message.catalog.bpp/providers[].fulfillments[].id` | 5/5 | string | "F1" |
| `message.catalog.bpp/providers[].fulfillments[].storeTimings` | 2/5 | array |  |
| `message.catalog.bpp/providers[].fulfillments[].storeTimings[]` | 2/5 | object |  |
| `message.catalog.bpp/providers[].fulfillments[].storeTimings[].daysRange` | 2/5 | object |  |
| `message.catalog.bpp/providers[].fulfillments[].storeTimings[].daysRange.from` | 2/5 | number | 1 |
| `message.catalog.bpp/providers[].fulfillments[].storeTimings[].daysRange.to` | 2/5 | number | 6 |
| `message.catalog.bpp/providers[].fulfillments[].storeTimings[].timings` | 2/5 | array |  |
| `message.catalog.bpp/providers[].fulfillments[].storeTimings[].timings[]` | 2/5 | object |  |
| `message.catalog.bpp/providers[].fulfillments[].storeTimings[].timings[].from` | 2/5 | string | "08:00" |
| `message.catalog.bpp/providers[].fulfillments[].storeTimings[].timings[].to` | 2/5 | string | "20:00" |
| `message.catalog.bpp/providers[].fulfillments[].type` | 5/5 | string | "Delivery" |
| `message.catalog.bpp/providers[].id` | 5/5 | string | "7bf9b561199f4a898b3f8a3cef91b6e6" |
| `message.catalog.bpp/providers[].items` | 5/5 | array |  |
| `message.catalog.bpp/providers[].items[]` | 5/5 | object |  |
| `message.catalog.bpp/providers[].items[].@ondc/org/available_on_cod` | 5/5 | boolean | false |
| `message.catalog.bpp/providers[].items[].@ondc/org/cancellable` | 5/5 | boolean | false |
| `message.catalog.bpp/providers[].items[].@ondc/org/contact_details_consumer_care` | 5/5 | string | "Himachal Factory,ananth@gmail.com,9845570111" |
| `message.catalog.bpp/providers[].items[].@ondc/org/return_window` | 5/5 | string | "P1D" |
| `message.catalog.bpp/providers[].items[].@ondc/org/returnable` | 5/5 | boolean | true |
| `message.catalog.bpp/providers[].items[].@ondc/org/seller_pickup_return` | 5/5 | boolean | true |
| `message.catalog.bpp/providers[].items[].@ondc/org/statutory_reqs_packaged_commodities` | 5/5 | object |  |
| `message.catalog.bpp/providers[].items[].@ondc/org/statutory_reqs_packaged_commodities.common_or_generic_name_of_commodity` | 5/5 | string | "Test" |
| `message.catalog.bpp/providers[].items[].@ondc/org/statutory_reqs_packaged_commodities.manufacturer_or_packer_address` | 5/5 | string | "#123" |
| `message.catalog.bpp/providers[].items[].@ondc/org/statutory_reqs_packaged_commodities.manufacturer_or_packer_name` | 5/5 | string | "Himachal" |
| `message.catalog.bpp/providers[].items[].@ondc/org/statutory_reqs_packaged_commodities.month_year_of_manufacture_packing_import` | 5/5 | string | "See back image" |
| `message.catalog.bpp/providers[].items[].@ondc/org/statutory_reqs_packaged_commodities.net_quantity_or_measure_of_commodity_in_pkg` | 2/5 | string | "5kg" |
| `message.catalog.bpp/providers[].items[].@ondc/org/statutory_reqs_prepackaged_food` | 2/5 | object |  |
| `message.catalog.bpp/providers[].items[].@ondc/org/statutory_reqs_prepackaged_food.additives_info` | 2/5 | string | "No Chemicals" |
| `message.catalog.bpp/providers[].items[].@ondc/org/statutory_reqs_prepackaged_food.brand_owner_FSSAI_license_no` | 2/5 | string | "12345678901234" |
| `message.catalog.bpp/providers[].items[].@ondc/org/statutory_reqs_prepackaged_food.importer_FSSAI_license_no` | 2/5 | string | "12345678901234" |
| `message.catalog.bpp/providers[].items[].@ondc/org/statutory_reqs_prepackaged_food.ingredients_info` | 1/5 | string | "Black Cherry, Syurps, Sugars & Sweeteners" |
| `message.catalog.bpp/providers[].items[].@ondc/org/statutory_reqs_prepackaged_food.nutritional_info` | 2/5 | string | "Energy(KCal)-(per 100kg) 420,Protein(g)-(per 100kg) 12" |
| `message.catalog.bpp/providers[].items[].@ondc/org/statutory_reqs_prepackaged_food.other_FSSAI_license_no` | 2/5 | string | "12345678901234" |
| `message.catalog.bpp/providers[].items[].@ondc/org/time_to_ship` | 5/5 | string | "PT60M" |
| `message.catalog.bpp/providers[].items[].category_id` | 5/5 | string | "Sauces, Spreads and Dips" |
| `message.catalog.bpp/providers[].items[].descriptor` | 5/5 | object |  |
| `message.catalog.bpp/providers[].items[].descriptor.code` | 5/5 | string | "1:9146733310256" |
| `message.catalog.bpp/providers[].items[].descriptor.images` | 5/5 | array |  |
| `message.catalog.bpp/providers[].items[].descriptor.images[]` | 3/5 | string | "https://storage.googleapis.com/bo3151920215/business/7bf9b5 |
| `message.catalog.bpp/providers[].items[].descriptor.long_desc` | 5/5 | string | "Jelly is a more sophisticated form which involves a two-ste |
| `message.catalog.bpp/providers[].items[].descriptor.name` | 5/5 | string | "Mixed Jelly 470g" |
| `message.catalog.bpp/providers[].items[].descriptor.short_desc` | 5/5 | string | "Mixed Jelly 470g" |
| `message.catalog.bpp/providers[].items[].descriptor.symbol` | 5/5 | string | "https://storage.googleapis.com/bo3151920215/business/7bf9b5 |
| `message.catalog.bpp/providers[].items[].fulfillment_id` | 5/5 | string | "F1" |
| `message.catalog.bpp/providers[].items[].id` | 5/5 | string | "18621c6080da4367b38e7a8c1418bcde" |
| `message.catalog.bpp/providers[].items[].location_id` | 5/5 | string | "7bf9b561199f4a898b3f8a3cef91b6e6-loc1" |
| `message.catalog.bpp/providers[].items[].parent_item_id` | 3/5 | string | "0a160d2cf41247f5a4e725dbddc77f14" |
| `message.catalog.bpp/providers[].items[].price` | 5/5 | object |  |
| `message.catalog.bpp/providers[].items[].price.currency` | 5/5 | string | "INR" |
| `message.catalog.bpp/providers[].items[].price.maximum_value` | 5/5 | string | "1500.0" |
| `message.catalog.bpp/providers[].items[].price.value` | 5/5 | string | "1380.0" |
| `message.catalog.bpp/providers[].items[].quantity` | 5/5 | object |  |
| `message.catalog.bpp/providers[].items[].quantity.available` | 5/5 | object |  |
| `message.catalog.bpp/providers[].items[].quantity.available.count` | 5/5 | string | "99" |
| `message.catalog.bpp/providers[].items[].quantity.maximum` | 5/5 | object |  |
| `message.catalog.bpp/providers[].items[].quantity.maximum.count` | 5/5 | string | "1" |
| `message.catalog.bpp/providers[].items[].quantity.minimum` | 2/5 | object |  |
| `message.catalog.bpp/providers[].items[].quantity.minimum.count` | 2/5 | string | "0" |
| `message.catalog.bpp/providers[].items[].quantity.unitized` | 5/5 | object |  |
| `message.catalog.bpp/providers[].items[].quantity.unitized.count` | 2/5 | string | "1" |
| `message.catalog.bpp/providers[].items[].quantity.unitized.measure` | 5/5 | object |  |
| `message.catalog.bpp/providers[].items[].quantity.unitized.measure.unit` | 5/5 | string | "gram" |
| `message.catalog.bpp/providers[].items[].quantity.unitized.measure.value` | 5/5 | string | "777" |
| `message.catalog.bpp/providers[].items[].rating` | 3/5 | string | "5" |
| `message.catalog.bpp/providers[].items[].recommended` | 2/5 | boolean | false |
| `message.catalog.bpp/providers[].items[].tags` | 5/5 | array |  |
| `message.catalog.bpp/providers[].items[].tags[]` | 5/5 | object |  |
| `message.catalog.bpp/providers[].items[].tags[].code` | 5/5 | string | "origin" |
| `message.catalog.bpp/providers[].items[].tags[].list` | 5/5 | array |  |
| `message.catalog.bpp/providers[].items[].tags[].list[]` | 5/5 | object |  |
| `message.catalog.bpp/providers[].items[].tags[].list[].code` | 5/5 | string | "country" |
| `message.catalog.bpp/providers[].items[].tags[].list[].value` | 5/5 | string | "IND" |
| `message.catalog.bpp/providers[].items[].time` | 5/5 | object |  |
| `message.catalog.bpp/providers[].items[].time.label` | 5/5 | string | "enable" |
| `message.catalog.bpp/providers[].items[].time.timestamp` | 5/5 | string | "2026-11-17T06:45:57.460Z" |
| `message.catalog.bpp/providers[].locations` | 5/5 | array |  |
| `message.catalog.bpp/providers[].locations[]` | 5/5 | object |  |
| `message.catalog.bpp/providers[].locations[].address` | 5/5 | object |  |
| `message.catalog.bpp/providers[].locations[].address.area_code` | 5/5 | string | "560035" |
| `message.catalog.bpp/providers[].locations[].address.city` | 5/5 | string | "Bengaluru" |
| `message.catalog.bpp/providers[].locations[].address.locality` | 5/5 | string | "Bengaluru" |
| `message.catalog.bpp/providers[].locations[].address.state` | 5/5 | string | "KA" |
| `message.catalog.bpp/providers[].locations[].address.street` | 5/5 | string | "Sarjapur road, kaikondrahalli, bengaluru 560035, India" |
| `message.catalog.bpp/providers[].locations[].circle` | 5/5 | object |  |
| `message.catalog.bpp/providers[].locations[].circle.gps` | 5/5 | string | "12.915893,77.676581" |
| `message.catalog.bpp/providers[].locations[].circle.radius` | 5/5 | object |  |
| `message.catalog.bpp/providers[].locations[].circle.radius.unit` | 5/5 | string | "km" |
| `message.catalog.bpp/providers[].locations[].circle.radius.value` | 5/5 | string | "50" |
| `message.catalog.bpp/providers[].locations[].gps` | 5/5 | string | "12.915893,77.676581" |
| `message.catalog.bpp/providers[].locations[].id` | 5/5 | string | "7bf9b561199f4a898b3f8a3cef91b6e6-loc1" |
| `message.catalog.bpp/providers[].locations[].time` | 5/5 | object |  |
| `message.catalog.bpp/providers[].locations[].time.days` | 5/5 | string | "1,2,3,4,5,6,7" |
| `message.catalog.bpp/providers[].locations[].time.label` | 5/5 | string | "enable" |
| `message.catalog.bpp/providers[].locations[].time.range` | 5/5 | object |  |
| `message.catalog.bpp/providers[].locations[].time.range.end` | 5/5 | string | "2359" |
| `message.catalog.bpp/providers[].locations[].time.range.start` | 5/5 | string | "0000" |
| `message.catalog.bpp/providers[].locations[].time.schedule` | 5/5 | object |  |
| `message.catalog.bpp/providers[].locations[].time.schedule.holidays` | 5/5 | array |  |
| `message.catalog.bpp/providers[].locations[].time.schedule.holidays[]` | 2/5 | string | "2026-09-30" |
| `message.catalog.bpp/providers[].locations[].time.timestamp` | 5/5 | string | "2026-11-17T06:45:57.460Z" |
| `message.catalog.bpp/providers[].offers` | 2/5 | array |  |
| `message.catalog.bpp/providers[].offers[]` | 2/5 | object |  |
| `message.catalog.bpp/providers[].offers[].descriptor` | 2/5 | object |  |
| `message.catalog.bpp/providers[].offers[].descriptor.code` | 2/5 | string | "buyXgetY" |
| `message.catalog.bpp/providers[].offers[].descriptor.images` | 2/5 | array |  |
| `message.catalog.bpp/providers[].offers[].descriptor.images[]` | 2/5 | string | "https://storage.googleapis.com/bo3151920215/business/7bf9b5 |
| `message.catalog.bpp/providers[].offers[].descriptor.long_desc` | 1/5 | string | "Buy X get Y - Offer C - long" |
| `message.catalog.bpp/providers[].offers[].descriptor.name` | 1/5 | string | "Buy_X_get_Y_-_Offer_C" |
| `message.catalog.bpp/providers[].offers[].descriptor.short_desc` | 1/5 | string | "Buy X get Y - Offer C - short" |
| `message.catalog.bpp/providers[].offers[].id` | 2/5 | string | "185e54b726b7408cb046eb7f1a327037" |
| `message.catalog.bpp/providers[].offers[].item_ids` | 2/5 | array |  |
| `message.catalog.bpp/providers[].offers[].item_ids[]` | 2/5 | string | "73bf1ffd390e4a78a038726864497f3c" |
| `message.catalog.bpp/providers[].offers[].location_ids` | 1/5 | array |  |
| `message.catalog.bpp/providers[].offers[].location_ids[]` | 1/5 | string | "6866b3b4cffea4126a863e45" |
| `message.catalog.bpp/providers[].offers[].tags` | 2/5 | array |  |
| `message.catalog.bpp/providers[].offers[].tags[]` | 2/5 | object |  |
| `message.catalog.bpp/providers[].offers[].tags[].code` | 2/5 | string | "qualifier" |
| `message.catalog.bpp/providers[].offers[].tags[].list` | 2/5 | array |  |
| `message.catalog.bpp/providers[].offers[].tags[].list[]` | 2/5 | object |  |
| `message.catalog.bpp/providers[].offers[].tags[].list[].code` | 2/5 | string | "min_value" |
| `message.catalog.bpp/providers[].offers[].tags[].list[].value` | 2/5 | string | "500.0" |
| `message.catalog.bpp/providers[].offers[].time` | 2/5 | object |  |
| `message.catalog.bpp/providers[].offers[].time.label` | 2/5 | string | "valid" |
| `message.catalog.bpp/providers[].offers[].time.range` | 2/5 | object |  |
| `message.catalog.bpp/providers[].offers[].time.range.end` | 2/5 | string | "2026-12-31T12:32:00Z" |
| `message.catalog.bpp/providers[].offers[].time.range.start` | 2/5 | string | "2026-10-27T12:32:00Z" |
| `message.catalog.bpp/providers[].rating` | 3/5 | string | "5" |
| `message.catalog.bpp/providers[].tags` | 5/5 | array |  |
| `message.catalog.bpp/providers[].tags[]` | 5/5 | object |  |
| `message.catalog.bpp/providers[].tags[].code` | 5/5 | string | "serviceability" |
| `message.catalog.bpp/providers[].tags[].list` | 5/5 | array |  |
| `message.catalog.bpp/providers[].tags[].list[]` | 5/5 | object |  |
| `message.catalog.bpp/providers[].tags[].list[].code` | 5/5 | string | "location" |
| `message.catalog.bpp/providers[].tags[].list[].value` | 5/5 | string | "7bf9b561199f4a898b3f8a3cef91b6e6-loc1" |
| `message.catalog.bpp/providers[].time` | 5/5 | object |  |
| `message.catalog.bpp/providers[].time.label` | 5/5 | string | "enable" |
| `message.catalog.bpp/providers[].time.timestamp` | 5/5 | string | "2026-11-17T06:45:57.460Z" |
| `message.catalog.bpp/providers[].ttl` | 5/5 | string | "P1D" |

Tag groups seen:

- `attr`: name, seq
- `benefit`: item_count, item_id, item_value, value, value_cap, value_type
- `bpp_terms`: accept_bap_terms, np_type
- `config`: input, max, min, seq
- `display`: rank
- `image`: type, url
- `meta`: additive, auto
- `order_value`: min_value
- `origin`: country
- `qualifier`: item_count, min_value
- `serviceability`: category, location, type, unit, val
- `timing`: day_from, day_to, location, time_from, time_to, type
- `type`: type
- `veg_nonveg`: non_veg, veg
- `verification`: valid_from, valid_to, verify_url
