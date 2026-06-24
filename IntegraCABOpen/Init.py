# SPDX-License-Identifier: MIT
"""FreeCAD non-GUI initialization for IntegraCAB Open."""

try:
    import FreeCAD as App
    App.Console.PrintMessage("Loading IntegraCAB Open core\n")
except Exception:
    # Allows static tests outside FreeCAD.
    pass
