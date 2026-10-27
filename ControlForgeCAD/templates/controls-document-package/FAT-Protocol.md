# Factory Acceptance Test Protocol
## [Project name]

| | |
|---|---|
| **Document title** | Factory Acceptance Test Protocol (FAT) |
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

## 1. Scope and references

### 1.1 Scope
This protocol covers acceptance testing of the control system for [Project name] at the works
of [Your company], prior to despatch to site. Testing is performed on simulated field I/O.

**Not covered by this test.** Field device performance, actual process behaviour, and anything
that depends on real plant. Those belong to the SAT, and no result here should be read as
covering them.

### 1.2 References

| Ref | Document | Number | Rev |
|---|---|---|---|
| R1 | Functional Design Specification | | |
| R2 | I/O List | | |
| R3 | Cause and Effect Matrix | | |
| R4 | Bill of Materials | | |
| R5 | Panel general arrangement and schematics | | |

### 1.3 Attendees

| Name | Company | Role | Present for |
|---|---|---|---|
| | [Your company] | Test engineer | All |
| | [Client] | Witness | |
| | | | |

---

## 2. Entry criteria

The FAT does not begin until every item below is true. Starting a FAT that is not ready wastes
the witness's time and produces a punch list that is really a build list.

| # | Criterion | Met | Initial |
|---|---|---|---|
| 1 | Panel build complete and inspected | | |
| 2 | Program written, compiled, and version recorded | | |
| 3 | HMI application complete, version recorded | | |
| 4 | Internal pre-FAT completed and faults cleared | | |
| 5 | Simulation rig available and proven | | |
| 6 | All reference documents at current revision and available | | |
| 7 | Test protocol issued to client at least 5 working days beforehand | | |
| 8 | Calibration certificates for test equipment in date | | |

**Pre-FAT.** Run the entire protocol yourself first. The witnessed FAT is a demonstration, not
a debugging session.

---

## 3. Test environment

### 3.1 Simulation method

| I/O type | Simulation method |
|---|---|
| Digital input | Switch box on terminals, one switch per point |
| Digital output | Indicator lamp or LED on terminals |
| Analog input | Signal generator, 4-20 mA, calibrated |
| Analog output | Loop calibrator in read mode |
| Safety input | Dual channel switch box, with fault injection capability |
| Network devices | Simulator or actual device where available |

### 3.2 Test equipment

| Equipment | Serial | Cal due | Used for |
|---|---|---|---|
| Loop calibrator | | | Analog I/O |
| Multimeter | | | Electrical checks |
| Insulation tester | | | Insulation resistance |

### 3.3 Software versions under test

| Item | Version | Checksum | Recorded by |
|---|---|---|---|
| PLC program | | | |
| HMI application | | | |
| Safety program | | | |

> Record the checksum, not just the version number. Two builds can share a version.

---

## 4. Documentation verification

| # | Check | Result | Initial |
|---|---|---|---|
| 4.1 | Schematics match the as-built panel | Pass / Fail | |
| 4.2 | BOM matches installed components, item by item | Pass / Fail | |
| 4.3 | Equipment manuals present | Pass / Fail | |
| 4.4 | Calibration certificates present and in date | Pass / Fail | |
| 4.5 | Software version documentation complete | Pass / Fail | |
| 4.6 | Spare parts list supplied | Pass / Fail | |
| 4.7 | CE / UKCA declaration prepared | Pass / Fail | |

---

## 5. Visual and mechanical inspection

| # | Check | Result | Initial |
|---|---|---|---|
| 5.1 | Enclosure undamaged, correct IP rating, seals intact | | |
| 5.2 | All components mounted securely | | |
| 5.3 | Wiring neat, ferruled, and identified per drawings | | |
| 5.4 | Terminal numbering matches schematics | | |
| 5.5 | Earth continuity, all metallic parts bonded | | |
| 5.6 | Segregation of power, control, instrument and data | | |
| 5.7 | Labels present, legible, and correct | | |
| 5.8 | Warning labels and arc flash label fitted | | |
| 5.9 | Door interlock on isolator operates | | |
| 5.10 | Gland plate drilled correctly, spare glands blanked | | |
| 5.11 | No swarf or debris in enclosure | | |

