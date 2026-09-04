# Project Setup Hardware Catalog

integraCAD Open loads PLC hardware planning data from
[`controls_wb/resources/hardware/plc_catalog.xml`](../controls_wb/resources/hardware/plc_catalog.xml).

The PLC XML schema is
[`schemas/plc_hardware_catalog_v0_1.xsd`](../schemas/plc_hardware_catalog_v0_1.xsd).

Starter panel hardware placeholder data is loaded from
[`controls_wb/resources/hardware/panel_catalog.xml`](../controls_wb/resources/hardware/panel_catalog.xml).

The panel hardware XML schema is
[`schemas/panel_hardware_catalog_v0_1.xsd`](../schemas/panel_hardware_catalog_v0_1.xsd).

The Project Intake dialog uses this catalog for PLC make, line, CPU, compatible Ethernet/power choices, and the I/O expansion planning popup.

## Siemens S7-1200 verified seed

The first vendor-verified seed is Siemens S7-1200. The catalog currently includes:

| Kind | Part | I/O used by planner |
|---|---|---|
| CPU | CPU 1212C DC/DC/DC `6ES7212-1AE40-0XB0` | 8 DI, 6 DO, 2 AI, 0 AO |
| CPU | CPU 1214C DC/DC/DC `6ES7214-1AG40-0XB0` | 14 DI, 10 DO, 2 AI, 0 AO |
| DI module | SM 1221 DI 16x24 V DC `6ES7221-1BH32-0XB0` | 16 DI |
| DO module | SM 1222 DQ 16x24 VDC `6ES7222-1BH32-0XB0` | 16 DO |
| AI module | SM 1231 AI 8 `6ES7231-4HF32-0XB0` | 8 AI |
| AO module | SM 1232 AQ 4 `6ES7232-4HD32-0XB0` | 4 AO |

The catalog also records a local Siemens S7-1200 Easy Book source:

- `A5E02486774-AG`
- `/home/egrantjr/Downloads/s71200_easy_book_en-US_en-US.pdf`

CPU entries can include local CAD references. The current Siemens S7-1200 CPU entries point to the provided CADBaseLibrary STEP and SolidWorks part files by local path and SHA-256 checksum. These files are not copied into the repository.

Always verify final part selections against current Siemens catalog data and project electrical requirements before procurement.

## Panel hardware starter seed

The panel hardware catalog currently includes unverified generic placeholder parts for:

- `PANEL-001` enclosure/backplate.
- `DIN-001` DIN rail.
- `DUCT-001` wire duct.
- `TB-001` terminal strip.

These records are intended to make starter BOM and validation output cleaner while real enclosure, rail, duct, and terminal part numbers are selected. Keep them marked `verified="false"` until replaced with source-backed vendor parts.

## Updating the catalog

To add or revise hardware:

1. Edit [`controls_wb/resources/hardware/plc_catalog.xml`](../controls_wb/resources/hardware/plc_catalog.xml).
2. Keep vendor-verified parts marked `verified="true"` only when source-backed.
3. Add source entries under `<sources>` with official URLs where practical.
4. Add `<cadRefs>` entries with local paths and checksums when CADbase assets exist.
5. Keep unverified placeholders marked `verified="false"`.
6. Validate the XML shape against [`schemas/plc_hardware_catalog_v0_1.xsd`](../schemas/plc_hardware_catalog_v0_1.xsd).
7. Run:

```bash
python3 -m pytest
python3 -m compileall ControlForgeCAD
```

## Amperage calculation roadmap

Amperage calculation should not be based only on phase and voltage. Project Intake now stores starter controlled-load lines and estimates current with 20 percent spare capacity.

Use one load per line:

```text
type, label, quantity, watts-or-hp
```

Examples:

```text
motor, Conveyor motor, 2, 1hp
heat_strip, Cabinet heater, 1, 500W
vfd, Pump drive, 1, 2.2kW
power_supply, 24 VDC controls supply, 1, 240W
ethernet, Network switch, 1, 25W
coil, Contactor coils, 4, 8W
```

Supported starter load types are `motor`, `vfd`, `heat_strip`, `power_supply`, `ethernet`, `coil`, `relay`, and `other`.

The estimate uses type defaults for power factor and efficiency, then applies a 20 percent spare factor. It is a planning aid only. Final panel, feeder, breaker, conductor, SCCR, thermal, and code calculations still need engineering review and source-backed load data, including large current drawing devices controlled by the panel:

- Motors.
- Heat strips.
- VFDs.
- DC power supplies.
- Ethernet/network equipment.
- Solenoids, relays, and contactor coils where relevant.
- Spare capacity and diversity/usage assumptions.

The current phase/voltage dropdown prepares the power configuration input. This starter load estimate is the first power-drop/load model scaffold; richer device-level load records should replace the free-text lines later.
