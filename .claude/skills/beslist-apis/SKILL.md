---
name: beslist-apis
description: Documentation and tools for Beslist.nl internal APIs. Taxonomy API for categories, facets, and master data. Search API for product search with facet counts from Elasticsearch. Use when working with category structures, product facets, search queries, or Beslist product data.
---

# Beslist Internal APIs

## When to Use Which API

| Need | Use | Endpoint |
|------|-----|----------|
| Category structure/hierarchy | Taxonomy API | `/api/Categories` |
| Facet metadata (name, isTopFacet) | Taxonomy API | `/category-facets` |
| All possible facet values (master) | Taxonomy API | `/api/Facets/{id}/values` |
| Search products | Search API | `/search/products` |
| Facets with product counts | Search API | `/search/products` (returns facets) |
| Product recommendations | Search API | `/search/recommendations` |

## Quick Reference

| API | Base URL | Swagger |
|-----|----------|---------|
| Taxonomy API | `http://producttaxonomyunifiedapi-prod.azure.api.beslist.nl` | [swagger](http://producttaxonomyunifiedapi-prod.azure.api.beslist.nl/swagger/index.html) |
| Search API | `https://productsearch-v2.api.beslist.nl` | [swagger](https://productsearch-v2.api.beslist.nl/) |

## Utility Scripts

### Category Lookup (Most Used)
```bash
# Search category by name
python .claude/skills/beslist-apis/scripts/lookup_category.py "Schoonmaak"

# Lookup by category ID
python .claude/skills/beslist-apis/scripts/lookup_category.py --id 9001343

# Lookup by URL slug
python .claude/skills/beslist-apis/scripts/lookup_category.py --slug klussen_486260

# List all subcategories of a category
python .claude/skills/beslist-apis/scripts/lookup_category.py --id 9001343 --children

# List children by parent ID
python .claude/skills/beslist-apis/scripts/lookup_category.py --parent 35000
```

### Other Scripts
```bash
# Get facets with values for a category
python .claude/skills/beslist-apis/scripts/get_category_facets.py 9005238

# Get category hierarchy path
python .claude/skills/beslist-apis/scripts/get_category_tree.py 9005238

# Search products in a category
python .claude/skills/beslist-apis/scripts/search_products.py 655 --limit 10
```

## Common Examples

### Get facets for a category (Taxonomy API)
```bash
curl "http://producttaxonomyunifiedapi-prod.azure.api.beslist.nl/category-facets?categoryId=9005238"
```

### Get all values for a facet (Taxonomy API)
```bash
# Get all Merk (brand) values - returns 3700+ values
curl "http://producttaxonomyunifiedapi-prod.azure.api.beslist.nl/api/Facets/1289/values"
```

### Search products with facet counts (Search API)
```bash
# mainCategory must be top-level (655=Elektronica), use category for subcategories
curl "https://productsearch-v2.api.beslist.nl/search/products?mainCategory=655&countryLanguage=nl-nl&isBot=false&limit=10"
```

### Filter by facet value (Search API)
```bash
# Filter by brand (Merk facet ID 1289, value ID for Apple is 100052)
curl "https://productsearch-v2.api.beslist.nl/search/products?mainCategory=655&filters[merk][0]=100052&countryLanguage=nl-nl&isBot=false"
```

## Important Rules

- **mainCategory**: Search API requires top-level category (655 for Elektronica)
- **category**: Use for filtering to subcategories in Search API
- **Excluded facets**: Never use "Winkel" (ID: 1) - not a product attribute
- **Universal parent facets**: Merk (1289), Kleur (5657) - inherit to all children
- **Required params**: Search API always needs `countryLanguage=nl-nl` and `isBot=false`

## Main Categories (All 31)

Use these IDs as `mainCategory` in Search API queries.

| ID | Name | Slug |
|----|------|------|
| 37000 | Auto's | `autos` |
| 8 | Baby & peuter | `baby_peuter` |
| 701 | Boeken | `boeken` |
| 262 | Cadeaus & gadgets | `cadeaus_gadgets_culinair` |
| 6 | Computers | `computers` |
| 34000 | Dierenbenodigdheden | `dieren_accessoires` |
| 286 | Drogisterij | `gezond_mooi` |
| 655 | Elektronica | `elektronica` |
| 452 | Erotiek | `voor_volwassenen` |
| 11 | Eten & drinken | `eten_drinken` |
| 38000 | Fietsen | `fietsen` |
| 700 | Films & Series | `films-series` |
| 4 | Games | `cddvdrom` |
| 30000 | Horloges | `horloge` |
| 12000 | Huishoudelijk | `huishoudelijke_apparatuur` |
| 361 | Kantoor | `kantoorartikelen` |
| 137 | Kleding | `mode` |
| 35000 | Klussen | `klussen` |
| 10 | Meubels | `meubilair` |
| 33000 | Mode accessoires | `mode_accessoires` |
| 40000 | Multimedia-accessoires | `accessoires` |
| 31000 | Muziekinstrumenten | `muziekinstrument` |
| 29000 | Parfumerie | `parfum_aftershave` |
| 27000 | Sanitair | `main_sanitair` |
| 32000 | Schoenen | `schoenen` |
| 347 | Sieraden | `sieraden_horloges` |
| 155 | Software | `software` |
| 332 | Speelgoed | `speelgoed_spelletjes` |
| 206 | Sport & outdoor | `sport_outdoor_vrije-tijd` |
| 36000 | Tuinartikelen | `tuin_accessoires` |
| 165 | Woonaccessoires | `huis_tuin` |

For subcategories, use the lookup script or see [TAXONOMY_TREE.md](TAXONOMY_TREE.md).

## Common Facet IDs

| Facet | ID | Notes |
|-------|-----|-------|
| Merk (Brand) | 1289 | Universal, 3700+ values |
| Kleur (Color) | 5657 | Universal |
| Winkel (Shop) | 1 | EXCLUDED - not a product facet |

## Product Images

**CDN Base URL**: `https://hwimages.beslist.net/beslist-images`

The Search API returns image paths with a `{size}` placeholder:
```json
"images": [
  {"url": "pim/5025155113080/394/{size}/41651ccfc972be702fd370887817e71f/Haarstylers/Dyson-Airstrait.jpg"}
]
```

### Constructing Image URLs

```
https://hwimages.beslist.net/beslist-images/{path with size replaced}
```

**Example:**
```python
api_path = "pim/5025155113080/394/{size}/41651ccfc972be702fd370887817e71f/Haarstylers/Dyson.jpg"
full_url = f"https://hwimages.beslist.net/beslist-images/{api_path.replace('{size}', 'F300')}"
# Result: https://hwimages.beslist.net/beslist-images/pim/5025155113080/394/F300/.../Dyson.jpg
```

### Size Values

| Size | Use Case | Dimensions |
|------|----------|------------|
| `F300` | Browse/listing pages | ~300px |
| `V800` | PDP main image | ~800px |
| `F600` | Medium image | ~600px |
| `LARGE` | Alternative large | varies |

### Viewing Images in Browser

To view any product image directly, construct the full URL:

```
https://hwimages.beslist.net/beslist-images/{path}
```

**Example - change size by replacing the size segment:**
```
# API returns path with {size} placeholder:
pim/5025155113080/394/{size}/41651ccfc972be702fd370887817e71f/Haarstylers/Dyson.jpg

# Small (300px) - for thumbnails/listings:
https://hwimages.beslist.net/beslist-images/pim/5025155113080/394/F300/41651ccfc972be702fd370887817e71f/Haarstylers/Dyson.jpg

# Large (800px) - for product detail:
https://hwimages.beslist.net/beslist-images/pim/5025155113080/394/V800/41651ccfc972be702fd370887817e71f/Haarstylers/Dyson.jpg
```

Just paste the full URL in your browser to view the image.

## Parsing Beslist URLs

To identify a category from a Beslist.nl URL like `https://www.beslist.nl/products/klussen/klussen_486260/`:

1. Extract the slug from the URL path (e.g., `klussen_486260`)
2. Query the Search API with that category - the product response includes the full category hierarchy:

```bash
# Query Search API - the response includes category details
curl "https://productsearch-v2.api.beslist.nl/search/products?mainCategory=35000&category=9001343&countryLanguage=nl-nl&isBot=false&limit=1"
```

The product's `categories` array shows the full path:
```json
"categories": [
  {"depth": 0, "id": 35000, "name": "Klussen", "urlName": "klussen"},
  {"depth": 1, "id": 9001343, "name": "Schoonmaak", "urlName": "klussen_486260"}
]
```

**Note**: To get subcategories (children), use the Taxonomy API: `?parentId=9001343`

## Detailed Documentation

- **Taxonomy API**: See [TAXONOMY_API.md](TAXONOMY_API.md)
- **Search API**: See [SEARCH_API.md](SEARCH_API.md)
- **Full Category Tree**: See [TAXONOMY_TREE.md](TAXONOMY_TREE.md) - Complete hierarchy of all 3,575 categories with IDs, slugs, and URLs
