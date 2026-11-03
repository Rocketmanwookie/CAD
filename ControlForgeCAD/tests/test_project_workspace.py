# SPDX-License-Identifier: MIT

from pathlib import Path

import pytest

from controls_wb.project_workspace import (
    ProjectWorkspaceError,
    bind_project_workspace,
    create_project_workspace,
    export_destination_for_objects,
    export_path,
    load_workspace_parent,
    project_workspace_for_objects,
    save_workspace_parent,
)


def test_create_project_workspace_builds_the_agreed_project_tree(tmp_path):
    workspace = create_project_workspace(tmp_path, "Controls Project")

    assert workspace.root == tmp_path / "Controls Project"
    assert workspace.fcstd_path == tmp_path / "Controls Project" / "Controls Project.FCStd"
    assert workspace.ceproject_xml_path == tmp_path / "Controls Project" / "Controls Project.ceproject.xml"
    assert {path.relative_to(workspace.root).as_posix() for path in workspace.directories} == {
        "imports/cad/vendor",
        "imports/cad/customer",
        "imports/cad/reference",
        "imports/documents",
        "imports/data",
        "exports/bom",
        "exports/io",
        "exports/schedules",
        "exports/reports",
        "exports/package",
        "evidence/screenshots",
        "evidence/report-view",
        "evidence/acceptance",
    }
    assert all(path.is_dir() for path in workspace.directories)


@pytest.mark.parametrize("project_name", ["", "   ", "../outside", "project/name", "project\\name"])
def test_create_project_workspace_rejects_an_unsafe_project_name(tmp_path, project_name):
    with pytest.raises(ProjectWorkspaceError, match="project name"):
        create_project_workspace(tmp_path, project_name)


def test_create_project_workspace_is_idempotent_without_creating_artifacts(tmp_path):
    first = create_project_workspace(tmp_path, "Controls Project")
    first.fcstd_path.write_text("saved FreeCAD artifact", encoding="utf-8")

    second = create_project_workspace(tmp_path, "Controls Project")

    assert second == first
    assert second.fcstd_path.read_text(encoding="utf-8") == "saved FreeCAD artifact"
    assert not second.ceproject_xml_path.exists()


def test_export_path_uses_the_named_category_below_the_project_root(tmp_path):
    workspace = create_project_workspace(tmp_path, "Controls Project")

    target = export_path(workspace, "schedules", "integracad_wiring_schedule.csv")

    assert target == tmp_path / "Controls Project" / "exports/schedules/integracad_wiring_schedule.csv"
    assert target.is_relative_to(workspace.root)


def test_bind_project_workspace_persists_the_parent_and_root_on_the_project(tmp_path):
    project = type("Project", (), {"ProjectId": "CE-PROJECT-001", "ProjectName": "Controls Project"})()

    workspace = bind_project_workspace(project, tmp_path)

    assert project.WorkspaceParent == str(tmp_path)
    assert project.ProjectRoot == str(tmp_path / "Controls Project")
    assert workspace.root == Path(project.ProjectRoot)


def test_project_workspace_for_objects_uses_the_persisted_project_root(tmp_path):
    project = type("Project", (), {"ProjectId": "CE-PROJECT-001", "ProjectName": "Controls Project"})()
    bind_project_workspace(project, tmp_path)

    workspace = project_workspace_for_objects([object(), project])

    assert workspace.root == tmp_path / "Controls Project"


def test_project_workspace_for_objects_keeps_the_original_root_after_a_display_name_change(tmp_path):
    project = type("Project", (), {"ProjectId": "CE-PROJECT-001", "ProjectName": "Controls Project"})()
    bind_project_workspace(project, tmp_path)
    project.ProjectName = "Controls Project Revised"

    workspace = project_workspace_for_objects([project])

    assert workspace.root == tmp_path / "Controls Project"


def test_project_workspace_for_objects_requires_a_configured_project_root():
    project = type("Project", (), {"ProjectId": "CE-PROJECT-001", "ProjectName": "Controls Project", "ProjectRoot": ""})()

    with pytest.raises(ProjectWorkspaceError, match="project workspace"):
        project_workspace_for_objects([project])


def test_export_destination_for_objects_uses_the_project_workspace(tmp_path):
    project = type("Project", (), {"ProjectId": "CE-PROJECT-001", "ProjectName": "Controls Project"})()
    bind_project_workspace(project, tmp_path)

    target = export_destination_for_objects([project], "bom", "controlforgecad_bom.csv")

    assert target == tmp_path / "Controls Project" / "exports/bom/controlforgecad_bom.csv"


def test_workspace_parent_preference_uses_default_then_persists_selection(tmp_path):
    class Parameters:
        value = ""

        def GetString(self, _name, fallback):
            return self.value or fallback

        def SetString(self, _name, value):
            self.value = value

    parameters = Parameters()
    app = type("App", (), {"ParamGet": lambda _self, _path: parameters})()
    documents = tmp_path / "Documents"

    assert load_workspace_parent(app, documents) == documents / "ControlForgeCAD Projects"
    save_workspace_parent(app, tmp_path / "Projects")
    assert load_workspace_parent(app, documents) == tmp_path / "Projects"


@pytest.mark.parametrize("category", ["", "../../outside", "unknown"])
def test_export_path_rejects_unknown_or_unsafe_categories(tmp_path, category):
    workspace = create_project_workspace(tmp_path, "Controls Project")

    with pytest.raises(ProjectWorkspaceError, match="export category"):
        export_path(workspace, category, "report.csv")
