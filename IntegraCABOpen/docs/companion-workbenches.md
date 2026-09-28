# Companion Workbenches

IntegraCAB Open should remain focused on controls-engineering intake, validation, traceability, and integration with existing FreeCAD resources. HMI design and digital twin simulation are important enough to become companion workbenches later.

## Product family concept

```text
IntegraCAB Open      Controls / Automation intake and CAD integration
IntegraHMI Open      HMI / SCADA GUI design and requirements
IntegraTwin Open     Digital twin / simulation and I/O behavior
CADbase              Reusable CAD assets, datasheets, component library
BOM Workbench        BOM generation and schedule output
BIM/openBIM tools    IFC, COBie, BCF, spatial/facility handoff
```

## Shared source-of-truth rule

The companion workbenches should consume CEProject data instead of recreating it.
