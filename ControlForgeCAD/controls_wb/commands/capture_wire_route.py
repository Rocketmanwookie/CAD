# SPDX-License-Identifier: MIT
"""Capture a typed wire route from selected FreeCAD geometry."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.freecad_transactions import document_transaction
from controls_wb.model.electrical import update_wire_route_object
from controls_wb.route_capture import selected_wire_and_route_points


class CaptureWireRouteCommand:
    def GetResources(self):
        return {
            "MenuText": "Capture Wire Route from Geometry",
            "ToolTip": "Select one CE wire and route geometry to persist its ordered 3D route.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        try:
            wire, route = selected_wire_and_route_points(Gui.Selection.getSelectionEx())
            with document_transaction(App.ActiveDocument, "Capture wire route"):
                update_wire_route_object(wire, route)
                App.ActiveDocument.recompute()
            App.Console.PrintMessage(
                f"Captured {len(route)} route points for {wire.WireTag} ({wire.CalculatedLength}).\n"
            )
        except (RuntimeError, ValueError) as exc:
            App.Console.PrintWarning(f"{exc} Route was not changed.\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_CaptureWireRoute", CaptureWireRouteCommand())
