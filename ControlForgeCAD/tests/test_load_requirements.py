# SPDX-License-Identifier: MIT

import json

import pytest

from controls_wb.load_requirements import (
    HardwareRequirement,
    IORequirement,
    LoadRequirement,
    RESOLUTION_NEEDS_ENGINEERING_DECISION,
    io_requirements_from_project,
    hardware_requirements_from_project,
    load_requirements_from_project,
    persist_resolver_requirements,
    resolve_hardware_classes,
    serialize_hardware_requirement,
)


LOAD_ID = "urn:uuid:11111111-1111-1111-1111-111111111111"
OTHER_LOAD_ID = "urn:uuid:22222222-2222-2222-2222-222222222222"
IO_ID = "urn:uuid:33333333-3333-3333-3333-333333333333"
OTHER_IO_ID = "urn:uuid:44444444-4444-4444-4444-444444444444"
SIGNAL_ID = "urn:uuid:55555555-5555-5555-5555-555555555555"
OTHER_SIGNAL_ID = "urn:uuid:66666666-6666-6666-6666-666666666666"
ROBOT_ID = "urn:uuid:77777777-7777-7777-7777-777777777777"
GENERIC_ID = "urn:uuid:88888888-8888-8888-8888-888888888888"


def _motor() -> LoadRequirement:
    return LoadRequirement(
        identity=LOAD_ID,
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
        identity=IO_ID,
        signal_identity=SIGNAL_ID,
        signal_tag="DO-0001",
        direction="output",
        load_identity=LOAD_ID,
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
    assert all(item.load_identity == LOAD_ID for item in requirements)
    assert isinstance(requirements[0], HardwareRequirement)


def test_robot_and_generic_loads_keep_their_proposals_scoped_to_known_inputs():
    robot = LoadRequirement(ROBOT_ID, "RB-001", "robot", "Pick-and-place robot")
    generic = LoadRequirement(GENERIC_ID, "LOAD-001", "generic", "Cabinet light")

    assert "robot_interface" in {item.requirement_class for item in resolve_hardware_classes(robot)}
    assert "motor_overload_protection" not in {item.requirement_class for item in resolve_hardware_classes(generic)}


@pytest.mark.parametrize(
    "load, message",
    [
        (LoadRequirement("", "M-1", "motor", "Motor"), "identity"),
        (LoadRequirement(LOAD_ID, "", "motor", "Motor"), "tag"),
        (LoadRequirement(LOAD_ID, "M-1", "unknown", "Motor"), "Unsupported load class"),
        (LoadRequirement(LOAD_ID, "M-1", "motor", "Motor", quantity=0), "greater than zero"),
        (LoadRequirement(LOAD_ID, "M-1", "motor", "Motor", quantity=True), "greater than zero"),
        (LoadRequirement(LOAD_ID, "M-1", "motor", "Motor", quantity=1.5), "greater than zero"),
    ],
)
def test_load_requirement_validation_rejects_ambiguous_or_invalid_records(load, message):
    with pytest.raises(ValueError, match=message):
        resolve_hardware_classes(load)


def test_resolver_rejects_i_o_requirement_from_a_different_load():
    unrelated = IORequirement(OTHER_IO_ID, OTHER_SIGNAL_ID, "DO-0002", "output", OTHER_LOAD_ID, "Run")

    with pytest.raises(ValueError, match="does not belong"):
        resolve_hardware_classes(_motor(), (unrelated,))


@pytest.mark.parametrize(
    "requirement, message",
    [
        (IORequirement("", SIGNAL_ID, "DO-0001", "output", LOAD_ID, "Run"), "identity"),
        (IORequirement(IO_ID, "", "DO-0001", "output", LOAD_ID, "Run"), "signal identity"),
        (IORequirement(IO_ID, SIGNAL_ID, "DO-0001", "unknown", LOAD_ID, "Run"), "Unsupported"),
    ],
)
def test_i_o_requirement_validation_requires_stable_signal_identity(requirement, message):
    with pytest.raises(ValueError, match=message):
        requirement.validate()


def test_resolver_snapshot_persists_records_and_proposals_on_project():
    project = type("Project", (), {})()
    output = IORequirement(IO_ID, SIGNAL_ID, "DO-0001", "output", LOAD_ID, "Run command")

    hardware = persist_resolver_requirements(project, (_motor(),), (output,))

    assert load_requirements_from_project(project) == (_motor(),)
    assert io_requirements_from_project(project) == (output,)
    assert len(project.HardwareRequirements) == len(hardware)
    assert json.loads(project.HardwareRequirements[0])["status"] == RESOLUTION_NEEDS_ENGINEERING_DECISION


def test_resolver_snapshot_rejects_unknown_or_duplicate_load_references():
    project = type("Project", (), {})()
    duplicate = LoadRequirement(LOAD_ID, "CV-002", "motor", "Second motor")
    unrelated = IORequirement(OTHER_IO_ID, OTHER_SIGNAL_ID, "DO-0002", "output", OTHER_LOAD_ID, "Run")

    with pytest.raises(ValueError, match="Duplicate"):
        persist_resolver_requirements(project, (_motor(), duplicate), ())
    with pytest.raises(ValueError, match="unknown load"):
        persist_resolver_requirements(project, (_motor(),), (unrelated,))


def test_hydraulic_load_does_not_imply_a_motor_circuit_without_drive_evidence():
    hydraulic = LoadRequirement(OTHER_LOAD_ID, "HPU-001", "hydraulic", "Hydraulic power unit")

    requirements = resolve_hardware_classes(hydraulic)

    assert "hydraulic_power_interface" in {item.requirement_class for item in requirements}
    assert "motor_switching" not in {item.requirement_class for item in requirements}
    assert "motor_overload_protection" not in {item.requirement_class for item in requirements}
    assert "drive_type" in requirements[0].unresolved_fields


def test_explicit_motor_driven_hydraulic_load_gets_motor_review_classes_with_traceability():
    hydraulic = LoadRequirement(
        OTHER_LOAD_ID, "HPU-002", "hydraulic", "Hydraulic power unit", drive_type="electric_motor", evidence_locator="nameplate photo",
    )
    io_requirement = IORequirement(OTHER_IO_ID, OTHER_SIGNAL_ID, "DO-0003", "output", OTHER_LOAD_ID, "Pump run", evidence_locator="I/O list")

    first = resolve_hardware_classes(hydraulic, (io_requirement,))
    second = resolve_hardware_classes(hydraulic, (io_requirement,))

    assert "motor_switching" in {item.requirement_class for item in first}
    assert "motor_overload_protection" in {item.requirement_class for item in first}
    assert [item.identity for item in first] == [item.identity for item in second]
    assert all(item.linked_io_identities == (OTHER_IO_ID,) for item in first)
    assert all(item.evidence_locators == ("I/O list", "nameplate photo") for item in first)
    assert json.loads(serialize_hardware_requirement(first[0]))["identity"] == first[0].identity


def test_identity_validation_and_persisted_hardware_round_trip_are_strict():
    with pytest.raises(ValueError, match="valid CE identity"):
        resolve_hardware_classes(LoadRequirement("load-by-tag", "M-001", "motor", "Motor"))

    project = type("Project", (), {})()
    output = IORequirement(IO_ID, SIGNAL_ID, "DO-0001", "output", LOAD_ID, "Run command")
    expected = persist_resolver_requirements(project, (_motor(),), (output,))

    assert hardware_requirements_from_project(project) == expected
