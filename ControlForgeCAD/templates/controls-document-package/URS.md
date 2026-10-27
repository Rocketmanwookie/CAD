# User Requirement Specification
## [Project name]

| | |
|---|---|
| **Document title** | User Requirement Specification (URS) |
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

## 1. Purpose and scope

### 1.1 Purpose
This document states the requirements that [Client] places on [Project name]. It describes
*what* the system must do. It deliberately does not describe how, which is the subject of the
Functional Design Specification.

### 1.2 Scope
**In scope**

- [Equipment, area or process covered]
- [Control system boundary]

**Out of scope**

- [Explicitly excluded items. Be generous here. Most disputes at SAT trace back to something
  that was never written down as excluded.]

### 1.3 Definitions
See section 11.

---

## 2. System overview and boundaries

[One or two paragraphs describing the process in plain language, as an operator would explain it.]

### 2.1 Battery limits

| Boundary | Description | Responsibility |
|---|---|---|
| Upstream | [e.g. infeed conveyor handshake] | [Client / Supplier] |
| Downstream | [e.g. palletiser interface] | [Client / Supplier] |
| Electrical | [e.g. 400 V supply to panel isolator] | [Client / Supplier] |
| Network | [e.g. site OT switch, port assignment] | [Client / Supplier] |

---

## 3. Operational requirements

Each requirement carries a unique reference. That reference is quoted in the FDS, in the FAT
and in the SAT, and it is how anyone proves the delivered system matches what was asked for.

| Ref | Requirement | Priority | Acceptance |
|---|---|---|---|
| URS-OP-001 | The system shall [requirement]. | Mandatory | [How this is demonstrated] |
| URS-OP-002 | The system shall [requirement]. | Mandatory | |
| URS-OP-003 | The system should [requirement]. | Desirable | |

**Priority key.** Mandatory: the system is not accepted without it. Desirable: implement if it
does not affect cost or programme. Optional: record for a later phase.

---

## 4. Functional requirements

### 4.1 Operating modes

| Ref | Requirement | Priority |
|---|---|---|
| URS-FN-001 | The system shall provide Manual, Auto and Maintenance modes. | Mandatory |
| URS-FN-002 | Mode changes shall be possible only when [condition]. | Mandatory |

### 4.2 Sequence
| Ref | Requirement | Priority |
|---|---|---|
| URS-FN-010 | On start, the system shall [sequence]. | Mandatory |
| URS-FN-011 | On stop request, the system shall [controlled stop behaviour]. | Mandatory |
| URS-FN-012 | On power restoration, the system shall [restart behaviour]. | Mandatory |

### 4.3 Alarms
| Ref | Requirement | Priority |
|---|---|---|
| URS-FN-020 | Alarms shall be prioritised and presented per ISA-18.2. | Mandatory |
| URS-FN-021 | Alarm acknowledgement shall record user and timestamp. | Mandatory |

---

## 5. Data and records

| Ref | Requirement | Retention | Priority |
|---|---|---|---|
| URS-DR-001 | The system shall record [data] at [frequency]. | [Period] | Mandatory |
| URS-DR-002 | Records shall be attributable, legible, contemporaneous, original and accurate. | | Mandatory |
| URS-DR-003 | The system shall provide an audit trail of parameter changes. | | Mandatory |

> Where records support a regulated activity, ALCOA+ applies: attributable, legible,
> contemporaneous, original, accurate, plus complete, consistent, enduring and available.

---

## 6. Interfaces

| Ref | Interface | Direction | Protocol | Data |
|---|---|---|---|---|
| URS-IF-001 | [MES / ERP / SCADA] | Bidirectional | [OPC UA / Modbus TCP] | [Payload] |
| URS-IF-002 | [Upstream machine] | In | [Hardwired handshake] | [Signals] |

---

## 7. Environment and utilities

| Item | Requirement |
|---|---|
| Ambient temperature | [range] |
| Humidity | [range] |
| Ingress protection | [IP rating, and where] |
| Electrical supply | [voltage, phases, frequency, fault level] |
| Compressed air | [pressure, quality class] |
| Area classification | [safe area / zone, and the governing standard] |

---

## 8. Safety and regulatory

| Ref | Requirement | Standard |
|---|---|---|
| URS-SF-001 | Emergency stop shall meet the required performance level. | ISO 13849-1 |
| URS-SF-002 | Machinery safety functions shall be assessed and documented. | ISO 12100 |
| URS-SF-003 | The safety related parts shall achieve PL [d/e] / SIL [1/2/3]. | ISO 13849-1 / IEC 62061 |
| URS-SF-004 | Electrical equipment of the machine shall comply. | IEC 60204-1 |

---

## 9. Non-functional requirements

| Ref | Requirement | Target |
|---|---|---|
| URS-NF-001 | Availability | [%] |
| URS-NF-002 | Scan time | [ms] |
| URS-NF-003 | Operator response time for [action] | [ms] |
| URS-NF-004 | Spare I/O capacity at handover | [%, typically 20] |
| URS-NF-005 | Spare memory and network capacity | [%] |
| URS-NF-006 | Cyber security level | IEC 62443 SL-[n] |

---

## 10. Requirement traceability

Completed as the project runs. Every mandatory requirement above must appear here with a test
that demonstrates it.

| URS ref | FDS section | Test ref (FAT/SAT) | Verified | Date |
|---|---|---|---|---|
| URS-OP-001 | | | | |
| URS-FN-001 | | | | |

---

## 11. Glossary

| Term | Meaning |
|---|---|
| FAT | Factory Acceptance Test |
| FDS | Functional Design Specification |
| SAT | Site Acceptance Test |
| URS | User Requirement Specification |
