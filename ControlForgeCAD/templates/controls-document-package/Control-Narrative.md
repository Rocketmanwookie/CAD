# Control Narrative
## [Project name]

| | |
|---|---|
| **Document title** | Control Narrative (CN) |
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

## 1. Process overview

[Describe what the plant makes, and how. Write it so a new operator could read this section
alone and understand what they are looking at on the plant floor. Avoid control system
vocabulary here entirely.]

---

## 2. Equipment description

| Tag | Equipment | Function | Rating |
|---|---|---|---|
| [P-101] | [Feed pump] | [Transfers feed from T-101 to R-201] | [m3/h, kW] |
| | | | |

---

## 3. Control loops

One subsection per loop. The measurement, the final element, the strategy, and, importantly,
what the loop is protecting against.

### 3.1 [FIC-101, feed flow control]

| Item | Detail |
|---|---|
| Measurement | [FT-101, magnetic flow meter, 0 to 50 m3/h] |
| Controller | [FIC-101, PID] |
| Final element | [FCV-101, equal percentage, air to open] |
| Normal setpoint | [value and units] |
| Setpoint source | [Operator entry / recipe / cascade from LIC-201] |
| Action | [Direct / reverse, and why] |
| Failure position | [Fail open / closed / last, and the consequence of each] |

**Description.** [Prose: what the loop does, when it is in automatic, what an operator should
expect to see, and what it means when the valve sits at 100 percent.]

**Tuning.** [Initial values, and a note on the dominant time constant.]

---

## 4. Normal operation

[The steady state. What the operator watches, what the normal ranges are, what routine
interventions are expected during a shift.]

---

## 5. Start-up and shutdown

### 5.1 Cold start
[Numbered, in order, including the checks that must pass before each stage.]

### 5.2 Normal shutdown

### 5.3 Emergency shutdown
[What trips, in what order, and what stays running. State explicitly which items remain
energised, because that is the question the maintenance team will ask first.]

---

## 6. Upset conditions

| Condition | Symptom | Cause | System response | Operator action |
|---|---|---|---|---|
| [High level in T-101] | [LAH-101 alarm] | [Outfeed blocked] | [Feed pump stops] | [Investigate outfeed] |

---

## 7. Operator responsibilities

[What the operator is expected to do, and, just as usefully, what they must not do. If there
are actions that require a permit or a second person, say so here.]
