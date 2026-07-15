"""
Skill registry: one file per skill, discovered by scanning this folder.

Each skill module must expose:
  run(payload: dict) -> dict
"""

import importlib
import pkgutil
from pathlib import Path

_PACKAGE = "skills"
_DIR = Path(__file__).resolve().parent


def list_skills():
    """Return sorted skill names (module stems, no leading underscore)."""
    names = []
    for info in pkgutil.iter_modules([str(_DIR)]):
        if info.name.startswith("_"):
            continue
        names.append(info.name)
    return sorted(names)


def get_skill(name):
    """Import and return a skill module by name. Raises KeyError if missing."""
    if name not in list_skills():
        raise KeyError("unknown skill: %s" % name)
    return importlib.import_module("%s.%s" % (_PACKAGE, name))


def run_skill(name, payload=None):
    """Load skill `name` and call run(payload)."""
    mod = get_skill(name)
    if not hasattr(mod, "run"):
        raise AttributeError("skill %s has no run()" % name)
    return mod.run(payload or {})
