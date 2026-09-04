# SPDX-License-Identifier: MIT
"""Import-safe FreeCAD command metadata for workbench registration tests."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandSpec:
    command_id: str
    menu_text: str
    module_name: str


PROJECT_COMMANDS = ("CE_NewProject", "CE_AddIOSignal", "CE_AddConnection")
LAYOUT_COMMANDS = ("CE_CreatePanel",)
VALIDATION_COMMANDS = ("CE_ValidateProject", "CE_PreviewMissingData")
EXPORT_COMMANDS = (
    "CE_ExportBOM",
    "CE_ExportCEProjectXML",
    "CE_ExportIOList",
    "CE_ExportMissingDataCSV",
    "CE_ExportConnectionSchedule",
)

COMMAND_SPECS = (
    CommandSpec("CE_NewProject", "New Controls Project", "new_project"),
    CommandSpec("CE_AddIOSignal", "Add I/O Signal", "add_io_signal"),
    CommandSpec("CE_AddConnection", "Add Connection Record", "add_connection"),
    CommandSpec("CE_CreatePanel", "Create Control Panel", "create_panel"),
    CommandSpec("CE_ValidateProject", "Validate Controls Project", "validate_project"),
    CommandSpec("CE_PreviewMissingData", "Preview Missing Data", "missing_data"),
    CommandSpec("CE_ExportBOM", "Export BOM", "export_bom"),
    CommandSpec("CE_ExportCEProjectXML", "Export CEProject XML", "export_ceproject_xml"),
    CommandSpec("CE_ExportIOList", "Export I/O List", "export_io_list"),
    CommandSpec("CE_ExportMissingDataCSV", "Export Missing Data CSV", "export_missing_data_csv"),
    CommandSpec("CE_ExportConnectionSchedule", "Export Connection Schedule", "export_connection_schedule"),
)


def all_command_ids() -> tuple[str, ...]:
    return tuple(spec.command_id for spec in COMMAND_SPECS)


def command_menu_text(command_id: str) -> str:
    for spec in COMMAND_SPECS:
        if spec.command_id == command_id:
            return spec.menu_text
    raise KeyError(command_id)
