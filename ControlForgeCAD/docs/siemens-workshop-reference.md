# Siemens S7-1200 workshop implementation reference

Source: user-supplied `329495256-SIMATIC-S7-1200-Workshop-2016.pdf`, 67 PDF pages. Catalog source ID: `siemens-workshop-expansion`; its record stores the local path and SHA-256. Page numbers below mean PDF pages, not printed slide numbers. PDF metadata dates the file to April 2016; early slides carry Siemens AG 2013 notices.

This is a historical training reference. Retain its family and firmware context; verify current order numbers, electrical specifications, and asset matches separately. No vendor PDF content is bundled with the code.

## Applied rule

PDF page 23: CPU 1212C supports two signal modules; CPU 1214C supports eight. Both have a separate one-signal-board allowance. The catalog and export limit checks now use the signal-module limits. Signal-board selection is not yet modeled.

## Hardware work queue

The following observations were extracted from pages 18-22 and 28-31. They are implementation requirements to validate, not completed features.

| Pages | Reference observation | Project work |
|---|---|---|
| 18, 20 | Separate CPU, power, switch, communication, signal-module, technology-module, and board families | Model component roles explicitly instead of using one generic expansion-module count |
| 21 | Removable connectors; dedicated analog, RTD, and thermocouple modules | Capture connector inclusion and required sensor interface; do not infer analog compatibility from channel count alone |
| 22-23 | Signal boards add I/O within the CPU footprint and have a separate allowance | Add board-slot occupancy and compatibility without counting boards as side-mounted modules |
| 28 | Communication modules on the left; expansion modules on the right | Add mounting-side metadata and layout grouping; obtain exact dimensions and clearances from part documentation |
| 29-30 | Integrated networking supports selected PROFINET and TCP/IP workflows without an extra communication module | Distinguish built-in capabilities from purchased accessories and avoid creating a purchasable BOM row for an onboard interface |
| 29-31 | Other network and serial interfaces have distinct requirements | Resolve protocol, physical interface, adapter, and library requirements per exact CPU/module and firmware |

## Remaining document map

These ranges were indexed from headings, not fully reviewed:

- 1-17: controller positioning, TIA engineering, software and configuration concepts.
- 25-27: CPU 1215C/1217C capabilities and motion-oriented features.
- 32-35: motion, tracing, and PID.
- 36-40: access, know-how, copy, and manipulation protection.
- 41-46: HMI panels, integration, and screen navigation.
- 47-49: project-wide libraries and cross-references.
- 50-66: TIA introduction and workshop configuration exercises, including PLC tags and HMI tasks.
- 67: document disclaimer and terms.

## Next implementation sequence

1. Introduce explicit hardware roles and independent board/module allowances.
2. Add signal electrical requirements before automatic part recommendations.
3. Produce a project-selected parts export with visible unresolved equipment.
4. Match returned CAx assets to exact order numbers and record dimensions and mounting metadata.

Current limitations: historical references do not establish current catalog availability; the two CPU entries still share unverified CAD assets. Module-count validation alone does not establish electrical compatibility, power budget, or a complete cabinet design.
