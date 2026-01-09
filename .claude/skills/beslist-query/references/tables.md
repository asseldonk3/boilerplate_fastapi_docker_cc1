# Beslist.nl Redshift Tables Overview

This document contains all available tables for querying Beslist.nl performance data.

## Schema Overview

| Schema | Description |
|--------|-------------|
| `bt` | Business tables - shops, products, clicks, scores |
| `datamart` | Dimension and fact tables - aggregated data |
| `hda` | HDA analytics - visits, pageviews, attribution |
| `chan_deriv` | Channel derivation - channel statistics |
| `kpi` | KPI tables - pixel quality metrics |
| `spectrum` | Archived data - historical data (costs money to query!) |

## Tables by Priority

### High Priority Tables

These are the most commonly used tables for performance analysis.

#### `bt.cpa_outclicks_transactional`

**Columns:** 204 | **Update:** 1x per dag, rond 07:30

Deze tabel is de bron van alle omzet, zowel voor CPR als affiliates en WW. Vanuit deze tabel kan je shop omzet, onze omzet (en dus shop kosten), ROAS, CVR en aantal outclicks en orders uitrekenen.

**Belangrijke kenmerken:**
- **Granulariteit**: Per **order line** (niet per outclick). Eén outclick kan meerdere rijen hebben als de klant meerdere producten heeft gekocht.
- **Duplicaten**: Dezelfde `stats_id_stat` kan meerdere keren voorkomen met verschillende `revenue_excl` waarden.

**Correcte metric berekeningen**:
- **Outclicks**: `COUNT(DISTINCT stats_id_stat)`
- **Revenue**: `SUM(revenue_excl)`
- **Order lines**: `COUNT(*)` of `SUM(transactions)`
- **Unieke orders**: `COUNT(DISTINCT uuid)`

#### `bt.daily_standup_metrics_category`

**Columns:** 62 | **Update:** 1x per dag, rond 08:00

Deze tabel is heel handig om op een snelle manier metrics als omzet en marge, OPB, ROAS en bounce te berekenen op categorie, kanaal of domein niveau. 

#### `bt.productscore`

**Columns:** 66 | **Update:** 1x per dag, rond 16:00

In deze tabel wordt per product (= shop item) een score berekend, die we vervolgens gebruiken om A-items en lager te bepalen. De resulterende output wordt vervolgens gebruikt voor onze Google Shopping Direct campagnes. De tabel werkt met start en einddatums voor records, waardoor je steeds moet inprikken tussen deze twee datums om een staat van een item te vinden op een bepaalde datum. Let op: deze tabel is erg groot, en het is daarom altijd de bedoeling om goed te filteren of een limit te gebruiken in je query.

#### `bt.shop_list`

**Columns:** 117 | **Update:** 1x per dag, rond 08:30

In de shop lijst staan op dagbasis metrics per shop, zoals bijvoorbeeld de omzet van de shop, productscore en EAN score informatie, of een shop opgezegd heeft, contract informatie en gegevens zoals op welke domeinen de shop live stond, of het een pixel of affiliate shop was, de accountmanager en welk verdienmodel de shop had. 

#### `chan_deriv.ref_channel_derivation_stats`

**Columns:** 8 | **Update:** Handmatige updates

Dit is eigenlijk een dimensie tabel, die gebruikt kan worden om door middel van aff_id en channel_id het marketing kanaal te onderscheiden. Wordt vaak gebruikt in combinatie met de dim_visit tabel.

#### `datamart.dim_category`

**Columns:** 36 | **Update:** 1x per dag, rond 03:15

De categorie dimensie biedt informatie over welke categorieën we allemaal hebben als Beslist, en hoe de rangorde hier binnen vervolgens is. Bijvoorbeeld een maincat heeft eronder wel of niet een aantal subcats liggen, die vervolgens wel of niet verdeeld kunnen worden in subsubcats. Dit kan je zien in deze tabel. Ook biedt deze informatie inzichten over of een categorie wel of niet de diepste is in een rangorde, en of een categorie een bidcat is.

#### `datamart.dim_date`

**Columns:** 47 | **Update:** 1x per dag, rond 03:15

De datum dimensie is heel handig om te gebruiken wanneer je data net over een andere periode nodig hebt dan hetgene wat beschikbaar is in een andere dataset. De tabel bevat per datum ook in welke week, maand, jaar, kwartaal etc. deze zich bevindt, en er staan ook handige velden in de tabel om te bepalen of een datum de huidige datum is, of om alleen alle datums in het huidige jaar te selecteren bijvoorbeeld.

#### `datamart.dim_shop`

**Columns:** 60 | **Update:** 1x per dag, rond 03:15

De shop dimensie biedt alle huidige shop statussen, zoals bijvoorbeeld het huidige verdienmodel of de shop fase. Deze wordt dus iedere dag volledig ververst. 

#### `datamart.dim_visit`

**Columns:** 39 | **Update:** 1x per dag, rond 05:30

