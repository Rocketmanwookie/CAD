# SPDX-License-Identifier: MIT
"""Pure-Python project intake model and validation helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


SCHEMA_VERSION = "0.1.0"


class FieldStatus(str, Enum):
    UNKNOWN = "Unknown"
    REQUESTED = "Requested"
    RECEIVED = "Received"
    ASSUMED = "Assumed"
    ESTIMATED = "Estimated"
    VERIFIED = "Verified"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    SUPERSEDED = "Superseded"


@dataclass(frozen=True)
class IntakeField:
    field_id: str
    label: str
    stakeholder: str
    value: str = ""
    status: FieldStatus = FieldStatus.UNKNOWN


@dataclass(frozen=True)
class ValidationFinding:
    level: str
    field_id: str
    message: str
    ask: str = ""


@dataclass
class ProjectIntake:
    project_id: str
    name: str
    schema_version: str = SCHEMA_VERSION
    fields: dict[str, IntakeField] = field(default_factory=dict)
    deliverables: set[str] = field(default_factory=set)


REQUIRED_FIELDS_BY_DELIVERABLE: dict[str, tuple[IntakeField, ...]] = {
    "panelLayout": (
        IntakeField("project.name", "Project name", "Project manager"),
        IntakeField("powerFeed.nominalVoltage", "Nominal voltage", "Electrical engineering"),
        IntakeField("powerFeed.phaseCount", "Phase count", "Electrical engineering"),
        IntakeField("environment.enclosureRating", "Enclosure rating", "Operations / maintenance"),
    ),
    "ioList": (
        IntakeField("project.name", "Project name", "Project manager"),
        IntakeField("controls.plcPlatform", "PLC platform", "Controls lead"),
        IntakeField("io.sensorCount", "Sensor count or estimate", "Mechanical / materials handling"),
    ),
    "bomSourceExport": (
        IntakeField("project.name", "Project name", "Project manager"),
        IntakeField("purchasing.preferredVendors", "Preferred vendors", "Purchasing"),
        IntakeField("costing.budgetStatus", "Budget or quote status", "Sales / estimator"),
    ),
}


def default_project_intake(project_id: str = "CE-PROJECT-001", name: str = "Controls Project") -> ProjectIntake:
    """Create the starter intake used by the first FreeCAD project command."""
    fields = {
        "project.name": IntakeField(
            "project.name",
            "Project name",
            "Project manager",
            value=name,
            status=FieldStatus.RECEIVED,
        ),
        "powerFeed.nominalVoltage": IntakeField(
            "powerFeed.nominalVoltage",
            "Nominal voltage",
            "Electrical engineering",
            status=FieldStatus.REQUESTED,
        ),
        "powerFeed.phaseCount": IntakeField(
            "powerFeed.phaseCount",
            "Phase count",
            "Electrical engineering",
            status=FieldStatus.REQUESTED,
        ),
        "environment.enclosureRating": IntakeField(
            "environment.enclosureRating",
            "Enclosure rating",
            "Operations / maintenance",
            status=FieldStatus.REQUESTED,
        ),
        "controls.plcPlatform": IntakeField(
            "controls.plcPlatform",
            "PLC platform",
            "Controls lead",
            status=FieldStatus.REQUESTED,
        ),
        "io.sensorCount": IntakeField(
            "io.sensorCount",
            "Sensor count or estimate",
            "Mechanical / materials handling",
            status=FieldStatus.REQUESTED,
        ),
    }
    return ProjectIntake(
        project_id=project_id,
        name=name,
        fields=fields,
        deliverables={"panelLayout", "ioList"},
    )


def required_fields_for(deliverables: Iterable[str]) -> dict[str, IntakeField]:
    required: dict[str, IntakeField] = {}
    for deliverable in deliverables:
        for intake_field in REQUIRED_FIELDS_BY_DELIVERABLE.get(deliverable, ()):
            required.setdefault(intake_field.field_id, intake_field)
    return required


def validate_intake(intake: ProjectIntake) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    required = required_fields_for(intake.deliverables)

    for field_id, requirement in required.items():
        actual = intake.fields.get(field_id, requirement)
        if actual.status in {FieldStatus.UNKNOWN, FieldStatus.REQUESTED} or not actual.value:
            findings.append(
                ValidationFinding(
                    "WARNING",
                    field_id,
                    f"{requirement.label} is missing for selected deliverables.",
                    ask=requirement.stakeholder,
                )
            )
        elif actual.status in {FieldStatus.ASSUMED, FieldStatus.ESTIMATED}:
            findings.append(
                ValidationFinding(
                    "WARNING",
                    field_id,
                    f"{requirement.label} is {actual.status.value.lower()} and needs verification.",
                    ask=requirement.stakeholder,
                )
            )
        elif actual.status in {FieldStatus.REJECTED, FieldStatus.SUPERSEDED}:
            findings.append(
                ValidationFinding(
                    "ERROR",
                    field_id,
                    f"{requirement.label} uses a {actual.status.value.lower()} value.",
                    ask=requirement.stakeholder,
                )
            )

    if not findings:
        findings.append(ValidationFinding("INFO", "intake", "No intake validation messages."))
    return findings
