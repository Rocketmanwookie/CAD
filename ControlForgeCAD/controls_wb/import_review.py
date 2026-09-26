# SPDX-License-Identifier: MIT
"""Stage supported project imports for explicit review before document mutation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from controls_wb.ceproject_xml import parse_ceproject_xml
from controls_wb.gui.project_intake import (
    apply_form_values_to_project,
    ceproject_import_record,
    form_values_from_ceproject_xml,
    form_values_from_project,
    form_values_from_project_setup_text,
)


class ImportReviewError(ValueError):
    """Raised when an import cannot be staged or lacks explicit approval."""


@dataclass(frozen=True)
class ImportCandidate:
    """One changed, reviewable intake value proposed by an imported file."""

    key: str
    category: str
    current_value: str
    proposed_value: str


@dataclass(frozen=True)
class StagedProjectImport:
    """Read-only import preview produced by one supported source file."""

    source_path: str
    source_format: str
    source_text: str
    values: dict[str, object]
    candidates: tuple[ImportCandidate, ...]
    warnings: tuple[str, ...] = ()


_CATEGORY_BY_KEY = {
    "ProjectName": "Project",
    "Customer": "Project",
    "SiteLocation": "Project",
    "Deliverables": "Project",
    "PlcMake": "PLC / I/O",
    "PlcLine": "PLC / I/O",
    "PlcCPU": "PLC / I/O",
    "DICount": "PLC / I/O",
    "DOCount": "PLC / I/O",
    "AICount": "PLC / I/O",
    "AOCount": "PLC / I/O",
    "IOAccessories": "PLC / I/O",
    "EthernetAdapter": "PLC / I/O",
    "ExpansionPowerSupply": "PLC / I/O",
    "CommunicationProtocols": "PLC / I/O",
    "PowerConfiguration": "Power",
    "ControlledLoads": "Power",
    "EnclosureRatings": "Enclosure",
}


def stage_project_import(
    source_text: str | bytes, source_path: str = "", project: object | None = None
) -> StagedProjectImport:
    """Parse supported CEProject XML or setup YAML/UML without mutating ``project``."""

    text = source_text.decode("utf-8") if isinstance(source_text, bytes) else str(source_text)
    suffix = Path(source_path).suffix.lower()
    if suffix == ".xml" or text.lstrip().startswith("<"):
        source_format = "ceproject-xml"
        values: dict[str, object] = dict(form_values_from_ceproject_xml(text))
        document = parse_ceproject_xml(text)
        warnings = (
            (f"{len(document.connection_paths)} typed connection path(s) were detected but are not applied in phase 1.",)
            if document.connection_paths
            else ()
        )
    else:
        source_format = "uml" if suffix in {".uml", ".puml", ".plantuml"} else (
            "yaml" if suffix in {".yaml", ".yml"} else "auto"
        )
        setup_values = form_values_from_project_setup_text(text, source_format)
        values = {key: value for key, value in setup_values.items() if key != "ImportWarnings"}
        warnings = tuple(str(item) for item in setup_values.get("ImportWarnings", []) or [])

    current = form_values_from_project(project)
    candidates = []
    for key, proposed in values.items():
        if key not in _CATEGORY_BY_KEY:
            continue
        proposed_value = _display_value(proposed)
        current_value = _display_value(current.get(key, ""))
        if proposed_value != current_value:
            candidates.append(
                ImportCandidate(key, _CATEGORY_BY_KEY[key], current_value, proposed_value)
            )
    return StagedProjectImport(
        source_path=source_path,
        source_format=source_format,
        source_text=text,
        values=values,
        candidates=tuple(sorted(candidates, key=lambda item: (item.category, item.key))),
        warnings=warnings,
    )


def apply_approved_project_import(
    project: object, staged: StagedProjectImport, approved_keys: set[str] | frozenset[str]
) -> object:
    """Apply only explicitly approved staged candidates to an existing project.

    The caller owns the FreeCAD document transaction.  This function validates
    all approvals before writing, so an unapproved or unknown item cannot be
    silently imported.
    """

    available_keys = {candidate.key for candidate in staged.candidates}
    approved = {str(key) for key in approved_keys}
    if not approved:
        raise ImportReviewError("Select at least one staged item to approve before applying an import.")
    unknown = approved - available_keys
    if unknown:
        raise ImportReviewError("Import approval contains fields that were not staged: " + ", ".join(sorted(unknown)))

    values = form_values_from_project(project)
    for key in approved:
        values[key] = _display_value(staged.values[key])
    if staged.source_format == "ceproject-xml":
        values["CEProjectImportRecord"] = ceproject_import_record(staged.source_text, staged.source_path)
    return apply_form_values_to_project(project, values)


def _display_value(value: object) -> str:
    if isinstance(value, (list, tuple, set)):
        return ", ".join(str(item).strip() for item in value if str(item).strip())
    return str(value or "").strip()
