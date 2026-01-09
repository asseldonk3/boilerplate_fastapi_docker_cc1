#!/usr/bin/env python3
"""
Search products from Beslist Search API (Elasticsearch).

Usage:
    python search_products.py <main_category> [options]
    python search_products.py 655 --limit 10
    python search_products.py 655 --query "iphone" --limit 5
    python search_products.py 655 --facets  # Show facets with counts

Output: JSON with products and optionally facets
"""
import json
import argparse
import requests

SEARCH_API = "https://productsearch-v2.api.beslist.nl"


def search_products(
    main_category: int,
    query: str = None,
    limit: int = 10,
    offset: int = 0,
    include_facets: bool = False
) -> dict:
    """Search products in Elasticsearch."""
    params = {
        'mainCategory': main_category,
        'countryLanguage': 'nl-nl',
        'isBot': 'false',
        'limit': limit,
        'offset': offset
    }
    if query:
        params['query'] = query

    url = f"{SEARCH_API}/search/products"
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    result = {
        'total': data.get('total', 0),
        'products': []
    }

    for p in data.get('products', []):
        result['products'].append({
            'id': p.get('id'),
            'title': p.get('title'),
            'brand': p.get('brandName'),
            'min_price': p.get('minPrice'),
            'max_price': p.get('maxPrice'),
            'shop_count': p.get('shopCount'),
            'categories': [c.get('name') for c in p.get('categories', [])]
        })

    if include_facets:
        result['facets'] = []
        for f in data.get('facets', []):
            facet_data = {
                'id': f.get('id'),
                'name': f.get('label', f.get('name', 'Unknown')),
                'values': []
            }
            for v in f.get('values', [])[:10]:  # Top 10 values
                facet_data['values'].append({
                    'id': v.get('id'),
                    'label': v.get('facetValue'),
                    'count': v.get('count')
                })
            result['facets'].append(facet_data)

    return result


def get_product(group_id: str = None, product_id_v3: str = None) -> dict:
    """Get a single product by ID."""
    params = {
        'countryLanguage': 'nl-nl',
        'isBot': 'false'
    }
    if group_id:
        params['groupId'] = group_id
    elif product_id_v3:
        params['productIdV3'] = product_id_v3
    else:
        raise ValueError("Either groupId or productIdV3 required")

    url = f"{SEARCH_API}/search/product"
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search Beslist products')
    parser.add_argument('main_category', type=int, help='Main category ID (e.g., 655 for Elektronica)')
    parser.add_argument('--query', '-q', type=str, help='Search query')
    parser.add_argument('--limit', '-l', type=int, default=10, help='Number of results')
    parser.add_argument('--offset', '-o', type=int, default=0, help='Pagination offset')
    parser.add_argument('--facets', '-f', action='store_true', help='Include facets with counts')
    args = parser.parse_args()

    results = search_products(
        main_category=args.main_category,
        query=args.query,
        limit=args.limit,
        offset=args.offset,
        include_facets=args.facets
    )

    print(json.dumps(results, indent=2, ensure_ascii=False))
