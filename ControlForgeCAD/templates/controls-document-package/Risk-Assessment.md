# Machinery Risk Assessment
## [Project name]

| | |
|---|---|
| **Document title** | Machinery Risk Assessment (RA) |
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

## 1. Machine limits

Per ISO 12100, the assessment starts by stating the limits. A hazard outside the stated limits
is not assessed, so the limits must be honest about how the machine will really be used.

| Limit | Definition |
|---|---|
| Use limits | [Intended use, and reasonably foreseeable misuse] |
| Space limits | [Range of movement, space required for operation and maintenance] |
| Time limits | [Life, maintenance intervals, component replacement] |
| Other limits | [Materials processed, environment, cleanliness, skill level of operators] |

**Foreseeable misuse.** [State it explicitly. "Operator reaches into the infeed to clear a jam
without stopping the machine" is foreseeable, and assessing only correct use is the most common
way a risk assessment fails to protect anyone.]

---

## 2. Lifecycle phases assessed

| Phase | Assessed | Notes |
|---|---|---|
| Transport and installation | | |
| Commissioning | | |
| Normal operation | | |
| Setting and changeover | | |
| Cleaning | | |
| Fault finding | | |
| Maintenance | | |
| Decommissioning | | |

> Most machinery injuries happen outside normal operation. If only the operation row is
> assessed, the assessment is missing the dangerous part.

---

## 3. Hazard identification and risk estimation

Risk is estimated per ISO 13849-1 Annex A using S, F and P:

| Parameter | Value | Meaning |
|---|---|---|
| S, severity | S1 | Slight, normally reversible injury |
| | S2 | Serious, normally irreversible injury or death |
| F, frequency | F1 | Seldom to less often, or short exposure |
| | F2 | Frequent to continuous, or long exposure |
| P, possibility of avoidance | P1 | Possible under specific conditions |
| | P2 | Scarcely possible |

| # | Phase | Hazard | Hazardous event | Who | S | F | P | Required PL |
|---|---|---|---|---|---|---|---|---|
| H-001 | Operation | Crushing, inlet valve actuator | Body part in closing path | Operator | S2 | F1 | P2 | PL d |
| H-002 | Cleaning | Entanglement, rotating shaft | Contact during cleaning | Cleaner | S2 | F2 | P2 | PL e |
| H-003 | Fault finding | Electrical, live working | Contact with 400 V | Electrician | S2 | F1 | P2 | PL d |
| H-004 | Operation | Hot surface, reactor | Contact | Operator | S1 | F2 | P1 | PL b |
| H-005 | | | | | | | | |

**Determining PL from S, F and P.** Follow the risk graph in ISO 13849-1 Annex A. Where the
result sits on a boundary, record the reasoning rather than just the answer.

---

## 4. Protective measures

Applied in the order required by ISO 12100: eliminate by design first, then safeguard, then
inform. A guard is not an acceptable answer to a hazard that could have been designed out.

| Hazard | Measure | Type | Achieved PL | Verified |
|---|---|---|---|---|
| H-001 | [Reduce actuator force below injury threshold] | Inherently safe design | n/a | |
| H-001 | [Fixed guard over closing path] | Safeguarding | n/a | |
| H-002 | [Interlocked guard with guard locking] | Safeguarding | PL e | |
| H-003 | [Isolation procedure, lockable isolator] | Information and procedure | n/a | |
| H-004 | [Insulation, and warning label] | Safeguarding and information | n/a | |

---

## 5. Safety functions

Each safety function that the control system implements, with its required and achieved
performance level.

| SF ref | Safety function | Hazard | Required PL | Architecture | Category | DC | MTTFd | Achieved PL | Response time |
|---|---|---|---|---|---|---|---|---|---|
| SF-001 | Emergency stop, all motion | All | PL d | Dual channel | Cat 3 | High | [years] | | [ms] |
| SF-002 | Guard interlock, stop on open | H-002 | PL e | Dual channel with monitoring | Cat 4 | High | | | |
| SF-003 | Prevent start with guard open | H-002 | PL e | | Cat 4 | | | | |

**Calculation.** Record the calculation method and tool used, with version. Attach the report.

---

## 6. Safety distances

Where a guard or a device relies on distance, per ISO 13855.

| Ref | Device | Approach | Stopping time T (ms) | Speed K (mm/s) | Intrusion C (mm) | Minimum distance S (mm) | Actual (mm) | Pass |
|---|---|---|---|---|---|---|---|---|
| SD-001 | [Light curtain] | Perpendicular | | 2000 | | | | |

Stopping time is measured on the real machine at SAT, not taken from a catalogue.

---

## 7. Residual risk

Risk that remains after all protective measures. This is what goes into the instruction manual
and onto the machine.

| Ref | Residual risk | Communicated by | Location |
|---|---|---|---|
| RR-001 | [Description] | [Label, manual section, training] | [Where] |

---

## 8. Validation

| # | Safety function | Validation method | Result | Validated by | Date |
|---|---|---|---|---|---|
| | SF-001 | Test and analysis | | | |

| Role | Name | Signature | Date |
|---|---|---|---|
| Assessor (competent person) | | | |
| Design authority | | | |
| Client safety authority | | | |
