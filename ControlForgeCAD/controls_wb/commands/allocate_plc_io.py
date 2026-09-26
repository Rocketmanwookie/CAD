# SPDX-License-Identifier: MIT
"""Persist a complete catalog-backed PLC I/O allocation on the CE project."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.freecad_transactions import document_transaction
from controls_wb.io_list import persist_io_allocation_to_project
from controls_wb.model.layout import materialize_plc_allocation


def project_from_objects(objects):
    """Return the sole CE project in ``objects`` or raise an actionable error."""
    projects = [obj for obj in objects if hasattr(obj, "ProjectId") and hasattr(obj, "Deliverables")]
    if len(projects) != 1:
        raise ValueError("Allocate PLC I/O requires exactly one CE_Project in the active document.")
    return projects[0]


def persist_project_allocation(document):
    """Allocate and persist a document's only CE_Project atomically."""

    project = project_from_objects(getattr(document, "Objects", []) or [])
    with document_transaction(document, "Allocate PLC I/O"):
        # Allocation persistence and occurrence/link materialization are one
        # user-visible document operation: an aborted command cannot leave a
        # newly persisted mapping without its matching rack/channel objects.
        result = persist_io_allocation_to_project(project)
        # Lightweight unit-test and batch stubs may model only the persisted
        # project payload.  A real FreeCAD document always exposes addObject;
        # only it can host the occurrence graph.
        if callable(getattr(document, "addObject", None)):
            materialize_plc_allocation(document, project)
        recompute = getattr(document, "recompute", None)
        if callable(recompute):
            recompute()
    return result


class AllocatePLCIoCommand:
    """FreeCAD command boundary for atomic catalog allocation and occurrence creation."""
    def GetResources(self):
        return {
            "MenuText": "Allocate PLC I/O",
            "ToolTip": "Allocate selected PLC CPU and module channels, then persist the I/O mapping.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        try:
            result = persist_project_allocation(App.ActiveDocument)
        except ValueError as exc:
            App.Console.PrintWarning(f"PLC I/O allocation failed: {exc}\n")
            return
        App.Console.PrintMessage(
            f"Allocated {len(result.signals)} I/O signals across {len(result.modules)} PLC modules.\n"
        )

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_AllocatePLCIO", AllocatePLCIoCommand())
