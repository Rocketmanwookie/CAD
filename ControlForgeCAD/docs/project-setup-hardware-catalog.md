# Project Setup Hardware Catalog

IntegraCAB Open loads PLC hardware planning data from
[`controls_wb/resources/hardware/plc_catalog.xml`](../controls_wb/resources/hardware/plc_catalog.xml).

The XML schema is
[`schemas/plc_hardware_catalog_v0_1.xsd`](../schemas/plc_hardware_catalog_v0_1.xsd).

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

Amperage calculation should not be based only on phase and voltage. It needs modeled load data, including large current drawing devices controlled by the panel:

- Motors.
- Heat strips.
- VFDs.
- DC power supplies.
- Ethernet/network equipment.
- Solenoids, relays, and contactor coils where relevant.
- Spare capacity and diversity/usage assumptions.

The current phase/voltage dropdown prepares the power configuration input. Load-based current calculation belongs with the upcoming power-drop/load model.