---

## 6. Power up and electrical tests

**Safety.** These tests involve live working. Follow the site electrical safety rules and
ensure a second competent person is present.

| # | Test | Expected | Measured | Result | Initial |
|---|---|---|---|---|---|
| 6.1 | Insulation resistance, power circuits, 500 V | > 1 MOhm | | | |
| 6.2 | Earth continuity, < 0.1 Ohm to earth bar | Pass | | | |
| 6.3 | Phase rotation | [L1 L2 L3] | | | |
| 6.4 | Supply voltage at isolator | [400 V ± 10%] | | | |
| 6.5 | 24 VDC supply voltage on load | 24 V ± 5% | | | |
| 6.6 | 24 VDC ripple | < 100 mV | | | |
| 6.7 | Protective device ratings match schematic | Pass | | | |
| 6.8 | Panel current draw | [expected A] | | | |

---

## 7. I/O verification

Every point on the I/O list is tested individually. This is the tedious part and it is the part
that saves the most time later: a crossed pair found here costs five minutes.

**Method, digital input.** Operate the switch. Confirm the correct tag changes state in the
controller, and that no other tag changes.

**Method, digital output.** Force the output from the controller. Confirm the correct lamp
lights and the terminal reads 24 V, and that no other output changes.

**Method, analog input.** Inject 4, 8, 12, 16 and 20 mA. Confirm engineering values match the
I/O list scaling at each point, within tolerance.

**Method, analog output.** Command 0, 25, 50, 75 and 100 percent. Confirm the loop calibrator
reads 4, 8, 12, 16 and 20 mA within tolerance.

| Tag | Address | Type | Injected | Expected | Observed | Pass | Initial |
|---|---|---|---|---|---|---|---|
| XV-101-ZSO | %I0.0 | DI | Closed | TRUE | | | |
| FT-101 | %IW64 | AI | 12 mA | 25.0 m3/h | | | |
| MTR-101-RUN | %Q0.0 | DO | Force ON | 24 V at X5:01 | | | |
| FCV-101 | %QW96 | AO | 50% | 12 mA | | | |

> Copy one row per point from the I/O list. A partial I/O check is not an I/O check.

### 7.1 Cross-talk check
| # | Test | Result |
|---|---|---|
| 7.1.1 | With each output forced individually, confirm no other output energises | |

---

## 8. Functional tests

Written directly from the FDS. Each test quotes the FDS section it proves, and the URS
requirement behind it.

| Test ref | FDS ref | URS ref | Description | Method | Expected result | Actual | Pass | Initial |
|---|---|---|---|---|---|---|---|---|
| FAT-FN-001 | 3 | URS-FN-001 | Mode selection | Select each mode at HMI | Mode changes and is indicated | | | |
| FAT-FN-002 | 4.1 | URS-FN-010 | Start sequence | Satisfy permissives, press Start | Steps execute in order per FDS 4.1 | | | |
| FAT-FN-003 | 4.1 | | Step timeout | Withhold step 2 transition | Alarm raised after timeout, sequence holds | | | |
| FAT-FN-004 | 4.3 | URS-FN-011 | Controlled stop | Press Stop mid cycle | Cycle completes then stops | | | |
| FAT-FN-005 | 4.5 | URS-FN-012 | Restart after power loss | Remove and restore supply | No automatic restart, manual reset required | | | |
| FAT-FN-006 | 7 | | Analog scaling | Inject range points | Values match RATS | | | |
| FAT-FN-007 | 8.3 | | Security levels | Attempt actions at each level | Only permitted actions available | | | |

---

## 9. Interlock and safety tests

Every row of the cause and effect matrix. Test the marks *and* confirm the blanks.

| Test ref | Cause ref | Cause simulated | Expected effects | Effects NOT expected | Actual | Pass | Initial |
|---|---|---|---|---|---|---|---|
| FAT-SF-001 | C-001 | E-stop station 1 pressed | All per C-001 row | | | | |
| FAT-SF-002 | C-002 | Guard door opened | Per C-002 row | FCV-101 does not close | | | |
| FAT-IL-001 | C-003 | LT-101 above 95% | Per C-003 row | | | | |

