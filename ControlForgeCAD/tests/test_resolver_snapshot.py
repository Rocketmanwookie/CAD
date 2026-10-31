# SPDX-License-Identifier: MIT

import json

import pytest

from controls_wb.identity import imported_ce_identity
from controls_wb.load_requirements import IORequirement, LoadRequirement, persist_resolver_requirements
from controls_wb.resolver_snapshot import resolver_snapshot_from_project


PROJECT_ID = "urn:uuid:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
LOAD_ID = "urn:uuid:bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
IO_ID = "urn:uuid:cccccccc-cccc-cccc-cccc-cccccccccccc"
SIGNAL_ID = "urn:uuid:dddddddd-dddd-dddd-dddd-dddddddddddd"


def _project_with_requirements():
    project = type("Project", (), {"CEIdentity": PROJECT_ID, "SchemaVersion": "0.1"})()
    load = LoadRequirement(
        LOAD_ID,
        "CV-001",
        "conveyor",
        "Conveyor motor",
        quantity=2,
        control_mode="speed_control",
        drive_type="electric_motor",
        evidence_locator="intake line 1",
    )
    io_requirement = IORequirement(IO_ID, SIGNAL_ID, "DO-0001", "output", LOAD_ID, "Run")
    persist_resolver_requirements(project, (load,), (io_requirement,))
    return project


def test_resolver_snapshot_is_deterministic_and_counts_only_explicit_proposals():
    project = _project_with_requirements()

    first = resolver_snapshot_from_project(project, reserve_percent=20)
    second = resolver_snapshot_from_project(project, reserve_percent=20)

    assert first == second
    assert first.project_identity == PROJECT_ID
    assert first.capacity_envelope.equipment_unit_count == 14
    assert first.capacity_envelope.terminal_connection_count == 2
    assert first.capacity_envelope.reserve_equipment_units == 3
    assert first.capacity_envelope.required_equipment_units == 17
    assert first.capacity_envelope.rail_positions is None
    assert first.capacity_envelope.terminal_positions is None
    assert first.capacity_envelope.heat_input is None
    assert first.capacity_envelope.power_input is None
    assert dict(first.capacity_envelope.counts_by_requirement_class)["variable_frequency_drive"] == 2
    assert "physical_fit_not_calculated" in first.capacity_envelope.unresolved_inputs
    assert "thermal_power_input_not_calculated" in first.capacity_envelope.unresolved_inputs
    assert first.review_status == "blocked_missing_input"
    assert first.source_schema_version == "0.1"
    payload = json.loads(first.to_json())
    assert payload["capacity_envelope"]["required_equipment_units"] == 17


def test_resolver_snapshot_leaves_reserve_explicitly_unresolved_when_not_supplied():
    snapshot = resolver_snapshot_from_project(_project_with_requirements())

    assert snapshot.capacity_envelope.reserve_percent is None
    assert snapshot.capacity_envelope.required_equipment_units is None
    assert "reserve_policy_not_provided" in snapshot.capacity_envelope.unresolved_inputs


def test_resolver_snapshot_rejects_missing_project_identity_and_broken_links():
    project = _project_with_requirements()
    project.CEIdentity = "project-by-label"
    with pytest.raises(ValueError, match="project CE identity"):
        resolver_snapshot_from_project(project)

    project = _project_with_requirements()
    project.HardwareRequirements = list(project.HardwareRequirements)
    tampered = json.loads(project.HardwareRequirements[0])
    tampered["linked_io_identities"] = [imported_ce_identity("test", "missing-io")]
    project.HardwareRequirements[0] = json.dumps(tampered)
    with pytest.raises(ValueError, match="unknown I/O"):
        resolver_snapshot_from_project(project)
