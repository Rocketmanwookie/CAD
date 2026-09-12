# AutoCAD Electrical PLC feature-parity audit

Audit date: 2026-09-12

## Verdict

ControlForgeCAD does **not** currently provide FreeCAD with complete AutoCAD
Electrical PLC/electrical-design feature parity. It is a pre-alpha data and
workflow foundation. Its strongest implemented areas are project intake,
source-backed equipment catalogs, elementary I/O records, connection schedules,
starter 3D placeholders, validation, and XML/CSV exports.

AutoCAD Electrical itself is not a complete executable PLC digital twin or a
vendor PLC programming environment. Its Inventor link associates 2D electrical
data with a 3D assembly, synchronizes properties, and supports wire routing. A
complete digital twin additionally needs runtime behavior, PLC program execution
or emulation, process models, live connectivity, and verification scenarios.

Status vocabulary: **Implemented** means usable code and automated tests exist;
**Partial** means a data seed or narrow export exists; **Missing** means no
working implementation was found; **External target** means an explicit
integration is preferable to rebuilding the capability here.

## Parity matrix

| Capability | ControlForgeCAD status | Evidence / missing acceptance criteria |
|---|---|---|
| Project and drawing management | Partial | One `CE_Project` object and intake data exist. No managed multi-drawing set, templates, title-block update, sheet references, plotting set, or project-wide retag/update engine. |
| IEEE/IEC/NFPA schematic symbols | Missing | No symbol schema, placement command, component-pin model, icon menu, or standards profile. |
| Intelligent wires and nets | Partial | `SignalConnection` explicitly says it is not a schematic netlist. Completion requires graph-backed nets, pins, potentials, cables/cores, junctions, wire styles, numbering, continuation references, edit propagation, and rule checks. |
| Component tagging and cross-reference | Missing | Duplicate-tag validation exists, but automatic project/drawing/rung tagging and live coil/contact or source/destination cross-references do not. |
| Ladder representation | Missing | No ladder/rung model, renderer, editor, or reference engine. |
| PLC module database | Partial | XML catalogs hold Siemens parts and channel counts. They lack complete terminal templates, per-channel electrical behavior, drawing graphics, addressing constraints, and a module editor. |
| Spreadsheet-driven PLC drawings | Partial | CSV I/O rows can be produced; there is no configurable spreadsheet mapping profile or automatic ladder/module/device/wire generator. |
| I/O addressing and labels | Partial | `IOSignal` holds core fields, but addressing is a simple sequential default. There is no device-specific allocator, rack optimizer, conflict resolution, or vendor round trip. |
| PLC software matching | Missing / External target | PLCopen mapping is a stub. Completion requires versioned adapters, stable identities, dry-run diffs, conflict handling, fixtures, and at least one validated TIA Portal interchange path. |
| Terminals | Partial | A terminal-strip placeholder and string fields exist. Typed levels, sides/pins, jumpers, bridges, accessories, destinations, ordering, spares, renumbering, and generated terminal plans are missing. |
| Terminals embedded in 3D parts | Missing | Current 3D objects expose counts and metadata, not geometric ports. Persistent port objects, connector coordinate systems, pin mappings, and placement-safe topology are required. |
| Panel layout and footprints | Partial | Parametric boxes exist for the panel, rail, duct, terminal strip, and PLC. Accurate footprints, constraints, clearances, rail snapping, cutouts, labels, balloons, and logical/physical reconciliation are missing. |
| 3D wire/cable routing | Missing / External target | No route graph, connector ports, path constraints, bend radius, duct fill, bundles, length calculation, or routing solver. |
| Parts catalog and footprint lookup | Partial | Extensible XML catalogs and Siemens seeds include provenance and CAD references. A full taxonomy, editor UI, revisions, compatibility rules, symbol/footprint resolver, and broad vendor coverage are missing. |
| Parametric parts | Partial | Box dimensions and PLC counts are parameterized. Terminal geometry, pin locations, module families, mounting rules, and manufacturer variants are not catalog-driven geometry. |
| BOM and reports | Partial | Basic BOM, I/O, missing-data, CEProject XML, and connection exports exist. Complete component/wire/connector/PLC/terminal/cable/audit reports, drawing tables, balloons, and reconciliation are missing. |
| Real-time electrical validation | Partial | Intake and basic tag/terminal checks exist. Voltage conflicts, pin compatibility, open/short nets, ampacity, terminal capacity, safety separation, and cross-sheet integrity are missing. |
| Electromechanical synchronization | Missing | CAD paths are references only. Immutable logical/occurrence IDs, sync journal, property ownership, diff UI, conflicts, and transactional reconciliation are required. |
| PLC logic representation | Missing | A ladder/FBD/ST representation and PLCopen importer/exporter are needed. Documentation-only networks must be distinguished from executable vendor logic. |
| Executable digital twin | Missing / Companion system | Requires deterministic state and scan cycles, sensor/actuator/process behavior, scenarios, fault injection, traces, OPC UA/Modbus/S7 connectivity, runtime/emulator adapters, and 3D state binding. |
| Revision and collaboration | Partial | Source records and schema versions exist. Object migrations, changesets, merge/conflict behavior, audit history, baseline comparison, and multi-user locking are missing. |

