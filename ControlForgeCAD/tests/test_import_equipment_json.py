# SPDX-License-Identifier: MIT

import importlib.util
import json
from pathlib import Path
from xml.etree import ElementTree as ET


SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "import_equipment_json.py"


def _module():
    spec = importlib.util.spec_from_file_location("import_equipment_json", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_importer_preserves_all_product_properties_and_sorts_records(tmp_path: Path):
    source = tmp_path / "catalog.json"
    source.write_text(
        json.dumps(
            {
                "catalog": {"manufacturer": "Example", "family": "PLC", "edition": "1", "record_count": 2},
                "products": [
                    {
                        "manufacturer": "Example",
                        "family": "PLC",
                        "category": "CPU",
                        "product_name": "Second",
                        "article_number": "B-2",
                        "summary": "Second part",
                        "catalog_source": "Example catalog",
                        "source_page": 2,
                        "onboard_di": 8,
                        "fail_safe": False,
                    },
                    {
                        "manufacturer": "Example",
                        "family": "PLC",
                        "category": "CPU",
                        "product_name": "First",
                        "article_number": "A-1",
                        "summary": "First part",
                        "catalog_source": "Example catalog",
                        "source_page": 1,
                        "protocols": ["PROFINET", "Modbus TCP"],
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    reference = tmp_path / "manual.pdf"
    reference.write_bytes(b"reference")
    root = _module().build_catalog(source, references=(reference,)).getroot()
    records = root.findall("./records/record")

    assert [record.get("partNumber") for record in records] == ["A-1", "B-2"]
    first_properties = {item.get("name"): (item.get("valueType"), item.text) for item in records[0].findall("./properties/property")}
    assert first_properties["protocols"] == ("list", "PROFINET; Modbus TCP")
    second_properties = {item.get("name"): (item.get("valueType"), item.text) for item in records[1].findall("./properties/property")}
    assert second_properties["onboard_di"] == ("integer", "8")
    assert second_properties["fail_safe"] == ("boolean", "false")
    imported_source = root.find("./sources/source[@sourceType='reference-pdf']")
    assert imported_source is not None
    assert imported_source.get("localPath") == str(reference)
    assert len(imported_source.get("sha256", "")) == 64


def test_importer_rejects_duplicate_article_numbers(tmp_path: Path):
    source = tmp_path / "catalog.json"
    product = {
        "manufacturer": "Example",
        "family": "PLC",
        "category": "CPU",
        "product_name": "Duplicate",
        "article_number": "A-1",
        "catalog_source": "Example catalog",
    }
    source.write_text(
        json.dumps(
            {
                "catalog": {"manufacturer": "Example", "family": "PLC", "edition": "1", "record_count": 2},
                "products": [product, product],
            }
        ),
        encoding="utf-8",
    )

    try:
        _module().build_catalog(source)
    except ValueError as exc:
        assert str(exc) == "Duplicate article number: A-1"
    else:
        raise AssertionError("Duplicate article numbers must be rejected")
