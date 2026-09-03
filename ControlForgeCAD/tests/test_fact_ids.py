# SPDX-License-Identifier: MIT

import pytest

from controls_wb.fact_ids import (
    FACT_SPECS,
    FactIds,
    category_for_fact_id,
    fact_id_for_property,
    known_fact_ids,
    missing_data_item_id_for_fact_id,
    property_for_fact_id,
    question_id_for_fact_id,
)
from controls_wb.intake import required_fields_for
from controls_wb.model.project import PROJECT_PROPERTY_SPECS


def test_fact_registry_has_unique_deterministic_ids():
    ids = [spec.fact_id for spec in FACT_SPECS]

    assert len(ids) == len(set(ids))
    assert known_fact_ids() == tuple(sorted(ids))
    assert FactIds.PROJECT_NAME in known_fact_ids()
    assert FactIds.PLC_PLATFORM in known_fact_ids()
    assert FactIds.SENSOR_COUNT in known_fact_ids()


def test_project_properties_have_registered_fact_ids():
    property_names = {spec.name for spec in PROJECT_PROPERTY_SPECS}

    assert fact_id_for_property("ProjectName") == FactIds.PROJECT_NAME
    assert property_for_fact_id(FactIds.PLC_CPU) == "PlcCPU"
    assert {
        fact_id_for_property(property_name)
        for property_name in property_names
    }.issubset(set(known_fact_ids()))


def test_required_intake_fields_use_registered_fact_ids():
    required = required_fields_for(["panelLayout", "ioList", "bomSourceExport"])

    assert set(required).issubset(set(known_fact_ids()))
    assert required[FactIds.POWER_NOMINAL_VOLTAGE].label == "Nominal voltage"
    assert required[FactIds.BUDGET_STATUS].stakeholder == "Sales / estimator"


def test_fact_ids_drive_question_and_missing_data_ids():
    assert question_id_for_fact_id(FactIds.PLC_PLATFORM) == "Q-CONTROLS-PLCPLATFORM"
    assert missing_data_item_id_for_fact_id(FactIds.PLC_PLATFORM) == "MD-CONTROLS-PLCPLATFORM"
    assert category_for_fact_id(FactIds.PLC_PLATFORM) == "controls"


def test_unknown_fact_and_property_fail_loudly():
    with pytest.raises(KeyError, match="Unknown CEProject fact ID"):
        category_for_fact_id("unknown.fact")

    with pytest.raises(KeyError, match="No CEProject fact ID registered"):
        fact_id_for_property("UnknownProperty")
