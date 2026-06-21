# FreeCAD Controls Engineering Workbench

## Overview

This workbench is a model-based controls-engineering system for FreeCAD. Its purpose is to make one controls project model drive PLC I/O lists, ladder/logic documentation, 3D panel layout, wiring tables, power-distribution records, sensor installation data, BOMs, and XML interchange.

## Core concept

The central object is the controls project model. CAD geometry is a view of that model, not the master source of engineering truth.

```text
Signal Registry -> I/O List -> Ladder References -> Wiring -> Terminals -> BOM -> Panel Layout
```

## Main modules

| Module | Purpose |
|---|---|
| PLC I/O | PLCs, racks, slots, modules, channels, tags, addresses |
| Logic | Internal rung graph and ladder documentation |
| Panel Layout | Enclosures, backplates, DIN rail, wire duct, device placement |
| Wiring | Wire records, from/to lists, terminal schedules |
| Power | Disconnects, breakers, fuses, power supplies, load budgets |
| Sensors | Field devices, installation notes, signal metadata |
| XML | CEProject schema and mappings to industry exchange formats |

## Validation philosophy

The tool should report errors before exporting deliverables. Examples:

- Duplicate tags.
- Duplicate PLC addresses.
- Missing part numbers.
- Signal has no terminal assignment.
- Load has no power source.
- 24 VDC budget exceeds power supply rating.

## XML standards direction

The internal XML format is `CEProject`. It should map outward to existing standards instead of pretending to replace them:

- PLCopen XML for IEC 61131-3 project/logic interchange.
- AutomationML/CAEX for plant engineering topology and cross-domain integration.
- OPC UA NodeSet2 for runtime information model exports.
- STEP/AP242-related references for product/geometry data where needed.
