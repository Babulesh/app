import sys as _sys
from importlib import import_module

_pkg = import_module(__name__)
_sys.modules.setdefault("brone_hotel", _pkg)
