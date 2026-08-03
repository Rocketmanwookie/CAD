# SPDX-License-Identifier: MIT

from pathlib import Path
from xml.etree import ElementTree as ET

from controls_wb.panel_hardware_catalog import (
    default_panel_catalog_path,
    load_panel_hardware_catalog,
    part_for_layout,
)


def test_default_panel_hardware_catalog_loads_starter_parts():
    catalog = load_panel_hardware_catalog()

    backplate = part_for_layout(catalog, "CE_Backplate")
    terminal_strip = part_for_layout(catalog, "CE_Terminal_Strip")

    assert backplate is not None
    assert backplate.manufacturer == "Generic"
    assert backplate.part_number == "PANEL-BACKPLATE-800X1000"
    assert backplate.verified is False
    assert terminal_strip is not None
    assert terminal_strip.part_number == "TERMINAL-STRIP-16"


def test_panel_hardware_catalog_xml_and_schema_are_parseable():
    schema_path = Path(__file__).resolve().parents[1] / "schemas" / "panel_hardware_catalog_v0_1.xsd"

    assert ET.parse(default_panel_catalog_path()).getroot().tag == "panelHardwareCatalog"
    assert ET.parse(schema_path).getroot().tag.endswith("schema")
