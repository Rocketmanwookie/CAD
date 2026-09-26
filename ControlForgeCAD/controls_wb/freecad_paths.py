# SPDX-License-Identifier: MIT
"""Path helpers for FreeCAD workbench bootstrap code."""

from pathlib import Path
from typing import Mapping, Any


def workbench_root_from_module_globals(module_globals: Mapping[str, Any]) -> str:
    """Return the ControlForgeCAD workbench root for FreeCAD init modules."""
    candidate = module_globals.get("__file__")
    if candidate:
        root = Path(candidate).resolve().parent
        # A few FreeCAD addon loading paths supply an inherited or synthetic
        # ``__file__`` (for example ``~/InitGui.py``).  It identifies the
        # loader, not this workbench, so only trust it when it has the package
        # layout that makes it a ControlForgeCAD root.
        if (root / "controls_wb").is_dir():
            return str(root)

    module_spec = module_globals.get("__spec__")
    origin = getattr(module_spec, "origin", None)
    if origin:
        root = Path(origin).resolve().parent
        if (root / "controls_wb").is_dir():
            return str(root)

    import controls_wb

    package_file = getattr(controls_wb, "__file__", None)
    if package_file:
        return str(Path(package_file).resolve().parent.parent)

    package_path = getattr(controls_wb, "__path__", None)
    if package_path:
        return str(Path(next(iter(package_path))).resolve().parent)

    raise RuntimeError("Unable to determine ControlForgeCAD workbench root")
