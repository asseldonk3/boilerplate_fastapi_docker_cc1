# Example Queries for Beslist.nl

This document contains example queries from the official query library.

## `bt.cpa_outclicks_transactional`

### Primary Example

```sql
select dat.year_month_number
,tac.outclick_shop_id
,tac.marketing_channel_aff_id_name
,sum(coalesce(tac.click_revenue,0)) + sum(coalesce(transaction_costs,0)) as linked_shop_cost
,sum(tac.revenue_excl) as linked_shop_revenue
,count(distinct tac.stats_id_stat) as linked_outclicks
,sum(tac.transactions) as linked_transactions

from bt.cpa_outclicks_transactional tac
join datamart.dim_date dat on tac.date = dat.date

where tac.actual_ind = 1
and tac.deleted_ind = 0
and date(tac.date) >= '2025-01-01'
and label not in ('cpa_after_180_days','rejected_click')
and tac.uuid_linked = 1

group by dat.year_month_number,tac.outclick_shop_id,tac.marketing_channel_aff_id_name

order by dat.year_month_number,tac.outclick_shop_id,tac.marketing_channel_aff_id_name
```

### Additional Example

```sql
select dat.year_month_number
,tac.shop_id
,tac.marketing_channel_aff_id_name
,case when sum(coalesce(tac.click_revenue,0)) + sum(coalesce(transaction_costs,0)) > 0 then sum(tac.revenue_excl) / (sum(coalesce(tac.click_revenue,0)) + sum(coalesce(transaction_costs,0))) else 0 end as linked_roas
,case when count(distinct tac.stats_id_stat) > 0 then sum(tac.revenue_excl) / count(distinct tac.stats_id_stat) else 0 end as linked_rev_click

from bt.cpa_outclicks_transactional tac
join datamart.dim_date dat on tac.date = dat.date

where tac.actual_ind = 1
and tac.deleted_ind = 0
and date(tac.date) >= '2025-01-01'
and label not in ('cpa_after_180_days','unlinked_revenue')
and tac.uuid_linked = 1
and tac.shop_deelt_data = 1

group by dat.year_month_number,tac.shop_id,tac.marketing_channel_aff_id_name

order by dat.year_month_number,tac.shop_id,tac.marketing_channel_aff_id_name
```

## `bt.daily_standup_metrics_category`

### Primary Example

```sql
select date.year_week_number_sun_sat
, case when marketing_channel like 'SEO' then 'SEO'
when marketing_channel like 'Overig Kanaal' then 'SEO'
when marketing_channel like 'SEA' then 'SEA'
when marketing_channel like 'Google Shopping' then 'GS'
when marketing_channel like 'Google Shopping Direct' then 'GSD'
when marketing_channel like 'DMA organic' then 'DMA organic'
when marketing_channel like 'DMA paid' then 'DMA paid'
end as marketing_channel
, sum(omzet_total) as omzet
, sum(marge) as marge
, sum(omzet_total) / nullif((sum(omzet_total) - sum(marge)),0) as roi
, sum(ww_revenue) / nullif((sum(cpc_revenue) + sum(ww_revenue)),0) as ww_percentage
, sum(visits) as visits
, sum(omzet_visit) / nullif(sum(visits),0) as opb
, sum(marge) / nullif(sum(visits),0) as mpb
, (sum(bvb_clicks_visit) + sum(outclicks_visit_stats)) / nullif(cast(sum(visits) as float),0) as CTR    
, sum(bounce_clicks_visit) / nullif(cast(sum(visits) as float),0) as bounce
, sum(btdc.omzet_total_excl_affiliates) / nullif((sum(btdc.outclicks_excl_affiliates) + sum(btdc.bvb_clicks)),0) as ecpc
, sum(linked_revenue_excl_affiliates) / nullif(sum(linked_clicks_excl_affiliates),0) as rev_click
, sum(linked_revenue_excl_affiliates) / nullif(sum(linked_costs_excl_affiliates),0) as roas
, sum(linked_revenue_excl_affiliates) / nullif(sum(linked_transactions_excl_affiliates),0) as aov
, sum(transactions_excl_affiliates) / nullif(cast(sum(linked_clicks_excl_affiliates)as float),0) as cvr
, sum(outclicks) as outclicks
 
from bt.daily_standup_metrics_category btdc
join datamart.dim_date date on btdc.dim_date_key = date.dim_date_key
where (date.date >= current_date - 8 and date <= current_date - 2)
and btdc.deleted_ind = 0
and marketing_channel in ('SEO', 'Overig Kanaal', 'SEA', 'Google Shopping', 'Google Shopping Direct', 'DMA organic', 'DMA paid')
group by date.year_week_number_sun_sat,marketing_channel
order by marketing_channel desc
```

## `bt.productscore`

### Primary Example

