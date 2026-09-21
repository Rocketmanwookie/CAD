# integraCAD Open Master TODO

This file tracks the project scope, roadmap, interoperability commitments, documentation obligations, and companion workbench ideas for integraCAD Open. ControlForgeCAD remains the current FreeCAD workbench/module name.

## 0. Working identity

- [x] Use `integraCAD Open` as the project-facing name.
- [x] Keep `ControlForgeCAD` as the current FreeCAD workbench/module name.
- [ ] Decide whether a repository/folder rename is warranted; do not rename generated-artifact paths without a migration plan.
- [ ] Decide whether a Python package rename is warranted; preserve import compatibility if it is.
- [x] Use FreeCAD workbench/menu label: `Controls / Automation`.
- [x] Keep XML project format name: `CEProject`.
- [x] Keep tagline: `The open-source FreeCAD workbench that unites PLC controls with CAD.`
- [ ] Avoid the trademark symbol in filenames, Python imports, XML namespaces, or package identifiers.

## 1. Product philosophy

- [ ] Keep the core workbench light, integration-first, and useful before it is polished.
- [ ] Avoid brand-heavy engineering behavior; let open-source contributors improve packaging, themes, icons, installers, docs, and distribution when the structure is easy to work with.
- [ ] Prefer adapters into existing FreeCAD/openBIM resources instead of recreating mature tools.
- [x] Treat integraCAD Open as a controls-engineering orchestration layer: intake, validation, traceability, and handoff.
- [ ] Do not replace CADbase, BOM workbenches, BIM tools, TechDraw, Spreadsheet, PLC IDEs, HMI platforms, ERP systems, or vendor catalogs.
- [ ] Reduce project havoc: missing data, duplicate entry, stale assumptions, rework, quoting churn, procurement mistakes, and field surprises.

## 2. Core workbench responsibilities

- [x] Structured project intake.
- [x] Missing-data tracking.
- [ ] Role-based request templates.
- [x] CEProject XML source-of-truth model for the currently supported intake-related fact surface.
- [ ] Validation of missing, contradictory, assumed, estimated, and unapproved values.
- [ ] Traceability between requirements, devices, signals, terminals, circuits, CADbase parts, cost records, and exports.
- [ ] Adapter layer to CADbase, BOM tools, BIM/openBIM tools, spreadsheets, TechDraw, and future PLC/HMI/digital-twin tools.
- [ ] Controls-specific XML schema versioning and migration notes.
- [ ] Example projects that are non-proprietary and safe to publish.

## 3. Explicit non-goals

- [ ] Do not build a full BOM workbench.
- [ ] Do not build a full CAD component-library manager if CADbase can handle it.
- [ ] Do not build a full BIM/MEP electrical design platform.
- [ ] Do not build a proprietary PLC IDE.
- [x] Do not build a full HMI editor inside the first integraCAD workbench.
- [x] Do not build a digital twin simulator inside the first integraCAD workbench.
- [ ] Do not redistribute vendor CAD files, datasheets, or catalog data without clear rights.
- [ ] Do not claim automatic code, panel, or installation compliance.

## 4. Core roadmap by phase

### Phase 0 - Repository and governance

- [x] Establish integraCAD Open as the project-facing documentation name while retaining ControlForgeCAD for the current workbench/module.
- [x] Add contributor guide.
- [ ] Add issue templates.
- [ ] Add pull request template.
- [ ] Add coding style guide.
- [ ] Add schema style guide.
- [ ] Add external-asset policy.
- [ ] Add versioning and migration policy for CEProject XML.
- [ ] Add architecture decision record folder: `docs/adr/`.
- [ ] Add roadmap issue labels: `roadmap`, `intake`, `xml`, `adapter`, `documentation`, `learning`, `hmi`, `digital-twin`, `bim`, `cadbase`, `bom`, `costing`.

### Phase 1 - Intake-first workflow

- [x] Build project intake schema section.
- [x] Add contacts/stakeholder model.
- [x] Add question/response model.
- [x] Add missing-data matrix.
- [x] Add field status model: `Unknown`, `Requested`, `Received`, `Assumed`, `Estimated`, `Verified`, `Approved`, `Rejected`, `Superseded`.
- [x] Add source record model for email, meeting note, uploaded file, phone call, field note, vendor quote, CADbase asset, BIM object, or manual entry.
- [x] Add starter role-based request templates for the project-manager, electrical-feed, environmental, safety, controls-platform, and sensor/I/O workflows.
- [ ] Complete template coverage for sales, utility, operations, purchasing, maintenance, IT/OT, and customer stakeholders, and map every requested fact to CEProject fields.
- [x] Add validation output that tells the user who to ask for missing information.
- [x] Add CSV export for the missing-data matrix.
- [x] Expose starter intake validation and missing-data preview through FreeCAD workbench commands.
- [x] Create a real editable FreeCAD `CE_Project` document object for starter intake data.
- [x] Synchronize editable `CE_Project` properties into backend validation and missing-data intake payloads.
- [x] Add a New Project / Intake dialog for editing starter project intake values.

