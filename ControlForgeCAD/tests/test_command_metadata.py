# SPDX-License-Identifier: MIT

import importlib
import sys
import types
from pathlib import Path

from controls_wb.commands.metadata import (
    COMMAND_SPECS,
    EXPORT_COMMANDS,
    LAYOUT_COMMANDS,
    PROJECT_COMMANDS,
    VALIDATION_COMMANDS,
    all_command_ids,
    command_menu_text,
)
from controls_wb.freecad_paths import workbench_root_from_module_globals


def test_command_metadata_matches_expected_workbench_commands():
    assert all_command_ids() == (
        "CE_NewProject",
        "CE_AddIOSignal",
        "CE_CreatePanel",
        "CE_ValidateProject",
        "CE_PreviewMissingData",
        "CE_ExportBOM",
        "CE_ExportCEProjectXML",
        "CE_ExportIOList",
        "CE_ExportMissingDataCSV",
    )
    assert PROJECT_COMMANDS == ("CE_NewProject", "CE_AddIOSignal")
    assert LAYOUT_COMMANDS == ("CE_CreatePanel",)
    assert VALIDATION_COMMANDS == ("CE_ValidateProject", "CE_PreviewMissingData")
    assert EXPORT_COMMANDS == (
        "CE_ExportBOM",
        "CE_ExportCEProjectXML",
        "CE_ExportIOList",
        "CE_ExportMissingDataCSV",
    )


def test_command_metadata_exposes_menu_text_for_manual_validation_docs():
    assert command_menu_text("CE_NewProject") == "New Controls Project"
    assert command_menu_text("CE_AddIOSignal") == "Add I/O Signal"
    assert command_menu_text("CE_PreviewMissingData") == "Preview Missing Data"
    assert command_menu_text("CE_ExportCEProjectXML") == "Export CEProject XML"
    assert command_menu_text("CE_ExportIOList") == "Export I/O List"
    assert command_menu_text("CE_ExportMissingDataCSV") == "Export Missing Data CSV"


def test_command_modules_are_import_safe_without_freecad():
    for spec in COMMAND_SPECS:
        module = importlib.import_module(f"controls_wb.commands.{spec.module_name}")
        assert module.Gui is None


def test_freecad_init_files_import_without_freecad():
    init_module = importlib.import_module("Init")
    init_gui_module = importlib.import_module("InitGui")

    assert init_module is not None
    assert init_gui_module.Gui is None


def test_workbench_root_helper_falls_back_to_controls_package_without_file():
    root = workbench_root_from_module_globals({"__spec__": types.SimpleNamespace(origin=None)})

    assert Path(root).name == "ControlForgeCAD"
    assert (Path(root) / "controls_wb").is_dir()


def test_init_gui_initialize_without_file_uses_safe_workbench_root(monkeypatch):
    icon_paths = []
    workbenches = []
    fake_gui = types.SimpleNamespace(
        addIconPath=icon_paths.append,
        addWorkbench=workbenches.append,
    )
    fake_app = types.SimpleNamespace(
        Console=types.SimpleNamespace(PrintMessage=lambda message: None)
    )

    monkeypatch.setitem(sys.modules, "FreeCAD", fake_app)
    monkeypatch.setitem(sys.modules, "FreeCADGui", fake_gui)

    class FakeWorkbench:
        def appendToolbar(self, name, commands):
            pass

        def appendMenu(self, path, commands):
            pass

        def appendContextMenu(self, name, commands):
            pass

    init_gui_path = Path(__file__).resolve().parents[1] / "InitGui.py"
    module_globals = {
        "__name__": "InitGui_no_file_test",
        "__package__": "",
        "__spec__": types.SimpleNamespace(origin=None),
        "__builtins__": __builtins__,
        "Workbench": FakeWorkbench,
    }

    exec(compile(init_gui_path.read_text(), str(init_gui_path), "exec"), module_globals)
    workbenches[0].Initialize()

    assert icon_paths == [
        str(init_gui_path.parent / "controls_wb" / "resources" / "icons")
    ]