### 9.1 Safety function specific tests

| # | Test | Expected | Actual | Pass |
|---|---|---|---|---|
| 9.1.1 | Single channel fault, E-stop channel A | Safety function trips, fault annunciated | | |
| 9.1.2 | Single channel fault, E-stop channel B | Safety function trips, fault annunciated | | |
| 9.1.3 | Channel discrepancy time exceeded | Fault detected and latched | | |
| 9.1.4 | Reset with E-stop still pressed | Reset refused | | |
| 9.1.5 | Reset button held closed (welded contact) | Reset refused, requires falling edge | | |
| 9.1.6 | Safety response time | Within [ms] per calculation | | |

> Test 9.1.5 catches the most common reset circuit mistake. A reset that acts on level rather
> than edge will re-enable the machine the instant the guard closes if the button has stuck.

---

## 10. Alarm tests

| Test ref | Alarm | Trigger | Expected message | Priority correct | Ack works | Clears correctly | Pass |
|---|---|---|---|---|---|---|---|
| FAT-AL-001 | AL-003 | LT-101 above 95% | Per alarm list | | | | |

### 10.1 Alarm system behaviour
| # | Test | Expected | Pass |
|---|---|---|---|
| 10.1.1 | Alarm timestamp accuracy | Within 1 s of event | |
| 10.1.2 | Alarm ordering under simultaneous events | Chronological | |
| 10.1.3 | Acknowledgement records user and time | Recorded | |
| 10.1.4 | Alarm history survives power cycle | Retained | |

---

## 11. Communications tests

| # | Test | Expected | Actual | Pass |
|---|---|---|---|---|
| 11.1 | Link established to [peer] | Connected | | |
| 11.2 | Data exchange, all mapped points | Values match | | |
| 11.3 | Watchdog on link loss | Timeout detected within [s], defined action | | |
| 11.4 | Recovery on link restore | Automatic, no stale data | | |
| 11.5 | Network load under normal operation | < [%] | | |
| 11.6 | Unauthorised access attempt | Refused and logged | | |

---

## 12. Failure mode tests

| # | Failure injected | Expected response | Actual | Pass |
|---|---|---|---|---|
| 12.1 | Analog input open circuit | Below 3.6 mA detected, alarm, defined fail action | | |
| 12.2 | Analog input short circuit | Above 21 mA detected, alarm | | |
| 12.3 | Remote I/O disconnected | Comms alarm, outputs to defined state | | |
| 12.4 | 24 V supply removed | Outputs de-energise, orderly behaviour | | |
| 12.5 | CPU stopped | Outputs de-energise | | |
| 12.6 | HMI disconnected | Control continues, alarm raised | | |

---

## 13. Punch list

Items found during test. Category A must be closed before despatch. Category B may be closed
on site by agreement. Nothing ships with an open Category A.

| # | Category | Description | Raised by | Owner | Target date | Closed | Verified by |
|---|---|---|---|---|---|---|---|
| 1 | A / B | | | | | | |
| 2 | | | | | | | |

**Category A.** Prevents the system performing a specified function, or is a safety issue.
**Category B.** Cosmetic, documentation, or does not prevent the system being used.

---

## 14. Acceptance

### 14.1 Result summary

| Section | Tests | Passed | Failed | Not tested |
|---|---|---|---|---|
| 4 Documentation | | | | |
| 5 Visual | | | | |
| 6 Electrical | | | | |
| 7 I/O | | | | |
| 8 Functional | | | | |
| 9 Safety | | | | |
| 10 Alarms | | | | |
| 11 Communications | | | | |
| 12 Failure modes | | | | |

### 14.2 Recommendation

- [ ] **Accepted.** System may be despatched.
- [ ] **Accepted with punch list.** Category B items only, agreed for site closure.
- [ ] **Not accepted.** Retest required. Reason: ______________________________

### 14.3 Signatures

| Role | Name | Company | Signature | Date |
|---|---|---|---|---|
| Test engineer | | [Your company] | | |
| Quality | | [Your company] | | |
| Witness | | [Client] | | |
| Project manager | | [Client] | | |
