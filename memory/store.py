"""
Tiny file store.

Memory is a pipeline (raw text in, note file out), not a pile of dumps.
This module only reads and writes plain files under a root folder.
"""

from pathlib import Path

# Repo root is one level above memory/
ROOT = Path(__file__).resolve().parent.parent


def resolve(relative_path):
    """Return an absolute Path under the repo root."""
    path = ROOT / relative_path
    return path


def read_text(relative_path):
    """Read a UTF-8 text file. Returns None if missing."""
    path = resolve(relative_path)
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def write_text(relative_path, content):
    """Write UTF-8 text, creating parent folders as needed. Returns path str."""
    path = resolve(relative_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path)


def list_files(relative_dir, suffix=".md"):
    """List file paths under a folder (relative to repo root)."""
    folder = resolve(relative_dir)
    if not folder.is_dir():
        return []
    out = []
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.suffix == suffix:
            out.append(path)
    return out
