#!/usr/bin/env python3
"""
Get category hierarchy from Taxonomy API.

Usage:
    python get_category_tree.py <category_id>
    python get_category_tree.py 9005238

Output: Category path from root to specified category
"""
import sys
import json
import requests

TAXONOMY_API = "http://producttaxonomyunifiedapi-prod.azure.api.beslist.nl"


def get_category(category_id: int) -> dict | None:
    """Get category details."""
    url = f"{TAXONOMY_API}/api/Categories/{category_id}"
    resp = requests.get(url, timeout=15)
    if resp.status_code == 200:
        return resp.json()
    return None


def get_category_path(category_id: int) -> list[dict]:
    """Get full path from root to category."""
    path = []
    current_id = category_id

    while current_id:
        cat = get_category(current_id)
        if not cat:
            break
        path.insert(0, {
            "id": cat.get("id"),
            "name": cat.get("name"),
            "level": cat.get("level")
        })
        parent_id = cat.get("parentId")
        if parent_id and parent_id != current_id:
            current_id = parent_id
        else:
            break

    return path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_category_tree.py <category_id>")
        print("Example: python get_category_tree.py 9005238")
        sys.exit(1)

    category_id = int(sys.argv[1])
    path = get_category_path(category_id)

    print(json.dumps({
        "category_id": category_id,
        "path": path,
        "breadcrumb": " > ".join([c["name"] for c in path])
    }, indent=2, ensure_ascii=False))
