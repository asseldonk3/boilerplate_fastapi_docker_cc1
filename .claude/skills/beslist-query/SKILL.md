---
name: beslist-query
description: Helps write and execute SQL queries for Beslist.nl Redshift performance data. This skill should be used when the user asks about Beslist.nl metrics, revenue, clicks, ROAS, shops, categories, or needs to query the data warehouse. Can propose queries, execute them after user approval, and analyze results for insights and anomalies.
---

# Beslist.nl Query Assistant

This skill provides guidance for writing SQL queries against the Beslist.nl Redshift data warehouse for performance analysis. It can also execute queries and analyze results.

## When to Use This Skill

- User asks about Beslist.nl performance metrics (revenue, clicks, ROAS, CVR, CTR, OPB)
- User needs to query shop, product, category, or visit data
- User asks how to calculate specific KPIs
- User needs help with table joins or required filters
- User wants to find anomalies or insights in the data
- User mentions tables like `cpa_outclicks_transactional`, `daily_standup_metrics_category`, `productscore`, or `shop_list`

## Query Execution Workflow

**IMPORTANT**: Follow this workflow when the user wants to analyze data:

1. **Propose**: Explain what queries will be executed and why
2. **Show**: Display the SQL queries that will be run
3. **Confirm**: Ask the user for permission to execute
4. **Execute**: Run the queries using `scripts/run_query.py`
5. **Analyze**: Interpret results, identify patterns, anomalies, and insights

### Executing Queries

To execute a query after user approval:

```bash
python scripts/run_query.py "SELECT ... FROM ... WHERE ..."
```

Or with a file:
```bash
python scripts/run_query.py --file query.sql --output results.csv
```

### Credentials

Redshift credentials are stored in `.env`. Ensure `REDSHIFT_HOST` is uncommented before executing queries.

## Core Principles

### Always Apply Required Filters

**CRITICAL**: Most tables require mandatory filters to return valid data. Forgetting these filters will produce incorrect results.

Standard filters for most tables:
```sql
WHERE deleted_ind = 0    -- Exclude deleted records
  AND actual_ind = 1     -- Only current records
```

For `bt.cpa_outclicks_transactional`, always include:
```sql
WHERE actual_ind = 1
  AND deleted_ind = 0
  AND label NOT IN ('cpa_after_180_days', 'rejected_click')
```

For ROAS calculations, add:
```sql
  AND shop_deelt_data = 1   -- Only shops that share data
  AND uuid_linked = 1       -- Only linked conversions
```

See `references/filters.md` for complete filter requirements per table.

### Key Tables

| Table | Purpose |
|-------|---------|
| `bt.cpa_outclicks_transactional` | Main source for revenue, costs, outclicks, ROAS, CVR |
| `bt.daily_standup_metrics_category` | Pre-aggregated metrics by category/channel/domain |
| `bt.search_console` | Google Search Console SEO data + Beslist metrics (clicks, impressions, keywords, rankings) |
| `bt.productscore` | Product scores (A/B/C) for Google Shopping Direct |
| `bt.shop_list` | Daily shop information and attributes |
| `datamart.dim_date` | Date dimension for period groupings |
| `datamart.dim_category` | Category hierarchy (maincat → subcat → subsubcat) |
| `datamart.dim_shop` | Current shop statuses |
| `datamart.dim_visit` | Visitor properties (channel, device, landing URL) |

See `references/tables.md` for complete table documentation.

### Common Join Patterns

```sql
-- Join to date dimension
JOIN datamart.dim_date dat ON date(tac.date) = date(dat.date)

-- Join to category dimension
JOIN datamart.dim_category cat ON tac.deepest_category_id = cat.deepest_category_id

-- Join to channel derivation (for marketing channel)
JOIN chan_deriv.ref_channel_derivation_stats chan
  ON tac.aff_id = chan.aff_id AND tac.channel_id = chan.channel_id
```

See `references/joins.md` for all join patterns.

### Key Metrics Calculations

