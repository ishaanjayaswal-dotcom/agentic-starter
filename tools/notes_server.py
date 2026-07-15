"""
One tiny MCP-style tool surface for notes.

Not a full MCP server. Just the shape: a dict of tools, each with
name, description, and a handler. Agents discover tools; they do not
memorise them.
"""

from memory.vault import search_notes, write_note

TOOLS = {}


def _register(name, description, handler):
    TOOLS[name] = {
        "name": name,
        "description": description,
        "handler": handler,
    }


def _tool_write_note(args):
    title = (args or {}).get("title") or "untitled"
    body = (args or {}).get("body") or ""
    links = (args or {}).get("links") or []
    path = write_note(title=title, body=body, links=links)
    return {"ok": True, "path": path}


def _tool_search_notes(args):
    query = (args or {}).get("query") or ""
    hits = search_notes(query)
    return {"ok": True, "count": len(hits), "hits": hits}


_register(
    "write_note",
    "Write a markdown note into the vault.",
    _tool_write_note,
)
_register(
    "search_notes",
    "Search vault notes by keyword.",
    _tool_search_notes,
)


def list_tools():
    """Return tool metadata without handlers (safe to print or send over HTTP)."""
    out = []
    for name, meta in sorted(TOOLS.items()):
        out.append({"name": name, "description": meta["description"]})
    return out


def call_tool(name, args=None):
    """Run a tool by name. Raises KeyError if unknown."""
    if name not in TOOLS:
        raise KeyError("unknown tool: %s" % name)
    return TOOLS[name]["handler"](args or {})


if __name__ == "__main__":
    print("[notes_server] tools:")
    for t in list_tools():
        print("  - %s: %s" % (t["name"], t["description"]))
