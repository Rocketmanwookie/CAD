# SPDX-License-Identifier: MIT

import importlib
import sys
import types
from pathlib import Path
from xml.etree import ElementTree as ET

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
        "CE_AllocatePLCIO",
        "CE_AddConnection",
        "CE_AddElectricalPath",
        "CE_EditElectricalPath",
        "CE_CaptureWireRoute",
        "CE_RouteWireWithCables",
        "CE_CreatePanel",
        "CE_ValidateProject",
        "CE_PreviewMissingData",
        "CE_ExportBOM",
        "CE_ExportCEProjectXML",
        "CE_ExportIOList",
        "CE_ExportMissingDataCSV",
        "CE_ExportConnectionSchedule",
        "CE_ExportElectricalSchedules",
        "CE_ExportTerminalPlan",
    )
    assert PROJECT_COMMANDS == (
        "CE_NewProject", "CE_AddIOSignal", "CE_AllocatePLCIO", "CE_AddConnection",
        "CE_AddElectricalPath", "CE_EditElectricalPath", "CE_CaptureWireRoute", "CE_RouteWireWithCables",
    )
    assert LAYOUT_COMMANDS == ("CE_CreatePanel",)
    assert VALIDATION_COMMANDS == ("CE_ValidateProject", "CE_PreviewMissingData")
    assert EXPORT_COMMANDS == (
        "CE_ExportBOM",
        "CE_ExportCEProjectXML",
        "CE_ExportIOList",
        "CE_ExportMissingDataCSV",
        "CE_ExportConnectionSchedule",
        "CE_ExportElectricalSchedules",
        "CE_ExportTerminalPlan",
    )


def test_command_metadata_exposes_menu_text_for_manual_validation_docs():
    assert command_menu_text("CE_NewProject") == "New Controls Project"
    assert command_menu_text("CE_AddIOSignal") == "Add I/O Signal"
    assert command_menu_text("CE_AllocatePLCIO") == "Allocate PLC I/O"
    assert command_menu_text("CE_AddConnection") == "Add Connection Record"
    assert command_menu_text("CE_AddElectricalPath") == "Add Electrical Path"
    assert command_menu_text("CE_EditElectricalPath") == "Edit Electrical Path"
    assert command_menu_text("CE_CaptureWireRoute") == "Capture Wire Route from Geometry"
    assert command_menu_text("CE_RouteWireWithCables") == "Route CE Wire with Cables"
    assert command_menu_text("CE_PreviewMissingData") == "Preview Missing Data"
    assert command_menu_text("CE_ExportCEProjectXML") == "Export CEProject XML"
    assert command_menu_text("CE_ExportIOList") == "Export I/O List"
    assert command_menu_text("CE_ExportMissingDataCSV") == "Export Missing Data CSV"
    assert command_menu_text("CE_ExportConnectionSchedule") == "Export Connection Schedule"
    assert command_menu_text("CE_ExportElectricalSchedules") == "Export Electrical Schedules"
    assert command_menu_text("CE_ExportTerminalPlan") == "Export Terminal Plan"


def test_command_modules_are_import_safe_without_freecad():
    for spec in COMMAND_SPECS:
        module = importlib.import_module(f"controls_wb.commands.{spec.module_name}")
        assert module.Gui is None


def test_freecad_init_files_import_without_freecad():
    init_module = importlib.import_module("Init")
    init_gui_module = importlib.import_module("InitGui")

    assert init_module is not None
    assert init_gui_module.Gui is None


def test_package_manifest_has_addon_manager_metadata():
    root = Path(__file__).resolve().parents[1]
    package = ET.parse(root / "package.xml").getroot()
    namespace = {"fc": "https://wiki.freecad.org/Package_Metadata"}

    assert package.tag == "{https://wiki.freecad.org/Package_Metadata}package"
    assert package.findtext("fc:name", namespaces=namespace) == "ControlForgeCAD"
    assert package.findtext("fc:freecadmin", namespaces=namespace) == "1.0.0"
    assert package.findtext("fc:content/fc:workbench/fc:classname", namespaces=namespace) == (
        "ControlsEngineeringWorkbench"
    )
    icon = package.findtext("fc:icon", namespaces=namespace)
    assert icon == "Resources/Icons/ControlForgeCAD.svg"
    assert (root / icon).is_file()

    repository = package.find("fc:url[@type='repository']", namespace)
    assert repository is not None
    assert repository.get("branch") == "controlforgecad"


def test_workbench_root_helper_falls_back_to_controls_package_without_file():
    root = workbench_root_from_module_globals({"__spec__": types.SimpleNamespace(origin=None)})

    assert Path(root).name == "ControlForgeCAD"
    assert (Path(root) / "controls_wb").is_dir()


def test_workbench_root_helper_ignores_synthetic_loader_file():
    root = workbench_root_from_module_globals({"__file__": "/home/example/InitGui.py"})

    assert Path(root).name == "ControlForgeCAD"
    assert (Path(root) / "Resources" / "Icons" / "ControlForgeCAD.svg").is_file()


def test_init_gui_icon_ignores_synthetic_loader_file(monkeypatch):
    fake_gui = types.SimpleNamespace(addWorkbench=lambda workbench: None)
    monkeypatch.setitem(sys.modules, "FreeCADGui", fake_gui)

    class FakeWorkbench:
        pass

    init_gui_path = Path(__file__).resolve().parents[1] / "InitGui.py"
    module_globals = {
        "__name__": "InitGui_synthetic_file_test",
        "__file__": "/home/example/InitGui.py",
        "__builtins__": __builtins__,
        "Workbench": FakeWorkbench,
    }

    exec(compile(init_gui_path.read_text(), str(init_gui_path), "exec"), module_globals)

    assert module_globals["ControlsEngineeringWorkbench"].Icon == str(
        init_gui_path.parent / "Resources" / "Icons" / "ControlForgeCAD.svg"
    )


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

    assert icon_paths == [str(init_gui_path.parent / "Resources" / "Icons")]
