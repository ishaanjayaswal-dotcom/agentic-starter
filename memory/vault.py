"""
Vault writer: raw input -> note file with simple frontmatter.

Two-stage pipeline only:
  1. raw  - the title, body, and links you pass in
  2. note - a markdown file under vault/ with a links: field

The links field shows the *idea* of a graph without building one.
"""

import re
from datetime import datetime, timezone

from memory.store import list_files, read_text, write_text

VAULT_DIR = "vault"


def _slug(title):
    """Turn a title into a safe filename stem."""
    text = (title or "note").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-") or "note"
    return text[:60]


def _frontmatter(title, links):
    """Build a tiny YAML-ish header. Kept simple on purpose."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    link_list = links or []
    # One line list so beginners can read it without a YAML library.
    links_str = "[" + ", ".join(link_list) + "]"
    lines = [
        "---",
        "title: %s" % title,
        "created: %s" % now,
        "links: %s" % links_str,
        "---",
        "",
    ]
    return "\n".join(lines)


def write_note(title, body, links=None):
    """
    Write a note into vault/.

    Returns the relative path as a string (e.g. vault/hello.md).
    """
    name = _slug(title) + ".md"
    relative = "%s/%s" % (VAULT_DIR, name)
    content = _frontmatter(title, links) + (body or "").rstrip() + "\n"
    write_text(relative, content)
    return relative


def read_note(relative_or_name):
    """
    Read a vault note by relative path or bare filename.
    Returns the full text, or None.
    """
    name = relative_or_name
    if not name.startswith(VAULT_DIR):
        name = "%s/%s" % (VAULT_DIR, name)
    if not name.endswith(".md"):
        name = name + ".md"
    return read_text(name)


def search_notes(query):
    """
    Case-insensitive substring search across vault/*.md.

    Returns a list of {path, title, snippet} dicts.
    """
    q = (query or "").lower()
    hits = []
    for path in list_files(VAULT_DIR, suffix=".md"):
        text = path.read_text(encoding="utf-8")
        if q not in text.lower():
            continue
        title = path.stem
        for line in text.splitlines():
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip()
                break
        # First matching line as a short snippet
        snippet = ""
        for line in text.splitlines():
            if q in line.lower():
                snippet = line.strip()[:120]
                break
        hits.append(
            {
                "path": "vault/%s" % path.name,
                "title": title,
                "snippet": snippet,
            }
        )
    return hits
