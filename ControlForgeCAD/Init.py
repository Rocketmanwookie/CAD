# SPDX-License-Identifier: MIT
"""FreeCAD non-GUI initialization for ControlForgeCAD."""

try:
    import FreeCAD as App
    App.Console.PrintMessage("Loading ControlForgeCAD core\n")
except Exception:
    # Allows static tests outside FreeCAD.
    pass
