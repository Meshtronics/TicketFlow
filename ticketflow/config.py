from __future__ import annotations
from pathlib import Path
from typing import Any

import os
from functools import lru_cache
from ruamel.yaml import YAML

@lru_cache(maxsize=1)
def get_config() -> dict[str, Any]:
    yaml = YAML(typ="safe")
    path = Path.cwd() / ".ticketflow.yml"
    if path.exists():
        return yaml.load(path) or {}
    return {}

def cfg(*keys, default=None):
    """Shorthand to read nested keys with dot path."""
    node = get_config()
    for k in keys:
        node = node.get(k, {})
    return node or default
