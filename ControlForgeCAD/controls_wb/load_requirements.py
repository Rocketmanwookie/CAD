# SPDX-License-Identifier: MIT
"""Typed, reviewable controls-load and I/O requirements for Release 1.

This module deliberately proposes *hardware classes*, never electrical ratings,
vendor parts, safety functions, or approval decisions.  It provides the stable
input records that later panel-capacity and export adapters consume.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


LOAD_CLASSES = frozenset({"motor", "conveyor", "hydraulic", "robot", "generic"})
IO_DIRECTIONS = frozenset({"input", "output", "analog_input", "analog_output"})
CONTROL_MODES = frozenset({"on_off", "speed_control", "position_control", "process_control", "unknown"})
RESOLUTION_NEEDS_ENGINEERING_DECISION = "needs_engineering_decision"


@dataclass(frozen=True)
class LoadRequirement:
    """A described controlled load, independent of physical CAD realization."""

    identity: str
    tag: str
    load_class: str
    description: str
    quantity: int = 1
    control_mode: str = "unknown"
    supply_voltage: str = ""
    power: str = ""
    current: str = ""
    duty: str = ""
    environment: str = ""
    evidence_locator: str = ""

    def validate(self) -> None:
        if not self.identity.strip():
            raise ValueError("Load requirement identity is required.")
        if not self.tag.strip():
            raise ValueError("Load requirement tag is required.")
        if self.load_class not in LOAD_CLASSES:
            raise ValueError(f"Unsupported load class: {self.load_class!r}.")
        if not self.description.strip():
            raise ValueError("Load requirement description is required.")
        if self.quantity <= 0:
            raise ValueError("Load requirement quantity must be greater than zero.")
        if self.control_mode not in CONTROL_MODES:
            raise ValueError(f"Unsupported control mode: {self.control_mode!r}.")

    def to_dict(self) -> dict[str, object]:
        self.validate()
        return asdict(self)


@dataclass(frozen=True)
class IORequirement:
    """The required behavior for one named I/O point tied to a load."""

    identity: str
    signal_tag: str
    direction: str
    load_identity: str
    behavior: str
    fail_state: str = ""
    evidence_locator: str = ""

    def validate(self) -> None:
        if not self.identity.strip():
            raise ValueError("I/O requirement identity is required.")
        if not self.signal_tag.strip():
            raise ValueError("I/O requirement signal tag is required.")
        if self.direction not in IO_DIRECTIONS:
            raise ValueError(f"Unsupported I/O requirement direction: {self.direction!r}.")
        if not self.load_identity.strip():
            raise ValueError("I/O requirement must link to a load identity.")
        if not self.behavior.strip():
            raise ValueError("I/O requirement behavior is required.")

    def to_dict(self) -> dict[str, object]:
        self.validate()
        return asdict(self)


@dataclass(frozen=True)
class HardwareRequirement:
    """A non-approved hardware class proposed from explicit resolver rules."""

    requirement_class: str
    quantity: int
    load_identity: str
    rationale: str
    rule_id: str
    status: str = RESOLUTION_NEEDS_ENGINEERING_DECISION

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def resolve_hardware_classes(load: LoadRequirement, io_requirements: tuple[IORequirement, ...] = ()) -> tuple[HardwareRequirement, ...]:
    """Return review-required generic hardware classes for one described load.

    The resolver is intentionally conservative.  It returns the hardware
    categories an engineer must resolve, rather than pretending to determine
    ratings, trip curves, SCCR, protection coordination, safety category, or
    a supplier part number from incomplete project intake.
    """

    load.validate()
    linked_io = tuple(io_requirements)
    for requirement in linked_io:
        requirement.validate()
        if requirement.load_identity != load.identity:
            raise ValueError(f"I/O requirement {requirement.identity!r} does not belong to load {load.identity!r}.")

    proposals: list[tuple[str, str, str]] = [
        ("branch_protection", "resolver.branch-protection.v1", "Every described controlled load requires an engineering review of branch protection."),
        ("disconnecting_means", "resolver.disconnect.v1", "Every described controlled load requires an engineering review of isolation/disconnecting means."),
    ]
    if load.load_class in {"motor", "conveyor", "hydraulic"}:
        proposals.extend(
            [
                ("motor_switching", "resolver.motor-switching.v1", "Motor-driven load requires an engineering review of a contactor/starter or equivalent switching method."),
                ("motor_overload_protection", "resolver.motor-overload.v1", "Motor-driven load requires an engineering review of overload/motor protection."),
            ]
        )
    if load.control_mode == "speed_control":
        proposals.append(("variable_frequency_drive", "resolver.speed-control.v1", "Speed-control mode requires an engineering review of a VFD or equivalent drive."))
    if load.load_class == "robot":
        proposals.append(("robot_interface", "resolver.robot-interface.v1", "Robot load requires an engineering review of its control/power interface."))
    if any(requirement.direction in {"output", "analog_output"} for requirement in linked_io):
        proposals.append(("control_interface", "resolver.output-interface.v1", "An output requirement needs an engineering review of relay/interface/drive compatibility."))
    proposals.append(("terminal_connection", "resolver.terminal-connection.v1", "A controlled load requires an engineering review of terminal and field-connection requirements."))

    return tuple(
        HardwareRequirement(
            requirement_class=requirement_class,
            quantity=load.quantity,
            load_identity=load.identity,
            rationale=rationale,
            rule_id=rule_id,
        )
        for requirement_class, rule_id, rationale in proposals
    )
