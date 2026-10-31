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
| Tag | Issued engineering designation under the project's naming convention | A display/cross-reference designation; stable CE identities remain the internal keys. Record renames and reconcile affected documents. |
| Description | Plain language, 40 characters or fewer | This becomes the HMI text and the alarm text. Write it for an operator at 3 am. |
| Signal Type | Electrical nature, e.g. 24VDC Sourcing, 4-20mA 2-wire, RTD Pt100 3-wire | Decides the card, and decides whether a barrier is needed. |
| I/O Type | DI, DO, AI, AO, and the Safety variants | Drives the card count. |
| Rack / Slot / Channel | Physical location | The path from a tag to a screw terminal. |
| Address | Controller address | Vendor specific. Keep the vendor's own syntax. |
| Panel / Terminal | Where it lands in the panel | The panel builder works from this. |
| Cable / Core | Field cable and core number | Must agree with the cable schedule. |
| Range Low / High / Units | Engineering range for analog | Must agree with the transmitter configuration, not with what somebody hoped. |
| Fail Safe State | What the signal does on failure | The column most often left blank and most often needed. |
| Normally | Physical NO/NC state with its reference condition, supply, and input interpretation | Supports circuit review; contact type alone does not establish fault detection or a safety function. |
| Alarm Low / High / Trip | Limits | Feeds the RATS and the alarm list. |
| Interlock Ref | Cross reference to the FDS | Ties this signal to the logic that uses it. |
| Loop Drawing | Drawing number | Where to look when it does not work. |
| Tested FAT / SAT | Sign-off | Initial and date. This is the evidence. |

The I/O list must be reconciled with the PLC drawing, loop/field drawing,
terminal plan, cable schedule, and deployed PLC configuration using the
addressing and signal-traceability rules in
[`IEC-61082-1-Addressing-and-Traceability.md`](IEC-61082-1-Addressing-and-Traceability.md).
For each implemented field I/O, the controlled record must permit tracing the
tag through cable/core, panel terminal, wire, PLC module/channel, native PLC
address, and functional/test references.

## Conventions worth holding to

**Failure behavior.** Record the required response to loss of power, broken
wire, communication failure, and device fault for the specific circuit. Link
any safety function to its independent assessment and reviewed architecture;
NO/NC or a Boolean PLC state alone is not evidence of a safe implementation.

**Spare capacity.** Record actual demand, the project-approved reserve policy,
and installed capacity separately. The current workbench uses a 20-percent
capacity-planning rule for ordinary I/O; this is not a universal engineering
requirement or a safety-channel rule. List unused installed channels as spare
channel occurrences, not actual signal or field-device occurrences.

**Analog fail state.** "Hold last" is a decision, not a default. A held value on a failed flow
transmitter will keep a sequence running that should have stopped. Decide per signal.

**Do not renumber.** Once the panel is wired, a tag change is a change to the panel, the
drawings, the program and the HMI. Add, do not renumber.

## Input verification and dependent instances

For each actual signal, retain its stable identity, parent/owning device and
function references, source document/revision, verification evidence, reviewer,
and disposition. Retain electrical characteristics separately from DI/DO/AI/AO
classification. Link PLC channel, power domain, controlled-load/interface,
terminal/cable/wire, circuit, drawing, and rung/function references through
identities rather than display tags. An input revision change must mark those
dependent results for review without silently replacing physical occurrences.

The original authored [engineering readiness supplement](Engineering-Readiness.md)
defines proposed intake gates. It does not approve this provenance-blocked
package or implement a generator.
