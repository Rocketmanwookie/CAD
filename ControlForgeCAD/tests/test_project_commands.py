# SPDX-License-Identifier: MIT

from types import SimpleNamespace

import pytest

from controls_wb.commands.export_ceproject_xml import ceproject_xml_for_objects
from controls_wb.commands.missing_data import format_missing_data_rows, missing_data_rows_for_objects, project_objects
import controls_wb.commands.new_project as new_project_module


def _project_object():
    return SimpleNamespace(
        ProjectId="CE-PROJECT-001",
        ProjectName="Controls Project",
        SchemaVersion="0.1.0",
        Deliverables=["ioList"],
        PlcPlatformStatus="Requested",
        SensorCountStatus="Requested",
    )


def test_project_objects_finds_intake_payloads_only():
    project = _project_object()

    assert project_objects([SimpleNamespace(Tag="M101"), project]) == [project]


def test_missing_data_command_helpers_format_project_rows():
    lines = format_missing_data_rows(missing_data_rows_for_objects([_project_object()]))

    assert any("controls.plcPlatform [missing_response]" in line for line in lines)
    assert any("Ask Controls lead" in line for line in lines)


def test_missing_data_command_helpers_report_missing_project():
    assert format_missing_data_rows(missing_data_rows_for_objects([])) == [
        "INFO: No controls project intake object found."
    ]


def test_ceproject_xml_command_helper_exports_first_project_object():
    xml_text = ceproject_xml_for_objects([_project_object()])

    assert 'projectId="CE-PROJECT-001"' in xml_text
    assert "<Name>Controls Project</Name>" in xml_text
    assert 'fieldId="controls.plcPlatform"' in xml_text


def test_ceproject_xml_command_helper_requires_project_object():
    with pytest.raises(ValueError, match="No controls project intake object"):
        ceproject_xml_for_objects([SimpleNamespace(Tag="M101")])


def test_new_project_command_asks_for_a_workspace_only_when_project_has_no_root(monkeypatch):
    project = SimpleNamespace(ProjectName="Controls Project", ProjectRoot="")
    document = SimpleNamespace(recompute=lambda: None)
    app = SimpleNamespace(ActiveDocument=document, Console=SimpleNamespace(PrintMessage=lambda *_: None))
    selected = []

    monkeypatch.setattr(new_project_module, "App", app)
    monkeypatch.setattr(new_project_module, "Gui", None)
    monkeypatch.setattr(new_project_module, "show_project_intake_dialog", lambda *_args, **_kwargs: project)
    monkeypatch.setattr(
        new_project_module,
        "_select_and_bind_workspace",
        lambda selected_project, _parent: selected.append(selected_project),
        raising=False,
    )

    new_project_module.NewProjectCommand().Activated()

    assert selected == [project]