| Metric | Formula |
|--------|---------|
| ROAS | `SUM(revenue_excl) / (SUM(click_revenue) + SUM(transaction_costs))` |
| Rev/Click | `SUM(revenue_excl) / COUNT(DISTINCT stats_id_stat)` |
| CVR | `SUM(transactions) / COUNT(DISTINCT stats_id_stat)` |
| OPB | `SUM(omzet_visit) / SUM(visits)` |
| CTR | `(SUM(bvb_clicks) + SUM(outclicks)) / SUM(visits)` |
| Bounce | `SUM(bounce_clicks_visit) / SUM(visits)` |

See `references/metrics.md` for detailed calculation formulas.

## Workflow

1. **Identify the question**: What metrics does the user need?
2. **Select the right table**:
   - For detailed transactional data → `bt.cpa_outclicks_transactional`
   - For quick aggregated metrics → `bt.daily_standup_metrics_category`
   - For shop information → `bt.shop_list`
   - For product scores → `bt.productscore`
3. **Apply required filters**: Check `references/filters.md`
4. **Add necessary joins**: Check `references/joins.md`
5. **Calculate metrics correctly**: Check `references/metrics.md`
6. **Group appropriately**: Use `dim_date` for period groupings

## Reference Files

- `references/tables.md` - All tables with descriptions and update frequencies
- `references/columns.md` - All 1,205 columns with types and descriptions
- `references/filters.md` - Required filters per table
- `references/joins.md` - Join patterns between tables
- `references/metrics.md` - KPI calculation formulas
- `references/example_queries.md` - Example queries from the official library

## Marketing Channels

To get marketing channel names, join to `chan_deriv.ref_channel_derivation_stats`:

| Channel | Description |
|---------|-------------|
| SEO | Organic search |
| SEA | Paid search |
| Google Shopping | Google Shopping campaigns |
| Google Shopping Direct | GSD campaigns |
| DMA organic | Dynamic Marketing Ads (organic) |
| DMA paid | Dynamic Marketing Ads (paid) |

## Domain Codes

| Code | Domain |
|------|--------|
| 1 | nl (Netherlands) |
| 2 | be (Belgium) |
| 12 | de (Germany) |

## Data Granularity Patterns

**CRITICAL**: Understand what one row represents before querying. Some tables have "apparent duplicates" that are actually valid multi-level data.

| Table | Granularity | Deduplication Key | Notes |
|-------|-------------|-------------------|-------|
| `bt.cpa_outclicks_transactional` | **Order line** | `stats_id_stat` | Same outclick appears multiple times for multi-product orders |
| `bt.search_console` | **URL variant × keyword × device × country** | `clean_url` | Same page has multiple rows due to different `aff_id` tracking parameters |
| `bt.daily_standup_metrics_category` | **Category × channel × domain × date** | Composite key | No duplicates - properly pre-aggregated |

### Correct Metric Calculations by Table

**`bt.cpa_outclicks_transactional`**:
```sql
COUNT(DISTINCT stats_id_stat) as outclicks,  -- NOT COUNT(*)
SUM(revenue_excl) as revenue,
COUNT(DISTINCT uuid) as unique_orders
```

**`bt.search_console`** (when aggregating by clean_url):
```sql
SUM(clicks) as total_clicks,
SUM(impressions) as total_impressions,
SUM(clicks)::float / NULLIF(SUM(impressions), 0) as ctr  -- Recalculate CTR!
```

## Important Notes

- **Spectrum tables cost money**: Queries on `spectrum.archived_*` tables incur costs. Only use when historical data beyond Redshift retention is needed.
- **Large tables need limits**: `bt.productscore` and `dl_hot_partition.search_data_details` are very large. Always filter or use LIMIT.
- **Productscore uses date ranges**: Join using `load_start_date` and `load_end_date`, not exact date matching.
- **Shop ID distinction**: Use `outclick_shop_id` for revenue/costs, use `shop_id` for ROAS calculations.
