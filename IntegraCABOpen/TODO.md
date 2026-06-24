# IntegraCAB Open Master TODO

## 0. Working identity

- [x] Rename working-title references from the historical seed name to `IntegraCAB Open`.
- [x] Use display name: `IntegraCAB™ Open`.
- [x] Use Python package name: `integracab`.
- [x] Use FreeCAD workbench/menu label: `Controls / Automation`.
- [x] Keep XML project format name: `CEProject`.
- [x] Keep tagline: `The open-source FreeCAD workbench that unites PLC controls with CAD.`
- [x] Avoid the trademark symbol in filenames, Python imports, XML namespaces, or package identifiers.

## 1. Product philosophy

- [ ] Keep the core workbench light, integration-first, and useful before it is polished.
- [ ] Let open-source contributors improve packaging, themes, icons, installers, docs, and distribution when the structure is easy to work with.
- [ ] Prefer adapters into existing FreeCAD/openBIM resources instead of recreating mature tools.
- [ ] Treat IntegraCAB Open as a controls-engineering orchestration layer: intake, validation, traceability, and handoff.
- [ ] Do not replace CADbase, BOM workbenches, BIM tools, TechDraw, Spreadsheet, PLC IDEs, HMI platforms, ERP systems, or vendor catalogs.
- [ ] Reduce project havoc: missing data, duplicate entry, stale assumptions, rework, quoting churn, procurement mistakes, and field surprises.

## 2. Core responsibilities

- [ ] Structured project intake.
- [ ] Missing-data tracking.
- [ ] Role-based request templates.
- [ ] CEProject XML source-of-truth model.
- [ ] Validation of missing, contradictory, assumed, estimated, and unapproved values.
- [ ] Traceability between requirements, devices, signals, terminals, circuits, CADbase parts, cost records, and exports.
- [ ] Adapter layer to CADbase, BOM tools, BIM/openBIM tools, spreadsheets, TechDraw, and future PLC/HMI/digital-twin tools.

## 3. Explicit non-goals

- [ ] Do not build a full BOM workbench.
- [ ] Do not build a full CAD component-library manager if CADbase can handle it.
- [ ] Do not build a full BIM/MEP electrical design platform.
- [ ] Do not build a proprietary PLC IDE.
- [ ] Do not build a full HMI editor inside the first IntegraCAB workbench.
- [ ] Do not build a digital twin simulator inside the first IntegraCAB workbench.
- [ ] Do not redistribute vendor CAD files, datasheets, or catalog data without clear rights.
- [ ] Do not claim automatic code, panel, or installation compliance.

## 4. Roadmap

- [ ] Phase 0: repository, governance, contributors, issue templates, schema style guide.
- [ ] Phase 1: project intake schema, stakeholder templates, missing-data matrix, source records.
- [ ] Phase 2: CEProject data model with requirements, BIM references, CADbase references, devices, signals, circuits, power interface, safety functions, HMI requirements, costing references, and validation findings.
- [ ] Phase 3: power drop-in object and BIM/MEP interface.
- [ ] Phase 4: CADbase integration.
- [ ] Phase 5: BOM and costing integration.
- [ ] Phase 6: PLC/I/O and signal registry.
- [ ] Phase 7: HMI and digital twin companion workbench tracks.

## 5. Business thesis

- [ ] Less havoc = more money.
- [ ] Less missing information = fewer redesigns.
- [ ] Less duplicate entry = fewer clerical errors.
- [ ] Less vendor chasing = faster quoting and purchasing.
- [ ] Less drawing churn = better schedule control.
- [ ] Less field surprise = better margin.
- [ ] Capture once; validate early; reuse everywhere.
