# SPDX-License-Identifier: MIT

import importlib

from controls_wb.commands.metadata import (
    COMMAND_SPECS,
    EXPORT_COMMANDS,
    LAYOUT_COMMANDS,
    PROJECT_COMMANDS,
    VALIDATION_COMMANDS,
    all_command_ids,
    command_menu_text,
)


def test_command_metadata_matches_expected_workbench_commands():
    assert all_command_ids() == (
        "CE_NewProject",
        "CE_CreatePanel",
        "CE_ValidateProject",
        "CE_PreviewMissingData",
        "CE_ExportBOM",
        "CE_ExportCEProjectXML",
    )
    assert PROJECT_COMMANDS == ("CE_NewProject",)
    assert LAYOUT_COMMANDS == ("CE_CreatePanel",)
    assert VALIDATION_COMMANDS == ("CE_ValidateProject", "CE_PreviewMissingData")
    assert EXPORT_COMMANDS == ("CE_ExportBOM", "CE_ExportCEProjectXML")


def test_command_metadata_exposes_menu_text_for_manual_validation_docs():
    assert command_menu_text("CE_NewProject") == "New Controls Project"
    assert command_menu_text("CE_PreviewMissingData") == "Preview Missing Data"
    assert command_menu_text("CE_ExportCEProjectXML") == "Export CEProject XML"


def test_command_modules_are_import_safe_without_freecad():
    for spec in COMMAND_SPECS:
        module = importlib.import_module(f"controls_wb.commands.{spec.module_name}")
        assert module.Gui is None


def test_freecad_init_files_import_without_freecad():
    init_module = importlib.import_module("Init")
    init_gui_module = importlib.import_module("InitGui")

    assert init_module is not None
    assert init_gui_module.Gui is None
