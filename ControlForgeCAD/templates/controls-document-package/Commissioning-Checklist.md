# Commissioning Checklist
## [Project name]

| | |
|---|---|
| **Document title** | Commissioning Checklist (COMM) |
| **Document number** | [Doc no.] |
| **Revision** | 0 |
| **Date** | [Date] |
| **Project** | [Project name] |
| **Client** | [Client] |
| **Prepared by** | [Author], [Your company] |

### Revision history

| Rev | Date | Description | Author | Approved |
|---|---|---|---|---|
| 0 | [Date] | First issue | [Author] | |
| | | | | |

### Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Author | [Author] | | |
| Reviewer (engineering) | | | |
| Approver ([Your company]) | | | |
| Approver ([Client]) | | | |

---

> **Do not skip ahead.** Each stage assumes the previous one passed. The order is the safety
> argument, not a suggestion.

## Stage 1. Dead checks, before any power

| # | Check | Result | Initial | Date |
|---|---|---|---|---|
| 1.1 | Isolation confirmed and locked off, permit in place | | | |
| 1.2 | Panel free of debris, tools removed | | | |
| 1.3 | All terminals tight, checked to torque | | | |
| 1.4 | Cable identification present both ends | | | |
| 1.5 | Wiring matches schematics, point to point | | | |
| 1.6 | Earth continuity, every metallic enclosure and door | | | |
| 1.7 | Protective device ratings correct | | | |
| 1.8 | Insulation resistance, power circuits, > 1 MOhm | | | |
| 1.9 | No short circuits, phase to phase and phase to earth | | | |
| 1.10 | Electronic modules removed or isolated before insulation test | | | |

> 1.10 matters. An insulation test at 500 V through an analog input card destroys the card.

## Stage 2. First energisation, control only

| # | Check | Result | Initial |
|---|---|---|---|
| 2.1 | Power circuits still isolated, control circuit only energised | | |
| 2.2 | 24 VDC present and within tolerance, on load | | |
| 2.3 | No unexpected heating, smell or noise | | |
| 2.4 | Controller powers up, no fault LEDs | | |
| 2.5 | Remote I/O online, all nodes present | | |
| 2.6 | HMI powers up and connects | | |
| 2.7 | Time and date set, and synchronised if applicable | | |

## Stage 3. I/O proving, before any motion

| # | Check | Result | Initial |
|---|---|---|---|
| 3.1 | Every digital input proved from the field device | | |
| 3.2 | Every analog input reads plausibly, and at range extremes | | |
| 3.3 | Outputs proved with the load isolated, using the test facility | | |
| 3.4 | Safety inputs proved, both channels | | |

> 3.3. Prove outputs before connecting loads. A crossed output that starts the wrong motor is
> found here for the cost of a moment, or found later for the cost of a repair.

## Stage 4. Power circuits

| # | Check | Result | Initial |
|---|---|---|---|
| 4.1 | Motor circuits energised one at a time | | |
| 4.2 | Overload settings match motor nameplate | | |
| 4.3 | Direction of rotation confirmed, uncoupled where possible | | |
| 4.4 | Drive parameters loaded and recorded | | |
| 4.5 | Motor current on no load within expectation | | |
| 4.6 | Brakes and holding devices operate | | |

## Stage 5. Safety, before production running

| # | Check | Result | Initial | Witness |
|---|---|---|---|---|
| 5.1 | Every E-stop station tested individually | | | |
| 5.2 | Every guard interlock tested individually | | | |
| 5.3 | Start refused with any guard open | | | |
| 5.4 | Reset requires deliberate action and cannot be defeated | | | |
| 5.5 | Stopping time measured | | | |
| 5.6 | Safety distances confirmed against measured stopping time | | | |

## Stage 6. Sequence dry run

| # | Check | Result | Initial |
|---|---|---|---|
| 6.1 | Full sequence run empty, at reduced speed | | |
| 6.2 | Each step transition observed and timed | | |
| 6.3 | Interlocks tested during motion | | |
| 6.4 | Controlled stop and restart | | |
| 6.5 | Sequence run at full speed | | |

## Stage 7. Wet commissioning and product

| # | Check | Result | Initial |
|---|---|---|---|
| 7.1 | Utilities on, leaks checked | | |
| 7.2 | Loops in manual, response confirmed | | |
| 7.3 | Loops tuned, values recorded | | |
| 7.4 | First product run, quality checked | | |
| 7.5 | Throughput measured against target | | |
| 7.6 | 24 hour run completed without intervention | | |

## Sign-off

| Stage | Completed by | Signature | Date | Authority |
|---|---|---|---|---|
| 1 Dead checks | | | | |
| 2 First energisation | | | | |
| 3 I/O proving | | | | |
| 4 Power circuits | | | | |
| 5 Safety | | | | |
| 6 Dry run | | | | |
| 7 Wet commissioning | | | | |