```sql
select shop_id
,shop_name
,is_gsd_nl_shop
,is_gsd_be_shop
,is_gsd_de_shop
,country
,productscore_label
,label_reason
,count(distinct productidv3) as aantal_shopitems

from bt.productscore

where actual_ind = 1
and deleted_ind = 0
and is_productvalid = 1

group by shop_id
,shop_name
,is_gsd_nl_shop
,is_gsd_be_shop
,is_gsd_de_shop
,country
,productscore_label
,label_reason

order by shop_id
,country
,productscore_label
,label_reason

limit 100000
```

## `bt.shop_list`

### Primary Example

```sql
select dim_date_key, 
shop_id, 
shop_name, 
client_id, 
client_name, 
accountmanager_name, 
shop_shares_data, 
hide_online, 
is_disabled, 
shop_phase, 
is_affiliate_shop, 
shop_listed_on, 
is_gsd_nl_shop, 
is_gsd_be_shop, 
is_gsd_de_shop, 
is_pixel_shop, 
is_roas_garantie_shop, 
is_wecantrack_shop, 
shop_earningsmodel, 
onboarding_step, 
total_findable_items_current, 
highest_total_findable_items_365, 
delta_total_findable_items, 
shop_costs, 
shop_revenue, 
shop_costs_365, 
productscore_a_nl_shopitems, 
productscore_b_nl_shopitems, 
productscore_c_nl_shopitems, 
productscore_no_data_nl_shopitems, 
productscore_no_ean_nl_shopitems, 
plp_shopitems, 
plp_shopitems_2_aanbieders, 
first_live_date, 
data_sharing_source_system, 
shop_costs_ytd, 
shop_costs_ytd_previous_year, 
last_contact_date, 
shop_has_gsd_consent, 
shop_charging_model, 
opzegging, 
opzegreden, 
shop_priority_label 

from bt.shop_list

where deleted_ind = 0
and dim_date_key = 20251201
and accountmanager_name = 'Sales Support'
```

## `chan_deriv.ref_channel_derivation_stats`

### Primary Example

```sql
select chan.marketing_channel
,count(*) as visits

from datamart.dim_visit dv 
join chan_deriv.ref_channel_derivation_stats chan on dv.aff_id = chan.aff_id and dv.channel_id = chan.channel_id

where dv.is_real_visit = 1
and date(dv.intime) >= '2025-01-01'

group by chan.marketing_channel

order by chan.marketing_channel
```

## `datamart.dim_category`

### Primary Example

```sql
select cat.main_category_id
,cat.main_category_name
,cat.sub_category_id
,cat.sub_category_name
,cat.sub_sub_category_id
,cat.sub_sub_category_name
,sum(rev.revenue) as omzet

from datamart.fct_revenue_aggr rev
join datamart.dim_category cat on rev.dim_category_key = cat.dim_category_key

where rev.deleted_ind = 0
and rev.dim_date_key >= 20250101
and cat.category_is_live = 1
and cat.deleted_ind = 0

group by cat.main_category_id
,cat.main_category_name
,cat.sub_category_id
,cat.sub_category_name
,cat.sub_sub_category_id
,cat.sub_sub_category_name

order by cat.main_category_id
,cat.sub_category_id
,cat.sub_sub_category_id
```

## `datamart.dim_date`

### Primary Example

```sql
select dat.year_week_number
,sum(rev.revenue) as omzet

from datamart.fct_revenue_aggr rev
join datamart.dim_date dat on rev.dim_date_key = dat.dim_date_key

where rev.deleted_ind = 0
and dat.dim_date_key >= 20250101

group by dat.year_week_number

order by dat.year_week_number
```

## `datamart.dim_shop`

### Primary Example

```sql
select ds.shop_id
,ds.shop_name
,ds.client_accountmanager_name
,sum(rev.revenue) as omzet

from datamart.fct_revenue_aggr rev
join datamart.dim_shop ds on rev.dim_shop_key = ds.dim_shop_key

where rev.deleted_ind = 0
and rev.dim_date_key >= 20250101
and ds.deleted_ind = 0

group by ds.shop_id
,ds.shop_name
,ds.client_accountmanager_name

order by ds.shop_id
```

## `datamart.dim_visit`

### Primary Example

```sql
select dv.type_url
,dv.viewport_group
,count(*) as visits
,(sum(fcv.cpc_revenue) + sum(fcv.ww_revenue) + sum(fcv.affiliate_revenue)) / count(*) as opb
,case when sum(fcv.number_of_outclicks_revenue) + sum(fcv.number_of_bvb_clicks) > 0
then (sum(fcv.cpc_revenue) + sum(fcv.ww_revenue) + sum(fcv.affiliate_revenue)) / (sum(fcv.number_of_outclicks_revenue) + sum(fcv.number_of_bvb_clicks))
else 0 end as ecpc
,sum(case when fcv.number_of_cpc_productclicks = 0 and fcv.number_of_ww_productclicks = 0 then 1 else 0 end) / cast(count(*) as float) as bounce
,((sum(fcv.cpc_revenue) + sum(fcv.ww_revenue) + sum(fcv.affiliate_revenue)) - sum(fcv.acquisition_costs)) / count(*) as mpb
,(sum(fcv.cpc_shop_revenue) + sum(fcv.ww_shop_revenue)) / count(*) as webshop_rev_per_visitor

from datamart.fct_visits fcv
join datamart.dim_visit dv on fcv.dim_visit_key = dv.dim_visit_key

where fcv.dim_date_key >= 20250101
and dv.is_real_visit = 1

group by dv.type_url,dv.viewport_group

order by dv.type_url,dv.viewport_group
```