### Phase 2 - CEProject data model

- [ ] Define top-level schema sections: `Project`, `Contacts`, `Intake`, `Requirements`, `BIMReferences`, `CADbaseReferences`, `Devices`, `Signals`, `Circuits`, `PowerInterface`, `SafetyFunctions`, `HMIRequirements`, `CostingReferences`, `ExternalExports`, `ValidationFindings`.
- [x] Version the schema with XSD file name and internal `schemaVersion`.
- [x] Add pure-Python import for the supported CEProject intake XML structure.
- [x] Add export/import round-trip tests for intake metadata, contacts, source records, questions, validation findings, and missing-data rows.
- [x] Expose CEProject intake XML export through a FreeCAD workbench command.
- [x] Add Project Intake import for supported CEProject XML and remember imported XML on the editable `CE_Project` object for later selection.
- [x] Add project setup/import adapters for YAML and UML-derived interchange where practical.
- [x] Make every project fact addressable by ID.
- [x] Assign immutable CE identities and controlled roles immediately to current
  project and starter layout FreeCAD objects.
- [ ] Carry CE identities, roles, and references through the CEProject XSD and
  deterministic import/export round trip.
- [ ] Extend immediate identity assignment to devices, ports, PLC
  racks/modules/channels, signals, nets, terminals, wires, and cables as those
  typed entities are implemented.
- [ ] Make every generated artifact traceable to source fields.
- [ ] Support assumptions and estimates without treating them as verified values.
- [ ] Add migration notes from schema `0.1` to future versions.

### Phase 3 - Power drop-in and BIM/MEP interface

- [ ] Add `PowerDropReference` object.
- [ ] Track upstream transformer/source equipment.
- [ ] Track source distribution equipment and circuit ID.
- [ ] Track voltage, phase, frequency, feeder ampacity, conductor/raceway reference, available fault current, grounding system, disconnecting means, metering requirements, source drawing, and BIM object reference.
- [x] Add starter controlled-load lines on `CE_Project` and estimate load amperage from phase/voltage with 20 percent spare capacity.
- [ ] Calculate estimated amperage from configured phase/voltage and load assumptions once load data exists, including motors, heat strips, VFDs, DC power supplies, Ethernet/network equipment, controlled coils/relays/contactors, spare capacity, and diversity assumptions.
- [ ] Integrate with IFC/ifcXML references where available.
- [ ] Export unresolved coordination items as BCF-style issues later.
- [ ] Do not duplicate the full building electrical model.
- [x] Define the boundary: BIM/MEP owns distribution up to the cabinet; integraCAD Open owns the cabinet-side controls package from the main disconnect inward.

### Phase 4 - CADbase integration

- [ ] Treat CADbase as the preferred local component/CAD/datasheet library.
- [ ] Store CADbase references in CEProject rather than duplicating library content.
- [ ] Track CADbase part ID, model asset ID, datasheet asset ID, revision, source URL, local path, checksum, approval status, and last verified date.
- [x] Seed hardware catalog CADbase references for Siemens S7-1200 CPU STEP/SLDPRT files with local path and checksum metadata.
- [x] Apply selected PLC CPU catalog metadata to the starter PLC layout placeholder.
- [x] Add an approval-gated Siemens CAx asset-request manifest for selected seeded PLC parts; it records official sources but does not automate portal downloads.
- [x] Add a neutral XML equipment taxonomy and a source-traceable Siemens S7-1200 record seed that can grow without making vendor fields mandatory in the core domain.
- [ ] Audit the imported Siemens S7-1200 record seed against current manufacturer documents and mark individual records verified only after review.
- [ ] Add adapter for selected device to CADbase part reference.
- [ ] Add policy for official manufacturer sources and redistribution limits.
- [ ] Add manual upload path when download is unavailable or restricted.

### Phase 5 - BOM and costing integration

- [ ] Do not own BOM generation natively unless no adequate existing tool exists.
- [ ] Provide normalized BOM source records.
- [ ] Add adapter to existing FreeCAD BOM workbench or equivalent BOM tools.
- [ ] Add Spreadsheet export adapter.
- [ ] Add purchasing/quote CSV adapter.
- [ ] Add cost item reference model: device -> CADbase part -> BOM source item -> cost item -> quote item -> purchase item.
- [ ] Track quantity, unit, source device, library part reference, unit cost, quoted cost, lead time, vendor, quote number, cost code, and revision.
- [ ] Support estimated, quoted, approved, and superseded cost statuses.

