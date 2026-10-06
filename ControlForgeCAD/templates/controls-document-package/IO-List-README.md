# I/O List, conventions and column guide
## [Project name]

| | |
|---|---|
| **Document title** | I/O List, conventions and column guide (I/O) |
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

## How to use this list

The CSV is the deliverable. This note explains the columns and the conventions, so that the
list stays consistent when several people edit it.

## Column guide

| Column | What goes in it | Why it matters |
|---|---|---|
| Tag | Unique identifier, per ISA-5.1 | The primary key. Never reuse a tag, even after a device is removed. |
| Description | Plain language, 40 characters or fewer | This becomes the HMI text and the alarm text. Write it for an operator at 3 am. |
| Signal Type | Electrical nature, e.g. 24VDC Sourcing, 4-20mA 2-wire, RTD Pt100 3-wire | Decides the card, and decides whether a barrier is needed. |
| I/O Type | DI, DO, AI, AO, and the Safety variants | Drives the card count. |
| Rack / Slot / Channel | Physical location | The path from a tag to a screw terminal. |
| Address | Controller address | Vendor specific. Keep the vendor's own syntax. |
| Panel / Terminal | Where it lands in the panel | The panel builder works from this. |
| Cable / Core | Field cable and core number | Must agree with the cable schedule. |
| Range Low / High / Units | Engineering range for analog | Must agree with the transmitter configuration, not with what somebody hoped. |
| Fail Safe State | What the signal does on failure | The column most often left blank and most often needed. |
| Normally | NO or NC for discrete field devices | Determines whether a broken wire reads as safe or as normal. |
| Alarm Low / High / Trip | Limits | Feeds the RATS and the alarm list. |
| Interlock Ref | Cross reference to the FDS | Ties this signal to the logic that uses it. |
| Loop Drawing | Drawing number | Where to look when it does not work. |
| Tested FAT / SAT | Sign-off | Initial and date. This is the evidence. |

## Conventions worth holding to

**Fail safe direction.** Stop circuits and safety devices are normally closed, so that a broken
wire or a lost supply produces the safe state. If a column says NO for an E-stop, that is a
finding, not a preference.

**Spare capacity.** Carry at least 20 percent spare channels of each type at handover, and list
the spares explicitly with a Spare tag rather than leaving gaps. Gaps get filled by accident.

**Analog fail state.** "Hold last" is a decision, not a default. A held value on a failed flow
transmitter will keep a sequence running that should have stopped. Decide per signal.

**Do not renumber.** Once the panel is wired, a tag change is a change to the panel, the
drawings, the program and the HMI. Add, do not renumber.
