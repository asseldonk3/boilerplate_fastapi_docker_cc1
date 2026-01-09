# Required Filters for Beslist.nl Tables

**CRITICAL**: Always apply these filters to ensure data accuracy. Forgetting these filters will lead to incorrect results.

## Quick Reference

```sql
-- Standard filters for most tables
WHERE deleted_ind = 0           -- Exclude deleted records
  AND actual_ind = 1            -- Only current/actual records
```

## Filters by Table


### `bt.cpa_outclicks_transactional`

#### `deleted_ind` = `0`

**Reason:** Verwijderde records zijn niet meer geldig.

```sql
WHERE deleted_ind = 0
```

#### `actual_ind` =  `1`

**Reason:** Alleen actuele records zijn nog geldig qua omzet en kosten.

#### `label` not in `cpa_after_180_days, rejected_click`

**Reason:** Als je alle omzet wil berekenen, moet je 'ongeldige' omzet uitsluiten.

```sql
WHERE label NOT IN ('cpa_after_180_days', 'rejected_click')
```

#### `label` in `cpa, cpa_cpc, t3_fallback`

**Reason:** Als je alleen CPR/CPC resultaten wilt zien

```sql
WHERE label IN ('cpa', 'cpa_cpc', 't3_fallback')
```

#### `label` in `affiliate_linked_revenue, affilliate_unlinked_click`

**Reason:** Als je alleen affiliate resultaten wilt zien

```sql
WHERE label IN ('affiliate_linked_revenue', 'affilliate_unlinked_click')
```

#### `label` =  `shoppingcart`

**Reason:** Als je alleen WW omzet wilt zien.

#### `shop_deelt_data` = `1`

**Reason:** Als je alleen maar data wilt zien van shops die data delen. Relevant voor ROAS.

```sql
WHERE shop_deelt_data = 1
```


### `bt.daily_standup_metrics_category`

#### `deleted_ind` =  `0`

**Reason:** Verwijderde records zijn niet meer geldig.


### `bt.productscore`

#### `deleted_ind` = `0`

**Reason:** Verwijderde records zijn niet meer geldig.

```sql
WHERE deleted_ind = 0
```

#### `actual_ind` =  `1`

**Reason:** Voor wanneer je alleen actuele records wilt bekijken.

#### `date` >=  `date(load_start_date)`

**Reason:** Als je de data voor een bepaalde datum wilt bekijken, moet die datum tussen de startdatum en de einddatum van het record liggen.

#### `date` < `date(load_end_date)`

**Reason:** Als je de data voor een bepaalde datum wilt bekijken, moet die datum tussen de startdatum en de einddatum van het record liggen.

```sql
WHERE date < date(load_end_date)
```

#### `is_productvalid` =  `1`

**Reason:** Voor wanneer je alleen maar livestaande producten (op dat moment) wilt bekijken.


### `bt.shop_list`

#### `deleted_ind` = `0`

**Reason:** Verwijderde records zijn niet meer geldig.

```sql
WHERE deleted_ind = 0
```

#### `shop_phase` = `1`

**Reason:** Voor wanneer je alleen maar livestaande shops zou willen bekijken.

```sql
WHERE shop_phase = 1
```

#### `hide_online` = `0`

**Reason:** Voor wanneer je alleen maar livestaande shops zou willen bekijken.

```sql
WHERE hide_online = 0
```

#### `total_findable_items_current` >=  `1`

**Reason:** Voor wanneer je alleen maar livestaande shops zou willen bekijken.


### `datamart.dim_category`

#### `deleted_ind` = `0`

**Reason:** Verwijderde records zijn niet meer geldig.

```sql
WHERE deleted_ind = 0
```

#### `category_is_live` = `1`

**Reason:** Voor wanneer je alleen nu nog livestaande categorieën zou willen bekijken. Als je historisch ook nog data mee wilt nemen van categorieën die nu niet meer live staan, moet je dit filter niet meenemen.

```sql
WHERE category_is_live = 1
```


### `datamart.dim_shop`

#### `deleted_ind` = `0`

**Reason:** Verwijderde records zijn niet meer geldig.

```sql
WHERE deleted_ind = 0
```


### `datamart.dim_visit`

#### `is_real_visit` = `1`

**Reason:** Alleen echte visits (geen bots) moeten worden meegenomen.

```sql
WHERE is_real_visit = 1
```


### `dl_hot_partition.search_data_details`

#### `date(dl_processing_date)` = `[datum die je wil bekijken]`

**Reason:** Deze tabel is veel te groot om met de gehele dataset te werken. Een datum filter is dus op zijn minst nodig, en ook een limit op het aantal records als je niet filtert op iets anders wat de dataset klein genoeg maakt.

```sql
WHERE date(dl_processing_date) = [datum die je wil bekijken]
```

#### `is_productvalid` = `1`

**Reason:** Voor wanneer je alleen maar livestaande producten (op dat moment) wilt bekijken.

```sql
WHERE is_productvalid = 1
```


## Common Filter Combinations

### For Revenue/Outclick Analysis (bt.cpa_outclicks_transactional)

```sql
WHERE actual_ind = 1
  AND deleted_ind = 0
  AND label NOT IN ('cpa_after_180_days', 'rejected_click')
  AND date(date) >= '2025-01-01'
```

### For ROAS Analysis (add shop_deelt_data filter)

```sql
WHERE actual_ind = 1
  AND deleted_ind = 0
  AND label NOT IN ('cpa_after_180_days', 'rejected_click')
  AND shop_deelt_data = 1
  AND date(date) >= '2025-01-01'
```

### For Live Shops Only (bt.shop_list)

```sql
WHERE deleted_ind = 0
  AND shop_phase = 1
  AND hide_online = 0
  AND total_findable_items_current >= 1
```

### For Live Products (bt.productscore)

```sql
WHERE deleted_ind = 0
  AND actual_ind = 1
  AND is_productvalid = 1
```

### For Real Visits Only (datamart.dim_visit)

```sql
WHERE is_real_visit = 1
```