### Phase 6 - PLC/I/O controls package

**Immediate MVP path:** finish the rack/module/channel model, typed terminal and
wire graph, persistent 3D connection ports, and coordinated exports before
starting digital-twin runtime work.

- [x] Add PLC platform requirement fields.
- [ ] Add rack/slot/module/channel model.
- [x] Add starter signal registry.
- [x] Add I/O count estimates and starter unmapped assignments.
- [x] Validate PLC CPU onboard I/O capacity and suggest compatible expansion modules with 20 percent spare capacity.
- [x] Seed an XML-backed Siemens S7-1200 starter catalog with source-backed CPU and I/O module part numbers.
- [ ] Add signal-to-device, signal-to-terminal, signal-to-wire, and signal-to-HMI relationships.
- [ ] Add PLCopen XML export plan.
- [ ] Add vendor-neutral export first; vendor-specific adapters later.
- [ ] Include ladder/logic references without becoming a full PLC IDE.

### Phase 7 - Wiring, terminals, and cabinet-side power

- [x] Export a deterministic, validated terminal plan from the typed electrical graph.

- [x] Add starter terminal strip reference model.
- [x] Add a persisted, deterministic signal-to-terminal-to-wire connection-record foundation; it is not a schematic netlist or compliance engine.
- [x] Add the first fixed, deterministic continuous path contract from PLC channel
  terminal through ordered cabinet terminal levels and wire segments to the
  field-device terminal, including route-derived length and shared wiring/I/O
  schedule projections.
- [x] Materialize continuous paths as typed FreeCAD path, terminal, and wire
  objects with ordered links, immediate identity/role assignment, route/length
  properties, and preflight duplicate-identity rejection.
- [x] Embed continuous paths in CEProject through an explicit namespace/XSD
  import with typed round trips and duplicate path-identity validation.
- [x] Add whole-project duplicate/dangling-reference validation across current
  paths, terminal owners, signals, terminal endpoints, and wires.
- [x] Add typed signal/path/device link collections and canonical fact IDs to the
  `CE_Project` aggregate; register materialized signals and paths automatically.
- [x] Connect typed electrical graph reconstruction and whole-project findings to
  the existing FreeCAD validation command.
- [x] Add typed field-device creation with immediate identity/role assignment and
  project registration; automatically register placed PLC controllers and
  terminal strips as electrical device occurrences.
- [x] Add the first user-facing path creation workflow with registered owner
  selection, optional immediately identified field-device creation, a fixed
  PLC-terminal/terminal-strip/device-terminal chain, conductor metadata, and
  transaction-safe materialization.
- [x] Accept ordered 3D route coordinates during path creation, validate finite
  point sequences, persist them on typed wires, and derive schedule length from
  the routed polyline while retaining a separate specified-length input.
- [x] Add identity-preserving editing of signal tags, terminal designations,
  conductor metadata, specified lengths, and 3D routes for a selected path.
- [x] Add graphical 3D route selection for existing paths through selected-geometry vertex capture and the dependency-free Part-polyline fallback.
- [x] Integrate the optional FreeCAD Cables workbench as the physical wire/cable
  routing engine through `WireFlex`, with two-sided identity-safe links from each
  `CE_Wire` to its Cables route object; retain the Part polyline fallback when
  Cables is not installed.
- [x] Add a workbench command that exports canonical wiring and I/O path CSV
  schedules from the typed electrical graph.
- [x] Add a standalone namespace-correct, XSD-validated connection-path XML
  contract with deterministic round trips and semantic continuity validation.
- [x] Add route-derived wire length, conductor size/color/function/conduit fields
  to the canonical path and wiring-schedule projection.
- [x] Add profile-driven raceway fill calculation using NEC Chapter 9 Table 1
  fill percentages and caller-supplied edition/raceway/conductor areas.
- [ ] Add licensed/verified edition-specific conductor and raceway dimension data.
- [ ] Add complete conductor ampacity, correction/adjustment, terminal-rating,
  voltage-drop, protection, and project/AHJ sizing inputs before recommending a
  conductor size.
- [ ] Add project wire-color profiles that distinguish required/reserved
  identification from documented plant conventions.
