# XML Standards and Tools

## Internal format: CEProject

`CEProject` is the internal project interchange format for this workbench. It should remain simple, documented, versioned, and validated with XSD.

CEProject is not intended to replace existing open standards. It should hold controls-package intake, requirements, validation status, and references, then map outward to the right external resource.

## Integration-first standard targets

| Target | Role |
|---|---|
| PLCopen XML | IEC 61131-3 project and logic interchange |
| AutomationML / CAEX | Plant engineering topology and cross-domain integration |
| OPC UA NodeSet2 | Runtime data/information model export |
| IFC / ifcXML | BIM/facility/cabinet object handoff and upstream power references |
| COBie | Asset, component, maintenance, and handoff data |
| BCF | Coordination, validation findings, and issue handoff |
| CADbase references | Reusable CAD models, datasheets, and local part/library assets |
| BOM workbench / Spreadsheet | BOM and schedule output; IntegraCAB should provide source data and mappings |

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
- `templates/email/` contains stakeholder request templates.
- `templates/forms/` contains structured form schema seeds.
- `stubs/` should contain outward mapping examples.

## Do not duplicate

- Do not duplicate CADbase library records; store references.
- Do not duplicate BOM workbench data; provide BOM source records and adapters.
- Do not duplicate BIM/MEP electrical models; store upstream references.
- Do not copy restricted standards text into the repository.
- Do not commit proprietary vendor CAD or datasheet files unless redistribution rights are explicit.
