# Beslist.nl Column Reference

This document contains all columns for each table in the Beslist.nl Redshift database.

**Legend:**
- ⭐ = Important column (marked as "Belangrijk" in source)


## `bt.cpa_outclicks_transactional`

**Data granularity**: Per **order line** (not per outclick). One outclick can result in multiple rows if the customer purchased multiple products.

**Important**: The same `stats_id_stat` (outclick ID) can appear multiple times with different `revenue_excl` values - each row represents a different product/order line from the same purchase.

**Correct metric calculations**:
- **Outclicks**: `COUNT(DISTINCT stats_id_stat)`
- **Revenue**: `SUM(revenue_excl)`
- **Order lines**: `COUNT(*)` or `SUM(transactions)`
- **Unique orders**: `COUNT(DISTINCT uuid)`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `technical_uid` | bigint |  |  |
| `stats_technical_uid` | bigint |  |  |
| `stats_id_stat` | bigint | ⭐ | Unieke outclick ID. Use COUNT(DISTINCT stats_id_stat) for outclick counts. Same ID appears multiple times for multi-product orders. |
| `shop_id` | bigint | ⭐ | Shop ID waarop de conversie heeft plaatsgevonden. |
| `shop_name` | character varying | ⭐ | Shop waarop de conversie heeft plaatsgevonden. |
| `run_date` | date |  |  |
| `date` | date | ⭐ | Datum waarop we de omzet toekennen (conversie datum, en als die er niet is, outclick datum). |
| `conversion_date` | date | ⭐ | Datum van de conversie. |
| `outclick_date` | date | ⭐ | Datum van de outclick. |
| `outclick_datetime` | timestamp without time zone | ⭐ | Datum en tijd waarop de outclick plaatsvond. |
| `number_of_days_since_outclick` | bigint |  |  |
| `conversion_number_of_days_since_outclick` | bigint |  |  |
| `is_outclick_date` | integer |  |  |
| `uuid` | character varying | ⭐ | UUID waarmee we de link tussen outclick en conversie kunnen maken.  |
| `gclid` | character varying | ⭐ | GCLID die bij de conversie hoort. |
| `gclid_campaign_name` | character varying |  |  |
| `stats_price` | numeric |  |  |
| `stats_original_price` | numeric |  |  |
| `main_category_id` | bigint | ⭐ | Maincat waarop de outclick plaatsvond. |
| `main_category_name` | character varying | ⭐ | Maincat waarop de outclick plaatsvond. |
| `bid_category_id` | bigint | ⭐ | Bidcat waarop de outclick plaatsvond. |
| `bid_category_name` | character varying | ⭐ | Bidcat waarop de outclick plaatsvond. |
| `deepest_category_id` | bigint | ⭐ | Diepste cat waarop de outclick plaatsvond. |
| `deepest_category_name` | character varying | ⭐ | Diepste cat waarop de outclick plaatsvond. |
| `sb_roas_type_code` | character varying |  |  |
| `sb_roas_medium_percentage` | smallint |  |  |
| `shop_or_cat_target` | character varying |  |  |
| `bidcat_roas_target` | integer |  |  |
| `meetgat_target_pct` | double precision |  |  |
| `roas_target_catman_wens` | double precision |  |  |
| `roas_target_from_shopbid` | double precision |  |  |
| `roas_target_used` | double precision | ⭐ | Het ROAS target wat we gebruikt hebben om CPR uit te rekenen.  |
| `uuid_linked` | integer | ⭐ | Kunnen we een UUID linken met een conversie ja (1) of nee. |
| `transactions` | bigint | ⭐ | Het aantal transacties wat gedaan is. |
| `revenue_excl` | double precision | ⭐ | De shop omzet die gemaakt is vanuit een UUID. |
| `bidcat_t3_tariff` | numeric |  |  |
| `stats_bidcat_t3_tariff` | numeric |  |  |
| `stats_bidcat_tariff_uuid` | character varying |  |  |
| `tariff_data_t3_tariff_by_uuid` | numeric |  |  |
| `tariff_data_t3_tariff_category` | numeric |  |  |
| `tariff_data_t3_tariff_shop` | numeric |  |  |
| `shop_deelt_data` | integer | ⭐ | Deelt een shop data met ons (1) of niet (0). |
| `cpa_cpc_unlinked_clicks_date` | date |  |  |
| `cpa_cpc_linked_rev_linked_click` | double precision |  |  |
| `cpa_cpc_calculations` | integer |  |  |
| `cpa_cpc_period_used` | character varying |  |  |
| `cpa_cpc_linkage` | double precision |  |  |
| `cpa_cpc_coverage` | double precision |  |  |
| `cpa_cpc_linked_outclicks` | bigint |  |  |
| `is_conversie_na_7_dagen` | integer |  |  |
| `is_0_conversie_na_7_dagen` | integer |  |  |
| `label` | character varying | ⭐ | De manier waarop een UUID is afgerekend op die dag, dus bijvoorbeeld CPA, t3 fallback, unlinked revenue. |
| `cpa` | double precision |  |  |
| `cpa_cpc` | double precision |  |  |
| `t3_fallback` | double precision |  |  |
| `calculated_revenue` | numeric |  |  |
| `refund_invoiced_click_revenue` | numeric |  |  |
| `click_revenue` | numeric | ⭐ | De berekende shop kosten / onze omzet vanuit het CPR proces. |
| `is_cpa_roas_target_used_available` | smallint |  |  |
| `is_cpa_cpc_linkedrevlinkedclick_available` | smallint |  |  |
| `is_cpa_cpc_roas_target_used_available` | smallint |  |  |
| `is_t3_fallback_stats_original_price_available` | smallint |  |  |
| `is_t3_fallback_sb_roas_medium_percentage_available` | smallint |  |  |
| `is_t3_fallback_roas_target_catman_wens_available` | smallint |  |  |
| `is_t3_fallback_bidcat_t3_tariff_available` | smallint |  |  |
| `outclick_shop_id` | bigint | ⭐ | De shop waarop de outclick gedaan is. |
| `brand_id` | bigint | ⭐ | Merk wat hoort bij de outclick. |
| `visit_id` | bigint | ⭐ | Visit ID. |
| `item_price` | numeric | ⭐ | Prijs van het product waarop uitgeklikt is. |
| `domain` | character varying | ⭐ | Het domein waarop uitgeklikt is. |
| `ignore_cpc` | integer |  |  |
| `date_specification` | character varying |  |  |
| `is_conversion_without_uuid` | smallint |  |  |
| `is_shop_on_sb30` | smallint |  |  |
| `gclid_from_visit` | character varying |  |  |
| `gclid_from_visit_campaign_name` | character varying |  |  |
| `is_invoiced_by_cpa_next_month` | smallint |  |  |
| `shop_advertising_type` | character varying |  |  |
| `item_id` | bigint |  |  |
| `brand_name` | character varying | ⭐ | Merk wat hoort bij de outclick. |
| `aff_id` | integer | ⭐ | Vanaf welke aff ID de click heeft plaatsgevonden, nodig voor de afleiding van het kanaal. |
| `marketing_channel_aff_id_name` | character varying | ⭐ | Marketing kanaal afleiding. |
| `vis_url` | character varying | ⭐ | De URL van de shop waar naar toe uitgeklikt is. |
| `vis_ref` | character varying | ⭐ | De URL vanuit waar uitgeklikt is naar de shop. |
| `splittest_id` | integer |  |  |
| `transactions_with_uuid` | bigint | ⭐ | Het aantal transacties wat gedaan is en waarvoor we een UUID hebben kunnen terugvinden. |
| `transactions_with_known_revenue_composition` | bigint |  |  |
| `productidv3` | character varying | ⭐ | Productidv3 wat hoort bij de outclick. |
| `marketing_channel_id` | integer |  |  |
| `label_shop_as_t3` | smallint |  |  |
| `shop_linked_outclicks_28d` | integer |  |  |
| `shop_coverage_28d` | double precision |  |  |
| `etl_load_date` | timestamp without time zone |  |  |
| `etl_update_date` | timestamp without time zone |  |  |
| `actual_ind` | smallint | ⭐ | Kolom om vast te stellen of dit record nog actueel is of niet. |
| `deleted_ind` | smallint | ⭐ | Kolom om vast te stellen of dit record nog actueel is of niet. |
| `bidcat_t1_tariff` | numeric |  |  |
| `tariff_data_t1_tariff_by_uuid` | numeric |  |  |
| `tariff_data_t1_tariff_category` | numeric |  |  |
| `tariff_data_t1_tariff_shop` | numeric |  |  |
| `outclick_t1_price` | numeric | ⭐ | De prijs die voor de outclick had moeten worden betaald als we T1 moesten afrekenen. Dit veld wordt gebruikt om te kijken of een shop onder T1 draa... |
| `shop_phase` | integer | ⭐ | Shop fase op het moment van de outclick. |
| `last_valid_conversion_day` | date |  |  |
| `is_shop_phase23_revenue_after_valid_period` | smallint |  |  |
| `is_paying_t1` | smallint | ⭐ | Veld om aan te geven of een shop T1 moest betalen (en dus onder T1 zat). |
| `invoicing_price` | numeric | ⭐ | Gefactureerde shop kosten / onze omzet. Wordt pas gevuld als de facturatie is geweest (meestal de derde werkdag van de maand). |
| `invoicing_price_timestamp` | timestamp without time zone |  |  |
| `tracking_system_name` | character varying |  |  |
| `moduletype_id` | integer | ⭐ | De module waar de outclick vandaan heeft plaatsgevonden. |
| `t3_fallback_factor` | numeric |  |  |
| `t3_fallback_with_factor` | numeric |  |  |
| `affiliate_transaction_id` | character varying |  |  |
| `affiliate_transaction_status` | character varying | ⭐ | Het veld wat aangeeft voor affiliate conversies of de conversie al goedgekeurd is, afgekeurd is of nog pending is. |
| `affiliate_approval_date` | date | ⭐ | De datum waarop een affiliate conversie is goedgekeurd of afgekeurd. |
| `outclick_shop_phase` | integer |  |  |
| `is_pixel_shop` | smallint | ⭐ | Shop werd op de tag afgerekend op het moment van de outclick ja (1) of nee (0). |
| `update_reason` | character varying |  |  |
| `useragent` | character varying | ⭐ | Useragent (device, browser) waar de outclick op plaats heeft gevonden. |
| `is_ios_safari` | smallint |  |  |
| `pim_id` | character varying | ⭐ | Pim ID waarop de outclick heeft plaatsgevonden. |
| `is_roas_garantie_shop` | smallint | ⭐ | Shop was een ROAS garantie shop op het moment van de outclick. |
| `channel_id` | smallint | ⭐ | Channel ID wat gebruikt wordt om het marketing kanaal af te leiden. |
| `first_touch_attribution` | numeric |  |  |
| `last_touch_attribution` | numeric |  |  |
| `linear_attribution` | numeric |  |  |
| `position_based_attribution` | numeric |  |  |
| `last_click_attribution` | numeric |  |  |
| `time_decay_attribution` | numeric |  |  |
| `cpa_cpc_calculations_first_touch` | integer |  |  |
| `cpa_cpc_calculations_last_touch` | integer |  |  |
| `cpa_cpc_calculations_linear` | integer |  |  |
| `cpa_cpc_calculations_position_based` | integer |  |  |
| `cpa_cpc_calculations_last_click` | integer |  |  |
| `cpa_cpc_calculations_time_decay` | integer |  |  |
| `cpa_cpc_linked_rev_linked_click_first_touch` | double precision |  |  |
| `cpa_cpc_linked_rev_linked_click_last_touch` | double precision |  |  |
| `cpa_cpc_linked_rev_linked_click_linear` | double precision |  |  |
| `cpa_cpc_linked_rev_linked_click_position_based` | double precision |  |  |
| `cpa_cpc_linked_rev_linked_click_last_click` | double precision |  |  |
| `cpa_cpc_linked_rev_linked_click_time_decay` | double precision |  |  |
| `label_first_touch` | character varying |  |  |
| `label_last_touch` | character varying |  |  |
| `label_linear` | character varying |  |  |
| `label_position_based` | character varying |  |  |
| `label_last_click` | character varying |  |  |
| `label_time_decay` | character varying |  |  |
| `cpa_first_touch` | double precision |  |  |
| `cpa_last_touch` | double precision |  |  |
| `cpa_linear` | double precision |  |  |
| `cpa_position_based` | double precision |  |  |
| `cpa_last_click` | double precision |  |  |
| `cpa_time_decay` | double precision |  |  |
| `cpa_cpc_first_touch` | double precision |  |  |
| `cpa_cpc_last_touch` | double precision |  |  |
| `cpa_cpc_linear` | double precision |  |  |
| `cpa_cpc_position_based` | double precision |  |  |
| `cpa_cpc_last_click` | double precision |  |  |
| `cpa_cpc_time_decay` | double precision |  |  |
| `calculated_revenue_first_touch` | numeric |  |  |
| `calculated_revenue_last_touch` | numeric |  |  |
| `calculated_revenue_linear` | numeric |  |  |
| `calculated_revenue_position_based` | numeric |  |  |
| `calculated_revenue_last_click` | numeric |  |  |
| `calculated_revenue_time_decay` | numeric |  |  |
| `t3_fallback_with_factor_first_touch` | double precision |  |  |
| `t3_fallback_with_factor_last_touch` | double precision |  |  |
| `t3_fallback_with_factor_linear` | double precision |  |  |
| `t3_fallback_with_factor_position_based` | double precision |  |  |
| `t3_fallback_with_factor_last_click` | double precision |  |  |
| `t3_fallback_with_factor_time_decay` | double precision |  |  |
| `click_revenue_first_touch` | numeric | ⭐ | Shop kosten / onze omzet die we zouden hebben afgerekend als we volgens het first touch attributiemodel zouden hebben geattribueerd. |
| `click_revenue_last_touch` | numeric | ⭐ | Shop kosten / onze omzet die we zouden hebben afgerekend als we volgens het last touch attributiemodel zouden hebben geattribueerd. |
| `click_revenue_linear` | numeric | ⭐ | Shop kosten / onze omzet die we zouden hebben afgerekend als we volgens het lineaire attributiemodel zouden hebben geattribueerd. |
| `click_revenue_position_based` | numeric | ⭐ | Shop kosten / onze omzet die we zouden hebben afgerekend als we volgens het position based attributiemodel zouden hebben geattribueerd. |
| `click_revenue_last_click` | numeric | ⭐ | Shop kosten / onze omzet die we zouden hebben afgerekend als we volgens het last click attributiemodel zouden hebben geattribueerd. (dit is dus ons... |
| `click_revenue_time_decay` | numeric | ⭐ | Shop kosten / onze omzet die we zouden hebben afgerekend als we volgens het time decay attributiemodel zouden hebben geattribueerd. |
| `pricebucket_tariff` | numeric | ⭐ | Het tarief wat we afrekenen als we geen CPR kunnen afrekenen omdat een shop geen data deelt, of de linkage te slecht is. |
| `pricebucket_name` | character varying |  |  |
| `old_t3_fallback` | numeric |  |  |
| `old_t3_fallback_with_factor` | numeric |  |  |
| `dashboard_migratie_start_date` | timestamp without time zone |  |  |
| `dashboard_shop_roas_target` | integer |  |  |
| `dashboard_bidcat_is_cpc` | smallint |  |  |
| `dashboard_bidcat_roas_target` | integer |  |  |
| `roas_target_dashboard` | integer |  |  |
| `dashboard_maincat_is_cpc` | smallint |  |  |
| `dashboard_maincat_roas_target` | integer |  |  |
| `affiliate_bruto_commission` | numeric | ⭐ | De bruto commissie voor een affiliate conversie die we binnen krijgen vanuit Wecantrack. |
| `affiliate_number_of_days_to_approval` | smallint | ⭐ | Het aantal dagen tussen de conversie en het goedkeuren of afkeuren van de conversie. |
| `wct_network_id` | character varying | ⭐ | Het Wecantrack netwerk waarop de shop live staat. |
| `bid_label` | character varying | ⭐ | Het promotielabel wat meegegeven wordt bij het product waarop de outclick heeft plaatsgevonden. |
| `bid_label_roas_target` | smallint |  |  |
| `affiliate_paid_to_publisher` | smallint |  |  |
| `was_unlinked_revenue` | smallint |  |  |
| `product_score_label` | character varying | ⭐ | Het productscore label van het product waarop de outclick heeft plaatsgevonden. |
| `shop_order_item_id` | bigint |  |  |
| `shop_order_id` | bigint |  |  |
| `bvb_order_id` | bigint | ⭐ | Het WW order ID, die je uniek kan tellen om het aantal WW bestellingen te tellen. |
| `bvb_order_nr` | character varying |  |  |
| `transaction_costs` | numeric | ⭐ | De WW transactiekosten die berekend zijn voor een WW bestelling. |
| `shoppingcart_shipping_costs` | numeric | ⭐ | De WW verzendkosten die berekend zijn voor een WW bestelling. |
| `shoppingcart_vat_costs` | numeric | ⭐ | De WW BTW kosten die berekend zijn voor een WW bestelling. |
| `shoppingcart_number_ordered` | smallint | ⭐ | Het aantal bestelde producten in een WW bestelling. |
| `affiliate_avg_number_of_days_to_decline` | smallint | ⭐ | Het gemiddelde aantal dagen dat het duurt totdat een affiliate conversie wordt afgekeurd. |

## `bt.daily_standup_metrics_category`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `technical_uid` | bigint |  |  |
| `dim_date_key` | bigint | ⭐ | Datum in YYYYMMDD format. |
| `year_week_number` | character varying | ⭐ | Jaar-week nummer. |
| `year_month_number` | character varying | ⭐ | Jaar-maand nummer. |
| `deepest_category_id` | bigint | ⭐ | Diepste categorie ID. |
| `omzet_total` | numeric | ⭐ | Totale omzet. |
| `visits` | bigint | ⭐ | Bezoekers. |
| `omzet_visit` | numeric | ⭐ | Omzet die we kunnen toekennen aan die bezoekers, die je kan gebruiken voor de OPB. |
| `bvb_clicks_visit` | bigint | ⭐ | In WW clicks gedaan door onze bezoekers, bruikbaar voor de CTR. |
| `outclicks_visit` | bigint | ⭐ | Outclicks gedaan door onze bezoekers, bruikbaar voor de CTR. |
| `cpc_revenue_visit` | numeric | ⭐ | CPR omzet die we kunnen toekennen aan onze bezoekers. |
| `ww_revenue_visit` | numeric | ⭐ | WW omzet die we kunnen toekennen aan onze bezoekers. |
| `bounce_clicks_visit` | bigint | ⭐ | Het aantal visits wat bouncet (geen CPC of WW productclicks doet). |
| `true_ctr_clicks_visit` | bigint | ⭐ | Het aantal outclicks wat gedaan wordt door mensen die outclicks doen, voor de true CTR. |
| `revenue` | double precision | ⭐ | De shop omzet. |
| `linked_costs` | numeric | ⭐ | Gelinkte shop kosten. |
| `linked_clicks` | bigint | ⭐ | Gelinkte outclicks. |
| `costs` | numeric | ⭐ | Shop kosten. |
| `marge` | numeric | ⭐ | Totale marge. |
| `load_date` | timestamp without time zone |  |  |
| `update_date` | timestamp without time zone |  |  |
| `deleted_ind` | integer | ⭐ | Geeft aan of een record nog actueel is of niet. |
| `conv_revenue_excl_roas_type` | numeric |  |  |
| `conv_costs_roas_type` | numeric |  |  |
| `marketing_channel` | character varying | ⭐ | Marketing kanaal. |
| `linked_revenue` | numeric | ⭐ | Linked shop omzet. |
| `conv_linked_revenue_roas_type` | numeric |  |  |
| `cpc_revenue` | numeric | ⭐ | CPR omzet, exclusief affiliates. |
| `ww_revenue` | numeric | ⭐ | WW omzet. |
| `outclicks` | bigint | ⭐ | Outclicks. |
| `bvb_clicks` | bigint | ⭐ | In WW clicks. |
| `total_outclicks_conversions` | bigint | ⭐ | Totale outclicks, gedaan voor shops die data delen. |
| `transactions` | bigint | ⭐ | Aantal transacties, gemeten voor shops die data delen. |
| `avg_roas_target` | numeric | ⭐ | Het gemiddelde ROAS target waartegen we outclicks hebben afgerekend. |
| `cpa_label_outclicks` | bigint | ⭐ | Het aantal outclicks dat we hebben afgerekend via CPA. |
| `cpa_cpc_label_outclicks` | bigint | ⭐ | Het aantal outclicks dat we hebben afgerekend via CPA CPC. |
| `t3_fallback_label_outclicks` | bigint | ⭐ | Het aantal outclicks dat we hebben afgerekend via T3 fallback. |
| `cpa_label_revenue` | numeric | ⭐ | Onze omzet die gemaakt wordt via CPA. |
| `cpa_cpc_label_revenue` | numeric | ⭐ | Onze omzet die gemaakt wordt via CPA CPC. |
| `t3_fallback_label_revenue` | numeric | ⭐ | Onze omzet die gemaakt wordt via T3 fallback. |
| `ingekochte_visits` | bigint | ⭐ | Het aantal visits wat we ingekocht hebben bij DM. |
| `outclicks_visit_stats` | bigint | ⭐ | Outclicks die toegekend kunnen worden aan visits. Deze wordt gebruikt om de CTR te kunnen bepalen voordat het door CPR heen gaat. Omdat we normaal ... |
| `linked_transactions` | bigint | ⭐ | Gelinkte transacties. |
| `affiliate_revenue_visit` | numeric | ⭐ | Affiliate omzet die we kunnen toekennen aan onze bezoekers. |
| `omzet_visit_excl_affiliates` | numeric | ⭐ | Omzet die we kunnen toekennen aan die bezoekers, die je kan gebruiken voor de OPB. Excl. affiliates. |
| `affiliate_revenue` | numeric | ⭐ | Affiliate omzet. |
| `omzet_total_excl_affiliates` | numeric | ⭐ | Totale omzet, excl. affiliates. |
| `marge_excl_affiliates` | numeric | ⭐ | Totale marge, excl. affiliates. |
| `avg_roas_target_excl_affiliates` | numeric | ⭐ | Het gemiddelde ROAS target waartegen we outclicks hebben afgerekend, excl. affiliates. |
| `revenue_excl_affiliates` | numeric | ⭐ | Shop omzet, excl. affiliates. |
| `linked_revenue_excl_affiliates` | numeric | ⭐ | Linked shop omzet, excl. affiliates. |
| `linked_costs_excl_affiliates` | numeric | ⭐ | Linked shop kosten, excl. affiliates. |
| `linked_clicks_excl_affiliates` | bigint | ⭐ | Linked outclicks, excl. affiliates. |
| `total_outclicks_conversions_excl_affiliates` | bigint | ⭐ | Totale outclicks, gedaan voor shops die data delen, excl. affiliates. |
| `transactions_excl_affiliates` | bigint | ⭐ | Totale transacties, excl. affiliates. |
| `linked_transactions_excl_affiliates` | bigint | ⭐ | Totale linked transacties, excl. affiliates. |
| `conv_revenue_excl_roas_type_excl_affiliates` | numeric |  |  |
| `conv_linked_revenue_roas_type_excl_affiliates` | numeric |  |  |
| `conv_costs_roas_type_excl_affiliates` | numeric |  |  |
| `outclicks_excl_affiliates` | bigint | ⭐ | Totale outclicks, excl. affiliates. |
| `unique_ip_visits` | bigint | ⭐ | Het aantal bezoekers wat geland is op Beslist, geteld door middel van unieke IPs.  |
| `domain` | character varying | ⭐ | Domein. |

## `bt.ean_score`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `technical_uid` | bigint |  |  |
| `ean` | character varying |  |  |
| `shop_id` | bigint |  |  |
| `shop_name` | character varying |  |  |
| `country` | character varying |  |  |
| `pim_id` | character varying |  |  |
| `title` | character varying |  |  |
| `is_productvalid` | integer |  |  |
| `deliverytimesort` | integer |  |  |
| `price` | numeric |  |  |
| `deliverycost` | numeric |  |  |
| `price_deliverycost` | numeric |  |  |
| `saleprice` | numeric |  |  |
| `min_price` | numeric |  |  |
| `max_price` | numeric |  |  |
| `total_shops_with_ean` | bigint |  |  |
| `shop_has_lowest_price` | integer |  |  |
| `min_rank` | bigint |  |  |
| `total_clients_per_ean` | integer |  |  |
| `pct_diff_min_price` | numeric |  |  |
| `euro_diff_min_price` | numeric |  |  |
| `price_range_min` | numeric |  |  |
| `price_range_max` | numeric |  |  |
| `is_gsd_nl_shop` | integer |  |  |
| `is_gsd_be_shop` | integer |  |  |
| `score_offers_per_ean` | integer |  |  |
| `score_lowest_price` | integer |  |  |
| `score_bestseller` | integer |  |  |
| `score_bestseller_100` | integer |  |  |
| `score_top_revenue` | integer |  |  |
| `score_productscore` | integer |  |  |
| `score_deliverytimesort` | integer |  |  |
| `totaal_ean_score` | integer |  |  |
| `ean_score_label` | character varying |  |  |
| `load_start_date` | timestamp without time zone |  |  |
| `load_end_date` | timestamp without time zone |  |  |
| `actual_ind` | integer |  |  |
| `deleted_ind` | integer |  |  |
| `main_category_id` | bigint |  |  |
| `year` | character varying |  |  |
| `month` | character varying |  |  |
| `day` | character varying |  |  |
| `is_zombie_product` | integer |  |  |

## `bt.productscore`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `technical_uid` | bigint |  |  |
| `productidv3` | character varying | ⭐ | Unieke identifier van het product (shopitem). |
| `shop_id` | bigint | ⭐ | Shop ID. |
| `shop_name` | character varying | ⭐ | Shop naam. |
| `country` | character varying | ⭐ | Land waarop het product in de search index stond. |
| `ean` | character varying | ⭐ | Bijbehorende EAN. |
| `title` | character varying | ⭐ | Product titel. |
| `is_productvalid` | integer | ⭐ | Stond het product live of niet. |
| `price` | numeric | ⭐ | Prijs van het product. |
| `deliverycost` | numeric | ⭐ | Verzendkosten. |
| `price_deliverycost` | numeric | ⭐ | Prijs inclusief verzending. |
| `saleprice` | numeric | ⭐ | De verkoopprijs van het product. De korting is eraf als het product in de aanbieding is, en anders is het de normale prijs. |
| `min_price` | numeric | ⭐ | De laagste prijs van het product, op EAN bepaald. |
| `max_price` | numeric | ⭐ | De hoogste prijs van het product, op EAN bepaald. |
| `total_shops_with_ean` | bigint | ⭐ | Het aantal shops dat het product aanbiedt in de search index. |
| `shop_has_lowest_price` | integer | ⭐ | Heeft de shop de laagste prijs voor het product, ja (1) of nee (0). |
| `shop_has_highest_price` | integer | ⭐ | Heeft de shop de hoogste prijs voor het product, ja (1) of nee (0). |
| `shop_is_only_retailer` | integer | ⭐ | Shop is de enige aanbieder van een product, ja (1) of nee (0). |
| `min_rank` | bigint | ⭐ | De laagste rank voor een EAN, vanuit de Google Bestseller dataset. |
| `score_top_revenue` | integer | ⭐ | Als een product over de afgelopen 30 dagen binnen de top 20% van de producten valt qua omzet, dan krijgt deze 2 punten. Tussen de 20% en 50%, dan 1... |
| `score_aanbod_beslist` | integer | ⭐ | Als een product door meerdere shops wordt aangeboden, en een shop heeft de laagste prijs, dan krijgt deze 4 punten. Als er meerdere aanbieders zijn... |
| `score_uniek_beslist` | integer | ⭐ | Als een shop de enige aanbieder is van een product, dan krijgt deze 1 punt, anders 0. |
| `score_bestseller` | integer | ⭐ | Als een product een bestseller is volgens Google, dan krijgt deze 1 punt, anders 0. |
| `score_bestseller_100` | integer | ⭐ | Als een product een bestseller is volgens Google en een rank van maximaal 100 heeft, dan krijgt deze 1 punt, anders 0. |
| `score_pricerange_google` | integer | ⭐ | Als een product een prijs heeft die onder de minimale prijsrange volgens Google ligt, dan krijgt deze 4 punten. Binnen de prijsrange krijgt hij 1 p... |
| `totaal_productscore` | integer | ⭐ | De totale telling van alle punten aantallen. |
| `load_start_date` | timestamp without time zone |  |  |
| `load_end_date` | timestamp without time zone |  |  |
| `actual_ind` | integer | ⭐ | Een getal wat aangeeft of we te maken hebben met het actuele record. |
| `deleted_ind` | integer | ⭐ | Deze geeft aan of een record nog gebruikt mag worden of verwijderd/niet meer geldig is. |
| `is_gsd_nl_shop` | integer | ⭐ | Op het moment van berekenen was de shop een GSD NL shop of niet. |
| `is_gsd_be_shop` | integer | ⭐ | Op het moment van berekenen was de shop een GSD BE shop of niet. |
| `total_clients_per_ean` | integer | ⭐ | Het totaal aantal klanten met een EAN. |
| `only_shop_with_lowest_price` | integer | ⭐ | De shop is de enige met een laagste prijs van een product (1) of niet (0). |
| `pct_diff_min_price` | numeric | ⭐ | Het percentage verschil tussen de laagste prijs van een product en de prijs waarvoor een shop het aanbiedt. |
| `euro_diff_min_price` | numeric | ⭐ | Het verschil bedrag tussen de laagste prijs van een product en de prijs waarvoor een shop het aanbiedt. |
| `productscore_label` | character varying | ⭐ | Het uiteindelijke productscore label, bepaald op basis van het aantal productscore punten en wat andere ruling (zoals bijvoorbeeld de top label rul... |
| `price_range_min` | numeric | ⭐ | De laagste prijs in de prijsrange van een product volgens Google. |
| `price_range_max` | numeric | ⭐ | De hoogste prijs in de prijsrange van een product volgens Google. |
| `main_category_id` | bigint | ⭐ | Maincat ID waarin het product is ingedeeld. |
| `year` | character varying |  |  |
| `month` | character varying |  |  |
| `day` | character varying |  |  |
| `pim_id` | character varying | ⭐ | Bijbehorende PIM ID. |
| `is_gsd_de_shop` | integer | ⭐ | Op het moment van berekenen was de shop een GSD DE shop of niet. |
| `is_zombie_product` | integer | ⭐ | Is een product aangemerkt als zombie product (1, geen outclicks of WW productclicks in de afgelopen 30 dagen) of niet (0). |
| `is_dm_hottie` | integer | ⭐ | Is een product aangemerkt als hottie product wat we extra moeten stimuleren (1) of niet (0). |
| `outclicks_30_days` | bigint | ⭐ | Het aantal outclicks op het product over de afgelopen 30 dagen. |
| `linked_outclicks_30_days` | bigint | ⭐ | Het aantal gelinkte outclicks op het product over de afgelopen 30 dagen. |
| `linked_cpc_shop_revenue_30_days` | numeric | ⭐ | De gelinkte CPC shop omzet op een product in de afgelopen 30 dagen. |
| `deliverytimesort` | integer | ⭐ | Verzendtijden van het product, gegroepeerd. |
| `ean_quality` | character varying | ⭐ | Een veld wat aangeeft of het EAN invalide is (te lang of te kort), of duplicaat is (1 product heeft meerdere EANs bij een shop). |
| `score_aanbod_beslist_nieuw_conditie` | integer | ⭐ | Bij de berekening worden alleen nieuwe items meegenomen. Als een product door meerdere shops wordt aangeboden, en een shop heeft de laagste prijs, ... |
| `label_reason` | character varying | ⭐ | Uitleg van waarom een product een bepaald productscore label toegekend krijgt. |
| `new_min_price` | numeric | ⭐ | De laagste prijs van het product, op EAN bepaald, waarbij alleen nieuwe items (= nieuw conditie) worden meegenomen. |
| `new_max_price` | numeric | ⭐ | De hoogste prijs van het product, op EAN bepaald, waarbij alleen nieuwe items (= nieuw conditie) worden meegenomen. |
| `new_total_shops_with_ean` | bigint | ⭐ | Het aantal shops dat het product aanbiedt in de search index, waarbij we alleen producten met een nieuw conditie meenemen. |
| `new_shop_has_lowest_price` | integer | ⭐ | Heeft de shop de laagste prijs voor het product, ja (1) of nee (0), waarbij we alleen producten met een nieuw conditie meenemen. |
| `new_shop_has_highest_price` | integer | ⭐ | Heeft de shop de hoogste prijs voor het product, ja (1) of nee (0), waarbij we alleen producten met een nieuw conditie meenemen. |
| `new_shop_is_only_retailer` | integer | ⭐ | Shop is de enige aanbieder van een product, ja (1) of nee (0), waarbij we alleen producten met een nieuw conditie meenemen. |
| `is_dm_hottie_test` | integer |  |  |
| `shop_boost` | integer | ⭐ | Soms willen we een shop een boost geven door items een A productscore label te geven, als wij zien dat een shop in zijn geheel uitzonderlijk goed p... |
| `shop_boost_test` | integer |  |  |
| `condition` | character varying | ⭐ | De conditie van een product, is deze nieuw, refurbished, tweedehands of tweedekans? |
| `pct_items_with_bidlabel` | numeric | ⭐ | Het percentage van het totaal aantal items van een shop met het bidlabel wat bij het product staat weggeschreven. Producten worden uitgesloten van ... |
| `is_top_bidlabel` | integer | ⭐ | Op basis van omzet over de afgelopen 30 dagen wordt bepaald of een bidlabel qua omzet goed scoort (minimaal 50 outclicks en 2,65 euro rev/click). Z... |

## `bt.search_console`

**Data granularity**: Per day, per URL (with aff_id), per keyword, per device, per country. Use `clean_url` for aggregation without tracking parameters.

**Important**: Multiple rows can exist for the same underlying page due to different `aff_id` tracking parameters in the URL. When aggregating, group by `clean_url` instead of `url` and recalculate CTR as `SUM(clicks)/SUM(impressions)`.

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `technical_uid` | bigint |  | Unique row identifier. |
| `dim_date_key` | bigint | ⭐ | Date in YYYYMMDD format. Join to dim_date for period groupings. |
| `country` | character varying | ⭐ | Country code (ISO 3166-1 alpha-3). Main values: 'nld' (Netherlands), 'bel' (Belgium), 'deu' (Germany). |
| `device` | character varying | ⭐ | Device type: 'DESKTOP', 'MOBILE', 'TABLET'. |
| `url` | character varying | ⭐ | Full URL as seen by Google (includes aff_id tracking parameters). |
| `keywords` | character varying | ⭐ | Search keyword/query from Google Search Console. |
| `clicks` | integer | ⭐ | Number of clicks from Google search results to this URL for this keyword. |
| `impressions` | integer | ⭐ | Number of times URL appeared in Google search results for this keyword. |
| `ctr` | numeric | ⭐ | Click-through rate from Google (clicks/impressions). Recalculate when aggregating. |
| `avg_position` | numeric | ⭐ | Average ranking position in Google search results (1.0 = top position). |
| `clean_url` | character varying | ⭐ | URL without aff_id tracking parameters. Use this for aggregation. |
| `deepest_category_id` | bigint | ⭐ | Deepest category ID. Join to dim_category for category hierarchy. |
| `type_url` | character varying | ⭐ | URL type: 'R-url' (search/r/keyword), 'C-url' (filtered/c/facet), 'PLP' (product page), 'Browse-url zonder /r/ en /c/' (category browse), 'Homepage'. |
| `label` | character varying |  | Additional label/classification. |
| `year` | character varying |  | Year extracted from date. |
| `month` | character varying |  | Month extracted from date. |
| `day` | character varying |  | Day extracted from date. |
| `load_date` | timestamp without time zone |  | When data was loaded into Redshift. |
| `update_date` | timestamp without time zone |  | When data was last updated. |
| `deleted_ind` | integer |  | Soft delete indicator (0=active, 1=deleted). Always filter deleted_ind=0. |
| `is_commercial_own_brand` | integer | ⭐ | Keyword intent: mentions Beslist brand (1=yes, 0=no). |
| `is_commercial_shop` | integer | ⭐ | Keyword intent: mentions a shop/retailer name like "action" (1=yes, 0=no). Example: "strooizout action". |
| `is_commercial_brand` | integer | ⭐ | Keyword intent: mentions a product brand (1=yes, 0=no). Example: "nintendo switch 2". |
| `is_transactional_general` | integer | ⭐ | Keyword intent: general buying intent like "kopen", "bestellen" (1=yes, 0=no). |
| `is_transactional_sale` | integer | ⭐ | Keyword intent: sale/discount intent like "aanbieding", "korting" (1=yes, 0=no). |
| `is_informational` | integer | ⭐ | Keyword intent: informational/generic search (1=yes, 0=no). Example: "slee", "switch 2". |
| `keyword_count` | integer |  | Number of words in the keyword. |
| `keyword_length` | character varying | ⭐ | Keyword length category: 'Short-tail', 'Mid-tail', 'Long-tail'. |
| `visits` | bigint | ⭐ | Beslist visits from this keyword (internal tracking). |
| `ww_revenue` | numeric | ⭐ | WW (White Wallet) revenue generated from this keyword. |
| `cpc_revenue` | numeric | ⭐ | CPC revenue generated from this keyword. |
| `number_of_outclicks` | bigint | ⭐ | Outclicks generated from this keyword. |
| `number_of_bvb_clicks` | bigint |  | BVB clicks from this keyword. |
| `number_of_orders` | bigint | ⭐ | Orders generated from this keyword. |
| `number_of_cpc_productclicks` | bigint |  | CPC product clicks from this keyword. |
| `number_of_ww_productclicks` | bigint |  | WW product clicks from this keyword. |
| `acquisition_costs` | numeric |  | Acquisition costs for this keyword. |
| `adsense_revenue` | numeric |  | Adsense revenue from this keyword. |
| `bounce_visits` | bigint |  | Bounced visits from this keyword. |
| `cpc_roas_revenue` | numeric |  | CPC ROAS revenue. |
| `cpc_roas_costs` | numeric |  | CPC ROAS costs. |
| `user` | character varying |  | User identifier. |
| `affiliate_revenue` | numeric |  | Affiliate revenue from this keyword. |

## `bt.shop_list`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `technical_uid` | bigint |  |  |
| `dim_date_key` | bigint | ⭐ | Datum waarvoor de shop status wordt weergegeven, in YYYYMMDD format. |
| `date` | date | ⭐ | Datum. |
| `shop_id` | bigint | ⭐ | Shop ID. |
| `shop_name` | character varying | ⭐ | Shop naam. |
| `client_id` | bigint | ⭐ | Klant ID. |
| `client_name` | character varying | ⭐ | Klant naam. |
| `accountmanager_name` | character varying | ⭐ | Accountmanager voor de shop. |
| `hide_online` | smallint | ⭐ | Staat de shop op hide online ja (1) of nee (0). |
| `is_disabled` | smallint | ⭐ | Is de shop disabled door finance ja (1) of nee (0).  |
| `has_contract` | integer | ⭐ | Shop heeft een contract ja (1) of nee (0). |
| `shop_phase` | integer | ⭐ | Shop fase. |
| `is_css_shop` | bigint | ⭐ | Shop is een CSS shop ja (1) of nee (0). |
| `is_affiliate_shop` | smallint | ⭐ | Shop is een affiliate shop ja (1) of nee (0). |
| `has_cpc_contract` | integer | ⭐ | Shop heeft een CPC contract ja (1) of nee (0). |
| `has_cps_contract` | integer | ⭐ | Shop heeft een CPS contract ja (1) of nee (0). |
| `has_ms_contract` | integer | ⭐ | Shop heeft een MS contract ja (1) of nee (0). |
| `has_smartbidding_contract` | integer |  |  |
| `has_conversiontracking_contract` | integer |  |  |
| `listed_on_nl` | smallint | ⭐ | Shop staat live op NL ja (1) of nee (0). |
| `listed_on_be` | smallint | ⭐ | Shop staat live op BE ja (1) of nee (0). |
| `listed_on_de` | integer | ⭐ | Shop staat live op DE ja (1) of nee (0). |
| `cpc_contract_start_date` | timestamp without time zone | ⭐ | Startdatum van het CPC contract (waar relevant). |
| `cpc_contract_end_date` | timestamp without time zone | ⭐ | Einddatum van het CPC contract (waar relevant). |
| `cps_contract_start_date` | timestamp without time zone | ⭐ | Startdatum van het CPS contract (waar relevant). |
| `cps_contract_end_date` | timestamp without time zone | ⭐ | Einddatum van het CPS contract (waar relevant). |
| `ms_contract_start_date` | timestamp without time zone | ⭐ | Startdatum van het MS contract (waar relevant). |
| `ms_contract_end_date` | timestamp without time zone | ⭐ | Einddatum van het MS contract (waar relevant). |
| `cpc_contract_start` | character varying | ⭐ | Startdatum van het CPC contract (waar relevant), in jaar-week. |
| `cps_contract_start` | character varying | ⭐ | Startdatum van het CPS contract (waar relevant), in jaar-week. |
| `ms_contract_start` | character varying | ⭐ | Startdatum van het MS contract (waar relevant), in jaar-week. |
| `product_count` | integer |  |  |
| `is_gsd_nl_shop` | integer | ⭐ | Shop is een GSD NL shop ja (1) of nee (0). |
| `is_gsd_be_shop` | integer | ⭐ | Shop is een GSD BE shop ja (1) of nee (0). |
| `is_pixel_shop` | integer | ⭐ | Shop wordt afgerekend op de tag ja (1) of nee (0). |
| `is_roas_garantie_shop` | integer | ⭐ | Shop is een ROAS garantie shop ja (1) of nee (0). |
| `is_gsd_de_shop` | integer | ⭐ | Shop is een GSD DE shop ja (1) of nee (0). |
| `is_wecantrack_shop` | integer | ⭐ | Shop wordt afgerekend op wecantrack ja (1) of nee (0). |
| `last_phase_change_date` | date | ⭐ | De laatste datum waarop de shop fase is veranderd. |
| `last_productclick_date` | timestamp without time zone | ⭐ | De laatste datum waarop de shop productclicks heeft gehad. |
| `shop_earningsmodel` | character varying | ⭐ | Het verdienmodel van de shop (CPC, WW of Blended). |
| `shop_listed_on` | character varying | ⭐ | De verschillende domeinen waarop een shop live staat. |
| `feed_bidding` | smallint |  |  |
| `shop_registered_by` | character varying | ⭐ | De manieren waarop de shop bij ons is binnengekomen als klant. |
| `onboarding_step` | character varying | ⭐ | De onboarding stappen waar de shop op dat moment in zit. |
| `total_findable_items_current` | bigint | ⭐ | Het totaal aantal livestaande items van de shop. |
| `total_findable_shopitems_current` | bigint | ⭐ | Het totaal aantal livestaande shopitems van de shop. |
| `total_findable_items_current_merk` | bigint | ⭐ | Het totaal aantal livestaande items van de shop met een merk. |
| `highest_total_findable_items_365` | bigint | ⭐ | Het hoogste aantal livestaande items van een shop in de afgelopen 365 dagen. |
| `items_not_deepestcat` | bigint | ⭐ | Het totaal aantal items van de shop wat niet in de diepste categorie is ingedeeld. |
| `items_not_overig` | bigint | ⭐ | Het totaal aantal items van de shop, excl. !Overig. |
| `bidcats_met_items` | bigint | ⭐ | Het aantal bidcats waarin een shop items heeft in de search index. |
| `bidcats_met_valid_items` | bigint | ⭐ | Het aantal bidcats waarin een shop livestaande items heeft in de search index. |
| `suc_pct` | double precision | ⭐ | Het SUC percentage wat gemeten is voor de shop op die dag. |
| `ean_coverage` | numeric | ⭐ | De EAN dekking (items met een EAN gedeeld door het aantal items van de shop). |
| `delta_total_findable_items` | bigint | ⭐ | Het verschil tussen de livestaande items en het hoogste aantal livestaande items in de afgelopen 365 dagen. |
| `gsd_outclicks` | bigint | ⭐ | Het aantal gedane Google Shopping Direct outclicks naar de shop. |
| `gsd_shop_costs` | numeric | ⭐ | De gemaakte Google Shopping Direct shop kosten (= onze omzet). |
| `gsd_shop_revenue` | double precision | ⭐ | De gemaakte Google Shopping Direct shop omzet. |
| `outclicks` | bigint | ⭐ | Het aantal gedane outclicks naar de shop. |
| `linked_outclicks` | bigint | ⭐ | Het aantal gedane gelinkte outclicks naar de shop. |
| `shop_costs` | numeric | ⭐ | De gemaakte shop kosten (= onze omzet). |
| `shop_revenue` | double precision | ⭐ | De gemaakte shop omzet. |
| `shop_costs_365` | numeric | ⭐ | De gemaakte shop kosten (= onze omzet) in de afgelopen 365 dagen. |
| `shop_below_t1` | integer | ⭐ | Draait de shop onder T1 ja (1) of nee (0). |
| `productscore_a_nl_shopitems` | bigint | ⭐ | Het aantal A productscore shopitems op NL. |
| `productscore_b_nl_shopitems` | bigint | ⭐ | Het aantal B productscore shopitems op NL. |
| `productscore_c_nl_shopitems` | bigint | ⭐ | Het aantal C productscore shopitems op NL. |
| `productscore_no_data_nl_shopitems` | bigint | ⭐ | Het aantal no data productscore shopitems op NL. |
| `productscore_no_ean_nl_shopitems` | bigint | ⭐ | Het aantal no EAN productscore shopitems op NL. |
| `productscore_a_be_shopitems` | bigint | ⭐ | Het aantal A productscore shopitems op BE. |
| `productscore_b_be_shopitems` | bigint | ⭐ | Het aantal B productscore shopitems op BE. |
| `productscore_c_be_shopitems` | bigint | ⭐ | Het aantal C productscore shopitems op BE. |
| `productscore_no_data_be_shopitems` | bigint | ⭐ | Het aantal no data productscore shopitems op BE. |
| `productscore_no_ean_be_shopitems` | bigint | ⭐ | Het aantal no EAN productscore shopitems op BE. |
| `productscore_a_de_shopitems` | bigint | ⭐ | Het aantal A productscore shopitems op DE. |
| `productscore_b_de_shopitems` | bigint | ⭐ | Het aantal B productscore shopitems op DE. |
| `productscore_c_de_shopitems` | bigint | ⭐ | Het aantal C productscore shopitems op DE. |
| `productscore_no_data_de_shopitems` | bigint | ⭐ | Het aantal no data productscore shopitems op DE. |
| `productscore_no_ean_de_shopitems` | bigint | ⭐ | Het aantal no EAN productscore shopitems op DE. |
| `plp_shopitems` | bigint | ⭐ | Het aantal items wat een shop live heeft staan waarvoor meerdere aanbieders per EAN zijn. |
| `plp_shopitems_2_aanbieders` | bigint | ⭐ | Het aantal items wat een shop live heeft staan waarvoor twee aanbieders per EAN zijn. Als de shop deze offline haalt, zijn er dus geen PLPs meer te... |
| `bvb_clicks` | bigint | ⭐ | Het aantal gedane in WW clicks. |
| `cpc_bid_categories` | bigint | ⭐ | Het aantal bid categorieën waarvoor een ROAS target is ingevuld in het dashboard. |
| `dashboard_changes` | bigint | ⭐ | Het aantal bid categorieën waarvoor een ROAS target is gewijzigd in het dashboard. |
| `load_date` | timestamp without time zone |  |  |
| `update_date` | timestamp without time zone |  |  |
| `deleted_ind` | integer | ⭐ | Dit veld geeft aan of een record verwijderd is en dus niet meer actueel is. |
| `first_live_date` | timestamp without time zone | ⭐ | De eerste datum waarop een shop live kwam te staan, dat wil zeggen: niet op hide online, shop fase 1 en met items live. |
| `first_live_date_label` | character varying |  |  |
| `cpc_revenue` | numeric | ⭐ | CPR omzet (= shop kosten) die gemaakt is door de shop. |
| `transactions` | bigint | ⭐ | Het aantal transacties dat we gemeten hebben bij de shop. |
| `shop_shares_data` | integer | ⭐ | Deelt de shop conversie data ja (1) of nee (0). |
| `data_sharing_source_system` | character varying | ⭐ | De manier waarop de shop data deelt, via welk systeem. |
| `outclicks_30_days` | bigint | ⭐ | Het aantal outclicks naar de shop in de afgelopen 30 dagen. |
| `outclicks_30_days_earlier` | bigint | ⭐ | Het aantal outclicks naar de shop in de 30 dagen voor die 30 dagen periode. |
| `bvb_clicks_30_days` | bigint | ⭐ | Het aantal in WW clicks naar de shop in de afgelopen 30 dagen. |
| `bvb_clicks_30_days_earlier` | bigint | ⭐ | Het aantal in WW clicks naar de shop in de 30 dagen voor die 30 dagen periode. |
| `shop_costs_ytd` | numeric | ⭐ | De gemaakte shop kosten (= onze omzet) in het jaar tot dusver. |
| `shop_costs_ytd_previous_year` | numeric | ⭐ | De gemaakte shop kosten (= onze omzet) in het vorige jaar tot dusver. |
| `last_contact_date` | timestamp without time zone | ⭐ | De datum waarop we voor het laatst contact hebben gehad met de shop door middel van (video)meetings of telefoongesprekken. |
| `last_contact_date_label` | character varying |  |  |
| `shop_has_gsd_consent` | integer | ⭐ | Shop heeft consent gegeven om gebruikt te worden in Google Shopping Direct, ja (1) of nee (0). |
| `has_ms_mf_contract` | integer | ⭐ | Shop heeft een MS MF contract, ja (1) of nee (0). |
| `ms_mf_contract_start` | character varying | ⭐ | MS MF contract startdatum, in jaar-week. |
| `ms_mf_contract_start_date` | timestamp without time zone | ⭐ | Startdatum van het MS MF contract, waar relevent. |
| `ms_mf_contract_end_date` | timestamp without time zone | ⭐ | Einddatum van het MS MF contract, waar relevant. |
| `is_plp_only_shop` | integer | ⭐ | Shop wordt alleen weergegeven op PLPs als er dubbelingen in items zijn, ja (1) of nee (0). |
| `accountmanager_first_date` | timestamp without time zone | ⭐ | De eerste datum waarop de huidige accountmanager de accountmanager is geworden. |
| `accountmanager_first_date_label` | character varying |  |  |
| `shop_charging_model` | character varying | ⭐ | De manier waarop een shop wordt afgerekend. Bijvoorbeeld, een shop met een CPC verdienmodel wordt afgerekend op CPR als deze ook data deelt, en op ... |
| `opzegging` | integer | ⭐ | Shop heeft/is opgezegd, ja (1) of nee (0). |
| `opzegreden` | character varying | ⭐ | Als een shop heeft opgezegd, wordt hier de reden in gezet. |
| `opzegreden_numeriek` | character varying |  |  |
| `shop_priority_label` | character varying | ⭐ | De prioriteit die wij geven aan een shop, op basis van bepalingen vanuit een script van Bram. |
| `shop_suc_status` | integer | ⭐ | De SUC status van een shop, die we gebruiken om te bepalen of we fails voor een shop wel of niet als echte fail zien. Als wij namelijk zelf iets fo... |
| `previous_hide_online` | integer | ⭐ | Hide online status van een dag eerder. |

## `bt.shop_main_attributes_by_day`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `technical_uid` | bigint |  |  |
| `dim_date_key` | bigint |  |  |
| `date` | date |  |  |
| `shop_id` | bigint |  |  |
| `shop_name` | character varying |  |  |
| `listed_on_nl` | smallint |  |  |
| `listed_on_be` | smallint |  |  |
| `is_disabled` | smallint |  |  |
| `hide_online` | smallint |  |  |
| `shop_phase` | integer |  |  |
| `shop_verdienmodel` | character varying |  |  |
| `client_id` | bigint |  |  |
| `client_name` | character varying |  |  |
| `accountmanager_id` | bigint |  |  |
| `accountmanager_name` | character varying |  |  |
| `prospect_id` | integer |  |  |
| `prospect_name` | character varying |  |  |
| `prospect_feedpartner_id` | bigint |  |  |
| `prospect_feedpartner_name` | character varying |  |  |
| `prospect_winkelwagen_partner_id` | bigint |  |  |
| `prospect_winkelwagen_partner_name` | character varying |  |  |
| `prospect_mediapartner_id` | bigint |  |  |
| `prospect_mediapartner_name` | character varying |  |  |
| `prospect_ict_partner_id` | bigint |  |  |
| `prospect_ict_partner_name` | character varying |  |  |
| `bv_bucket` | smallint |  |  |
| `product_count` | integer |  |  |
| `shop_value` | bigint |  |  |
| `is_css_shop` | bigint |  |  |
| `is_beslist_propositie_geladen` | bigint |  |  |
| `storypoints_relatie_tbv_beslist_propositie` | bigint |  |  |
| `roas_percentage_eis_klant` | numeric |  |  |
| `roas_percentage_acceptabel_voor_klant` | numeric |  |  |
| `cos_percentage_eis_klant` | numeric |  |  |
| `cos_percentage_acceptabel_voor_klant` | numeric |  |  |
| `cpo_percentage_eis_klant` | numeric |  |  |
| `cpo_percentage_acceptabel_voor_klant` | numeric |  |  |
| `google_analytics_plugin` | character varying |  |  |
| `load_date` | timestamp without time zone |  |  |
| `update_date` | timestamp without time zone |  |  |
| `deleted_ind` | smallint |  |  |
| `has_shop_stats_api_access` | smallint |  |  |
| `shop_advertising_type` | character varying |  |  |
| `feed_bidding` | smallint |  |  |
| `smartbidding` | smallint |  |  |
| `is_active_kpi_shop` | integer |  |  |
| `is_active_ga_plugin_kpi_shop` | integer |  |  |
| `verzamel_shop_id` | bigint |  |  |
| `verzamel_shop_name` | character varying |  |  |
| `verzamel_shop_advertising_type` | character varying |  |  |
| `webshopplatform_id` | integer |  |  |
| `webshopplatform_name` | character varying |  |  |
| `is_important_niche_player` | smallint |  |  |
| `is_important_for_data` | smallint |  |  |
| `is_gs_lead_generator` | smallint |  |  |
| `weergavekolom` | integer |  |  |
| `has_contract` | integer |  |  |
| `has_cpc_contract` | integer |  |  |
| `has_cps_contract` | integer |  |  |
| `has_css_contract` | integer |  |  |
| `has_nda_contract` | integer |  |  |
| `has_smartbidding_contract` | integer |  |  |
| `has_conversiontracking_contract` | integer |  |  |
| `shop_live_date` | timestamp without time zone |  |  |
| `shop_live_update_date` | timestamp without time zone |  |  |
| `onboardingquality` | integer |  |  |
| `roas_types` | character varying |  |  |
| `roas_a_wens` | bigint |  |  |
| `roas_a_ondergrens` | bigint |  |  |
| `roas_a_omzetdoel` | bigint |  |  |
| `roas_b_wens` | bigint |  |  |
| `roas_b_ondergrens` | bigint |  |  |
| `roas_b_omzetdoel` | bigint |  |  |
| `roas_c_wens` | bigint |  |  |
| `roas_c_ondergrens` | bigint |  |  |
| `roas_c_omzetdoel` | bigint |  |  |
| `roas_a_date` | timestamp without time zone |  |  |
| `roas_b_date` | timestamp without time zone |  |  |
| `roas_c_date` | timestamp without time zone |  |  |
| `cpc_contract_start_date` | timestamp without time zone |  |  |
| `cpc_contract_end_date` | timestamp without time zone |  |  |
| `cps_contract_start_date` | timestamp without time zone |  |  |
| `cps_contract_end_date` | timestamp without time zone |  |  |
| `css_contract_start_date` | timestamp without time zone |  |  |
| `css_contract_end_date` | timestamp without time zone |  |  |
| `conversiontracking_contract_start_date` | timestamp without time zone |  |  |
| `conversiontracking_contract_end_date` | timestamp without time zone |  |  |
| `smartbidding_contract_start_date` | timestamp without time zone |  |  |
| `smartbidding_contract_end_date` | timestamp without time zone |  |  |
| `nda_contract_start_date` | timestamp without time zone |  |  |
| `nda_contract_end_date` | timestamp without time zone |  |  |
| `roas_sturing` | character varying |  |  |
| `roas_a_wens_catman` | bigint |  |  |
| `roas_b_wens_catman` | bigint |  |  |
| `roas_c_wens_catman` | bigint |  |  |
| `roas_a_omzetdoel_catman` | bigint |  |  |
| `roas_b_omzetdoel_catman` | bigint |  |  |
| `roas_c_omzetdoel_catman` | bigint |  |  |
| `roas_a_date_catman` | timestamp without time zone |  |  |
| `roas_b_date_catman` | timestamp without time zone |  |  |
| `roas_c_date_catman` | timestamp without time zone |  |  |
| `is_niche_shop` | integer |  |  |
| `zoekvolume_nl` | bigint |  |  |
| `css_merchant_center_id` | bigint |  |  |
| `css_multichannel_account_id` | bigint |  |  |
| `css_switch_type` | character varying |  |  |
| `css_business_name` | character varying |  |  |
| `css_shop_url` | character varying |  |  |
| `css_id` | character varying |  |  |
| `css_active` | smallint |  |  |
| `efficy_k_shop` | bigint |  |  |
| `shop_name_short` | character varying |  |  |
| `shop_suc_status` | integer |  |  |
| `shoporcat_leading` | integer |  |  |
| `content_score` | character varying |  |  |
| `gap_score` | character varying |  |  |
| `is_cpa_shop` | integer |  |  |
| `has_ms_contract` | integer |  |  |
| `ms_contract_start_date` | timestamp without time zone |  |  |
| `ms_contract_end_date` | timestamp without time zone |  |  |
| `shop_branche` | character varying |  |  |
| `is_affiliate_shop` | smallint |  |  |
| `is_gsd_nl_shop` | integer |  |  |
| `is_gsd_be_shop` | integer |  |  |
| `is_pixel_shop` | integer |  |  |
| `meetgat_achterkant` | integer |  |  |
| `shop_deelt_data` | smallint |  |  |
| `is_roas_garantie_shop` | integer |  |  |
| `is_gsd_de_shop` | integer |  |  |
| `listed_on_de` | integer |  |  |
| `is_wecantrack_shop` | integer |  |  |
| `shop_has_gsd_consent` | integer |  |  |
| `has_ms_mf_contract` | integer |  |  |
| `ms_mf_contract_start_date` | timestamp without time zone |  |  |
| `ms_mf_contract_end_date` | timestamp without time zone |  |  |
| `is_plp_only_shop` | integer |  |  |
| `roas_bandwidth_id` | smallint |  |  |
| `shop_priority_label` | character varying |  |  |
| `is_branded` | integer |  |  |
| `is_branded_date` | timestamp without time zone |  |  |

## `bt.unique_products_multiple_providers`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `technical_uid` | bigint |  |  |
| `date` | timestamp without time zone |  |  |
| `main_category_id` | bigint |  |  |
| `main_category_name` | character varying |  |  |
| `country` | character varying |  |  |
| `unique_products_multiple_providers_ean` | bigint |  |  |
| `unique_products_2_providers_ean` | bigint |  |  |
| `unique_products_3_providers_ean` | bigint |  |  |
| `unique_products_4_providers_ean` | bigint |  |  |
| `unique_products_5_providers_ean` | bigint |  |  |
| `unique_products_6_providers_ean` | bigint |  |  |
| `unique_products_7_providers_ean` | bigint |  |  |
| `unique_products_8_providers_ean` | bigint |  |  |
| `unique_products_9_providers_ean` | bigint |  |  |
| `unique_products_10_providers_ean` | bigint |  |  |
| `unique_products_morethan10_providers_ean` | bigint |  |  |
| `load_date` | timestamp without time zone |  |  |
| `update_date` | timestamp without time zone |  |  |
| `deleted_ind` | integer |  |  |
| `unique_products_multiple_providers_pim_id` | bigint |  |  |
| `unique_products_2_providers_pim_id` | bigint |  |  |
| `unique_products_3_providers_pim_id` | bigint |  |  |
| `unique_products_4_providers_pim_id` | bigint |  |  |
| `unique_products_5_providers_pim_id` | bigint |  |  |
| `unique_products_6_providers_pim_id` | bigint |  |  |
| `unique_products_7_providers_pim_id` | bigint |  |  |
| `unique_products_8_providers_pim_id` | bigint |  |  |
| `unique_products_9_providers_pim_id` | bigint |  |  |
| `unique_products_10_providers_pim_id` | bigint |  |  |
| `unique_products_morethan10_providers_pim_id` | bigint |  |  |
| `unique_products_multiple_providers_ean_incl_noimage` | bigint |  |  |
| `unique_products_2_providers_ean_incl_noimage` | bigint |  |  |
| `unique_products_3_providers_ean_incl_noimage` | bigint |  |  |
| `unique_products_4_providers_ean_incl_noimage` | bigint |  |  |
| `unique_products_5_providers_ean_incl_noimage` | bigint |  |  |
| `unique_products_6_providers_ean_incl_noimage` | bigint |  |  |
| `unique_products_7_providers_ean_incl_noimage` | bigint |  |  |
| `unique_products_8_providers_ean_incl_noimage` | bigint |  |  |
| `unique_products_9_providers_ean_incl_noimage` | bigint |  |  |
| `unique_products_10_providers_ean_incl_noimage` | bigint |  |  |
| `unique_products_morethan10_providers_ean_incl_noimage` | bigint |  |  |
| `unique_products_multiple_providers_ean_incl_invalid` | bigint |  |  |
| `unique_products_2_providers_ean_incl_invalid` | bigint |  |  |
| `unique_products_3_providers_ean_incl_invalid` | bigint |  |  |
| `unique_products_4_providers_ean_incl_invalid` | bigint |  |  |
| `unique_products_5_providers_ean_incl_invalid` | bigint |  |  |
| `unique_products_6_providers_ean_incl_invalid` | bigint |  |  |
| `unique_products_7_providers_ean_incl_invalid` | bigint |  |  |
| `unique_products_8_providers_ean_incl_invalid` | bigint |  |  |
| `unique_products_9_providers_ean_incl_invalid` | bigint |  |  |
| `unique_products_10_providers_ean_incl_invalid` | bigint |  |  |
| `unique_products_morethan10_providers_ean_incl_invalid` | bigint |  |  |
| `unique_products_10_providers_pim_id_incl_invalid` | bigint |  |  |
| `unique_products_multiple_providers_pim_id_incl_invalid` | bigint |  |  |
| `unique_products_2_providers_pim_id_incl_invalid` | bigint |  |  |
| `unique_products_3_providers_pim_id_incl_invalid` | bigint |  |  |
| `unique_products_4_providers_pim_id_incl_invalid` | bigint |  |  |
| `unique_products_5_providers_pim_id_incl_invalid` | bigint |  |  |
| `unique_products_6_providers_pim_id_incl_invalid` | bigint |  |  |
| `unique_products_7_providers_pim_id_incl_invalid` | bigint |  |  |
| `unique_products_8_providers_pim_id_incl_invalid` | bigint |  |  |
| `unique_products_9_providers_pim_id_incl_invalid` | bigint |  |  |
| `unique_products_morethan10_providers_pim_id_incl_invalid` | bigint |  |  |
| `unique_products_multiple_providers_pim_id_incl_noimage` | bigint |  |  |
| `unique_products_2_providers_pim_id_incl_noimage` | bigint |  |  |
| `unique_products_3_providers_pim_id_incl_noimage` | bigint |  |  |
| `unique_products_4_providers_pim_id_incl_noimage` | bigint |  |  |
| `unique_products_5_providers_pim_id_incl_noimage` | bigint |  |  |
| `unique_products_6_providers_pim_id_incl_noimage` | bigint |  |  |
| `unique_products_7_providers_pim_id_incl_noimage` | bigint |  |  |
| `unique_products_8_providers_pim_id_incl_noimage` | bigint |  |  |
| `unique_products_9_providers_pim_id_incl_noimage` | bigint |  |  |
| `unique_products_10_providers_pim_id_incl_noimage` | bigint |  |  |
| `unique_products_morethan10_providers_pim_id_incl_noimage` | bigint |  |  |

## `chan_deriv.ref_channel_derivation_stats`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `aff_id` | integer | ⭐ | Aff ID die we gebruiken om een marketing kanaal af te leiden. |
| `channel_id` | integer | ⭐ | Channel ID die we gebruiken om een marketing kanaal af te leiden. |
| `affiliate` | character varying | ⭐ | De specifieke bron waar bezoekers vandaan komen. Dit is een onderscheid binnen het marketing kanaal. |
| `marketing_channel` | character varying | ⭐ | Het marketing kanaal wat we afleiden via aff ID en channel ID. |
| `load_date` | timestamp without time zone |  |  |
| `update_date` | timestamp without time zone |  |  |
| `deleted_ind` | smallint | ⭐ | Geeft aan of een record nog actueel is of niet. |
| `traffic_type` | character varying |  |  |

## `datamart.dim_category`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `dim_category_key` | bigint | ⭐ | De unieke sleutel van een record, die je kan gebruiken om te joinen met datamart feitentabellen. |
| `deepest_category_id` | bigint | ⭐ | De unieke sleutel van een diepste categorie, die je kan gebruiken om te joinen met vooral de BT. |
| `deepest_category_name` | character varying | ⭐ | De naam van de diepste categorie in dit record. |
| `deepest_cat_level` | smallint | ⭐ | Het niveau waarop de categorie in dit record ligt (maincat, subcat of subsubcat). |
| `deepest_cat_level_name` | character varying |  |  |
| `deepest_cat_matching` | smallint |  |  |
| `sub_sub_category_id` | bigint | ⭐ | Subsubcat ID, ingevuld als het record een subsubcat is. |
| `sub_sub_category_name` | character varying | ⭐ | Subsubcat naam, ingevuld als het record een subsubcat is. |
| `sub_sub_category_min_price` | numeric |  |  |
| `sub_sub_category_min_pct` | numeric |  |  |
| `sub_category_id` | bigint | ⭐ | Subcat ID, als het record een subcat record betreft. |
| `sub_category_name` | character varying | ⭐ | Subcat naam, als het record een subcat record betreft. |
| `sub_category_min_price` | numeric |  |  |
| `sub_category_min_pct` | numeric |  |  |
| `main_category_id` | bigint | ⭐ | Maincat ID. |
| `main_category_name` | character varying | ⭐ | Maincat naam. |
| `main_category_min_price` | numeric |  |  |
| `main_category_min_pct` | numeric |  |  |
| `bid_category_id` | bigint | ⭐ | Bidcat ID die hoort bij het record, alleen ingevuld als de categorie bij een bidcat hoort. |
| `bid_category_name` | character varying | ⭐ | Bidcat naam die hoort bij het record, alleen ingevuld als de categorie bij een bidcat hoort. |
| `bid_cat_min_cpc_price` | numeric |  |  |
| `bid_cat_min_cps_pct` | numeric |  |  |
| `category_is_live` | smallint | ⭐ | Geeft aan of de category nog live staat of niet. |
| `is_lowest_category` | smallint | ⭐ | Geeft aan of het record de diepste categorie in de rangorde bevat of dat er nog diepere categorieën zijn. |
| `dm_load_date` | timestamp without time zone |  |  |
| `dm_update_date` | timestamp without time zone |  |  |
| `deleted_ind` | smallint | ⭐ | Geeft aan of een record nog actueel is of niet. |
| `table_name` | character varying |  |  |
| `sb_roas_type_code` | character varying |  |  |
| `sb_roas_medium_percentage` | smallint |  |  |
| `branche` | character varying |  |  |
| `branche_team` | character varying |  |  |
| `category_type` | character varying |  |  |
| `thuiswinkel_branche` | character varying | ⭐ | Een groepering op branche vanuit thuiswinkel data, waarmee categorieën tot een groep worden gemaakt. |
| `sb_roas_minimum_percentage` | smallint |  |  |
| `sb_roas_maximum_percentage` | smallint |  |  |

## `datamart.dim_date`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `dim_date_key` | bigint | ⭐ | De datum in YYYYMMDD format, die je kan gebruiken om te joinen met tabellen. |
| `date` | date | ⭐ | De datum. |
| `date_full_name` | character varying | ⭐ | Datum inclusief weekdag. |
| `week_day_name` | character varying | ⭐ | Weekdag naam. |
| `week_day_code` | character varying |  |  |
| `week_day_number` | character varying | ⭐ | Het dagnummer in de week. |
| `month_name` | character varying | ⭐ | Maand. |
| `month_code` | character varying |  |  |
| `month_number` | character varying | ⭐ | Nummer van de maand in het jaar. |
| `year_month_number` | character varying | ⭐ | Jaar-maand nummer. |
| `year_number` | character varying | ⭐ | Jaar. |
| `quarter_code` | character varying | ⭐ | Kwartaal code (bijv. Q1). |
| `quarter_number` | character varying | ⭐ | Kwartaal nummer. |
| `week_number` | character varying | ⭐ | Weeknummer van het jaar. |
| `year_week_number` | character varying | ⭐ | Jaar-week nummer. |
| `year_day_number` | character varying | ⭐ | Jaar-dag nummer. |
| `day_of_year_number` | character varying | ⭐ | Dag van het jaar nummer. |
| `current_year_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in het huidige jaar ligt (1) of niet (0). |
| `year_to_date_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in het huidige jaar tot dusver ligt (1) of niet (0). |
| `previous_year_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in het vorige jaar ligt (1) of niet (0). |
| `current_quarter_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in het huidige kwartaal ligt (1) of niet (0). |
| `quarter_to_date_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in het huidige kwartaal tot dusver ligt (1) of niet (0). |
| `previous_quarter_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in het vorige kwartaal ligt (1) of niet (0). |
| `current_month_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in de huidige maand ligt (1) of niet (0). |
| `month_to_date_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in de huidige maand tot dusver ligt (1) of niet (0). |
| `previous_month_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in de vorige maand ligt (1) of niet (0). |
| `current_week_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in de huidige week ligt (1) of niet (0). |
| `week_to_date_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in de huidige week tot dusver ligt (1) of niet (0). |
| `previous_week_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in de vorige week ligt (1) of niet (0). |
| `current_day_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum de huidige datum is (1) of niet (0). |
| `previous_day_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum de datum van gisteren is (1) of niet (0). |
| `rolling_365_days_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in een periode van 365 dagen geleden tot vandaag ligt (1) of niet (0). |
| `previous_365_days_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in een periode van 365 dagen voor de afgelopen 365 dagen ligt (1) of niet (0). |
| `rolling_30_days_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in een periode van 30 dagen geleden tot vandaag ligt (1) of niet (0). |
| `previous_30_days_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in een periode van 30 dagen voor de afgelopen 30 dagen ligt (1) of niet (0). |
| `rolling_28_days_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in een periode van 28 dagen geleden tot vandaag ligt (1) of niet (0). |
| `previous_28_days_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in een periode van 28 dagen voor de afgelopen 28 dagen ligt (1) of niet (0). |
| `rolling_7_days_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in een periode van 7 dagen geleden tot vandaag ligt (1) of niet (0). |
| `previous_7_days_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum in een periode van 7 dagen voor de afgelopen 7 dagen ligt (1) of niet (0). |
| `feestdag_ind` | smallint | ⭐ | Indicator waarmee we aangeven of een datum een feestdag is (1) of niet (0). |
| `feestdag_naam` | character varying | ⭐ | Naam van de feestdag als een datum een feestdag is. |
| `dm_load_date` | timestamp without time zone |  |  |
| `month_day_number` | character varying | ⭐ | Dag van de maand nummer. |
| `year_week_number_sun_sat` | character varying | ⭐ | Jaar-week nummer als de week begint op zondag. |
| `year_week_number_sat_fri` | character varying | ⭐ | Jaar-week nummer als de week begint op zaterdag. |
| `speciale_dag_naam` | character varying | ⭐ | De naam van de dag als we een speciale dag onderscheiden. Dit zijn de dagen die een eigen index krijgen in onze target berekeningen, en dit betreft... |
| `weekday_in_month_number` | integer |  |  |

## `datamart.dim_shop`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `dim_shop_key` | bigint | ⭐ | Unieke sleutel van de shop, waarmee je kan joinen met vooral Datamart tabellen. |
| `shop_id` | bigint | ⭐ | Shop ID. |
| `shop_name` | character varying | ⭐ | Shop naam. |
| `shop_postal_code` | character varying |  |  |
| `shop_adress` | character varying |  |  |
| `shop_phase` | smallint | ⭐ | Fase waarin de shop op dit moment staat. |
| `shop_verdienmodel` | character varying | ⭐ | Verdienmodel waarop de shop op dit moment staat. |
| `shop_hide_online` | smallint | ⭐ | Of de shop op dit moment op hide online staat of niet. |
| `shop_listed_on_nl` | smallint | ⭐ | Of de shop op dit moment live staat op NL of niet. |
| `shop_listed_on_be` | smallint | ⭐ | Of de shop op dit moment live staat op BE of niet. |
| `shop_is_disabled` | smallint | ⭐ | Of de shop op dit moment disabled is of niet. |
| `shop_hide_items` | smallint |  |  |
| `client_id` | bigint | ⭐ | Klant ID. |
| `client_name` | character varying | ⭐ | Klant naam. |
| `client_accountmanager_id` | bigint |  |  |
| `client_accountmanager_name` | character varying | ⭐ | Huidige accountmanager van de shop. |
| `shop_feedpartner_id` | integer |  |  |
| `shop_feedpartner_name` | character varying |  |  |
| `shop_platform_id` | integer |  |  |
| `shop_platform_name` | character varying |  |  |
| `dm_load_date` | timestamp without time zone |  |  |
| `dm_update_date` | timestamp without time zone |  |  |
| `deleted_ind` | smallint | ⭐ | Of het record nog actueel is of niet. |
| `current_shop_value` | bigint |  |  |
| `current_shop_bucket` | integer |  |  |
| `current_shop_productcount` | bigint |  |  |
| `shop_in_css` | smallint | ⭐ | Of de shop momenteel op CSS staat. |
| `shop_winkelwagen_partner_id` | integer |  |  |
| `shop_winkelwagen_partner_name` | character varying |  |  |
| `shop_mediapartner_id` | integer |  |  |
| `shop_mediapartner_name` | character varying |  |  |
| `shop_ict_partner_id` | integer |  |  |
| `shop_ict_partner_name` | character varying |  |  |
| `phase_date` | timestamp without time zone | ⭐ | De laatste wijzigingsdatum van de fase waarin de shop staat. |
| `hideonline_date` | timestamp without time zone | ⭐ | De laatste wijzigingsdatum in de hide online status van de shop. |
| `verdienmodel_live_date` | timestamp without time zone | ⭐ | De laatste wijzigingsdatum van het verdienmodel van de shop. |
| `shop_type` | character varying |  |  |
| `shop_is_musthave` | integer |  |  |
| `catman_shop_type` | character varying |  |  |
| `branche_team` | character varying |  |  |
| `current_shop_bucket_nl` | integer |  |  |
| `current_bvtotal_nl` | bigint |  |  |
| `current_shop_bucket_be` | integer |  |  |
| `current_bvtotal_be` | bigint |  |  |
| `current_score_potential_nl` | numeric |  |  |
| `current_score_actual_nl` | numeric |  |  |
| `current_score_potential_be` | numeric |  |  |
| `current_score_actual_be` | numeric |  |  |
| `shop_is_musthave365` | integer |  |  |
| `branche` | character varying |  |  |
| `is_affiliate_shop` | integer | ⭐ | Of een shop aangesloten is als affiliate of niet. |
| `is_gsd_nl_shop` | integer | ⭐ | Of de shop een GSD NL shop is. |
| `is_gsd_be_shop` | integer | ⭐ | Of de shop een GSD BE shop is. |
| `is_pixel_shop` | integer | ⭐ | Of een shop momenteel wordt afgerekend op de tag data of niet. |
| `is_roas_garantie_shop` | integer | ⭐ | Of een shop een ROAS garantie shop is. |
| `shop_listed_on_de` | integer | ⭐ | Of de shop op dit moment live staat op DE of niet. |
| `is_wecantrack_shop` | integer | ⭐ | Of een shop momenteel wordt afgerekend op wecantrack data of niet. |
| `is_groei30_shop` | integer | ⭐ | Of een shop binnen het groei 30 project valt of niet. |
| `is_groei50_shop` | integer | ⭐ | Of een shop binnen het groei 50 project valt of niet. |
| `is_groei200_shop` | integer | ⭐ | Of een shop binnen het groei 200 project valt of niet. |

## `datamart.dim_visit`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `dim_visit_key` | bigint | ⭐ | Unieke sleutel van een bezoeker, die je kan gebruiken om te joinen binnen de Datamart. |
| `visit_id` | bigint | ⭐ | Visit ID. |
| `intime` | timestamp without time zone | ⭐ | Tijd waarop de bezoeker landde op Beslist. |
| `ip` | character varying |  |  |
| `referer` | character varying | ⭐ | De referer URL waar de bezoeker door op Beslist landde (bijv. www.google.com). |
| `main_cat_id` | bigint |  |  |
| `main_cat_name` | character varying |  |  |
| `deepest_subcat_id` | bigint | ⭐ | De diepste categorie waarop de bezoeker landde. |
| `deepest_subcat_name` | character varying | ⭐ | De diepste categorie waarop de bezoeker landde. |
| `channel_id` | smallint | ⭐ | ID wat we gebruiken om het marketing kanaal waar de bezoeker vandaan kwam te achterhalen. |
| `channel_name` | character varying |  |  |
| `channel_page_id` | smallint | ⭐ | ID wat weergeeft op wat voor soort pagina de bezoeker landde. |
| `channel_page_name` | character varying |  |  |
| `first_visit_id` | bigint | ⭐ | Op basis van cookies wordt vastgelegd op welk visit ID een bezoeker voor het eerst op Beslist kwam. Als de visit ID gelijk is aan de first visit ID... |
| `aff_id` | integer | ⭐ | ID wat we gebruiken om het marketing kanaal waar de bezoeker vandaan kwam te achterhalen. |
| `domain` | character varying | ⭐ | Het domein van Beslist waarop de bezoeker landde. |
| `country_code` | character varying | ⭐ | Het land van herkomst van de bezoeker. |
| `dm_load_date` | timestamp without time zone |  |  |
| `dm_update_date` | timestamp without time zone |  |  |
| `deleted_ind` | smallint |  |  |
| `splittest_id` | integer |  |  |
| `is_real_visit` | smallint | ⭐ | Of wij denken dat de bezoeker een echte bezoeker (1) is of een bot. |
| `marketing_channel` | bigint |  |  |
| `url` | character varying | ⭐ | De URL waarop de bezoeker landde. |
| `height_viewport` | bigint |  |  |
| `width_viewport` | bigint |  |  |
| `viewport_group` | character varying | ⭐ | Het device waarmee de bezoeker op Beslist kwam (0-767 wordt vaak gezien als mobile, 768-1023 als tablet en 1024+ als desktop). |
| `useragent` | character varying | ⭐ | De useragent van de bezoeker. Bevat device en browse informatie. |
| `r_terms` | character varying | ⭐ | Of er /r/ termen in de URL stonden, en zo ja, welke. |
| `c_terms` | character varying | ⭐ | Of er /c/ termen (facets) in de URL stonden, en zo ja, welke. |
| `referer_source` | character varying | ⭐ | Een afleiding van de referer, die weergeeft van de referer URL wat de herkomst is (bijv. Google). |
| `campaign` | character varying | ⭐ | Als er een UTM campagne in de URL staat, dan staat hier de naam in. |
| `campaign_id` | character varying | ⭐ | Als er een UTM campagne in de URL staat, dan staat hier de ID in. |
| `year` | character varying |  |  |
| `month` | character varying |  |  |
| `day` | character varying |  |  |
| `gclid` | character varying |  |  |
| `type_url` | character varying | ⭐ | Het type URL waar de bezoeker op geland is (bijv. browse of PLP). |
| `page_heading` | character varying | ⭐ | De H1 van de pagina waarop de bezoeker landde. |

## `datamart.fct_revenue_aggr`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `fct_revenue_aggr_key` | bigint |  |  |
| `dim_shop_key` | bigint |  |  |
| `dim_category_key` | bigint |  |  |
| `dim_brand_key` | bigint |  |  |
| `dim_date_key` | bigint |  |  |
| `dim_shop_advertising_type_key` | integer |  |  |
| `revenue` | numeric |  |  |
| `number_of_visits` | integer |  |  |
| `dm_load_date` | timestamp without time zone |  |  |
| `dm_update_date` | timestamp without time zone |  |  |
| `deleted_ind` | smallint |  |  |
| `dim_verzamel_shop_advertising_type_key` | bigint |  |  |
| `year` | character varying |  |  |
| `month` | character varying |  |  |
| `day` | character varying |  |  |
| `invoicing_price` | numeric |  |  |

## `datamart.fct_visits`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `fct_visits_key` | bigint |  |  |
| `dim_date_key` | bigint | ⭐ | Datum waarop de visit landde (YYYYMMDD format). Kan je joinen met dim_date. |
| `dim_category_key` | bigint | ⭐ | De unieke categorie sleutel waarop de bezoeker landde. Kan je joinen met dim_category. |
| `dim_visit_key` | bigint | ⭐ | De unieke sleutel voor de visit. Om te joinen met dim_visit (verplicht bij gebruik van deze tabel!). |
| `ww_revenue` | numeric | ⭐ | De WW omzet (voor ons) die we kunnen toekennen aan deze bezoeker. |
| `cpc_revenue` | numeric | ⭐ | De CPR omzet (voor ons) die we kunnen toekennen aan deze bezoeker. |
| `number_of_outclicks_revenue` | integer | ⭐ | Het aantal outclicks dat de bezoeker gedaan heeft. |
| `number_of_outclicks` | integer |  |  |
| `number_of_bvb_clicks` | integer | ⭐ | Het aantal in WW clicks dat de bezoeker gedaan heeft. |
| `number_of_pageviews` | integer | ⭐ | Het aantal pageviews dat de bezoeker gedaan heeft. |
| `number_of_orders` | integer | ⭐ | Het aantal WW bestellingen dat de bezoeker gedaan heeft. Hierbij is 1 bestelling met meerdere shop bestellingen erin nog steeds 1 bestelling. |
| `number_of_orderlines` | integer | ⭐ | Het aantal WW bestellingen dat de bezoeker gedaan heeft. Hierbij leidt 1 bestelling met meerdere shop bestellingen erin tot het aantal shop bestell... |
| `number_of_popup_views` | integer |  |  |
| `dm_load_date` | timestamp without time zone |  |  |
| `dm_update_date` | timestamp without time zone |  |  |
| `number_of_cpc_productclicks` | integer | ⭐ | Het aantal CPC productclicks dat de bezoeker gedaan heeft. |
| `number_of_ww_productclicks` | integer | ⭐ | Het aantal WW productclicks dat de bezoeker gedaan heeft. |
| `number_of_browse_pageviews` | integer | ⭐ | Het aantal browse pageview dat de bezoeker gedaan heeft. |
| `number_of_plp_pageviews` | integer | ⭐ | Het aantal PLP pageview dat de bezoeker gedaan heeft. |
| `bruto_display_revenue` | numeric |  |  |
| `netto_display_revenue` | numeric |  |  |
| `ww_revenue_commission` | numeric | ⭐ | Onze WW commissie die de bezoeker ons heeft opgeleverd. |
| `ww_revenue_transaction` | numeric | ⭐ | Onze WW transactie omzet die de bezoeker ons heeft opgeleverd. |
| `cpc_revenue_no_smartbidding` | numeric |  |  |
| `cpc_revenue_all_smartbidding` | numeric |  |  |
| `cpc_shop_revenue` | numeric | ⭐ | De CPR shop omzet die de bezoeker heeft opgeleverd. |
| `cpc_shop_costs` | numeric | ⭐ | De CPR shop kosten die de bezoeker heeft opgeleverd. |
| `ww_shop_revenue` | numeric | ⭐ | De WW shop omzet die de bezoeker heeft opgeleverd. |
| `ww_shop_costs` | numeric | ⭐ | De WW shop kosten die de bezoeker heeft opgeleverd. |
| `acquisition_costs` | numeric | ⭐ | De kosten die we gemaakt hebben om een bezoeker te kunnen inkopen. Let op: dit weten we niet exact op bezoeker niveau, maar verdelen we lineair ove... |
| `adsense_revenue` | numeric |  |  |
| `year` | character varying |  |  |
| `month` | character varying |  |  |
| `day` | character varying |  |  |
| `cpc_revenue_only` | numeric |  |  |
| `cpa_revenue_only` | numeric |  |  |
| `affiliate_revenue` | numeric | ⭐ | De affiliate omzet (voor ons) die we kunnen toekennen aan deze bezoeker. |
| `transactions` | integer | ⭐ | Het aantal transacties wat we kunnen linken aan deze bezoeker. |

## `dl_hot_partition.search_data_details`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `main_category_id` | bigint | ⭐ | Maincat ID waarin het product is ingedeeld. |
| `year` | character varying |  |  |
| `month` | character varying |  |  |
| `day` | character varying |  |  |
| `hour` | character varying |  |  |
| `brandid` | integer | ⭐ | Merk van het product. |
| `shop_id` | bigint | ⭐ | Shop ID. |
| `blockstatus` | integer | ⭐ | Krijgt het item in de search index een block status, dan staat deze hier in. Dat betekent dat hij niet live komt te staan. |
| `country` | character varying | ⭐ | Het land waarop het product is ingedeeld. |
| `externalid` | character varying |  |  |
| `itemid` | integer |  |  |
| `shoptype` | character varying | ⭐ | Het type shop waarvan het product is, heeft te maken met het verdienmodel van de shop. |
| `deepest_cat_id` | integer | ⭐ | Diepste cat ID. |
| `is_bid_active` | smallint |  |  |
| `is_bid_display_guaranteed` | smallint |  |  |
| `is_shop_active` | smallint | ⭐ | Staat de shop live (1) of niet (0), bijvoorbeeld vanwege het hebben van de juiste shop fase. |
| `is_shop_closed_on_sunday` | smallint | ⭐ | Is de shop dicht op zondag ja (1) of nee (0). Op zondagen hebben wij deze producten dus niet online staan. |
| `productidv3` | character varying | ⭐ | Unieke identifier van een product (= shopitem). |
| `is_css_shop` | smallint | ⭐ | Is de shop een CSS shop (1) of niet (0). |
| `is_disabled_in_feed` | smallint | ⭐ | Is een item door de shop disabled (1) of niet (0). |
| `title` | character varying | ⭐ | Titel van het product. |
| `predictedrevenueperclick` | double precision |  |  |
| `valid` | smallint | ⭐ | Is het product (niet shopitem, maar het hele item in stapelcats) live of niet. |
| `ean` | character varying | ⭐ | Bijbehorende EAN. |
| `shopversion` | character varying |  |  |
| `price` | double precision | ⭐ | Prijs van het product. |
| `shop_name` | character varying | ⭐ | Shop naam. |
| `deliverycost` | character varying | ⭐ | Verzendkosten voor het product. |
| `deliverytext` | character varying | ⭐ | Tekst over levertijden die bij het product staat. |
| `url` | character varying | ⭐ | URL van het product. |
| `batchtimestamp_date` | timestamp without time zone |  |  |
| `dl_processing_date` | date | ⭐ | De datum van de search index. Hier altijd op filteren voor deze tabel. |
| `familyidv3` | character varying | ⭐ | Family ID van het product. |
| `is_productvalid` | smallint | ⭐ | Is het product (shopitem) live of niet. |
| `deliverytimesort` | integer | ⭐ | De groepering van levertijden voor het product. |
| `condition` | character varying | ⭐ | De conditie van het product, is deze nieuwe, tweedehands etc.? |
| `category_predictor_main_category_id` | bigint | ⭐ | De maincat ID waarin het product volgens de category predictor het beste kan worden ingedeeld. |
| `category_predictor_timestamp` | character varying |  |  |
| `pim_id` | character varying | ⭐ | Het bijbehorende PIM ID. |
| `country_language` | character varying | ⭐ | Het land waarop het product is ingedeeld, deze moet je altijd in de join conditie zetten wanneer je dieper wilt inzoomen op items via andere dl_hot... |
| `deepest_category_predictor_main_category_id` | bigint | ⭐ | De maincat ID waarin het product volgens de deepest category predictor het beste kan worden ingedeeld. |
| `deepest_category_predictor_sub_category_id` | bigint | ⭐ | De subcat ID waarin het product volgens de deepest category predictor het beste kan worden ingedeeld. |
| `deepest_category_predictor_deepest_category_ids` | character varying | ⭐ | De diepste cat IDs waarin het product volgens de deepest category predictor het beste kan worden ingedeeld. |
| `deepest_category_predictor_timestamp` | character varying |  |  |
| `urlclean` | character varying | ⭐ | De opgeschoonde URL van een product, waarvoor bepaalde elementen zijn verwijderd uit de URL. |
| `bidlabel` | character varying | ⭐ | Het promotie label wat een shop (of wij) kunnen geven aan een shop, zodat we daar extra op kunnen sturen. |
| `description` | character varying | ⭐ | De beschrijving van een product. |
| `advertisementidv3` | character varying | ⭐ | Advertisement ID horend bij het product. |
| `saleprice` | numeric | ⭐ | Als je nu korting krijgt op een product, dan staat hier de kortingsprijs weggeschreven. |
| `variantid` | character varying | ⭐ | Variant ID horend bij het product. Wordt gevuld vanaf het binnenhalen van de gegroepeerde index. |
| `plpurl` | character varying | ⭐ | Onze PLP url voor een product. Wordt gevuld vanaf het binnenhalen van de gegroepeerde index. |
| `lowest_price` | numeric | ⭐ | De laagste prijs voor een product. Wordt gevuld vanaf het binnenhalen van de gegroepeerde index. |
| `eans` | character varying | ⭐ | De verschillende EANs die bij een product horen. Wordt gevuld vanaf het binnenhalen van de gegroepeerde index. |

## `hda.componentvisit`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `technical_uid` | bigint |  |  |
| `id` | bigint |  |  |
| `componentvisitid` | character varying |  |  |
| `urlpart1` | character varying |  |  |
| `urlpart2` | character varying |  |  |
| `maincat_id` | bigint |  |  |
| `subcat_id` | bigint |  |  |
| `best_category_id` | bigint |  |  |
| `item_id` | bigint |  |  |
| `ip` | character varying |  |  |
| `visitid` | bigint |  |  |
| `channelid` | bigint |  |  |
| `intime` | timestamp without time zone |  |  |
| `splittest_id` | integer |  |  |
| `auto` | smallint |  |  |
| `url` | character varying |  |  |
| `cachekey` | character varying |  |  |
| `totalproducts` | integer |  |  |
| `first_visit_id` | bigint |  |  |
| `visitchannelid` | bigint |  |  |
| `in` | smallint |  |  |
| `out` | bigint |  |  |
| `price` | numeric |  |  |
| `unique_visit` | smallint |  |  |
| `domain` | character varying |  |  |
| `aff_id` | bigint |  |  |
| `load_date` | timestamp without time zone |  |  |
| `update_date` | timestamp without time zone |  |  |
| `deleted_ind` | smallint |  |  |
| `pageview_uuid` | character varying |  |  |
| `year` | character varying |  |  |
| `month` | character varying |  |  |
| `day` | character varying |  |  |
| `basewindow_uuid` | character varying |  |  |
| `client_uuid` | character varying |  |  |
| `utm_medium` | character varying |  |  |
| `utm_source` | character varying |  |  |
| `marketing_channel` | integer |  |  |
| `referer` | character varying |  |  |
| `websession_id` | bigint |  |  |
| `params` | character varying |  |  |

## `hda.landingpage_views`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `technical_uid` | bigint |  |  |
| `id` | bigint |  |  |
| `pageview_uuid` | character varying |  |  |
| `direct_match_count` | integer |  |  |
| `first_offer_product_id_v3` | character varying |  |  |
| `load_date` | timestamp without time zone |  |  |
| `update_date` | timestamp without time zone |  |  |
| `deleted_ind` | integer |  |  |
| `is_pim_id_found` | integer |  |  |
| `is_pim_title_used` | integer |  |  |
| `is_pim_description_used` | integer |  |  |
| `pim_group_id` | character varying |  |  |
| `pim_id` | character varying |  |  |

## `hda.pixel_attribution_beslist_last_click`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `technical_uid` | bigint |  |  |
| `shop_id` | character varying |  |  |
| `client_beslist_user_id` | character varying |  |  |
| `client_beslist_session_id` | bigint |  |  |
| `shop_outclick_uuid` | character varying |  |  |
| `location_host` | character varying |  |  |
| `conversion` | character varying |  |  |
| `conversion_timestamp` | timestamp without time zone |  |  |
| `conversion_shop_id` | character varying |  |  |
| `shop_conversion_value_string` | character varying |  |  |
| `shop_conversion_transaction_id` | character varying |  |  |
| `shop_including_vat` | character varying |  |  |
| `beslist_timestamp` | timestamp without time zone |  |  |
| `final_timestamp` | timestamp without time zone |  |  |
| `final_shop_id` | character varying |  |  |
| `timestamp_session_start` | timestamp without time zone |  |  |
| `load_date` | timestamp without time zone |  |  |
| `update_date` | timestamp without time zone |  |  |
| `deleted_ind` | integer |  |  |
| `pixel_attribution_id` | integer |  |  |
| `pixel_attribution_name` | character varying |  |  |
| `conversion_has_uuid` | integer |  |  |
| `utm_source_beslist` | integer |  |  |
| `referrer_beslist` | integer |  |  |
| `query_beslist` | integer |  |  |
| `shop_conversion_value` | numeric |  |  |
| `has_google_referrer` | integer |  |  |
| `has_bank_referrer` | integer |  |  |
| `query_bl3nlclid` | smallint |  |  |
| `utm_campaign_beslist` | smallint |  |  |
| `shop_user_ip` | character varying |  |  |
| `attribution_based_on` | character varying |  |  |
| `first_touch_attribution` | numeric |  |  |
| `last_touch_attribution` | numeric |  |  |
| `linear_attribution` | numeric |  |  |
| `position_based_attribution` | numeric |  |  |
| `last_click_attribution` | numeric |  |  |
| `time_decay_attribution` | numeric |  |  |
| `google_analytics_click_id` | character varying |  |  |
| `is_updated_uuid_from_stats` | smallint |  |  |
| `last_advertiser_timestamp` | timestamp without time zone |  |  |

## `hda.sa360_adgroup`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `technical_uid` | bigint |  |  |
| `date` | timestamp without time zone |  |  |
| `agency` | character varying |  |  |
| `agencyid` | bigint |  |  |
| `advertiser` | character varying |  |  |
| `advertiserid` | bigint |  |  |
| `accounttype` | character varying |  |  |
| `account` | character varying |  |  |
| `campaign` | character varying |  |  |
| `campaignid` | bigint |  |  |
| `adgroup` | character varying |  |  |
| `adgroupid` | bigint |  |  |
| `impr` | bigint |  |  |
| `clicks` | bigint |  |  |
| `cost` | numeric |  |  |
| `avgpos` | numeric |  |  |
| `qualityscoreavg` | numeric |  |  |
| `rev_fl` | numeric |  |  |
| `cpc_rev_fl` | numeric |  |  |
| `ww_rev_fl` | numeric |  |  |
| `cpc_conv_fl` | bigint |  |  |
| `ww_conv_fl` | bigint |  |  |
| `deepest_category_id` | bigint |  |  |
| `deepest_category_name` | character varying |  |  |
| `year` | character varying |  |  |
| `month` | character varying |  |  |
| `day` | character varying |  |  |
| `load_date` | timestamp without time zone |  |  |
| `update_date` | timestamp without time zone |  |  |
| `deleted_ind` | integer |  |  |
| `topimpressionpercentage` | numeric |  |  |
| `searchimpressionshare` | numeric |  |  |
| `searchtopimpressionshare` | numeric |  |  |
| `shop_id` | bigint |  |  |
| `aff_id` | bigint |  |  |
| `product_score_label` | character varying |  |  |

## `kpi.pixel_quality`

| Column | Type | Important | Description |
|--------|------|-----------|-------------|
| `technical_uid` | bigint |  |  |
| `date` | timestamp without time zone |  |  |
| `shop_id` | bigint |  |  |
| `shop_name` | character varying |  |  |
| `accountmanager` | character varying |  |  |
| `pixel_actief` | timestamp without time zone |  |  |
| `cpr_via_pixel` | timestamp without time zone |  |  |
| `has_orders` | character varying |  |  |
| `outclicks` | bigint |  |  |
| `linkage` | double precision |  |  |
| `coverage` | double precision |  |  |
| `transactions` | bigint |  |  |
| `revenue` | numeric |  |  |
| `ga_linkage` | double precision |  |  |
| `ga_coverage` | double precision |  |  |
| `ga_transactions` | bigint |  |  |
| `ga_revenue` | double precision |  |  |
| `ga_roas` | double precision |  |  |
| `ga_linked_roas` | double precision |  |  |
| `ga_costs` | numeric |  |  |
| `source` | character varying |  |  |
| `diff_transactions` | bigint |  |  |
| `diff_revenue` | double precision |  |  |
| `load_date` | timestamp without time zone |  |  |
| `update_date` | timestamp without time zone |  |  |
| `deleted_ind` | integer |  |  |
| `linked_outclicks` | bigint |  |  |
| `linked_transactions` | bigint |  |  |