- [ ] Add wire/from-to reference model.
- [ ] Add internal cabinet power circuits.
- [ ] Add control power distribution.
- [ ] Add protective-device references.
- [ ] Add VFD/motor branch references.
- [ ] Add sensor cable and field junction references.
- [ ] Feed wiring/terminal data to drawing or schedule tools.
- [x] Add starter CAD-side placeholder objects for panel/backplate, DIN rail, wire duct, terminal strip, and PLC rack/module.
- [x] Seed XML-backed generic panel hardware placeholders for backplate, DIN rail, wire duct, and terminal strip starter BOM metadata.

### Phase 8 - HMI as future companion workbench

- [ ] Create companion concept: `IntegraHMI Open` or `HMI / SCADA Design`.
- [ ] Keep HMI GUI design out of the initial core workbench.
- [ ] Define tag dictionary export from CEProject.
- [ ] Define screen requirements, alarm requirements, equipment hierarchy, modes/states, navigation, faceplate needs, trends, historian points, and operator actions.
- [ ] Include ISA-101/high-performance HMI concepts in documentation.
- [ ] Start vendor-neutral HMI requirements format before platform-specific adapters.
- [ ] Later adapters may target Ignition, FactoryTalk View, AVEVA/Wonderware, WinCC, and other systems only if legal/technical access is practical.

### Phase 9 - Digital twin as future companion workbench

- [ ] Create companion concept: `IntegraTwin Open` or `Digital Twin / Simulation`.
- [ ] Keep digital twin simulation out of the initial core workbench.
- [ ] Define links from CEProject to geometry, I/O state, simulated sensors, actuators, states, sequences, faults, and HMI behavior.
- [x] Select ROS/ROS 2 integration as the future digital-twin runtime boundary.
- [ ] Define CEProject-to-ROS 2 identity mapping for devices, I/O, terminals,
  geometry, state, commands, alarms, and simulation time.
- [ ] Define ROS 2 messages, services, actions, or adapters without making ROS a
  dependency of the core FreeCAD workbench.
- [ ] Evaluate Gazebo and other ROS-compatible simulators after the electrical
  graph and working MVP are stable.
- [ ] Add a future ROS/ROS 2 simulator boundary document.

### Phase 10 - Education docs for new controls engineers

- [x] Add `docs/learning-path.md`.
- [x] Add `docs/glossary.md`.
- [ ] Add `docs/resources.md`.
- [ ] Explain the interdisciplinary map: electrical power, controls, PLCs, CAD, sensors, pneumatics/hydraulics, motion, motor control, industrial networks, machine safety, HMI/SCADA, data/historians, cybersecurity, BIM/openBIM, costing, documentation, project management, commissioning, and maintenance.
- [ ] Link official resources where possible.
- [ ] Do not duplicate copyrighted manuals or standards text.
- [ ] Provide beginner examples: small conveyor panel, pump skid, robot cell I/O cabinet, simple building automation panel.
- [ ] Add practical checklists and vocabulary, not just theory.

## 5. Stakeholder intake templates to build

- [ ] Sales / estimator intake.
- [ ] Project manager intake.
- [ ] Customer engineering intake.
- [ ] Utility company electrical feed request.
- [ ] Electrical engineering feed and SCCR/fault-current request.
- [ ] Building superintendent/site conditions request.
- [ ] Safety/EHS requirements request.
- [ ] Controls platform standards request.
- [ ] IT/OT network and cybersecurity request.
- [ ] Mechanical/materials-handling sensor and sequence request.
- [ ] Operations/maintenance preference request.
- [ ] Purchasing/vendor/lead-time request.
- [ ] Commissioning and startup constraints request.

## 6. Required question domains

- [ ] Electrical feed: voltage, phase, frequency, transformer, source panel, circuit, breaker/fuse, feeder ampacity, conductor, raceway, grounding, available fault current, required SCCR, utility/company requirements.
- [ ] Environmental: indoor/outdoor, temperature, humidity, dust, washdown, corrosive exposure, vibration, area classification, NEMA/IP rating, enclosure material, cooling/heating.
- [ ] Equipment and process: machine type, sequence, throughput, motors, drives, actuators, materials handled, jam/fault conditions, manual modes, maintenance modes.
- [ ] I/O and sensors: sensor count, type, signal level, analog scaling, field wiring, connector type, junction boxes, spare I/O, calibration, installation constraints.
- [ ] Safety: E-stops, guards, light curtains, STO, safety relays/controllers, reset, EDM/feedback, zones, risk assessment references, required safety standard references.
- [ ] PLC/controls: preferred platform, programming standard, tag naming, network type, HMI/SCADA, alarms, historian, remote access, cybersecurity, backup policy.
- [ ] HMI: screens, operator tasks, alarm philosophy, trends, recipes, users, access levels, equipment hierarchy, state/mode model.
- [ ] BIM/site: room/space, panel location, upstream source references, raceway routes, IFC object references, COBie handoff expectations, BCF issue workflow.
- [ ] Cost/schedule: budget, quote deadline, delivery deadline, lead-time constraints, approved vendors, substitutions, alternates, labor assumptions, commissioning window.
- [ ] Documentation: drawing package, submittals, O&M manuals, datasheet package, training docs, FAT/SAT/IQ/OQ style requirements where applicable.

