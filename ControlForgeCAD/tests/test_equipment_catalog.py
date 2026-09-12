# SPDX-License-Identifier: MIT

from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from controls_wb.equipment_catalog import (
    default_equipment_catalog_path,
    equipment_class_by_id,
    linked_catalog_path,
    linked_schema_path,
    load_equipment_catalog,
)


def test_neutral_equipment_catalog_loads_specification_seed():
    catalog = load_equipment_catalog()

    assert catalog.catalog_id == "integracad-equipment"
    assert catalog.schema_version == "0.1.0"
    assert len(catalog.equipment_classes) == 7
    plc_module = equipment_class_by_id(catalog, "plc-module")
    assert plc_module is not None
    assert plc_module.implementation_phase == "1-MVP"
    assert plc_module.source_locator == "Sections 3 and 6 - PLC modules and bundled part library"
    assert {field.name for field in plc_module.required_data if field.required} == {
        "manufacturer",
        "productLine",
        "partNumber",
        "moduleType",
    }


def test_linked_equipment_catalogs_and_schemas_exist():
    path = default_equipment_catalog_path()
    catalog = load_equipment_catalog(path)

    assert {linked.kind for linked in catalog.linked_catalogs} == {
        "equipment-records",
        "panel-hardware",
        "plc-hardware",
        "technical-documents",
    }
    for linked in catalog.linked_catalogs:
        assert linked_catalog_path(path, linked).is_file()
        assert linked_schema_path(path, linked).is_file()


def test_equipment_catalog_rejects_unknown_source_reference(tmp_path: Path):
    path = tmp_path / "equipment_catalog.xml"
    path.write_text(
        """<?xml version="1.0"?>
<equipmentCatalog schemaVersion="0.1.0" catalogId="test">
  <sources><source id="known" title="Known" sourceType="test"/></sources>
  <equipmentClasses>
    <equipmentClass id="motor" name="Motor" category="load" implementationPhase="seed" recordStatus="seed" sourceId="missing" sourceLocator="test">
      <description>Test motor.</description>
    </equipmentClass>
  </equipmentClasses>
</equipmentCatalog>
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unknown equipment source IDs: missing"):
        load_equipment_catalog(path)


def test_siemens_equipment_records_are_complete_and_deterministic():
    catalog_path = default_equipment_catalog_path()
    records_path = catalog_path.parent / "siemens_s7_1200_2017.xml"
    root = ET.parse(records_path).getroot()
    records = root.findall("./records/record")

    assert root.get("manufacturer") == "Siemens"
    assert root.get("family") == "SIMATIC S7-1200"
    assert root.get("recordCount") == "104"
    assert len(records) == 104
    assert len({record.get("partNumber") for record in records}) == 104
    assert records == sorted(records, key=lambda record: (record.get("category", ""), record.get("partNumber", "")))
    assert len(root.findall("./profiles/profile/value")) == 20
    assert len(root.findall("./assets/asset")) == 2
    assert len(root.findall("./sources/source/alias")) == 2


def test_equipment_xml_schemas_are_parseable():
    schema_dir = Path(__file__).resolve().parents[1] / "schemas"

    for name in (
        "equipment_catalog_v0_1.xsd",
        "equipment_records_v0_1.xsd",
        "technical_document_registry_v0_1.xsd",
    ):
        assert ET.parse(schema_dir / name).getroot().tag.endswith("schema")
