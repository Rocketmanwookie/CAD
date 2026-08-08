# SPDX-License-Identifier: MIT
"""Starter load-based amperage estimates for project intake."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


LOAD_TYPE_DEFAULTS = {
    "motor": {"power_factor": 0.85, "efficiency": 0.9},
    "vfd": {"power_factor": 0.9, "efficiency": 0.95},
    "heat_strip": {"power_factor": 1.0, "efficiency": 1.0},
    "power_supply": {"power_factor": 0.9, "efficiency": 0.88},
    "ethernet": {"power_factor": 0.9, "efficiency": 0.9},
    "coil": {"power_factor": 0.8, "efficiency": 1.0},
    "relay": {"power_factor": 0.8, "efficiency": 1.0},
    "other": {"power_factor": 0.9, "efficiency": 1.0},
}


@dataclass(frozen=True)
class LoadEstimate:
    load_type: str
    label: str
    quantity: int
    watts: float
    current_amps: float


def parse_load_lines(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        raw_lines = value.replace(";", "\n").splitlines()
    else:
        raw_lines = list(value)
    return [str(line).strip() for line in raw_lines if str(line).strip()]


def format_load_lines(value: object) -> str:
    return "\n".join(parse_load_lines(value))


def estimate_loads(value: object, voltage: object, phase_count: object) -> tuple[LoadEstimate, ...]:
    return tuple(
        _estimate_load(line, voltage, phase_count)
        for line in parse_load_lines(value)
    )


def estimated_total_amps(value: object, voltage: object, phase_count: object, spare_factor: float = 1.2) -> str:
    total = sum(load.current_amps for load in estimate_loads(value, voltage, phase_count))
    if total <= 0:
        return ""
    return f"{total * spare_factor:.2f}"


def _estimate_load(line: str, voltage: object, phase_count: object) -> LoadEstimate:
    parts = [part.strip() for part in line.split(",")]
    load_type = _clean_load_type(parts[0] if parts else "")
    label = parts[1] if len(parts) > 1 and parts[1] else load_type.replace("_", " ").title()
    quantity = _int_value(parts[2] if len(parts) > 2 else "1", default=1)
    watts = _watts_value(parts[3] if len(parts) > 3 else "0")
    current_amps = load_current_amps(load_type, quantity, watts, voltage, phase_count)
    return LoadEstimate(load_type, label, quantity, watts, current_amps)


def load_current_amps(load_type: str, quantity: int, watts: float, voltage: object, phase_count: object) -> float:
    clean_voltage = _float_value(voltage)
    if clean_voltage <= 0 or watts <= 0 or quantity <= 0:
        return 0.0
    defaults = LOAD_TYPE_DEFAULTS.get(_clean_load_type(load_type), LOAD_TYPE_DEFAULTS["other"])
    apparent_watts = watts / max(defaults["power_factor"] * defaults["efficiency"], 0.01)
    divisor = clean_voltage * (sqrt(3) if _int_value(phase_count, default=1) == 3 else 1)
    return quantity * apparent_watts / divisor


def _clean_load_type(value: str) -> str:
    clean = str(value or "").strip().lower().replace(" ", "_").replace("-", "_")
    return clean if clean in LOAD_TYPE_DEFAULTS else "other"


def _int_value(value: object, default: int = 0) -> int:
    try:
        return max(int(str(value).strip()), 0)
    except (TypeError, ValueError):
        return default


def _float_value(value: object) -> float:
    text = str(value or "").strip().lower().replace("watts", "w").replace(" ", "")
    multiplier = 1.0
    if text.endswith("kw"):
        multiplier = 1000.0
        text = text[:-2]
    elif text.endswith("w"):
        text = text[:-1]
    try:
        return max(float(text), 0.0) * multiplier
    except ValueError:
        return 0.0


def _watts_value(value: object) -> float:
    text = str(value or "").strip().lower().replace(" ", "")
    if text.endswith("hp"):
        try:
            return max(float(text[:-2]), 0.0) * 746.0
        except ValueError:
            return 0.0
    return _float_value(text)
