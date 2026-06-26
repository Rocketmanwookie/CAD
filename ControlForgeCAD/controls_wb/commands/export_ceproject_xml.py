# SPDX-License-Identifier: MIT
"""Export CEProject XML from a controls project intake object."""

from pathlib import Path

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.ceproject_xml import ceproject_to_xml
from controls_wb.commands.missing_data import project_objects


def ceproject_xml_for_objects(objects) -> str:
    projects = project_objects(objects)
    if not projects:
        raise ValueError("No controls project intake object found.")
    return ceproject_to_xml(projects[0])


class ExportCEProjectXmlCommand:
    def GetResources(self):
        return {
            "MenuText": "Export CEProject XML",
            "ToolTip": "Export the active controls project intake object to CEProject XML.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        try:
            xml_text = ceproject_xml_for_objects(App.ActiveDocument.Objects)
        except ValueError as exc:
            App.Console.PrintWarning(f"{exc}\n")
            return
        output_path = Path.home() / "integracab_ceproject.xml"
        output_path.write_text(xml_text, encoding="utf-8")
        App.Console.PrintMessage(f"CEProject XML exported to {output_path}\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_ExportCEProjectXML", ExportCEProjectXmlCommand())
