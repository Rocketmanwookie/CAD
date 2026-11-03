# SPDX-License-Identifier: MIT
"""Project-root ownership and deterministic artifact destinations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


DEFAULT_WORKSPACE_PARENT_NAME = "ControlForgeCAD Projects"

_DIRECTORY_LAYOUT = (
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
)

_EXPORT_DIRECTORIES = {
    "bom": "exports/bom",
    "io": "exports/io",
    "schedules": "exports/schedules",
    "reports": "exports/reports",
    "package": "exports/package",
}


class ProjectWorkspaceError(ValueError):
    """Raised when a requested workspace or artifact destination is unsafe."""


@dataclass(frozen=True)
class ProjectWorkspace:
    """The one on-disk home for one controls project."""

    root: Path
    project_name: str

    @property
    def fcstd_path(self) -> Path:
        return self.root / f"{self.project_name}.FCStd"

    @property
    def ceproject_xml_path(self) -> Path:
        return self.root / f"{self.project_name}.ceproject.xml"

    @property
    def directories(self) -> tuple[Path, ...]:
        return tuple(self.root / relative_path for relative_path in _DIRECTORY_LAYOUT)


def default_workspace_parent(documents_directory: Path) -> Path:
    """Return the suggested parent; creation remains an explicit user action."""

    return Path(documents_directory) / DEFAULT_WORKSPACE_PARENT_NAME


def _validated_project_name(project_name: str) -> str:
    normalized = str(project_name or "").strip()
    if not normalized or normalized in {".", ".."} or "/" in normalized or "\\" in normalized:
        raise ProjectWorkspaceError("A project name must be a non-empty single folder name.")
    return normalized


def create_project_workspace(parent: Path, project_name: str) -> ProjectWorkspace:
    """Create the fixed tree without creating or overwriting project artifacts."""

    clean_name = _validated_project_name(project_name)
    root = Path(parent).expanduser() / clean_name
    root.mkdir(parents=True, exist_ok=True)
    workspace = ProjectWorkspace(root=root, project_name=clean_name)
    for directory in workspace.directories:
        directory.mkdir(parents=True, exist_ok=True)
    return workspace


def export_path(workspace: ProjectWorkspace, category: str, filename: str) -> Path:
    """Return a safe output path inside one named project export category."""

    relative_directory = _EXPORT_DIRECTORIES.get(str(category or ""))
    if relative_directory is None:
        raise ProjectWorkspaceError(f"Unknown export category {category!r}.")
    clean_filename = str(filename or "")
    if not clean_filename or Path(clean_filename).name != clean_filename:
        raise ProjectWorkspaceError("An export filename must not contain a path.")
    return workspace.root / relative_directory / clean_filename
