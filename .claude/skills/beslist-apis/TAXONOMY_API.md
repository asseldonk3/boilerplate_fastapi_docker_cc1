# Taxonomy API Reference

**Base URL**: `http://producttaxonomyunifiedapi-prod.azure.api.beslist.nl`

**Swagger UI**: [/swagger/index.html](http://producttaxonomyunifiedapi-prod.azure.api.beslist.nl/swagger/index.html)

## Endpoints

### Get All Categories

```bash
curl "http://producttaxonomyunifiedapi-prod.azure.api.beslist.nl/api/Categories?locale=nl-NL"
```

Returns flat list of all categories.

### Get Category by ID

```bash
curl "http://producttaxonomyunifiedapi-prod.azure.api.beslist.nl/api/Categories/9005238"
```

**Response:**
```json
{
  "id": 9005238,
  "parentId": 655,
  "name": "Koptelefoons",
  "locale": "nl-NL",
  "level": 2
}
```

Use `parentId` to traverse up the hierarchy.

### Get Category Tree

```bash
curl "http://producttaxonomyunifiedapi-prod.azure.api.beslist.nl/api/Categories/tree?locale=nl-NL"
```

Returns complete hierarchical tree from root categories.

### Get Category Facets

```bash
curl "http://producttaxonomyunifiedapi-prod.azure.api.beslist.nl/category-facets?categoryId=9005238"
```

**Response:**
```json
[
  {
    "id": 1409,
    "categoryId": 9005238,
    "facetId": 1795,
    "facet": {
      "id": 1795,
      "isEnabled": true,
      "isTopFacet": true,
      "labels": [
        {"locale": "nl-NL", "name": "Type koptelefoon", "urlSlug": "type_koptelefoon"}
      ]
    },
    "displayOrder": 0,
    "businessRelevance": 0,
    "describesVariance": false
  }
]
```

## Facet Response Fields

| Field | Description |
|-------|-------------|
| `facetId` | Unique facet identifier |
| `facet.isEnabled` | Only `true` facets show to users |
| `facet.isTopFacet` | Priority facet for UI display |
| `facet.labels[0].name` | User-facing facet name (nl-NL) |
| `displayOrder` | Sort order (0 = first) |
| `describesVariance` | Whether facet describes product variants |

## Parent-Child Facet Inheritance

Child categories often don't have their own facets. Use this pattern:

```python
def get_facets_with_parents(category_id: int) -> list:
    """Get facets merged with universal parent facets."""
    UNIVERSAL_FACETS = {'Merk', 'Kleur'}  # Always inherit these

    all_facets = []
    seen_ids = set()
    current_id = category_id
    is_first = True

    while current_id:
        facets = get_category_facets(current_id)

        for f in facets:
            if f['facet_id'] in seen_ids:
                continue
            # Add all facets from original category
            # Only add universal facets from parents
            if is_first or f['facet_name'] in UNIVERSAL_FACETS:
                all_facets.append(f)
                seen_ids.add(f['facet_id'])

        parent_id = get_parent_id(current_id)
        if parent_id and parent_id != current_id:
            current_id = parent_id
            is_first = False
        else:
            break

    return all_facets
```

## Category Hierarchy Examples

### Electronics
```
Elektronica (655) - has: Merk, Kleur
├── Koptelefoons (9005238) - has: Type koptelefoon, Draadloos, etc.
├── Speakers (9005241)
├── Televisies (9005285) - parent for TV types
│   ├── LED-TV's (9005291) - may only have Merk, Kleur from parent
│   ├── OLED-TV's (9005292)
│   └── QLED-TV's (9005290)
└── Mobiele telefoons (9005282)
```

### Furniture
```
Meubels (9000009)
├── Bankstellen (9000011)
│   ├── Driezitsbanken (9000015)
│   ├── Tweezitsbanken (9000016)
│   └── Hoekbanken (9000017)
└── Kasten (9000018)
    ├── TV-meubels (9000022)
    └── Vitrinekasten (9000023)
```

## Excluded Facets

Never use these as product facets:
- **Winkel** - represents shop/store, not product attribute

## Python Client Example

```python
import requests
from time import sleep

TAXONOMY_API = "http://producttaxonomyunifiedapi-prod.azure.api.beslist.nl"
EXCLUDED_FACETS = {'Winkel'}

def get_category_facets(category_id: int) -> list[dict]:
    """Get facets for a category."""
    url = f"{TAXONOMY_API}/category-facets?categoryId={category_id}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()

    facets = []
    for item in resp.json():
        facet = item.get('facet', {})
        labels = facet.get('labels', [])
        if labels:
            name = labels[0].get('name', '')
            if name not in EXCLUDED_FACETS:
                facets.append({
                    'facet_id': item.get('facetId'),
                    'facet_name': name,
                    'display_order': item.get('displayOrder', 0),
                    'is_top_facet': item.get('isTopFacet', False),
                    'is_enabled': item.get('isEnabled', True)
                })
    return facets

def get_category_parent_id(category_id: int) -> int | None:
    """Get parent category ID."""
    url = f"{TAXONOMY_API}/api/Categories/{category_id}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.json().get('parentId')
```

## Error Handling

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 400 | Invalid category ID |
| 404 | Category not found |
| 500 | Server error |

Always use retry logic for production:

```python
for attempt in range(3):
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        if attempt < 2:
            sleep(1)
            continue
        raise
```
