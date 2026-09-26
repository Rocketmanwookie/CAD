# SPDX-License-Identifier: MIT
"""Stage supported project imports for explicit review before document mutation."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

from controls_wb.ceproject_xml import CEPROJECT_NAMESPACE, parse_ceproject_xml
from controls_wb.gui.project_intake import (
    apply_form_values_to_project,
    ceproject_import_record,
    form_values_from_ceproject_xml,
    form_values_from_project,
    form_values_from_project_setup_text,
    merge_ceproject_import_records,
    normalized_form_values,
)
from controls_wb.io_allocation import validate_io_allocations
from controls_wb.io_list import (
    IOSignal,
    deserialize_io_signal,
    explicit_io_signals_from_project,
    serialize_io_signal,
)
from controls_wb.allocation_reconciliation import preflight_reconciliation


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


@dataclass(frozen=True)
class IOImportDiagnostic:
    """One non-mutating finding raised while staging CEProject signal rows."""

    severity: str
    code: str
    candidate_id: str
    message: str


@dataclass(frozen=True)
class IOImportCandidate:
    """One explicit logical-I/O add or label update proposed by a CEProject signal."""

    candidate_id: str
    signal_id: str
    action: str
    current: IOSignal | None
    proposed: IOSignal | None


@dataclass(frozen=True)
class StagedIOImport:
    """Read-only CEProject logical-I/O review with a stale-state fingerprint."""

    source_path: str
    source_text: str
    current_signals: tuple[IOSignal, ...]
    candidates: tuple[IOImportCandidate, ...]
    diagnostics: tuple[IOImportDiagnostic, ...]
    fingerprint: str


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
    warnings = tuple(warnings) + _plc_catalog_staging_warnings(current, values)
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


def _plc_catalog_staging_warnings(
    current_values: dict[str, str], imported_values: dict[str, object]
) -> tuple[str, ...]:
    """Describe unsupported imported PLC selections before approval.

    The apply boundary still validates every approved item and never mutates on
    a rewrite.  This preview diagnostic makes the same incompatibility visible
    while the reviewer is choosing checkboxes, rather than only after Apply.
    """

    catalog_fields = {
        "PlcMake": "PLC make",
        "PlcLine": "PLC line",
        "PlcCPU": "PLC CPU",
        "EthernetAdapter": "Ethernet adapter",
        "ExpansionPowerSupply": "expansion power supply",
    }
    # Stage a partial file in the same context Apply will use: unchanged
    # project fields remain current rather than falling back to Siemens defaults.
    effective_values = dict(current_values)
    effective_values.update(
        {key: _display_value(value) for key, value in imported_values.items()}
    )
    normalized = normalized_form_values(effective_values)
    unsupported = [
        label
        for key, label in catalog_fields.items()
        if key in imported_values
        and str(normalized[key]) != _display_value(imported_values[key]).strip()
    ]
    if not unsupported:
        return ()
    return (
        "Imported PLC selections are not exact bundled-catalog values: "
        + ", ".join(unsupported)
        + ". They can be reviewed but cannot be applied; select a supported catalog combination.",
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
    _require_explicit_plc_dependency_approval(
        form_values_from_project(project), values, approved
    )
    if staged.source_format == "ceproject-xml":
        values["CEProjectImportRecord"] = ceproject_import_record(staged.source_text, staged.source_path)
    return apply_form_values_to_project(project, values)


def _require_explicit_plc_dependency_approval(
    current_values: dict[str, str], proposed_values: dict[str, str], approved: set[str]
) -> None:
    """Reject a partial PLC selection that normalization would silently alter.

    The intake form keeps make, line, CPU, compatible Ethernet, compatible
    expansion power, and the derived platform mutually consistent.  Import
    review must not use that normalization to change a dependent value the user
    did not approve.  A source therefore needs to offer and the user needs to
    approve every affected selectable value; the derived platform changes only
    after its make and line inputs were both explicitly approved.
    """

    normalized = normalized_form_values(proposed_values)
    current_normalized = normalized_form_values(current_values)
    protected = {
        "PlcLine": "PLC line",
        "PlcCPU": "PLC CPU",
        "EthernetAdapter": "Ethernet adapter",
        "ExpansionPowerSupply": "expansion power supply",
    }
    changed = [
        label
        for key, label in protected.items()
        if str(normalized[key]) != str(current_values.get(key, "")) and key not in approved
    ]
    if (
        str(normalized["PlcPlatform"]) != str(current_normalized["PlcPlatform"])
        and not {"PlcMake", "PlcLine"}.issubset(approved)
    ):
        changed.append("derived PLC platform")
    # Approval means accepting the exact catalog value displayed in the review,
    # not merely accepting a value that the intake normalizer can replace with a
    # default.  This is especially important when a source names a vendor/line
    # or CPU that is not represented by the bundled catalog: accepting all of
    # those rows must fail, rather than silently storing a different supported
    # vendor/line/CPU combination.
    approved_catalog_values = {
        "PlcMake": "PLC make",
        "PlcLine": "PLC line",
        **protected,
    }
    rewritten = [
        label
        for key, label in approved_catalog_values.items()
        if key in approved
        and str(normalized[key]) != str(proposed_values.get(key, "")).strip()
    ]
    if rewritten:
        raise ImportReviewError(
            "Import approval contains PLC selections that are not compatible with "
            "the bundled catalog: " + ", ".join(rewritten) + ". "
            "No project values were changed; select a supported catalog combination instead."
        )
    if changed:
        raise ImportReviewError(
            "Import approval would normalize unapproved PLC fields: " + ", ".join(changed) + ". "
            "Approve a complete compatible PLC selection instead."
        )


_IO_TYPE_BY_CEPROJECT_TYPE = {
    "DI": "digital_input",
    "DO": "digital_output",
    "AI": "analog_input",
    "AO": "analog_output",
}


def stage_ceproject_io_import(
    source_text: str | bytes, source_path: str = "", current_signals: Iterable[IOSignal] = ()
) -> StagedIOImport:
    """Stage existing CEProject ``Signals`` as logical I/O rows without mutation.

    CEProject's ``plcAddress`` and ``terminal`` attributes are deliberately not
    imported.  Catalog allocation owns PLC terminal/address and physical
    rack/slot/channel coordinates in ControlForgeCAD.
    """

    text = source_text.decode("utf-8") if isinstance(source_text, bytes) else str(source_text)
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        raise ImportReviewError(f"Invalid CEProject XML: {exc}") from exc
    if root.tag != f"{{{CEPROJECT_NAMESPACE}}}CEProject":
        raise ImportReviewError("I/O review supports CEProject XML only.")

    current = tuple(current_signals)
    diagnostics: list[IOImportDiagnostic] = []
    current_by_tag: dict[str, IOSignal] = {}
    for signal in current:
        if signal.tag in current_by_tag:
            diagnostics.append(IOImportDiagnostic(
                "ERROR", "duplicate_current_tag", "", f"Current project has duplicate I/O tag {signal.tag!r}."
            ))
        current_by_tag[signal.tag] = signal

    candidates: list[IOImportCandidate] = []
    seen_ids: set[str] = set()
    seen_tags: set[str] = set()
    for element in root.iter():
        if element.tag != f"{{{CEPROJECT_NAMESPACE}}}Signal":
            continue
        signal_id = str(element.attrib.get("signalId", "")).strip()
        tag = str(element.attrib.get("tag", "")).strip()
        candidate_id = f"io:{signal_id}" if signal_id else ""
        raw_type = str(element.attrib.get("type", "")).strip().upper()
        if not signal_id:
            diagnostics.append(IOImportDiagnostic("ERROR", "missing_signal_id", "", "CEProject Signal is missing signalId."))
            continue
        if signal_id in seen_ids:
            diagnostics.append(IOImportDiagnostic("ERROR", "duplicate_signal_id", candidate_id, f"CEProject repeats signalId {signal_id!r}."))
            continue
        seen_ids.add(signal_id)
        if not tag:
            diagnostics.append(IOImportDiagnostic("ERROR", "missing_signal_tag", candidate_id, f"CEProject Signal {signal_id!r} is missing tag."))
            continue
        if tag in seen_tags:
            diagnostics.append(IOImportDiagnostic("ERROR", "duplicate_import_tag", candidate_id, f"CEProject repeats signal tag {tag!r}."))
            continue
        seen_tags.add(tag)
        signal_type = _IO_TYPE_BY_CEPROJECT_TYPE.get(raw_type)
        if signal_type is None:
            diagnostics.append(IOImportDiagnostic(
                "ERROR", "unsupported_ceproject_signal_type", candidate_id,
                f"CEProject Signal {tag!r} type {raw_type!r} cannot be allocated as supported PLC I/O."
            ))
            candidates.append(IOImportCandidate(candidate_id, signal_id, "conflict", current_by_tag.get(tag), None))
            continue
        for attribute in ("plcAddress", "terminal"):
            if str(element.attrib.get(attribute, "")).strip():
                diagnostics.append(IOImportDiagnostic(
                    "WARNING", "imported_coordinate_ignored", candidate_id,
                    f"CEProject Signal {tag!r} {attribute} is review-only and will not be imported."
                ))
        label = str(element.attrib.get("description", "")).strip() or tag
        existing = current_by_tag.get(tag)
        if existing is not None and existing.signal_type != signal_type:
            diagnostics.append(IOImportDiagnostic(
                "ERROR", "signal_type_conflict", candidate_id,
                f"CEProject Signal {tag!r} type {signal_type!r} conflicts with current type {existing.signal_type!r}."
            ))
            candidates.append(IOImportCandidate(candidate_id, signal_id, "conflict", existing, None))
            continue
        proposed = IOSignal(tag=tag, description=label, signal_type=signal_type, device=label, mapping_status="unmapped")
        if existing is not None:
            # Preserve every canonical allocation/address field.  Imported
            # text can propose readable engineering labels, never a move.
            proposed = IOSignal(
                tag=existing.tag, description=label, signal_type=existing.signal_type,
                address=existing.address, device=label, rack=existing.rack, slot=existing.slot,
                channel=existing.channel, terminal=existing.terminal,
                module_name=existing.module_name, catalog_part_number=existing.catalog_part_number,
                source_record_ids=existing.source_record_ids, mapping_status=existing.mapping_status,
            )
            if proposed == existing:
                continue
            action = "update"
        else:
            action = "add"
        candidates.append(IOImportCandidate(candidate_id, signal_id, action, existing, proposed))

    return StagedIOImport(
        source_path=source_path,
        source_text=text,
        current_signals=current,
        candidates=tuple(sorted(candidates, key=lambda item: item.candidate_id)),
        diagnostics=tuple(sorted(diagnostics, key=lambda item: (item.severity, item.code, item.candidate_id, item.message))),
        fingerprint=_io_import_fingerprint(text, current),
    )


def apply_approved_ceproject_io_import(
    project: object,
    staged: StagedIOImport,
    approved_candidate_ids: set[str] | frozenset[str],
    dependent_tags: Iterable[str] = (),
) -> tuple[IOSignal, ...]:
    """Apply reviewed logical I/O rows with all validation before one write.

    The enclosing command owns its FreeCAD transaction.  This boundary writes
    a complete ``IOSignals`` list only after it proves the staged review is
    current, approval IDs are exact, and the resulting allocation is safe.
    """

    invalid_records = _invalid_current_io_records(project)
    if invalid_records:
        raise ImportReviewError(
            "I/O import cannot be applied while current I/O records are malformed: "
            + ", ".join(invalid_records)
        )
    current = tuple(explicit_io_signals_from_project(project))
    if _io_import_fingerprint(staged.source_text, current) != staged.fingerprint:
        raise ImportReviewError("I/O import review is stale; stage the source again before applying.")
    approved = {str(candidate_id) for candidate_id in approved_candidate_ids}
    available = {candidate.candidate_id for candidate in staged.candidates}
    if not approved:
        raise ImportReviewError("Select at least one staged I/O row to approve before applying an import.")
    unknown = approved - available
    if unknown:
        raise ImportReviewError("I/O import approval contains rows that were not staged: " + ", ".join(sorted(unknown)))
    errors = [item for item in staged.diagnostics if item.severity == "ERROR"]
    selected_errors = [item for item in errors if not item.candidate_id or item.candidate_id in approved]
    if selected_errors:
        raise ImportReviewError("I/O import cannot be applied: " + "; ".join(item.message for item in selected_errors))

    proposed_by_tag = {signal.tag: signal for signal in current}
    for candidate in staged.candidates:
        if candidate.candidate_id in approved and candidate.proposed is not None:
            proposed_by_tag[candidate.proposed.tag] = candidate.proposed
    proposed = tuple(proposed_by_tag[tag] for tag in sorted(proposed_by_tag))
    preflight_reconciliation(current, proposed, dependent_tags)
    findings = validate_io_allocations(proposed)
    allocation_errors = [finding for finding in findings if finding.severity == "ERROR"]
    if allocation_errors:
        raise ImportReviewError("I/O import cannot be applied: " + "; ".join(item.message for item in allocation_errors))
    project.IOSignals = [serialize_io_signal(signal) for signal in proposed]
    return proposed


def remember_approved_ceproject_io_source(project: object, staged: StagedIOImport) -> None:
    """Retain the CEProject source after an approved I/O-only import.

    Field imports already retain this record through the intake form path.  An
    I/O-only decision bypasses that path, so this small explicit provenance
    write keeps both approved import branches equally traceable.  The caller
    owns the enclosing FreeCAD transaction.
    """

    project.CEProjectImports = merge_ceproject_import_records(
        getattr(project, "CEProjectImports", []),
        ceproject_import_record(staged.source_text, staged.source_path),
    )


def _io_import_fingerprint(source_text: str, current_signals: Iterable[IOSignal]) -> str:
    payload = {
        "source": source_text,
        "current": [json.loads(serialize_io_signal(signal)) for signal in sorted(current_signals, key=lambda item: item.tag)],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _invalid_current_io_records(project: object) -> tuple[str, ...]:
    """Return opaque persisted I/O records that cannot safely be overwritten.

    Generic readers skip malformed historical records so other read-only views
    can continue.  An import rewrites the complete list, however, and must
    fail closed rather than silently discard a record it cannot reconstruct.
    """

    invalid = []
    for index, record in enumerate(getattr(project, "IOSignals", []) or []):
        try:
            signal = deserialize_io_signal(record)
        except (TypeError, ValueError, json.JSONDecodeError):
            invalid.append(f"record {index + 1}")
            continue
        if not signal.tag:
            invalid.append(f"record {index + 1} (missing tag)")
    return tuple(invalid)




def _display_value(value: object) -> str:
    if isinstance(value, (list, tuple, set)):
        return ", ".join(str(item).strip() for item in value if str(item).strip())
    return str(value or "").strip()
