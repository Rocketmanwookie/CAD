# SPDX-License-Identifier: MIT

import csv
from io import StringIO
from pathlib import Path

import pytest

from controls_wb.technical_documents import (
    acceptance_test_csv,
    acceptance_tests,
    datasheet_csv,
    datasheet_links,
    load_cad_manifest,
    registry_xml,
)


HEADERS = (
    "RequestID,System,Category,ManufacturerPreference,ProductFamily,RequestedPart,"
    "MLFBOrSearchKey,PartSelection,Priority,ThreeDModel,TwoDDrawing,IECSymbol,"
    "NFPAJICSymbol,TerminalPinMap,ElectricalMacro,CableWorkbenchAsset,SourceURL,"
    "SourceBasis,VerificationStatus,DownloadStatus,Notes\n"
)


def _manifest(tmp_path: Path) -> Path:
    path = tmp_path / "cad.csv"
    path.write_text(
        HEADERS
        + "CAD-0001,PLC,CPU,Siemens,S7-1200,CPU,6ES7,Exact catalog seed,1,Required,Required,Required,Required,Required,Download if available,Not applicable,https://www.siemens.com/cax,source,review,Not started,\n"
        + "CAD-0002,Panel wiring,Wire duct and tray,Vendor neutral,Duct,Slotted duct,duct,Configuration required,1,Required,Required,Not applicable,Not applicable,Not applicable,Not applicable,Required,,request,unselected,Not started,\n",
        encoding="utf-8",
    )
    return path


def test_document_links_distinguish_local_pending_download_and_unselected(tmp_path: Path):
    rows = load_cad_manifest(_manifest(tmp_path))
    datasheet = tmp_path / "cpu.pdf"
    datasheet.write_bytes(b"test datasheet")

    links = datasheet_links(rows, {"6ES7": datasheet})

    assert [link.status for link in links] == ["linked_local", "pending_part_selection"]
    assert len(links[0].sha256) == 64
    assert links[0].local_path == str(datasheet.resolve())


def test_acceptance_plan_is_category_and_asset_aware(tmp_path: Path):
    rows = load_cad_manifest(_manifest(tmp_path))
    tests = acceptance_tests(rows)
    by_request = {}
    for test in tests:
        by_request.setdefault(test.request_id, set()).add(test.test_id)

    assert {"identity", "datasheet", "geometry", "pins", "iec_symbol", "nfpa_symbol", "ratings", "io_mapping", "termination"} <= by_request["CAD-0001"]
    assert "cables" in by_request["CAD-0002"]
    assert "pins" not in by_request["CAD-0002"]


def test_registry_xml_is_schema_valid_and_csv_exports_are_deterministic(tmp_path: Path):
    lxml = pytest.importorskip("lxml.etree")
    rows = load_cad_manifest(_manifest(tmp_path))
    links = datasheet_links(rows)
    tests = acceptance_tests(rows)
    xml_text = registry_xml(links, tests)
    schema_path = Path(__file__).resolve().parents[1] / "schemas" / "technical_document_registry_v0_1.xsd"
    lxml.XMLSchema(lxml.parse(str(schema_path))).assertValid(lxml.fromstring(xml_text.encode()))

    assert registry_xml(links, tests) == xml_text
    assert len(list(csv.DictReader(StringIO(datasheet_csv(links))))) == 2
    assert len(list(csv.DictReader(StringIO(acceptance_test_csv(tests))))) == len(tests)
