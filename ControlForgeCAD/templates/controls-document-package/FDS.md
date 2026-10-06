# Functional Design Specification
## [Project name]

| | |
|---|---|
| **Document title** | Functional Design Specification (FDS) |
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

## 1. Purpose and references

### 1.1 Purpose
This document describes how the control system for [Project name] satisfies the requirements
of the User Requirement Specification. It is written to be sufficient for a competent control
engineer to implement the system without further clarification, and for the FAT to be written
directly from it.

### 1.2 Reference documents

| Ref | Document | Number | Rev |
|---|---|---|---|
| R1 | User Requirement Specification | | |
| R2 | P&ID / General arrangement | | |
| R3 | I/O list | | |
| R4 | Cause and effect matrix | | |
| R5 | Risk assessment | | |

### 1.3 Standards
IEC 61131-3 for programming languages. ISA-88 for sequence and state model terminology.
ISA-18.2 for alarm management. IEC 60204-1 for electrical equipment of machines.

---

## 2. System architecture

### 2.1 Overview
[Describe the topology: controllers, remote I/O, drives, HMI, network segments.]

### 2.2 Hardware summary

| Item | Manufacturer | Model | Qty | Location |
|---|---|---|---|---|
| PLC CPU | | | | |
| Remote I/O | | | | |
| HMI | | | | |
| Safety controller | | | | |
| Managed switch | | | | |

### 2.3 Networks

| Network | Protocol | Media | Address range | Devices |
|---|---|---|---|---|
| Control | [EtherNet/IP, PROFINET] | | | |
| Safety | [CIP Safety, PROFIsafe] | | | |
| Plant | [OPC UA] | | | |

### 2.4 Software versions

| Item | Software | Version | Notes |
|---|---|---|---|
| PLC program | | | |
| HMI application | | | |
| Firmware, CPU | | | |

> Record exact versions. "Latest" is not a version, and at SAT it is the difference between
> a five minute check and an afternoon.

---

## 3. Operating modes

| Mode | Entry condition | Behaviour | Exit condition |
|---|---|---|---|
| Off | Power applied, no start | Outputs de-energised, no motion | Start selected |
| Manual | Selected at HMI, guards closed | Individual devices operable, interlocks active | Mode change |
| Auto | Selected, ready conditions met | Full sequence runs | Stop, fault, or mode change |
| Maintenance | Key switch, authorised user | [Reduced speed / bypass, define exactly what is bypassed] | Key removed |

**Mode change rules.** [State when a mode change is permitted and what happens to a running
sequence when it occurs. This is where the difference between an orderly stop and a mess lives.]

---

## 4. Sequence of operation

Written as numbered steps with an explicit transition condition. A step with no stated
transition is a step that can hang, and that is what an operator will report as "it stopped
and nothing happened".

### 4.1 Start sequence

| Step | Action | Transition to next step | Timeout | On timeout |
|---|---|---|---|---|
| 1 | [Action] | [Condition] | [s] | [Alarm ref, and behaviour] |
| 2 | | | | |
| 3 | | | | |

### 4.2 Normal running
[Describe steady state behaviour, cycle timing, and how throughput is regulated.]

### 4.3 Controlled stop
| Step | Action | Transition | Timeout |
|---|---|---|---|
| 1 | Complete current cycle | Cycle complete flag | [s] |
| 2 | [Action] | | |

### 4.4 Emergency stop
[Category 0 or 1 per IEC 60204-1. State which, and state exactly what remains energised.]

### 4.5 Recovery and restart
[What the operator must do after a fault or an E-stop. State whether a manual reset is required
before motion is possible, because the safety assessment almost certainly requires one.]

---

## 5. Interlocks and permissives

A **permissive** must be true to start. An **interlock** stops or prevents operation when it
goes false. They are not the same thing and confusing them produces machines that cannot be
restarted after a trip.

| Ref | Type | Condition | Affects | Action | Reset |
|---|---|---|---|---|---|
| INT-001 | Interlock | [Signal false] | [Device] | [Immediate stop] | [Auto / manual] |
| PRM-001 | Permissive | [Condition] | [Sequence] | [Prevents start] | n/a |

---

## 6. Alarms

Per ISA-18.2: every alarm requires a defined operator response. An indication that needs no
response is a status, not an alarm, and putting it in the alarm list is how alarm floods start.

| Tag | Description | Priority | Trip | Delay | Operator action | Auto reset |
|---|---|---|---|---|---|---|
| AL-001 | | High | | [s] | [What the operator does] | No |
| AL-002 | | Medium | | | | |

**Priority definitions.** High: immediate action required to avoid injury, damage or product
loss. Medium: action required this shift. Low: action required, not time critical.

---

## 7. Analog handling and scaling

| Tag | Signal | Raw range | Engineering range | Units | Filter | Fault action |
|---|---|---|---|---|---|---|
| | 4-20 mA | 0-27648 | | | [s] | [Hold / fail safe value] |

**Out of range.** [State the behaviour below 3.6 mA and above 21 mA. A broken wire reads as
zero flow, and if that is not detected the sequence will happily continue.]

---

## 8. Operator interface

### 8.1 Screen hierarchy
[List screens and navigation.]

### 8.2 Common conventions

| Element | Convention |
|---|---|
| Running | [Colour and shape] |
| Stopped | |
| Faulted | |
| Unacknowledged alarm | |

> Colour alone must not carry meaning. Use shape or text as well, for colour vision deficiency
> and for the fact that panel screens fade.

### 8.3 Security levels

| Level | Who | Permitted |
|---|---|---|
| 0 | Anyone | View only |
| 1 | Operator | Start, stop, acknowledge |
| 2 | Supervisor | Setpoint changes within limits |
| 3 | Engineer | Full, including bypasses |

---

## 9. Data, recipes and reporting

### 9.1 Recipe structure
| Parameter | Type | Range | Default | Units | Security level |
|---|---|---|---|---|---|

### 9.2 Records
| Record | Trigger | Fields | Retention | Format |
|---|---|---|---|---|

---

## 10. Communications

| Link | Peer | Protocol | Rate | Data exchanged | Failure behaviour |
|---|---|---|---|---|---|

**Watchdog.** [State the timeout and what happens when it expires. A comms link with no
watchdog will one day deliver a stale value that looks perfectly valid.]

---

## 11. Failure behaviour

| Failure | Detection | System response | Alarm | Recovery |
|---|---|---|---|---|
| Power loss | | Outputs de-energise | | [Manual restart required?] |
| CPU fault | | | | |
| Remote I/O comms loss | | | | |
| Sensor out of range | | | | |
| Drive fault | | | | |

---

## 12. Software structure

### 12.1 Program organisation

| POU | Language | Purpose | Scan |
|---|---|---|---|
| Main | LD | Coordination | Cyclic |
| | | | |

### 12.2 Naming conventions
[State the tag naming rule and stick to it. Include an example of each type.]

### 12.3 Memory map
| Area | Range | Use |
|---|---|---|

---

## 13. Requirement traceability

| URS ref | FDS section | Implemented in | Test ref |
|---|---|---|---|
| URS-OP-001 | | | |
