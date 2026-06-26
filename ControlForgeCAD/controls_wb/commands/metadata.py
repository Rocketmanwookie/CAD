# SPDX-License-Identifier: MIT
"""Import-safe FreeCAD command metadata for workbench registration tests."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandSpec:
    command_id: str
    menu_text: str
    module_name: str


PROJECT_COMMANDS = ("CE_NewProject",)
LAYOUT_COMMANDS = ("CE_CreatePanel",)
VALIDATION_COMMANDS = ("CE_ValidateProject", "CE_PreviewMissingData")
EXPORT_COMMANDS = ("CE_ExportBOM", "CE_ExportCEProjectXML")

COMMAND_SPECS = (
    CommandSpec("CE_NewProject", "New Controls Project", "new_project"),
    CommandSpec("CE_CreatePanel", "Create Control Panel", "create_panel"),
    CommandSpec("CE_ValidateProject", "Validate Controls Project", "validate_project"),
    CommandSpec("CE_PreviewMissingData", "Preview Missing Data", "missing_data"),
    CommandSpec("CE_ExportBOM", "Export BOM", "export_bom"),
    CommandSpec("CE_ExportCEProjectXML", "Export CEProject XML", "export_ceproject_xml"),
)


def all_command_ids() -> tuple[str, ...]:
    return tuple(spec.command_id for spec in COMMAND_SPECS)


def command_menu_text(command_id: str) -> str:
    for spec in COMMAND_SPECS:
        if spec.command_id == command_id:
            return spec.menu_text
    raise KeyError(command_id)
