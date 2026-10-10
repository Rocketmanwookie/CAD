# Alarm Rationalisation Record
## [Project name]

| | |
|---|---|
| **Document title** | Alarm Rationalisation Record (ALM) |
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

## Why this document exists

An alarm exists to tell an operator to do something they would not otherwise do, in time for it
to matter. ISA-18.2 makes that testable with three questions, and every alarm on the list must
answer all three:

1. What is the **consequence** if the operator does nothing?
2. How long do they have to **respond** before that consequence occurs?
3. What **action** do they take?

If a proposed alarm has no answer to question 3, it is an indication and belongs on a status
display. If it has no answer to question 1, delete it.

## Priority assignment

Priority follows from consequence severity and from the time available, not from how important
the equipment feels.

| Priority | Consequence | Time to respond | Target share of alarms |
|---|---|---|---|
| High | Injury, environmental release, major loss | Under 3 minutes | 5% |
| Medium | Product loss, equipment damage | 3 to 30 minutes | 15% |
| Low | Efficiency, minor quality | Over 30 minutes | 80% |

## Performance targets

From ISA-18.2, per operator console:

| Metric | Target | Maximum acceptable |
|---|---|---|
| Average alarms per hour | 6 | 12 |
| Peak alarms in 10 minutes | 5 | 10 |
| Time in flood condition | 0% | 1% |
| Standing alarms | 0 | 5 |

Measure these during the SAT and again after 30 days of operation. An alarm system that meets
them on day one and not on day thirty has a chattering alarm somewhere, and the deadband or the
delay is wrong.

## Rationalisation session record

| Date | Attendees | Alarms reviewed | Added | Removed | Re-prioritised |
|---|---|---|---|---|---|
| | | | | | |

## Chattering and stale alarms

| Alarm | Occurrences per hour | Cause | Action | Closed |
|---|---|---|---|---|
| | | | [Deadband, delay, or fix the instrument] | |
