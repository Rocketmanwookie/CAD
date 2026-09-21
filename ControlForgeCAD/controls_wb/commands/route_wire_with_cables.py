# SPDX-License-Identifier: MIT
"""Create or synchronize a CE wire's optional Cables Workbench route."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover - exercised by metadata tests without FreeCAD
    App = None
    Gui = None

from controls_wb.cables_routing import cables_available, create_or_update_cables_route, route_link_is_identity_safe, route_points_from_cables, route_points_from_ce_wire
from controls_wb.freecad_transactions import document_transaction
from controls_wb.model.electrical import update_wire_route_object
from controls_wb.route_capture import selected_ce_wire


class RouteWireWithCablesCommand:
    def GetResources(self):
        return {
            "MenuText": "Route CE Wire with Cables",
            "ToolTip": "Create or synchronize the selected CE wire's Cables WireFlex physical route.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        try:
            wire = selected_ce_wire(Gui.Selection.getSelectionEx())
            with document_transaction(App.ActiveDocument, "Route CE wire with Cables"):
                linked_route = getattr(wire, "CablesRouteObject", None)
                if route_link_is_identity_safe(wire, linked_route):
                    update_wire_route_object(wire, route_points_from_cables(linked_route))
                    message = "Synchronized"
                else:
                    route = route_points_from_ce_wire(wire)
                    create_or_update_cables_route(wire, route)
                    message = "Created"
                App.ActiveDocument.recompute()
            App.Console.PrintMessage(f"{message} Cables route for {wire.WireTag} ({wire.CalculatedLength}).\n")
        except (ImportError, ModuleNotFoundError):
            App.Console.PrintWarning("FreeCAD Cables workbench is not installed; the CE_Wire Part-polyline remains available.\n")
        except (RuntimeError, ValueError) as exc:
            App.Console.PrintWarning(f"{exc} Route was not changed.\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None and cables_available()


if Gui is not None:
    Gui.addCommand("CE_RouteWireWithCables", RouteWireWithCablesCommand())