## Required architecture

Use one authoritative electrical graph instead of copying facts independently
into drawings, 3D objects, spreadsheets, and simulations.

```text
Equipment catalog + symbol/footprint/port definitions
                         |
                         v
CEProject electrical graph (devices, pins, nets, terminals, PLC channels)
       |                 |                    |
       v                 v                    v
2D schematic/ladder   3D panel/routing    reports/BOM/I-O
       |                 |                    |
       +-----------------+--------------------+
                         |
             versioned adapter boundary
       PLCopen / TIA / AutomationML / OPC UA
                         |
                         v
           simulation and digital-twin runtime
```

Core invariants:

1. Every device, occurrence, pin/port, terminal level, PLC channel, signal, net,
   wire, cable/core, and logic variable has a stable unique ID.
2. A PLC I/O label is one fact with mapped representations, not duplicated text.
3. Every 2D symbol and 3D part resolves to the same logical device.
4. Connections form a validated graph; schedules and drawings are projections.
5. Vendor imports are staged as diffs and never silently overwrite approved data.
6. Simulation cannot alter master engineering data without reviewed write-back.

## Delivery gates

### 1. Authoritative electrical graph

Expand CEProject and Python models for devices, ports, nets, terminal levels,
wires, cables/cores, PLC modules/channels, and mappings. Add integrity, uniqueness,
allocation, and compatibility rules. Migrate existing I/O and connection records.

### 2. Intelligent schematic and ladder editor

Add standards-profiled symbols, component insertion, smart wires, numbering,
ladders/rungs, cross-references, deterministic output, and golden-project tests.

### 3. Terminal and physical panel model

Add typed multilevel terminals, jumpers/accessories, terminal-strip editing and
plans, manufacturer footprints with geometric ports, rail/duct placement,
clearance rules, and physical/logical comparison.

### 4. Catalog automation and reporting

Add a catalog editor/import pipeline, symbol-footprint-port resolution, lifecycle
controls, configurable reports, and spreadsheet-to-PLC drawing generation.

### 5. PLC engineering adapters

Implement PLCopen XML first, followed by validated vendor adapters. Require
bidirectional I/O/tag/address diffs, conflict resolution, reproducible fixtures,
and explicit capabilities per vendor/version. Never imply lossless round-trip
when a vendor format cannot provide it.

### 6. 3D routing and digital twin

Add port-aware wire/cable routing, physical lengths, bend/duct constraints, and a
separate runtime service for scan cycles, behaviors, scenarios, faults,
telemetry, protocol adapters, and 3D animation/state binding.

The selected future runtime boundary is ROS/ROS 2. The core workbench must remain
usable without ROS installed. A later adapter will translate stable CEProject
identities and geometry bindings into ROS graph interfaces, simulation time,
commands, state, and telemetry. Simulator-specific integration belongs beyond
that adapter so Gazebo or another ROS-compatible runtime can be replaced without
changing the electrical source of truth.

## Definition of parity

Parity may be claimed only when every in-scope row has automated acceptance
tests and a representative project round-trips through 2D schematics, 3D panel
layout, I/O assignment, terminal/wire reports, and the declared PLC adapter
without identity loss. “Complete digital twin” is a separate claim requiring
closed-loop runtime and scenario verification.

## Baseline sources

- Autodesk AutoCAD Electrical Toolset 2026 Hitchhiker's Guide
- Autodesk AutoCAD Electrical Toolset 2026 Quick Reference Guide
- Autodesk Electrical toolset feature list and schematic reports documentation
- Autodesk PLC database and spreadsheet-to-PLC documentation
- Autodesk AutoCAD Electrical–Inventor electromechanical documentation
