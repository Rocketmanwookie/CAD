#!/usr/bin/env python3
"""Build the technical-document XML registry and deterministic review CSVs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "ControlForgeCAD"))

from controls_wb.technical_documents import (  # noqa: E402
    acceptance_test_csv,
    acceptance_tests,
    datasheet_csv,
    datasheet_links,
    load_cad_manifest,
    registry_xml,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cad-manifest", type=Path, default=REPO_ROOT / "exports" / "siemens_cad_library_download_manifest.csv")
    parser.add_argument("--registry", type=Path, default=REPO_ROOT / "ControlForgeCAD" / "controls_wb" / "resources" / "hardware" / "technical_document_registry.xml")
    parser.add_argument("--datasheet-csv", type=Path, default=REPO_ROOT / "exports" / "equipment_datasheet_links.csv")
    parser.add_argument("--tests-csv", type=Path, default=REPO_ROOT / "exports" / "equipment_library_acceptance_tests.csv")
    args = parser.parse_args()
    known_datasheets = {
        "6ES7212-1AE40-0XB0": Path("/home/egrantjr/Documents/Reference Library/Manuals & Datasheets/6ES72121AE400XB0_datasheet_en.pdf"),
    }
    rows = load_cad_manifest(args.cad_manifest)
    links = datasheet_links(rows, known_datasheets)
    tests = acceptance_tests(rows)
    for path in (args.registry, args.datasheet_csv, args.tests_csv):
        path.parent.mkdir(parents=True, exist_ok=True)
    args.registry.write_text(registry_xml(links, tests), encoding="utf-8")
    args.datasheet_csv.write_text(datasheet_csv(links), encoding="utf-8")
    args.tests_csv.write_text(acceptance_test_csv(tests), encoding="utf-8")
    print(f"Wrote {len(links)} document links to {args.registry}")
    print(f"Wrote {len(links)} datasheet rows to {args.datasheet_csv}")
    print(f"Wrote {len(tests)} acceptance-test rows to {args.tests_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
