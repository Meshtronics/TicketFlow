from __future__ import annotations
from pathlib import Path
from typing import Any

from functools import lru_cache
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parent.parent


@lru_cache(maxsize=1)
def get_config() -> dict[str, Any]:
    yaml = YAML(typ="safe")
    # Prefer ticketflow/.ticketflow.yml, fall back to root/.ticketflow.yml
    local_path = ROOT / "ticketflow" / ".ticketflow.yml"
    root_path = ROOT / ".ticketflow.yml"
    if local_path.exists():
        return yaml.load(local_path) or {}
    if root_path.exists():
        return yaml.load(root_path) or {}
    return {}


def cfg(*keys, default=None):
    """Shorthand to read nested keys with dot path."""
    node = get_config()
    for k in keys:
        node = node.get(k, {})
    return node or default
