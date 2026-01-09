#!/usr/bin/env python3
"""
Lookup Beslist categories by name, ID, or URL slug.

Usage:
    python lookup_category.py "Schoonmaak"           # Search by name
    python lookup_category.py --id 9001343           # Lookup by ID
    python lookup_category.py --slug klussen_486260  # Lookup by slug
    python lookup_category.py --parent 35000         # List children of category
"""

import argparse
import json
import urllib.request
from collections import defaultdict

API_URL = "http://producttaxonomyunifiedapi-prod.azure.api.beslist.nl/api/Categories"
BASE_URL = "https://www.beslist.nl/products"

def fetch_categories():
    with urllib.request.urlopen(API_URL) as response:
        return json.load(response)

def build_index(categories):
    by_id = {}
    by_slug = {}
    children = defaultdict(list)
    
    for c in categories:
        cat_id = c['id']
        parent_id = c.get('parentId')
        label = c['labels'][0] if c.get('labels') else {}
        
        entry = {
            'id': cat_id,
            'name': label.get('name', 'N/A'),
            'slug': label.get('urlSlug', 'N/A'),
            'parentId': parent_id,
            'url': f"{BASE_URL}/{label.get('urlSlug', '')}/"
        }
        
        by_id[cat_id] = entry
        by_slug[label.get('urlSlug', '')] = entry
        children[parent_id].append(cat_id)
    
    return by_id, by_slug, children

def get_breadcrumb(cat_id, by_id):
    """Build category path from root to current"""
    path = []
    current = cat_id
    while current is not None:
        if current in by_id:
            path.append(by_id[current]['name'])
            current = by_id[current]['parentId']
        else:
            break
    return ' → '.join(reversed(path))

def print_category(cat, by_id, show_children=False, children=None):
    print(f"\n{'='*60}")
    print(f"📁 {cat['name']}")
    print(f"{'='*60}")
    print(f"  ID:         {cat['id']}")
    print(f"  Slug:       {cat['slug']}")
    print(f"  URL:        {cat['url']}")
    print(f"  Parent ID:  {cat['parentId']}")
    print(f"  Breadcrumb: {get_breadcrumb(cat['id'], by_id)}")
    
    if show_children and children:
        child_ids = children.get(cat['id'], [])
        if child_ids:
            print(f"\n  Subcategories ({len(child_ids)}):")
            for cid in sorted(child_ids, key=lambda x: by_id[x]['name']):
                print(f"    - {by_id[cid]['name']} (ID: {cid})")

def main():
    parser = argparse.ArgumentParser(description='Lookup Beslist categories')
    parser.add_argument('query', nargs='?', help='Search term (name)')
    parser.add_argument('--id', type=int, help='Lookup by category ID')
    parser.add_argument('--slug', help='Lookup by URL slug')
    parser.add_argument('--parent', type=int, help='List children of category ID')
    parser.add_argument('--children', action='store_true', help='Show subcategories')
    args = parser.parse_args()
    
    print("Fetching categories from API...")
    categories = fetch_categories()
    by_id, by_slug, children = build_index(categories)
    print(f"Loaded {len(categories)} categories.\n")
    
    results = []
    
    if args.id:
        if args.id in by_id:
            results = [by_id[args.id]]
        else:
            print(f"Category ID {args.id} not found.")
            
    elif args.slug:
        if args.slug in by_slug:
            results = [by_slug[args.slug]]
        else:
            # Try partial match
            matches = [v for k, v in by_slug.items() if args.slug in k]
            results = matches[:10]
            
    elif args.parent is not None:
        child_ids = children.get(args.parent, [])
        if child_ids:
            print(f"Children of category {args.parent}:")
            results = [by_id[cid] for cid in sorted(child_ids, key=lambda x: by_id[x]['name'])]
        else:
            print(f"No children found for category {args.parent}")
            
    elif args.query:
        # Search by name (case-insensitive)
        query_lower = args.query.lower()
        matches = [c for c in by_id.values() if query_lower in c['name'].lower()]
        results = sorted(matches, key=lambda x: x['name'])[:15]
        
        if not results:
            print(f"No categories found matching '{args.query}'")
    else:
        parser.print_help()
        return
    
    for cat in results:
        print_category(cat, by_id, args.children or args.parent is not None, children)

if __name__ == '__main__':
    main()
