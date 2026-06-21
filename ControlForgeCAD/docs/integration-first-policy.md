# Integration-First Policy

IntegraCAB Open should integrate with existing FreeCAD, openBIM, CADbase, BOM, spreadsheet, drawing, PLC, and future HMI/digital-twin resources instead of replacing them.

## Principle

Capture once. Validate early. Reuse everywhere.

IntegraCAB Open exists to reduce controls-engineering chaos by collecting project requirements, recording assumptions, validating missing data, and feeding downstream tools from one structured source of truth.

## What IntegraCAB owns

- Project intake and missing-data tracking.
- Role-based request templates.
- CEProject XML schema.
- Controls requirements and traceability.
- Power drop-in reference from BIM/MEP/electrical teams.
- PLC/I/O and signal registry source data.
- HMI requirement source data for a future companion workbench.
- Digital twin requirement source data for a future companion workbench.
- Validation findings and coordination records.
- Adapter mappings to external tools.

## What IntegraCAB should not replace

| Area | Preferred owner |
|---|---|
| Reusable CAD parts, datasheets, CAD files | CADbase or equivalent library |
| BOM generation | Existing FreeCAD BOM workbench, Spreadsheet, BIM schedules, or ERP/export tools |
| BIM/facility model | FreeCAD BIM/openBIM tools and IFC workflows |
| Drawing sheet production | TechDraw or other drawing tools |
| Full PLC programming IDE | Vendor PLC IDEs or PLCopen-compatible tools |
| HMI screen editor | Future HMI companion workbench or vendor HMI tools |
| Simulation/digital twin engine | Future digital twin companion workbench or external simulators |
| Product certification/compliance | Qualified engineering review and applicable standards processes |

## Adapter pattern

```text
CEProject XML
    -> CADbase references
    -> BOM source rows
    -> Spreadsheet exports
    -> TechDraw annotations
    -> IFC/COBie/BCF references
    -> PLCopen XML mappings
    -> AutomationML mappings
    -> OPC UA NodeSet2 mappings
    -> Future HMI requirements
    -> Future digital twin requirements
```

## Power drop-in boundary

BIM/MEP/electrical tools own the building electrical distribution up to the cabinet boundary. IntegraCAB owns the cabinet-side controls package from the main disconnect inward.

## Documentation rule

When an existing tool or standard already owns a domain, IntegraCAB documentation should point to that resource and explain how IntegraCAB integrates with it. It should not duplicate entire manuals, standards, or proprietary vendor instructions.
