# SPDX-License-Identifier: MIT

import pytest

from controls_wb.load_requirements import (
    HardwareRequirement,
    IORequirement,
    LoadRequirement,
    RESOLUTION_NEEDS_ENGINEERING_DECISION,
    resolve_hardware_classes,
)


def _motor() -> LoadRequirement:
    return LoadRequirement(
        identity="load-conveyor-1",
        tag="CV-001",
        load_class="conveyor",
        description="Conveyor motor",
        quantity=2,
        control_mode="speed_control",
        supply_voltage="480 VAC, 3 phase",
        power="1.5 hp",
        evidence_locator="customer intake / line 1",
    )


def test_motor_load_resolves_review_required_hardware_classes():
    output = IORequirement(
        identity="io-cv-run",
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
    ],
)
def test_load_requirement_validation_rejects_ambiguous_or_invalid_records(load, message):
    with pytest.raises(ValueError, match=message):
        resolve_hardware_classes(load)


def test_resolver_rejects_i_o_requirement_from_a_different_load():
    unrelated = IORequirement("io-2", "DO-0002", "output", "other-load", "Run")

    with pytest.raises(ValueError, match="does not belong"):
        resolve_hardware_classes(_motor(), (unrelated,))
