# Handover and As-Built Pack
## [Project name]

| | |
|---|---|
| **Document title** | Handover and As-Built Pack (HO) |
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

## 1. Document register

Every document handed over, at the revision handed over. "Latest" is not a revision.

| # | Document | Number | Rev | Format | Location | Received |
|---|---|---|---|---|---|---|
| 1 | User Requirement Specification | | | PDF | | |
| 2 | Functional Design Specification | | | PDF | | |
| 3 | Software Design Specification | | | PDF | | |
| 4 | Control narrative | | | PDF | | |
| 5 | I/O list, as-built | | | XLSX | | |
| 6 | Cause and effect matrix | | | XLSX | | |
| 7 | RATS | | | XLSX | | |
| 8 | Alarm list, rationalised | | | XLSX | | |
| 9 | Panel schematics, as-built | | | PDF + DWG | | |
| 10 | Panel general arrangement | | | PDF + DWG | | |
| 11 | Cable schedule, as-built | | | XLSX | | |
| 12 | Loop drawings | | | PDF | | |
| 13 | Bill of materials | | | XLSX | | |
| 14 | Risk assessment | | | PDF | | |
| 15 | Safety calculations | | | PDF | | |
| 16 | FAT protocol and results | | | PDF | | |
| 17 | SAT protocol and results | | | PDF | | |
| 18 | Commissioning checklist, completed | | | PDF | | |
| 19 | Calibration certificates | | | PDF | | |
| 20 | O&M manual | | | PDF | | |
| 21 | Training records | | | PDF | | |
| 22 | Declaration of conformity | | | PDF | | |
| 23 | Equipment manuals, all devices | | | PDF | | |

**As-built means as-built.** If a wire was moved during commissioning and the drawing was not
updated, the pack is wrong and the next person will trust it.

---

## 2. Software and firmware record

| Item | Product | Version | Checksum | Licence key held by | Media |
|---|---|---|---|---|---|
| PLC program | | | | | |
| Safety program | | | | | |
| HMI application | | | | | |
| CPU firmware | | | | | |
| Remote I/O firmware | | | | | |
| Drive parameters | | | | | |
| Managed switch config | | | | | |
| Programming software | | | | | |

**Licences.** State who holds them and whether the site can open the program without buying
software. A program the site cannot open is a program the site does not own.

---

## 3. Backup and restore

### 3.1 What is backed up
| Item | Location | Frequency | Responsible |
|---|---|---|---|
| PLC program | | On change | |
| HMI application | | On change | |
| Recipes and parameters | | Weekly | |
| Historical data | | Daily | |

### 3.2 Restore procedure
[Numbered steps to restore a failed controller from backup, including how to verify the restore
worked. Write it so that someone who has never done it can follow it at 2 am.]

1. [Step]
2. [Step]

**Restore has been tested.** Date: __________ By: __________

> An untested backup is a hope. Test the restore before handover and record it here.

---

## 4. Spare parts

| Item | Manufacturer | Part number | Qty supplied | Qty recommended | Location | Lead time |
|---|---|---|---|---|---|---|
| | | | | | | |

**Critical spares.** [Items with a lead time long enough to matter. These are the ones worth
holding, and the ones the site will not think about until one fails.]

---

## 5. Maintenance schedule

| Task | Interval | Duration | Skill | Procedure ref |
|---|---|---|---|---|
| Panel inspection, thermal check | 6 months | 1 h | Electrician | |
| Filter fan replacement | 12 months | 30 min | Technician | |
| Instrument calibration | 12 months | | Instrument tech | |
| Safety function proof test | 12 months | | Competent person | |
| Backup verification | 6 months | 1 h | Engineer | |
| UPS battery test | 12 months | | Electrician | |

**Safety proof testing.** The interval comes from the safety calculation, not from convenience.
Record it and hold to it, because the achieved PL assumes it.

---

## 6. Support and escalation

| Level | Contact | Hours | Response | Covers |
|---|---|---|---|---|
| 1 | Site maintenance | | | First line |
| 2 | [Your company] support | | | Program and configuration |
| 3 | Vendor | | | Hardware failure |

| Detail | Value |
|---|---|
| Support contract reference | |
| Warranty expiry | |
| Remote access method | |
| Remote access approval process | |

---

## 7. Receipt

The items listed in section 1 have been received by [Client].

| Role | Name | Signature | Date |
|---|---|---|---|
| Issued by | | | |
| Received by | | | |
