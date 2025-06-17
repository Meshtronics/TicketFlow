from __future__ import annotations
from pathlib import Path
from typing import Any

from functools import lru_cache
try:
    from ruamel.yaml import YAML  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    class YAML:
        def __init__(self, *a, **kw) -> None:
            pass

        def load(self, f):
            return {}

ROOT = Path(__file__).resolve().parents[2]


@lru_cache(maxsize=1)
def get_config() -> dict[str, Any]:
    yaml = YAML(typ="safe")
    # Look for .ticketflow.yml at repo root
    root_path = ROOT / ".ticketflow.yml"
    if root_path.exists():
        return yaml.load(root_path) or {}
    return {}


def cfg(*keys, default=None):
    """Shorthand to read nested keys with dot path."""
    node = get_config()
    for k in keys:
        node = node.get(k, {})
    return node or default
