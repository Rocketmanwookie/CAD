# SPDX-License-Identifier: MIT
"""Code-profiled wire color and raceway-fill calculation primitives."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RacewaySize:
    trade_size: str
    internal_area_mm2: float


@dataclass(frozen=True)
class RacewayCodeProfile:
    standard: str
    edition: str
    raceway_type: str
    sizes: tuple[RacewaySize, ...]


@dataclass(frozen=True)
class RacewayFillResult:
    standard: str
    edition: str
    raceway_type: str
    trade_size: str
    conductor_count: int
    conductor_area_mm2: float
    permitted_fill_percent: float
    permitted_area_mm2: float
    actual_fill_percent: float
    status: str


def permitted_fill_percent(conductor_count: int, *, nipple: bool = False) -> float:
    """Return NEC Chapter 9 Table 1 fill percentage; nipple is <=600 mm/24 in."""

    if conductor_count < 1:
        raise ValueError("Raceway fill requires at least one conductor or cable.")
    if nipple:
        return 60.0
    if conductor_count == 1:
        return 53.0
    if conductor_count == 2:
        return 31.0
    return 40.0


def select_raceway_size(
    conductor_areas_mm2: list[float] | tuple[float, ...],
    profile: RacewayCodeProfile,
    *,
    nipple: bool = False,
) -> RacewayFillResult:
    """Select the smallest supplied trade size that satisfies the code profile."""

    if not conductor_areas_mm2:
        raise ValueError("Raceway sizing requires conductor or cable areas including insulation.")
    if any(area <= 0 for area in conductor_areas_mm2):
        raise ValueError("Conductor and cable areas must be positive square-millimetre values.")
    if not profile.standard.strip() or not profile.edition.strip() or not profile.raceway_type.strip():
        raise ValueError("Raceway sizing requires standard, edition, and raceway type.")
    fill = permitted_fill_percent(len(conductor_areas_mm2), nipple=nipple)
    used_area = sum(conductor_areas_mm2)
    for size in sorted(profile.sizes, key=lambda item: item.internal_area_mm2):
        if size.internal_area_mm2 <= 0:
            raise ValueError(f"Invalid internal area for raceway size {size.trade_size}.")
        permitted_area = size.internal_area_mm2 * fill / 100.0
        if used_area <= permitted_area:
            return RacewayFillResult(
                standard=profile.standard,
                edition=profile.edition,
                raceway_type=profile.raceway_type,
                trade_size=size.trade_size,
                conductor_count=len(conductor_areas_mm2),
                conductor_area_mm2=used_area,
                permitted_fill_percent=fill,
                permitted_area_mm2=permitted_area,
                actual_fill_percent=used_area / size.internal_area_mm2 * 100.0,
                status="preliminary_unverified",
            )
    raise ValueError("No supplied raceway size satisfies the permitted fill area.")


RESERVED_COLOR_RULES = {
    "equipment_grounding": "green or green/yellow",
    "grounded_ac": "white or gray",
    "grounded_dc": "white with blue stripe",
}


def standardized_wire_color(circuit_function: str, project_conventions: dict[str, str] | None = None) -> str:
    """Resolve reserved identification first, then an explicit project convention."""

    function = str(circuit_function).strip().lower()
    if function in RESERVED_COLOR_RULES:
        return RESERVED_COLOR_RULES[function]
    conventions = project_conventions or {}
    color = str(conventions.get(function, "")).strip()
    if not color:
        raise ValueError(
            f"No mandated/reserved or project-approved color is defined for {circuit_function!r}."
        )
    return color
