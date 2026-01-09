# Join Patterns for Beslist.nl Tables

This document describes how to join tables in the Beslist.nl Redshift database.

## Common Join Keys

| Join Type | Key Column(s) | Description |
|-----------|---------------|-------------|
| Date | `date` or `dim_date_key` | Join to `datamart.dim_date` for date dimensions |
| Shop | `shop_id` or `dim_shop_key` | Join to `datamart.dim_shop` for shop info |
| Category | `deepest_category_id` or `dim_category_key` | Join to `datamart.dim_category` |
| Visit | `visit_id` or `dim_visit_key` | Join to `datamart.dim_visit` |
| Channel | `aff_id` + `channel_id` | Join to `chan_deriv.ref_channel_derivation_stats` |

## Join Patterns by Table


### From `bt.cpa_outclicks_transactional`

#### → `datamart.dim_date`

**Join columns:** `date`

```sql
date(cpa_outclicks_transactional.date) = date(dim_date.date)
```

#### → `datamart.dim_category`

**Join columns:** `deepest_category_id`

```sql
cpa_outclicks_transactional.deepest_category_id = dim_category.deepest_category_id
```

#### → `datamart.dim_shop`

**Join columns:** `shop_id`

```sql
dim_shop.shop_id = cpa_outclicks_transactional.outclick_shop_id (voor omzet en kosten)
dim_shop.shop_id = cpa_outclicks_transactional.shop_id (voor ROAS)
```

#### → `bt.productscore`

**Join columns:** `productidv3, date, domain`

```sql
cpa_outclicks_transactional.productidv3 = productscore.productidv3 
and date(cpa_outclicks_transactional.date) >= date(productscore.load_start_date) 
and date(cpa_outclicks_transactional.date) < date(productscore.load_end_date) 
and case when cpa_outclicks_transactional.domain = '1' then 'nl' when cpa_outclicks_transactional.domain = '2' then 'be' when cpa_outclicks_transactional.domain = '12' then 'de' end = productscore.country
and productscore.deleted_ind = 0
```


### From `bt.daily_standup_metrics_category`

#### → `datamart.dim_category`

**Join columns:** `deepest_category_id`

```sql
daily_standup_metrics_category.deepest_category_id = dim_category.deepest_category_id
```

#### → `datamart.dim_date`

**Join columns:** `dim_date_key`

```sql
daily_standup_metrics_category.dim_date_key = dim_date.dim_date_key
```


### From `bt.productscore`

#### → `bt.cpa_outclicks_transactional`

**Join columns:** `productidv3, date, domain`

```sql
cpa_outclicks_transactional.productidv3 = productscore.productidv3 
and date(cpa_outclicks_transactional.date) >= date(productscore.load_start_date) 
and date(cpa_outclicks_transactional.date) < date(productscore.load_end_date) 
and case when cpa_outclicks_transactional.domain = '1' then 'nl' when cpa_outclicks_transactional.domain = '2' then 'be' when cpa_outclicks_transactional.domain = '12' then 'de' end = productscore.country
and productscore.deleted_ind = 0
```

#### → `datamart.dim_date`

**Join columns:** `date`

```sql
date(dim_date.date) >= date(productscore.load_start_date) 
and date(dim_date.date) < date(productscore.load_end_date) 
```

#### → `dl_hot_partition.search_data_details`

**Join columns:** `productidv3, load_start_date, load_end_date, country`

```sql
productscore.productidv3 = search_data_details.productidv3
and productscore.country = search_data_details.country
and search_data_details.dl_processing_date >= date(productscore_load_start_date)
and search_data_details.dl_processing_date < date(productscore.load_end_date)
```


### From `bt.shop_list`

#### → `bt.cpa_outclicks_transactional`

**Join columns:** `date, shop_id`

```sql
date(shop_list.date) = date(cpa_outclicks_transactional.date)
and shop_list.shop_id = cpa_outclicks_transactional.shop_id (voor ROAS)
and shop_list.shop_id = cpa_outclicks_transactional.outclick_shop_id (voor omzet)
```

#### → `bt.productscore`

**Join columns:** `date, shop_id`

```sql
date(shop_list.date) >= date(productscore.load_start_date)
and date(shop_list.date) < date(productscore.load_end_date)
and shop_list.shop_id = productscore.shop_id
```

#### → `bt.onboarding`

**Join columns:** `date, shop_id`

```sql
shop_list.date = onboarding.date
and shop_list.shop_id = onboarding.shop_id
```


### From `bt.shop_main_attributes_by_day`

#### → `bt.cpa_outclicks_transactional`

**Join columns:** `date, shop_id`

```sql
date(shop_main_attributes_by_day.date) = date(cpa_outclicks_transactional.date)
and shop_main_attributes_by_day.shop_id = cpa_outclicks_transactional.shop_id (voor ROAS)
and shop_main_attributes_by_day.shop_id = cpa_outclicks_transactional.outclick_shop_id (voor omzet)
```

#### → `bt.productscore`

**Join columns:** `date, shop_id`

```sql
date(shop_main_attributes_by_day.date) >= date(productscore.load_start_date)
and date(shop_main_attributes_by_day.date) < date(productscore.load_end_date)
and shop_main_attributes_by_day.shop_id = productscore.shop_id
```

