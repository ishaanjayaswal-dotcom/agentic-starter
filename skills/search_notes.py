"""
search_notes - find vault notes that contain a keyword (no model needed).

Input dict keys:
  query - text to search for (required)
"""

from memory.vault import search_notes


def run(payload):
    payload = payload or {}
    query = (payload.get("query") or "").strip()
    if not query:
        return {"ok": False, "error": "query is required"}

    hits = search_notes(query)
    return {
        "ok": True,
        "query": query,
        "count": len(hits),
        "hits": hits,
    }