De visit dimensie wordt altijd gebruikt in combinatie met de fct_visits tabel. Door middel van deze tabel kan je verschillende eigenschappen van de bezoeker gebruiken, zoals bijvoorbeeld het marketing kanaal, de landings URL, het device en de categorie waarop de bezoeker landde.

#### `datamart.fct_visits`

**Columns:** 38 | **Update:** 1x per dag, rond 07:45

Voor deze tabel worden alle bezoekers gepakt en wordt daar vervolgens allerlei informatie aan geplakt, zoals de (shop)omzet, clicks, orders en pageviews. Deze data kan je vervolgens gebruiken om getallen zoals de OPB, CTR, bounce, het aantal bezoekers en de webshop revenue per bezoeker uit te rekenen.

#### `dl_hot_partition.search_data_details`

**Columns:** 53 | **Update:** Maximaal 11x per dag (ieder uur), afhankelijk van hoe vaak de itemcount draait

Deze tabel bevat per product voor de afgelopen drie dagen informatie vanuit de search index, bijvoorbeeld of het product valid was, voor welke prijs deze aangeboden werd, het bijbehorende EAN en PIM ID, de URL van het product en de levertijd. Let op: deze tabel is erg groot, en het is daarom altijd de bedoeling om goed te filteren of een limit te gebruiken in je query.


### Medium Priority Tables

Useful for specific analysis needs.

#### `bt.ean_score`

**Columns:** 43 | **Update:** 1x per dag, rond 17:30

In deze tabel wordt per EAN een score berekend, die we vervolgens gebruiken om A-items en lager te bepalen. De resulterende output wordt vervolgens gebruikt voor onze DMA campagnes. De tabel werkt met start en einddatums voor records, waardoor je steeds moet inprikken tussen deze twee datums om een staat van een item te vinden op een bepaalde datum. 

#### `bt.revenue_per_product`

**Columns:** 127 | **Update:** 1x per dag, rond 7:00

Deze tabel is heel handig om te zien of we omzet en outclicks generen op productniveau over een bepaalde periode, waarbij we in de tabel 6 verschillende periodes beschikbaar hebben gemaakt. Ook wordt er in deze tabel vanuit de tag data weergegeven hoeveel session starts en shop omzet het product gegenereerd heeft.

#### `bt.shop_main_attributes_by_day`

**Columns:** 140 | **Update:** 1x per dag, rond 07:30

In deze tabel kan je op dagbasis de belangrijkste gegevens van een shop vinden, bijvoorbeeld de accountmanager, of het een tag shop is of een affiliate, het verdienmodel, op welke domeinen hij live staat en welke contracten zijn afgesloten.

#### `datamart.fct_revenue_aggr`

**Columns:** 16 | **Update:** 1x per dag, rond 07:45

In deze tabel wordt alle omzet samengevoegd op datum, shop en categorie niveau, zodat je hiermee heel snel en makkelijk berekeningen op die dimensies kan maken, zonder dat je met ruwe data en afkeurregels en dergelijke hoeft te werken.

#### `datamart.fct_search_itemcounts`

**Columns:** 61 | **Update:** Maximaal 11x per dag (ieder uur), afhankelijk van hoe vaak de itemcount draait

Met deze tabel kan je makkelijk op dagbasis, shop- en categorie niveau bepalen hoeveel items live stonden op de site, waarbij je ook nog kan splitsen per domein. Dit is vooral handig voor verklarende analyses, bijvoorbeeld bij dalende of sterk stijgende omzetten.

#### `hda.componentvisit`

**Columns:** 41 | **Update:** 1x per dag, rond 05:30

Deze tabel bevat allerlei informatie over de pageviews die bezoekers doen. Hij wordt vooral vaak gebruikt in combinatie met de visit tabel (hda.visit of datamart.dim_visit) in testen, zodat we kunnen kijken of een bepaalde wijziging in de website beter functioneert dan het huidig livestaande alternatief.

#### `hda.landingpage_views`

**Columns:** 13 | **Update:** 1x per dag, rond 09:35

In deze tabel staan alle PLP pageviews, met daarbij duidelijk weergegeven welke producten op de pagina stonden. 

#### `hda.pixel_attribution_beslist_last_click`

**Columns:** 41 | **Update:** 1x per dag, rond 06:30

In deze tabel staan de tag conversies die gedaan zijn op een bepaalde datum, met daarbij duiding of hij aan ons geattribueerd is, of een assisted conversion was, of dat Beslist er geen rol bij gespeeld heeft. Ook is in de tabel af te lezen of we op IP of User ID hebben geattribueerd.

#### `kpi.kpi_targets_le`

**Columns:** 27 | **Update:** 1x per dag, rond 00:30

In deze tabel worden de LE (maand)targets weggeschreven die we proberen te halen in een bepaald jaar.

#### `kpi.pixel_quality`

**Columns:** 28 | **Update:** 1x per dag, rond 09:00

