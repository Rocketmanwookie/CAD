# FreeCAD Controls / Automation Workbench

## Overview

IntegraCAB Open is a model-based controls-engineering workbench concept for FreeCAD. It is intended to make one structured controls project model feed PLC I/O lists, HMI requirements, cabinet layout, wiring tables, safety-circuit records, power-interface records, sensor installation data, BOM source rows, costing references, and XML interchange.

## Core concept

```text
Project Intake -> CEProject XML -> Validation -> Existing FreeCAD/openBIM/CADbase/BOM tools
```

## Main modules

| Module | Purpose |
|---|---|
| Intake | Stakeholders, questions, responses, missing data |
| PLC I/O | PLCs, racks, slots, modules, channels, tags, addresses |
| Panel Layout | Enclosures, backplates, DIN rail, wire duct, device placement |
| Wiring | Wire records, from/to lists, terminal schedules |
| Power Interface | Transformer/feed/circuit references from BIM/MEP/electrical teams |
| Safety | Safety functions, E-stops, safety relays, STO circuits |
| HMI Requirements | Future companion-workbench input |
| XML | CEProject schema and mappings to industry exchange formats |
