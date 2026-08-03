# SPDX-License-Identifier: MIT

from pathlib import Path
from xml.etree import ElementTree as ET

from controls_wb.hardware_catalog import (
    default_catalog_path,
    io_expansion_suggestion,
    line_catalog,
    load_hardware_catalog,
    part_by_name,
)


def test_default_hardware_catalog_loads_siemens_s7_1200_seed():
    catalog = load_hardware_catalog()
    line = line_catalog(catalog, "Siemens", "S7-1200")

    assert line is not None
    cpu = part_by_name(line.cpus, "CPU 1212C DC/DC/DC")
    assert cpu is not None
    assert cpu.part_number == "6ES7212-1AE40-0XB0"
    assert (cpu.di, cpu.do, cpu.ai, cpu.ao) == (8, 6, 2, 0)
    assert cpu.verified is True
    assert [cad_ref.format for cad_ref in cpu.cad_refs] == ["STEP", "SLDPRT"]
    assert cpu.cad_refs[0].local_path.endswith("Siemens S7-1200.STEP")
    assert cpu.cad_refs[0].sha256 == "e5cdccde78115ef54856dfedc8705b5fc3031057e5db17068369b92e33a7e3b8"

    module = part_by_name(line.io_modules, "SM 1222 DQ 16x24 VDC")
    assert module is not None
    assert module.part_number == "6ES7222-1BH32-0XB0"
    assert module.verified is True

    easy_book = catalog.sources["siemens-s7-1200-easy-book-local"]
    assert easy_book.document_number == "A5E02486774-AG"
    assert easy_book.local_path.endswith("s71200_easy_book_en-US_en-US.pdf")
    assert easy_book.sha256 == "ce2f5a5d7f8d9c1410b3e5718230eb5c6b975c9a8a0be2b5bc9977f9d299694f"


def test_hardware_catalog_xml_and_schema_are_parseable():
    catalog_path = default_catalog_path()
    schema_path = Path(__file__).resolve().parents[1] / "schemas" / "plc_hardware_catalog_v0_1.xsd"

    assert ET.parse(catalog_path).getroot().tag == "plcHardwareCatalog"
    assert ET.parse(schema_path).getroot().tag.endswith("schema")


def test_io_expansion_suggestion_uses_verified_catalog_parts():
    suggestion = io_expansion_suggestion(
        load_hardware_catalog(),
        "Siemens",
        "S7-1200",
        "CPU 1212C DC/DC/DC",
        "20",
        "12",
        "4",
        "2",
    )

    assert "SM 1221 DI 16x24 V DC (6ES7221-1BH32-0XB0, vendor-verified)" in suggestion
    assert "SM 1222 DQ 16x24 VDC (6ES7222-1BH32-0XB0, vendor-verified)" in suggestion
    assert "SM 1231 AI 8 (6ES7231-4HF32-0XB0, vendor-verified)" in suggestion
    assert "SM 1232 AQ 4 (6ES7232-4HD32-0XB0, vendor-verified)" in suggestion
