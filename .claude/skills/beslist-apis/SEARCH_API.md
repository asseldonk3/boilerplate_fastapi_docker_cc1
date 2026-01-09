# Search API Reference (ProductSearch v2)

**Base URL**: `https://productsearch-v2.api.beslist.nl`

**Swagger UI**: [https://productsearch-v2.api.beslist.nl/](https://productsearch-v2.api.beslist.nl/)

## URL to API Mapping

Convert Beslist.nl URLs to Search API calls:

### URL Pattern Structure

```
https://www.beslist.nl/products/{main}/{category}/r/{search}/c/{facets}
```

| URL Part | API Parameter | Example |
|----------|---------------|---------|
| `/{category}/` | `category={category}` | `category=elektronica_19875536_19934132` |
| `/r/{search}/` | `query={search}` | `query=airtag apple` |
| `/c/{facet}~{value}/` | `filters[{facet}][0]={value}` | `filters[merk][0]=100052` |
| `~~` (facet separator) | Multiple filter params | `&filters[x][0]=a&filters[y][0]=b` |
| `+` (value separator) | Multiple values same facet | `&filters[x][0]=a&filters[x][1]=b` |

### Conversion Examples

**Example 1: Category + brand + model filters**
```
URL:  /products/elektronica/elektronica_19875536_19934132/c/merk~100052~~modelnaam_mob~23541684+23596503

API:  /search/products?category=elektronica_19875536_19934132
      &filters[merk][0]=100052
      &filters[modelnaam_mob][0]=23541684
      &filters[modelnaam_mob][1]=23596503
      &countryLanguage=nl-nl&isBot=false
```

**Example 2: Text search only**
```
URL:  /products/accessoires/accessoires_2701112/r/airtag_apple/

API:  /search/products?category=accessoires_2701112
      &query=airtag apple
      &countryLanguage=nl-nl&isBot=false
```
Note: Underscores in search term become spaces.

**Example 3: Combined search + facet filter**
```
URL:  /products/accessoires/accessoires_2701112/r/airtag_apple/c/type_cases~3304682

API:  /search/products?category=accessoires_2701112
      &query=airtag apple
      &filters[type_cases][0]=3304682
      &countryLanguage=nl-nl&isBot=false
```

### URL Parsing Rules

1. **Category**: Extract from path (e.g., `elektronica_19875536_19934132`)
2. **Search term** (`/r/`): Replace underscores with spaces
3. **Facets** (`/c/`): Split by `~~` for multiple facets
4. **Facet values**: Split by `~` → `[facet_name, values]`
5. **Multiple values**: Split by `+` for OR within same facet

## Required Parameters

All endpoints require:
- `countryLanguage=nl-nl` (or other locale)
- `isBot=false`

## Endpoints

### Search Products

```bash
GET /search/products
```

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| mainCategory | int | No | Top-level category (655=Elektronica) |
| category | string | No | Subcategory filter |
| query | string | No | Search text |
| filters | object | No | Facet filters (see below) |
| limit | int | No | Results per page (default: 20) |
| offset | int | No | Pagination offset |
| sort | string | No | popularity, price, first_addition |
| sortDirection | string | No | asc, desc |

**Example:**
```bash
curl "https://productsearch-v2.api.beslist.nl/search/products?mainCategory=655&countryLanguage=nl-nl&isBot=false&limit=5"
```

**Response includes:**
- `products[]` - Product listings
- `facets[]` - Available facets with value counts
- `total` - Total matching products

### Search with Filters

Filter by facet values using `filters[facet_name][index]=value_id`:

```bash
# Filter by brand (Merk=Apple, value_id=100052)
curl "https://productsearch-v2.api.beslist.nl/search/products?mainCategory=655&filters[merk][0]=100052&countryLanguage=nl-nl&isBot=false"

# Filter by price range
curl "https://productsearch-v2.api.beslist.nl/search/products?mainCategory=655&filters[price][min]=100&filters[price][max]=500&countryLanguage=nl-nl&isBot=false"

# Multiple filters
curl "https://productsearch-v2.api.beslist.nl/search/products?mainCategory=655&filters[merk][0]=100052&filters[kleur][0]=19949326&countryLanguage=nl-nl&isBot=false"
```

### Get Single Product

```bash
GET /search/product
```

**Parameters:**
- `groupId` - Product group ID (e.g., "9005282-Samsung Galaxy S22")
- `productIdV3` - Product V3 ID (e.g., "3eXaEsMSjcGiQb7vYTPn2wPZP6MD")

```bash
curl "https://productsearch-v2.api.beslist.nl/search/product?groupId=4895229151192&countryLanguage=nl-nl&isBot=false"
```

### Get Multiple Products by IDs

```bash
GET /search/products-by-ids
```

```bash
curl "https://productsearch-v2.api.beslist.nl/search/products-by-ids?ids=4255843808221,9501736719712&countryLanguage=nl-nl&isBot=false"
```

### Get Recommendations

```bash
GET /search/recommendations
```

```bash
curl "https://productsearch-v2.api.beslist.nl/search/recommendations?id=5600001700173&mainCategory=655&limit=10&countryLanguage=nl-nl&isBot=false"
```

### Get Facets Only

```bash
GET /search/facets
```

**Parameters:**
- `mainCategory` - Top-level category
- `facetIds` - Comma-separated facet IDs to retrieve

```bash
curl "https://productsearch-v2.api.beslist.nl/search/facets?mainCategory=655&facetIds=1289,5657&countryLanguage=nl-nl&isBot=false"
```

### Shop Information

```bash
# Get shop info by IDs
GET /shops-info?shopIds=1,2,3&countryLanguage=nl-nl&isBot=false

# Get shop stats
GET /shop-stats/{shopId}?isBot=false

# Get shop stats by category
GET /shop-stats/{shopId}/category/{categoryId}?isBot=false
```

## Response Structures

### Product Object

```json
{
  "id": "4895229151192",
  "title": "Philips Sonicare DiamondClean",
  "brandName": "Philips",
  "minPrice": 199.00,
  "maxPrice": 249.00,
  "shopCount": 12,
  "categories": [
    {"id": 655, "name": "Elektronica", "depth": 0},
    {"id": 9005269, "name": "Elektrische tandenborstels", "depth": 2}
  ],
  "image": "https://...",
  "url": "/product/..."
}
```

### Facet Object (from /search/products)

```json
{
  "id": 1289,
  "label": "Merk",
  "values": [
    {
      "id": 100052,
      "facetValue": "Apple",
      "count": 966,
      "selected": false
    },
    {
      "id": 100217,
      "facetValue": "Braun",
      "count": 859,
      "selected": false
    }
  ]
}
```

## EAN Variants by Category

Products in different categories have different EAN structures:

| Category Type | EAN Pattern | Example |
|--------------|-------------|---------|
| **Fashion (schoenen, mode)** | Multiple EANs per product | 15 EANs for shoe sizes (38-46) |
| **Electronics** | Single EAN per product | Each color/storage combo = separate product |
| **Accessories (koffers)** | Single EAN per product | No size variants |
| **Furniture (meubilair)** | Single EAN per product | No size variants |

**Fashion Example (Nike shoe):**
```json
{
  "id": "V4_00a3bf37-f613-4786-a985-ab74eace6b0d",
  "title": "Nike - P-6000 - Hardloopschoenen - Wit",
  "eans": [
    "0198482539740",  // Size 38
    "0198482525132",  // Size 38.5
    "0198482527853",  // Size 39
    // ... 15 EANs total for all sizes
  ]
}
```

**Electronics Example (Google Pixel):**
```json
{
  "id": "0840353914421",
  "title": "Google Pixel 9 Pro 128GB Groen",
  "eans": ["0840353914421"]  // Single EAN - other colors are separate products
}
```

**Key insight**: Fashion categories group size variants under one product with multiple EANs. Electronics/accessories treat each variant as a separate product listing.

## Full Response Structure

The `/search/products` endpoint returns rich data:

```json
{
  "total": 1234,
  "products": [
    {
      "id": "V4_xxx or EAN",
      "title": "Product Name",
      "brandName": "Brand",
      "description": "Full product description...",
      "eans": ["ean1", "ean2"],
      "minPrice": 99.00,
      "maxPrice": 149.00,
      "minPriceOnlyNew": 99.00,
      "shopCount": 5,
      "popularity": 84019,
      "firstAddition": "2025-10-03",
      "pimId": "nl-nl-gold-xxx",
      "plpUrl": "/p/product-slug/category/id/",
      "mainCategoryId": 655,
      "categories": [
        {"id": 655, "name": "Elektronica", "depth": 0, "urlName": "elektronica"},
        {"id": 9005282, "name": "Mobiele telefoons", "depth": 2, "isBidding": true}
      ],
      "images": [
        {"url": "path/{size}/hash.jpg", "size": {"width": 1080, "height": 488}}
      ],
      "labels": [
        {"name": "goodDeal", "value": "-12%"},
        {"name": "isNew"}
      ],
      "pimRating": {
        "averageRating": 4.7,
        "totalRatingCount": 204,
        "bestRating": 5
      },
      "priceHistory": {
        "lowestPrice": 89.00
      },
      "shops": [
        {
          "id": 1,
          "name": "bol.com",
          "logo": "/beslist-images/shop_images/LARGE/1.png",
          "isAffiliate": true,
          "shopType": "CPC",
          "coolingOffPeriod": 30,
          "deliveryCompanies": [{"id": 4, "name": "DHL"}],
          "offers": [
            {
              "bestOffer": true,
              "condition": "nieuw",
              "regularPrice": {"price": 119.00},
              "salePrice": {"price": 99.00},
              "discountPercentage": 16.8,
              "productIdV3": "xxx",
              "url": "https://shop.com/product",
              "labels": [{"name": "freeReturn"}, {"name": "highDiscount"}],
              "roas": {"percentage": 650}
            }
          ]
        }
      ],
      "facets": []
    }
  ],
  "facets": [
    {
      "id": 1289,
      "label": "Merk",
      "values": [
        {"id": 100052, "facetValue": "Apple", "count": 966, "selected": false}
      ]
    }
  ]
}
```

### Key Response Fields

| Field | Description |
|-------|-------------|
| `id` | Product ID (V4_uuid for fashion, EAN for electronics) |
| `eans` | Array of EANs (multiple for fashion size variants) |
| `minPrice` / `maxPrice` | Price range across all shops |
| `minPriceOnlyNew` | Lowest price for new condition |
| `popularity` | Popularity score (higher = more popular) |
| `firstAddition` | Date product was first added |
| `pimRating` | Product ratings (averageRating, totalRatingCount) |
| `priceHistory.lowestPrice` | Historical lowest price |
| `shops[].offers[].roas` | ROAS percentage for affiliate tracking |
| `labels` | Product badges (goodDeal, isNew, googleTop100) |

## Important Notes

1. **mainCategory must be top-level**: Use 655 (Elektronica), not subcategory IDs
2. **Subcategory filtering**: Use `category` param for subcategories
3. **Facet counts**: Only `/search/products` returns facets with product counts
4. **No index for subcategories**: Subcategory IDs like 9005238 don't have their own ES index
5. **Fashion vs Electronics IDs**: Fashion uses V4_uuid format, electronics often use EAN as ID

## Python Example

```python
import requests

SEARCH_API = "https://productsearch-v2.api.beslist.nl"

def search_products(main_category, query=None, limit=20):
    params = {
        'mainCategory': main_category,
        'countryLanguage': 'nl-nl',
        'isBot': 'false',
        'limit': limit
    }
    if query:
        params['query'] = query

    resp = requests.get(f"{SEARCH_API}/search/products", params=params)
    resp.raise_for_status()
    return resp.json()

# Search electronics
results = search_products(655, query="iphone", limit=10)
print(f"Found {results['total']} products")
for p in results['products']:
    print(f"  - {p['title']} ({p['minPrice']})")
```
