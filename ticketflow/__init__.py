from __future__ import annotations
import sys
from importlib import import_module

module = import_module(__name__ + ".ticketflow")
sys.modules[__name__] = module
