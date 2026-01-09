#!/usr/bin/env python3
"""
Get facets with values for a category from Taxonomy API.

Usage:
    python get_category_facets.py <category_id> [--values]
    python get_category_facets.py 9005238
    python get_category_facets.py 9005238 --values  # Include facet values

Output: JSON with facet details and optionally values
"""
import sys
import json
import argparse
import requests
from typing import Optional

TAXONOMY_API = "http://producttaxonomyunifiedapi-prod.azure.api.beslist.nl"
EXCLUDED_FACETS = {'Winkel'}
UNIVERSAL_PARENT_FACETS = {'Merk', 'Kleur'}


def get_category_facets(category_id: int) -> list[dict]:
    """Get facets for a single category."""
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


def get_facet_values(facet_id: int, limit: int = 20) -> list[dict]:
    """Get values for a specific facet."""
    url = f"{TAXONOMY_API}/api/Facets/{facet_id}/values"
    resp = requests.get(url, timeout=15)
    if resp.status_code != 200:
        return []

    values = []
    for item in resp.json()[:limit]:
        labels = item.get('labels', [])
        # Labels use 'valueLabel' or 'caption', not 'name'
        name = ''
        if labels:
            name = labels[0].get('valueLabel', labels[0].get('caption', ''))
        if name:
            values.append({
                'value_id': item.get('id'),
                'value': name
            })
    return values


def get_parent_id(category_id: int) -> Optional[int]:
    """Get parent category ID."""
    url = f"{TAXONOMY_API}/api/Categories/{category_id}"
    resp = requests.get(url, timeout=15)
    if resp.status_code == 200:
        return resp.json().get('parentId')
    return None


def get_facets_with_parents(category_id: int, include_values: bool = False, max_depth: int = 5) -> list[dict]:
    """Get facets merged with universal parent facets (Merk, Kleur)."""
    all_facets = []
    seen_ids = set()
    current_id = category_id
    is_first = True
    depth = 0

    while current_id and depth < max_depth:
        facets = get_category_facets(current_id)

        for f in facets:
            if f['facet_id'] in seen_ids:
                continue
            if is_first or f['facet_name'] in UNIVERSAL_PARENT_FACETS:
                if include_values:
                    f['values'] = get_facet_values(f['facet_id'])
                all_facets.append(f)
                seen_ids.add(f['facet_id'])

        parent_id = get_parent_id(current_id)
        if parent_id and parent_id != current_id:
            current_id = parent_id
            depth += 1
            is_first = False
        else:
            break

    return all_facets


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get category facets from Taxonomy API')
    parser.add_argument('category_id', type=int, help='Category ID (e.g., 9005238)')
    parser.add_argument('--values', action='store_true', help='Include facet values')
    args = parser.parse_args()

    facets = get_facets_with_parents(args.category_id, include_values=args.values)

    print(json.dumps({
        "category_id": args.category_id,
        "facet_count": len(facets),
        "facets": facets
    }, indent=2, ensure_ascii=False))
