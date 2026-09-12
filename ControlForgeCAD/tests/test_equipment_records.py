# SPDX-License-Identifier: MIT

from controls_wb.equipment_records import (
    categories,
    load_equipment_records,
    record_by_part_number,
    search_records,
)


def test_siemens_records_support_category_and_part_lookup():
    catalog = load_equipment_records()

    assert len(catalog.records) == 104
    assert "CPU" in categories(catalog)
    cpu = record_by_part_number(catalog, "6es7211-1ae40-0xb0")
    assert cpu is not None
    assert cpu.product_name == "CPU 1211C DC/DC/DC"
    assert cpu.properties["onboard_di"] == "6"
    assert cpu.properties["profinet_ports"] == "1"


def test_siemens_records_searches_summary_and_properties():
    catalog = load_equipment_records()

    fail_safe = search_records(catalog, "fail-safe")
    assert fail_safe
    assert any(record.category == "Fail-safe Signal Module" for record in fail_safe)
    assert record_by_part_number(catalog, "not-a-part") is None
