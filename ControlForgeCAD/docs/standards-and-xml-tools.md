# XML Standards and Tools

## Internal format: CEProject

`CEProject` is the internal project interchange format for this workbench. It should remain simple, documented, versioned, and validated with XSD.

## External mapping targets

| Target | Role |
|---|---|
| PLCopen XML | IEC 61131-3 project and logic interchange |
| AutomationML / CAEX | Plant engineering topology and cross-domain integration |
| OPC UA NodeSet2 | Runtime data/information model export |
| STEP/AP242 references | CAD/product-data integration where applicable |

## Python XML tools

| Tool | Use |
|---|---|
| `xml.etree.ElementTree` | Simple built-in parsing and writing |
| `lxml` | XSD validation, XPath, richer XML tooling |
| `xsdata` | Python dataclasses from XSD, future option |
| `xmlschema` | XSD validation and data conversion, future option |

## Repo tools

- `schemas/ce_project_v0_1.xsd` defines the first draft schema.
- `examples/conveyor_demo.ceproject.xml` is the initial demo project.
- `stubs/` should contain outward mapping examples.
