# SPDX-License-Identifier: MIT

from controls_wb.power_loads import estimated_total_amps, estimate_loads, format_load_lines, parse_load_lines


def test_parse_load_lines_accepts_multiline_or_semicolon_text():
    assert parse_load_lines("motor, Conveyor, 1, 1hp;\nheat_strip, Heater, 1, 500W") == [
        "motor, Conveyor, 1, 1hp",
        "heat_strip, Heater, 1, 500W",
    ]
    assert format_load_lines([" motor, Conveyor, 1, 1hp ", ""]) == "motor, Conveyor, 1, 1hp"


def test_estimate_loads_calculates_three_phase_current():
    loads = estimate_loads("motor, Conveyor, 2, 1hp", "480", "3")

    assert len(loads) == 1
    assert loads[0].load_type == "motor"
    assert loads[0].label == "Conveyor"
    assert loads[0].quantity == 2
    assert loads[0].watts == 746.0
    assert round(loads[0].current_amps, 2) == 2.35


def test_estimated_total_amps_includes_spare_capacity():
    estimate = estimated_total_amps(
        "\n".join(
            [
                "motor, Conveyor, 2, 1hp",
                "heat_strip, Cabinet heater, 1, 500W",
            ]
        ),
        "480",
        "3",
    )

    assert estimate == "3.54"
