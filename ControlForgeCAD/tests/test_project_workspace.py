# SPDX-License-Identifier: MIT

from pathlib import Path

import pytest

from controls_wb.project_workspace import (
    ProjectWorkspaceError,
    create_project_workspace,
    export_path,
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


@pytest.mark.parametrize("category", ["", "../../outside", "unknown"])
def test_export_path_rejects_unknown_or_unsafe_categories(tmp_path, category):
    workspace = create_project_workspace(tmp_path, "Controls Project")

    with pytest.raises(ProjectWorkspaceError, match="export category"):
        export_path(workspace, category, "report.csv")