## 7. Standards and interoperability watchlist

### Schematic-symbol library

- [ ] Define a namespace-correct, XSD-validated neutral symbol-library contract
  with immutable definition/occurrence identity separation and structured pins.
- [ ] Seed IEC and NFPA/JIC variants for PLC CPU and I/O modules, power supplies,
  terminal blocks, fuses, breakers, contactor coils and contacts, overloads,
  safety relays, emergency stops, illuminated buttons, pull-rope switches, limit
  switches, stack-light elements, HMIs, receptacles, and two-wire 4–20 mA
  temperature/pressure transmitters.
- [ ] Add parent/child cross-references, terminal/pin maps, insertion points,
  rotation/mirroring rules, and device-tag propagation.
- [ ] Link every placed symbol occurrence to the same equipment occurrence and
  `CEIdentity` used by the 3D object, electrical path, BOM, and schedules.
- [ ] Add deterministic schematic-sheet and ladder/rung rendering from smart nets.
- [x] Link every CAD acquisition request to an XSD-validated datasheet registry
  with local/checksummed, pending-download, or pending-part-selection state and
  export category-aware library acceptance-test instructions to CSV.
- [ ] Download and verify the outstanding official datasheets, populate revision
  and document-date metadata, and resolve exact MLFBs before marking tests passed.

- [ ] FreeCAD workbench/addon architecture.
- [ ] FreeCAD BIM and IFC workflows.
- [ ] FreeCAD Spreadsheet/BOM/TechDraw resources.
- [ ] CADbase or equivalent local library workflows.
- [ ] PLCopen XML / IEC 61131-3.
- [ ] AutomationML / CAEX.
- [ ] OPC UA / NodeSet2 XML.
- [ ] IFC / ifcXML / openBIM.
- [ ] COBie / asset handoff.
- [ ] BCF / model coordination issues.
- [ ] ETIM / ECLASS / IEC CDD product classification.
- [ ] ISA-101 HMI guidance.
- [ ] ISA/IEC 62443 industrial cybersecurity guidance.
- [ ] NEC / NFPA 70, NFPA 79, UL 508A, IEC 60204-1, ISO 13849, IEC 62061, IEC 61508 as reference domains; do not reproduce restricted text.
- [ ] FMI/FMU and ROS 2 for future digital twin links.

## 8. Validation engine backlog

- [x] Missing required data by selected deliverables.
- [ ] Contradictory voltage/phase values.
- [ ] Missing available fault current.
- [ ] Missing SCCR target.
- [ ] Missing enclosure/environmental rating.
- [x] Missing PLC platform.
- [ ] Missing preferred vendors.
- [x] Missing sensor count or I/O estimate.
- [ ] Missing HMI requirement set.
- [ ] Missing upstream BIM/feed reference.
- [ ] Missing CADbase part reference.
- [ ] Missing BOM export mapping.
- [ ] Missing cost item reference.
- [ ] Unverified assumption used in a deliverable.
- [ ] Superseded answer still referenced.
- [ ] Conflicting answers from different stakeholders.

## 9. Open-source maintainability

- [x] Use small, readable modules.
- [ ] Keep schema examples human-readable.
- [ ] Keep dependencies minimal.
- [x] Add tests for deterministic CEProject XML intake export.
- [x] Add tests for CEProject XML intake import and round-trip behavior.
- [x] Add FreeCAD workbench smoke tests for import-safe init files and command metadata.
- [x] Add documented FreeCAD user `Mod` install/link workflow.
- [ ] Add tests for XML examples and validators.
- [ ] Add CI later if GitHub Actions access is available.
- [ ] Add documentation build later.
- [ ] Keep all sample data non-proprietary.
- [ ] Provide clear extension points for adapters.
- [ ] Make packaging easy for the FreeCAD Addon Manager when the project matures.

## 10. Business thesis

- [ ] Less havoc = more money.
- [ ] Less missing information = fewer redesigns.
- [ ] Less duplicate entry = fewer clerical errors.
- [ ] Less vendor chasing = faster quoting and purchasing.
- [ ] Less drawing churn = better schedule control.
- [ ] Less field surprise = better margin.
- [ ] Capture once; validate early; reuse everywhere.
