# SPDX-License-Identifier: MIT
"""Import-safe FreeCAD command metadata for workbench registration tests."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandSpec:
    command_id: str
    menu_text: str
    module_name: str


PROJECT_COMMANDS = (
    "CE_NewProject", "CE_AddIOSignal", "CE_AllocatePLCIO", "CE_AddConnection",
    "CE_AddElectricalPath", "CE_EditElectricalPath", "CE_CaptureWireRoute", "CE_RouteWireWithCables",
)
LAYOUT_COMMANDS = ("CE_CreatePanel",)
VALIDATION_COMMANDS = ("CE_ValidateProject", "CE_PreviewMissingData")
EXPORT_COMMANDS = (
    "CE_ExportBOM",
    "CE_ExportCEProjectXML",
    "CE_ExportIOList",
    "CE_ExportMissingDataCSV",
    "CE_ExportConnectionSchedule",
    "CE_ExportElectricalSchedules",
    "CE_ExportTerminalPlan",
)

COMMAND_SPECS = (
    CommandSpec("CE_NewProject", "New Controls Project", "new_project"),
    CommandSpec("CE_AddIOSignal", "Add I/O Signal", "add_io_signal"),
    CommandSpec("CE_AllocatePLCIO", "Allocate PLC I/O", "allocate_plc_io"),
    CommandSpec("CE_AddConnection", "Add Connection Record", "add_connection"),
    CommandSpec("CE_AddElectricalPath", "Add Electrical Path", "add_electrical_path"),
    CommandSpec("CE_EditElectricalPath", "Edit Electrical Path", "edit_electrical_path"),
    CommandSpec("CE_CaptureWireRoute", "Capture Wire Route from Geometry", "capture_wire_route"),
    CommandSpec("CE_RouteWireWithCables", "Route CE Wire with Cables", "route_wire_with_cables"),
    CommandSpec("CE_CreatePanel", "Create Control Panel", "create_panel"),
    CommandSpec("CE_ValidateProject", "Validate Controls Project", "validate_project"),
    CommandSpec("CE_PreviewMissingData", "Preview Missing Data", "missing_data"),
    CommandSpec("CE_ExportBOM", "Export BOM", "export_bom"),
    CommandSpec("CE_ExportCEProjectXML", "Export CEProject XML", "export_ceproject_xml"),
    CommandSpec("CE_ExportIOList", "Export I/O List", "export_io_list"),
    CommandSpec("CE_ExportMissingDataCSV", "Export Missing Data CSV", "export_missing_data_csv"),
    CommandSpec("CE_ExportConnectionSchedule", "Export Connection Schedule", "export_connection_schedule"),
    CommandSpec("CE_ExportElectricalSchedules", "Export Electrical Schedules", "export_electrical_schedules"),
    CommandSpec("CE_ExportTerminalPlan", "Export Terminal Plan", "export_terminal_plan"),
)


def all_command_ids() -> tuple[str, ...]:
    return tuple(spec.command_id for spec in COMMAND_SPECS)


def command_menu_text(command_id: str) -> str:
    for spec in COMMAND_SPECS:
        if spec.command_id == command_id:
            return spec.menu_text
    raise KeyError(command_id)
