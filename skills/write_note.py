"""
write_note - save a note into the vault (no model needed).

Input dict keys:
  title  - short title (required)
  body   - note body text (required)
  links  - optional list of related note titles or tags
"""

from memory.vault import write_note


def run(payload):
    payload = payload or {}
    title = (payload.get("title") or "").strip()
    body = payload.get("body") or ""
    links = payload.get("links") or []

    if not title:
        return {"ok": False, "error": "title is required"}

    path = write_note(title=title, body=body, links=links)
    return {
        "ok": True,
        "path": path,
        "title": title,
    }
