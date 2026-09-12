#!/usr/bin/env python3
"""Explore a normalized integraCAD equipment-record XML catalog."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "ControlForgeCAD"))

from controls_wb.equipment_records import (  # noqa: E402
    categories,
    default_siemens_records_path,
    load_equipment_records,
    record_by_part_number,
    search_records,
)


def _print_record(record) -> None:
    print(f"{record.part_number} | {record.category} | {record.product_name}")
    if record.summary:
        print(f"  {record.summary}")
    print(f"  source: {record.source_id} {record.source_locator}".rstrip())
    print(f"  verified: {str(record.verified).lower()}")
    for name, value in sorted(record.properties.items()):
        print(f"  {name}: {value}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=default_siemens_records_path())
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--categories", action="store_true", help="List categories and record counts")
    group.add_argument("--search", help="Search names, part numbers, categories, summaries, and properties")
    group.add_argument("--part", help="Show one exact part number")
    args = parser.parse_args()
    catalog = load_equipment_records(args.catalog)

    if args.categories:
        counts = Counter(record.category for record in catalog.records)
        for category in categories(catalog):
            print(f"{category}: {counts[category]}")
        return 0
    if args.part:
        record = record_by_part_number(catalog, args.part)
        if record is None:
            print(f"No exact part-number match: {args.part}", file=sys.stderr)
            return 1
        _print_record(record)
        return 0
    if args.search is not None:
        matches = search_records(catalog, args.search)
        for record in matches:
            print(f"{record.part_number} | {record.category} | {record.product_name}")
        print(f"{len(matches)} match(es)")
        return 0

    print(f"{catalog.manufacturer} {catalog.family} - {catalog.edition}")
    print(f"Records: {len(catalog.records)}")
    print(f"Categories: {len(categories(catalog))}")
    print("Use --categories, --search TEXT, or --part PART_NUMBER to explore.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