#### → `bt.onboarding`

**Join columns:** `date, shop_id`

```sql
shop_main_attributes_by_day.date = onboarding.date
and shop_main_attributes_by_day.shop_id = onboarding.shop_id
```


### From `chan_deriv.ref_channel_derivation_stats`

#### → `datamart.dim_visit`

**Join columns:** `aff_id, channel_id`

```sql
ref_channel_derivation_stats.aff_id = dim_visit.aff_id
and ref_channel_derivation_stats.channel_id = dim_visit.channel_id
```


### From `datamart.dim_category`

#### → `Alles met een deepest_category_id (bijv. BT)`

**Join columns:** `deepest_category_id`

```sql
dim_category.deepest_category_id = [tabel].deepest_category_id
```

#### → `Alles met een dim_category_key (alleen Datamart)`

**Join columns:** `dim_category_key`

```sql
dim_category.dim_category_key = [tabel].dim_category_key
```


### From `datamart.dim_date`

#### → `Alles met een date`

**Join columns:** `date`

```sql
date(dim_date.date) = date([tabel].date)
```

#### → `Alles met een dim_date_key`

**Join columns:** `dim_date_key`

```sql
dim_date.dim_date_key = [tabel].dim_date_key
```

#### → `Alles met een load_start_date & load_end_date`

**Join columns:** `date`

```sql
date(dim_date.date) >= date([tabel].load_start_date)
and date(dim_date.date) < date([tabel].load_end_date)
```


### From `datamart.dim_shop`

#### → `Alles met een shop_id`

**Join columns:** `shop_id`

```sql
dim_shop.shop_id = [tabel].shop_id
```

#### → `Alles met een dim_shop_key`

**Join columns:** `dim_shop_key`

```sql
dim_shop.dim_shop_key = [tabel].dim_shop_key
```


### From `datamart.dim_visit`

#### → `datamart.fct_visits`

**Join columns:** `dim_visit_key`

```sql
fct_visits.dim_visit_key = dim_visit.dim_visit_key
```

#### → `Alles met een visit_id (bijv. BT)`

**Join columns:** `visit_id`

```sql
dim_visit.visit_id = [tabel].visit_id
```

#### → `Alles met een dim_visit_key (alleen Datamart)`

**Join columns:** `dim_visit_key`

```sql
dim_visit.dim_visit_key = [tabel].dim_visit_key
```


### From `datamart.fct_visits`

#### → `datamart.dim_visit`

**Join columns:** `dim_visit_key`

```sql
fct_visits.dim_visit_key = dim_visit.dim_visit_key
```


### From `dl_hot_partition.search_data_details`

#### → `bt.productscore`

**Join columns:** `productidv3, load_start_date, load_end_date, country`

```sql
productscore.productidv3 = search_data_details.productidv3
and productscore.country = search_data_details.country
and search_data_details.dl_processing_date >= date(productscore_load_start_date)
and search_data_details.dl_processing_date < date(productscore.load_end_date)
```


## Quick Reference Examples

### Join to Date Dimension

```sql
-- Using date column
FROM bt.cpa_outclicks_transactional tac
JOIN datamart.dim_date dat ON date(tac.date) = date(dat.date)

-- Using dim_date_key
FROM bt.daily_standup_metrics_category dsm
JOIN datamart.dim_date dat ON dsm.dim_date_key = dat.dim_date_key
```

### Join to Category Dimension

```sql
-- Using deepest_category_id (for bt.* tables)
FROM bt.cpa_outclicks_transactional tac
JOIN datamart.dim_category cat ON tac.deepest_category_id = cat.deepest_category_id

-- Using dim_category_key (for datamart.* tables)
FROM datamart.fct_revenue_aggr rev
JOIN datamart.dim_category cat ON rev.dim_category_key = cat.dim_category_key
```

### Join to Shop Dimension

```sql
-- For revenue/costs (use outclick_shop_id)
FROM bt.cpa_outclicks_transactional tac
JOIN datamart.dim_shop ds ON tac.outclick_shop_id = ds.shop_id

-- For ROAS analysis (use shop_id)
FROM bt.cpa_outclicks_transactional tac
JOIN datamart.dim_shop ds ON tac.shop_id = ds.shop_id
```

### Join to Channel Derivation

```sql
FROM datamart.dim_visit dv
JOIN chan_deriv.ref_channel_derivation_stats chan 
  ON dv.aff_id = chan.aff_id 
  AND dv.channel_id = chan.channel_id
```

### Join to Productscore (Date Range Join)

```sql
-- Productscore uses date ranges, not exact dates
FROM bt.cpa_outclicks_transactional tac
JOIN bt.productscore ps 
  ON tac.productidv3 = ps.productidv3
  AND date(tac.date) >= date(ps.load_start_date)
  AND date(tac.date) < date(ps.load_end_date)
  AND CASE 
        WHEN tac.domain = '1' THEN 'nl'
        WHEN tac.domain = '2' THEN 'be'
        WHEN tac.domain = '12' THEN 'de'
      END = ps.country
  AND ps.deleted_ind = 0
```
