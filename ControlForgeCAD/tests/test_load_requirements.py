# SPDX-License-Identifier: MIT

import pytest
import json

from controls_wb.load_requirements import (
    HardwareRequirement,
    IORequirement,
    LoadRequirement,
    RESOLUTION_NEEDS_ENGINEERING_DECISION,
    io_requirements_from_project,
    load_requirements_from_project,
    persist_resolver_requirements,
    resolve_hardware_classes,
    serialize_hardware_requirement,
)


def _motor() -> LoadRequirement:
    return LoadRequirement(
        identity="load-conveyor-1",
        tag="CV-001",
        load_class="conveyor",
        description="Conveyor motor",
        quantity=2,
        control_mode="speed_control",
        drive_type="electric_motor",
        supply_voltage="480 VAC, 3 phase",
        power="1.5 hp",
        evidence_locator="customer intake / line 1",
    )


def test_motor_load_resolves_review_required_hardware_classes():
    output = IORequirement(
        identity="io-cv-run",
        signal_identity="signal-cv-run",
        signal_tag="DO-0001",
        direction="output",
        load_identity="load-conveyor-1",
        behavior="Run command",
    )

    requirements = resolve_hardware_classes(_motor(), (output,))

    assert [item.requirement_class for item in requirements] == [
        "branch_protection",
        "disconnecting_means",
        "motor_switching",
        "motor_overload_protection",
        "variable_frequency_drive",
        "control_interface",
        "terminal_connection",
    ]
    assert all(item.status == RESOLUTION_NEEDS_ENGINEERING_DECISION for item in requirements)
    assert all(item.quantity == 2 for item in requirements)
    assert all(item.load_identity == "load-conveyor-1" for item in requirements)
    assert isinstance(requirements[0], HardwareRequirement)


def test_robot_and_generic_loads_keep_their_proposals_scoped_to_known_inputs():
    robot = LoadRequirement("robot-1", "RB-001", "robot", "Pick-and-place robot")
    generic = LoadRequirement("generic-1", "LOAD-001", "generic", "Cabinet light")

    assert "robot_interface" in {item.requirement_class for item in resolve_hardware_classes(robot)}
    assert "motor_overload_protection" not in {item.requirement_class for item in resolve_hardware_classes(generic)}


@pytest.mark.parametrize(
    "load, message",
    [
        (LoadRequirement("", "M-1", "motor", "Motor"), "identity"),
        (LoadRequirement("load-1", "", "motor", "Motor"), "tag"),
        (LoadRequirement("load-1", "M-1", "unknown", "Motor"), "Unsupported load class"),
        (LoadRequirement("load-1", "M-1", "motor", "Motor", quantity=0), "greater than zero"),
        (LoadRequirement("load-1", "M-1", "motor", "Motor", quantity=True), "greater than zero"),
        (LoadRequirement("load-1", "M-1", "motor", "Motor", quantity=1.5), "greater than zero"),
    ],
)
def test_load_requirement_validation_rejects_ambiguous_or_invalid_records(load, message):
    with pytest.raises(ValueError, match=message):
        resolve_hardware_classes(load)


def test_resolver_rejects_i_o_requirement_from_a_different_load():
    unrelated = IORequirement("io-2", "signal-2", "DO-0002", "output", "other-load", "Run")

    with pytest.raises(ValueError, match="does not belong"):
        resolve_hardware_classes(_motor(), (unrelated,))


@pytest.mark.parametrize(
    "requirement, message",
    [
        (IORequirement("", "signal-1", "DO-0001", "output", "load-conveyor-1", "Run"), "identity"),
        (IORequirement("io-1", "", "DO-0001", "output", "load-conveyor-1", "Run"), "signal identity"),
        (IORequirement("io-1", "signal-1", "DO-0001", "unknown", "load-conveyor-1", "Run"), "Unsupported"),
    ],
)
def test_i_o_requirement_validation_requires_stable_signal_identity(requirement, message):
    with pytest.raises(ValueError, match=message):
        requirement.validate()


def test_resolver_snapshot_persists_records_and_proposals_on_project():
    project = type("Project", (), {})()
    output = IORequirement("io-cv-run", "signal-cv-run", "DO-0001", "output", "load-conveyor-1", "Run command")

    hardware = persist_resolver_requirements(project, (_motor(),), (output,))

    assert load_requirements_from_project(project) == (_motor(),)
    assert io_requirements_from_project(project) == (output,)
    assert len(project.HardwareRequirements) == len(hardware)
    assert json.loads(project.HardwareRequirements[0])["status"] == RESOLUTION_NEEDS_ENGINEERING_DECISION


def test_resolver_snapshot_rejects_unknown_or_duplicate_load_references():
    project = type("Project", (), {})()
    duplicate = LoadRequirement("load-conveyor-1", "CV-002", "motor", "Second motor")
    unrelated = IORequirement("io-2", "signal-2", "DO-0002", "output", "other-load", "Run")

    with pytest.raises(ValueError, match="Duplicate"):
        persist_resolver_requirements(project, (_motor(), duplicate), ())
    with pytest.raises(ValueError, match="unknown load"):
        persist_resolver_requirements(project, (_motor(),), (unrelated,))


def test_hydraulic_load_does_not_imply_a_motor_circuit_without_drive_evidence():
    hydraulic = LoadRequirement("hyd-1", "HPU-001", "hydraulic", "Hydraulic power unit")

    requirements = resolve_hardware_classes(hydraulic)

    assert "hydraulic_power_interface" in {item.requirement_class for item in requirements}
    assert "motor_switching" not in {item.requirement_class for item in requirements}
    assert "motor_overload_protection" not in {item.requirement_class for item in requirements}
    assert "drive_type" in requirements[0].unresolved_fields


def test_explicit_motor_driven_hydraulic_load_gets_motor_review_classes_with_traceability():
    hydraulic = LoadRequirement(
        "hyd-2", "HPU-002", "hydraulic", "Hydraulic power unit", drive_type="electric_motor", evidence_locator="nameplate photo",
    )
    io_requirement = IORequirement("io-hyd-run", "signal-hyd-run", "DO-0003", "output", "hyd-2", "Pump run", evidence_locator="I/O list")

    first = resolve_hardware_classes(hydraulic, (io_requirement,))
    second = resolve_hardware_classes(hydraulic, (io_requirement,))

    assert "motor_switching" in {item.requirement_class for item in first}
    assert "motor_overload_protection" in {item.requirement_class for item in first}
    assert [item.identity for item in first] == [item.identity for item in second]
    assert all(item.linked_io_identities == ("io-hyd-run",) for item in first)
    assert all(item.evidence_locators == ("I/O list", "nameplate photo") for item in first)
    assert json.loads(serialize_hardware_requirement(first[0]))["identity"] == first[0].identity
