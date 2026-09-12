# SPDX-License-Identifier: MIT

import pytest

from controls_wb.wire_engineering import (
    RacewayCodeProfile,
    RacewaySize,
    permitted_fill_percent,
    select_raceway_size,
    standardized_wire_color,
)


def test_nec_chapter_9_fill_percentages_and_nipple_rule():
    assert permitted_fill_percent(1) == 53.0
    assert permitted_fill_percent(2) == 31.0
    assert permitted_fill_percent(3) == 40.0
    assert permitted_fill_percent(12, nipple=True) == 60.0


def test_raceway_selection_uses_supplied_edition_specific_areas():
    profile = RacewayCodeProfile(
        standard="NFPA 70",
        edition="project-selected",
        raceway_type="test-raceway",
        sizes=(RacewaySize("small", 100.0), RacewaySize("large", 200.0)),
    )

    result = select_raceway_size([20.0, 20.0, 20.0], profile)

    assert result.trade_size == "large"
    assert result.permitted_fill_percent == 40.0
    assert result.actual_fill_percent == 30.0
    assert result.status == "preliminary_unverified"


def test_raceway_selection_requires_real_conductor_areas():
    profile = RacewayCodeProfile("NFPA 70", "project-selected", "test", (RacewaySize("1", 100),))

    with pytest.raises(ValueError, match="including insulation"):
        select_raceway_size([], profile)


def test_reserved_colors_are_separate_from_project_conventions():
    assert standardized_wire_color("equipment_grounding") == "green or green/yellow"
    assert standardized_wire_color("grounded_ac") == "white or gray"
    assert standardized_wire_color("dc_control", {"dc_control": "blue"}) == "blue"

    with pytest.raises(ValueError, match="project-approved color"):
        standardized_wire_color("dc_control")