Het doel van deze tabel is om de tag data per shop weer te geven (linkage, coverage, transacties, outclicks) om te kijken of deze shop afgerekend zou moeten worden op CPR of niet.


### Low Priority Tables

Specialized tables for specific use cases.

#### `bt.daily_standup_metrics`

**Columns:** 72 | **Update:** 1x per dag, rond 08:00

In deze tabel staat op dagniveau een overzicht van een aantal hele belangrijke metrics, zoals omzet en marge, OPB, visits, transacties en CPR label informatie. 

#### `bt.ean_score_itemcount`

**Columns:** 17 | **Update:** 1x per dag, rond 18:00

Deze tabel is eigenlijk een vervolg op de ean_score tabel, waarin we weergeven per datum, shop, categorie en EAN score label combinatie hoeveel items er live stonden op de site.

#### `bt.facetdekking_deepestcat`

**Columns:** 29 | **Update:** 1x per dag, rond 04:30

Deze tabel wordt gebruikt om de facetdekking te berekenen, oftewel per facet kan worden gekeken hoeveel items er mogelijk ingedeeld hadden kunnen zijn op dat facet, en hoeveel er daadwerkelijk op ingedeeld zijn.

#### `bt.onboarding`

**Columns:** 28 | **Update:** 4x per dag, rond 09:15, 11:15, 13:15 en 15:15

In deze tabel wordt een koppeling gemaakt tussen shops die via het onboarding proces binnen komen en shops die in Efficy in het shop aanmelding proces staan, met daarbij per dag de huidige status van waar in het proces deze zich bevindt.

#### `bt.productscore_itemcount`

**Columns:** 18 | **Update:** 1x per dag, rond 17:00

Deze tabel is eigenlijk een vervolg op de productscore tabel, waarin we weergeven per datum, shop, categorie en productscore label combinatie hoeveel items er live stonden op de site.

#### `bt.ranking_input_pricebuckets_bidcat`

**Columns:** 332 | **Update:** 1x per dag, rond 14:00

Deze tabel wordt gebruikt om de revenue per click te berekenen die we naar IT sturen voor gebruik in de ranking. Vooral interessant voor analyse doeleinden zijn de bakjes en periodes op basis waarvan een uiteindelijke rev/click wordt berekend voor een shop, categorie en pricebucket combinatie. 

#### `bt.search_console`

**Columns:** 43 | **Update:** 1x per dag, rond 10:45

Google Search Console data gecombineerd met Beslist interne metrics. Toont SEO performance per URL, keyword, device en land.

**Belangrijke kenmerken:**
- **Granulariteit**: Per dag, per URL (met aff_id), per keyword, per device, per country
- **URL varianten**: Dezelfde pagina kan meerdere rijen hebben door verschillende `aff_id` tracking parameters. Gebruik `clean_url` voor aggregatie.
- **Keyword intent classificatie**: `is_informational`, `is_commercial_brand`, `is_commercial_shop`, `is_transactional_general`, `is_transactional_sale`
- **URL types**: `R-url` (zoekresultaten), `C-url` (gefilterde pagina's), `PLP` (productpagina's), `Browse-url zonder /r/ en /c/`, `Homepage`

**Google metrics**: `clicks`, `impressions`, `ctr`, `avg_position`
**Beslist metrics**: `visits`, `number_of_outclicks`, `ww_revenue`, `cpc_revenue`, `affiliate_revenue`

**Let op bij aggregatie**: Herbereken CTR als `SUM(clicks)/SUM(impressions)` wanneer je groepeert op `clean_url`.

#### `bt.unique_products_multiple_providers`

**Columns:** 74 | **Update:** Maximaal 11x per dag (ieder uur), afhankelijk van hoe vaak de itemcount draait

Met deze tabel is uit te vinden op dag, maincat en land niveau hoeveel producten er gedubbeld kunnen worden op basis van EAN of PIM ID. Dit is vervolgens weer uitgesplitst op basis van de hoeveelheid aanbieders per product.

#### `hda.browsepage_views_search_types`

**Columns:** 12 | **Update:** 1x per dag, rond 09:45

Deze tabel geeft weer per browsepage bezoek hoeveel AND en OR results van een bepaald type er op de pagina stonden. Dit is vooral interessant voor analyse doeleinden met betrekking tot long-tail of short-tail verkeer.

#### `hda.pim_data`

**Columns:** 48 | **Update:** 1x per week, zondag 11:00 UTC tijd

In deze tabel komt te staan per input bron wat er allemaal wel en niet gevuld is in PIM. De tabel bevat een snapshot die 1x per week gemaakt wordt van de huidige ingevulde PIM data.

#### `hda.sa360_adgroup`

**Columns:** 36 | **Update:** 1x per dag, rond 07:00

In deze tabel worden de marketing kosten, impressies en ingekochte clicks vanuit SA360 weggeschreven per account, campagne en adgroup. Tech-BI matcht deze vervolgens 1x per week naar een diepste cat zodat hier ook op gerapporteerd kan worden.