## `datamart.fct_visits`

### Primary Example

```sql
select fcv.dim_date_key
,count(*) as visits
,(sum(fcv.cpc_revenue) + sum(fcv.ww_revenue) + sum(fcv.affiliate_revenue)) / count(*) as opb
,(sum(fcv.cpc_revenue) + sum(fcv.ww_revenue) + sum(fcv.affiliate_revenue)) / (sum(fcv.number_of_outclicks_revenue) + sum(fcv.number_of_bvb_clicks)) as ecpc
,sum(case when fcv.number_of_cpc_productclicks = 0 and fcv.number_of_ww_productclicks = 0 then 1 else 0 end) / cast(count(*) as float) as bounce
,((sum(fcv.cpc_revenue) + sum(fcv.ww_revenue) + sum(fcv.affiliate_revenue)) - sum(fcv.acquisition_costs)) / count(*) as mpb
,(sum(fcv.cpc_shop_revenue) + sum(fcv.ww_shop_revenue)) / count(*) as webshop_rev_per_visitor

from datamart.fct_visits fcv
join datamart.dim_visit dv on fcv.dim_visit_key = dv.dim_visit_key

where fcv.dim_date_key >= 20250101
and dv.is_real_visit = 1

group by fcv.dim_date_key

order by fcv.dim_date_key
```

## `dl_hot_partition.search_data_details`

### Primary Example

```sql
select main_category_id, 
shop_name,
productidv3, 
ean, 
pim_id, 
country, 
title, 
deepest_cat_id,
price, 
saleprice, 
url, 
condition, 
bidlabel

from dl_hot_partition.search_data_details

where date(dl_processing_date) = date(sysdate)-1
and is_productvalid = 1
and main_category_id = 32000
and shop_id = 1

limit 10000
```

## `bt.search_console`

### Primary Example - Top keywords by clicks

```sql
-- Top performing keywords (aggregated by clean_url)
SELECT
    dim_date_key,
    clean_url,
    keywords,
    type_url,
    SUM(clicks) as total_clicks,
    SUM(impressions) as total_impressions,
    SUM(clicks)::float / NULLIF(SUM(impressions), 0) as calculated_ctr,
    AVG(avg_position) as avg_position,
    SUM(visits) as total_visits,
    SUM(number_of_outclicks) as total_outclicks,
    SUM(ww_revenue) + SUM(cpc_revenue) as total_revenue
FROM bt.search_console
WHERE deleted_ind = 0
    AND country = 'nld'
    AND dim_date_key >= 20260101
GROUP BY dim_date_key, clean_url, keywords, type_url
ORDER BY total_clicks DESC
LIMIT 100
```

### Additional Example - Keyword intent analysis

```sql
-- SEO performance by keyword intent type
SELECT
    CASE
        WHEN is_informational = 1 THEN 'Informational'
        WHEN is_commercial_brand = 1 THEN 'Commercial Brand'
        WHEN is_commercial_shop = 1 THEN 'Commercial Shop'
        WHEN is_transactional_general = 1 THEN 'Transactional'
        WHEN is_transactional_sale = 1 THEN 'Transactional Sale'
        ELSE 'Other'
    END as intent_type,
    SUM(clicks) as total_clicks,
    SUM(impressions) as total_impressions,
    SUM(clicks)::float / NULLIF(SUM(impressions), 0) as ctr,
    SUM(number_of_outclicks) as outclicks,
    SUM(ww_revenue) + SUM(cpc_revenue) as revenue
FROM bt.search_console
WHERE deleted_ind = 0
    AND country = 'nld'
    AND dim_date_key >= 20260101
GROUP BY 1
ORDER BY total_clicks DESC
```

### Additional Example - URL type performance

```sql
-- Performance by URL type (PLP, R-url, C-url, etc.)
SELECT
    type_url,
    COUNT(DISTINCT clean_url) as unique_urls,
    SUM(clicks) as total_clicks,
    SUM(impressions) as total_impressions,
    SUM(clicks)::float / NULLIF(SUM(impressions), 0) as ctr,
    AVG(avg_position) as avg_position,
    SUM(number_of_outclicks) as outclicks
FROM bt.search_console
WHERE deleted_ind = 0
    AND country = 'nld'
    AND dim_date_key >= 20260101
GROUP BY type_url
ORDER BY total_clicks DESC
```

## `bt.revenue_per_product`

### Primary Example

```sql
 
```

