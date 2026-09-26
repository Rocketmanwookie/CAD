# SPDX-License-Identifier: MIT

import pytest

from controls_wb.allocation_reconciliation import allocation_delta, preflight_reconciliation
from controls_wb.io_list import IOSignal


def _signal(tag="DI-0001", signal_type="digital_input", slot="1", channel="0"):
    return IOSignal(tag, "test", signal_type, rack="0", slot=slot, channel=channel, mapping_status="allocated")


def test_preflight_reports_same_type_move_without_mutating_inputs():
    current = _signal(slot="2")
    proposed = _signal(slot="1")

    delta = preflight_reconciliation([current], [proposed], dependent_tags=[current.tag])

    assert delta[0].kind == "moved"
    assert current.slot == "2"
    assert proposed.slot == "1"


def test_preflight_rejects_removal_of_path_dependent_signal():
    with pytest.raises(ValueError, match="DI-0001: removed"):
        preflight_reconciliation([_signal()], [], dependent_tags=["DI-0001"])


def test_preflight_rejects_same_tag_type_change():
    with pytest.raises(ValueError, match="DI-0001: type_changed"):
        preflight_reconciliation([_signal()], [_signal(signal_type="digital_output")])


def test_delta_rejects_duplicate_tags():
    with pytest.raises(ValueError, match="Duplicate current"):
        allocation_delta([_signal(), _signal()], [])
