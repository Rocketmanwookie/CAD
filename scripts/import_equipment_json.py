#!/usr/bin/env python3
"""Convert a structured vendor JSON catalog into deterministic equipment XML."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET


RESERVED_PRODUCT_FIELDS = {
    "manufacturer",
    "family",
    "category",
    "product_name",
    "article_number",
    "summary",
    "catalog_source",
    "source_page",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _xml_id(prefix: str, value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip()).strip("-").lower()
    return f"{prefix}-{slug or 'unknown'}"


def _value_type(value: object) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, list):
        return "list"
    return "string"


def _value_text(value: object) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    return str(value)


def build_catalog(
    source_path: Path,
    datatype_path: Path | None = None,
    aliases: tuple[Path, ...] = (),
    assets: tuple[Path, ...] = (),
    references: tuple[Path, ...] = (),
) -> ET.ElementTree:
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    metadata = payload["catalog"]
    products = payload["products"]
    root = ET.Element(
        "equipmentRecords",
        {
            "schemaVersion": "0.1.0",
            "catalogId": _xml_id("catalog", f"{metadata['manufacturer']}-{metadata['family']}-{metadata['edition']}"),
            "manufacturer": metadata["manufacturer"],
            "family": metadata["family"],
            "edition": metadata.get("edition", ""),
            "recordCount": str(len(products)),
        },
    )
    sources_element = ET.SubElement(root, "sources")
    catalog_source_id = "source-siemens-s7-1200-2017-brochure-catalog"
    source_element = ET.SubElement(
        sources_element,
        "source",
        {
            "id": catalog_source_id,
            "title": products[0].get("catalog_source", metadata.get("edition", "Vendor catalog")),
            "sourceType": "normalized-json-catalog",
            "localPath": str(source_path),
            "sha256": _sha256(source_path),
        },
    )
    for alias in sorted(aliases, key=lambda item: str(item)):
        ET.SubElement(source_element, "alias", {"localPath": str(alias), "sha256": _sha256(alias)})

    datatype_source_id = "source-siemens-s7-1200-datatypes-v20"
    datatype_payload = None
    if datatype_path is not None:
        datatype_payload = json.loads(datatype_path.read_text(encoding="utf-8"))
        ET.SubElement(
            sources_element,
            "source",
            {
                "id": datatype_source_id,
                "title": datatype_payload["source_title"],
                "sourceType": "normalized-json-profile",
                "localPath": str(datatype_path),
                "url": datatype_payload.get("source_url", ""),
                "sha256": _sha256(datatype_path),
                "checkedDate": datatype_payload.get("checked_date", ""),
            },
        )

    for reference_path in sorted(references, key=lambda item: str(item)):
        suffix = reference_path.suffix.lower()
        source_type = {
            ".pdf": "reference-pdf",
            ".xsd": "reference-schema",
            ".json": "reference-json",
            ".py": "reference-adapter",
            ".md": "reference-documentation",
        }.get(suffix, "reference-file")
        digest = _sha256(reference_path)
        ET.SubElement(
            sources_element,
            "source",
            {
                "id": _xml_id("source", f"{reference_path.stem}-{digest[:10]}"),
                "title": reference_path.stem.replace("_", " "),
                "sourceType": source_type,
                "localPath": str(reference_path),
                "sha256": digest,
            },
        )

    if assets:
        assets_element = ET.SubElement(root, "assets")
        for asset_path in sorted(assets, key=lambda item: str(item)):
            suffix = asset_path.suffix.lstrip(".").upper()
            ET.SubElement(
                assets_element,
                "asset",
                {
                    "id": _xml_id("asset", asset_path.name),
                    "kind": "cad-model" if suffix in {"STEP", "STP", "SLDPRT"} else "reference-image",
                    "format": suffix,
                    "localPath": str(asset_path),
                    "sha256": _sha256(asset_path),
                    "applicability": "family-reference-unverified",
                    "verified": "false",
                },
            )

    if datatype_payload is not None:
        profiles_element = ET.SubElement(root, "profiles")
        profile = ET.SubElement(
            profiles_element,
            "profile",
            {
                "id": "profile-s7-1200-datatypes-v20",
                "profileType": "programming-data-types",
                "title": datatype_payload["source_title"],
                "basis": datatype_payload.get("tia_version_basis", ""),
                "published": datatype_payload.get("publication_date", ""),
                "sourceId": datatype_source_id,
            },
        )
        ET.SubElement(profile, "note").text = datatype_payload.get("scope_note", "")
        for value in datatype_payload.get("types", []):
            ET.SubElement(profile, "value").text = str(value)

    records_element = ET.SubElement(root, "records")
    seen_ids: set[str] = set()
    for product in sorted(products, key=lambda item: (item.get("category", ""), item.get("article_number", ""))):
        part_number = product.get("article_number", "")
        record_id = _xml_id("part", part_number)
        if record_id in seen_ids:
            raise ValueError(f"Duplicate article number: {part_number}")
        seen_ids.add(record_id)
        locator = f"page {product['source_page']}" if product.get("source_page") else ""
        record = ET.SubElement(
            records_element,
            "record",
            {
                "id": record_id,
                "category": product.get("category", ""),
                "productName": product.get("product_name", ""),
                "partNumber": part_number,
                "sourceId": catalog_source_id,
                "sourceLocator": locator,
                "verified": "false",
            },
        )
        if product.get("summary"):
            ET.SubElement(record, "summary").text = product["summary"]
        extra_fields = [(key, value) for key, value in product.items() if key not in RESERVED_PRODUCT_FIELDS]
        if extra_fields:
            properties = ET.SubElement(record, "properties")
            for key, value in sorted(extra_fields):
                property_element = ET.SubElement(properties, "property", {"name": key, "valueType": _value_type(value)})
                property_element.text = _value_text(value)
    ET.indent(root, space="  ")
    return ET.ElementTree(root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--datatypes", type=Path)
    parser.add_argument("--alias", action="append", default=[], type=Path)
    parser.add_argument("--asset", action="append", default=[], type=Path)
    parser.add_argument("--reference", action="append", default=[], type=Path)
    args = parser.parse_args()
    tree = build_catalog(args.source, args.datatypes, tuple(args.alias), tuple(args.asset), tuple(args.reference))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(args.output, encoding="utf-8", xml_declaration=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
