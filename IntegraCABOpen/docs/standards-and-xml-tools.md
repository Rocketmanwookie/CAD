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
