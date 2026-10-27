# Change Control Record
## [Project name]

| | |
|---|---|
| **Document title** | Change Control Record (MOC) |
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

| Field | Value |
|---|---|
| Change reference | |
| Raised by | |
| Date raised | |
| System affected | [Project name] |
| Urgency | Routine / Urgent / Emergency |

---

## 1. Description of change

**What is changing.**
[Describe precisely. "Improve the sequence" is not a description.]

**Why.**
[The problem being solved. If the answer is "somebody asked", find out why they asked.]

**What happens if we do nothing.**
[Sometimes the honest answer is "nothing", and that is a valid outcome for this form.]

---

## 2. Impact assessment

Tick everything the change touches. Anything ticked needs its document updated and its tests
repeated.

| Area | Affected | Document to update | Updated |
|---|---|---|---|
| PLC program | | SDS, program backup | |
| Safety program | | Risk assessment, safety calc | |
| HMI application | | FDS section 8 | |
| I/O allocation | | I/O list, schematics | |
| Field wiring | | Cable schedule, loop drawings | |
| Alarms | | Alarm list, rationalisation | |
| Interlocks | | Cause and effect matrix | |
| Recipes or parameters | | FDS section 9 | |
| Network or interfaces | | FDS section 10 | |
| Operating procedure | | O&M manual | |
| Training | | Training records | |

---

## 3. Safety review

| Question | Answer |
|---|---|
| Does the change affect a safety function? | Yes / No |
| Does it affect an interlock or a trip? | Yes / No |
| Does it change the risk assessment? | Yes / No |
| Does it affect the achieved performance level? | Yes / No |
| Is a new hazard introduced? | Yes / No |

**If any answer is Yes**, the change requires review by a competent person and revalidation of
the affected safety function. It does not proceed on an operator's request alone.

| Safety review by | Signature | Date |
|---|---|---|
| | | |

---

## 4. Test plan

| # | Test | Expected result | Actual | Pass | Tester |
|---|---|---|---|---|---|
| 1 | [Test the change itself] | | | | |
| 2 | [Test what the change might have broken] | | | | |
| 3 | [Regression: the interlocks still work] | | | | |

Test 2 and 3 are the ones that matter. Testing only the change proves only that the change
does something, not that everything else still does.

---

## 5. Rollback plan

| Item | Detail |
|---|---|
| Backup taken before change | Yes / No, location: |
| Backup verified | Yes / No |
| Rollback procedure | [Numbered steps] |
| Time to roll back | [minutes] |
| Point of no return | [If any, state it clearly] |

---

## 6. Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Requester | | | |
| Technical review | | | |
| Safety authority (if applicable) | | | |
| System owner | | | |

---

## 7. Implementation record

| Field | Value |
|---|---|
| Implemented by | |
| Date and time started | |
| Date and time completed | |
| Program version before | |
| Program version after | |
| Checksum after | |
| Tests completed | |
| Documents updated | |
| Backup taken after change | |

## 8. Closure

| Role | Name | Signature | Date |
|---|---|---|---|
| Verified by | | | |
| Closed by | | | |
