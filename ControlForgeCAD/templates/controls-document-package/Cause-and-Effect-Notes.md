# Cause and Effect Matrix, notes and rules
## [Project name]

| | |
|---|---|
| **Document title** | Cause and Effect Matrix, notes and rules (C&E) |
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

## How to read the matrix

Each row is a cause. Each column after the delay is an effect. An X means that cause produces
that effect. A blank means it does not, and a blank is a statement, not an omission.

## Rules that apply to the whole matrix

**Fail safe.** Every effect listed is the de-energised state unless the row says otherwise. A
loss of control power produces every effect in the C-010 row, and that row is not optional.

**Delays.** A delay is a deliberate filter against a noisy signal or a transient. A zero delay
on a safety cause is correct and must not be "tuned out" during commissioning because it is
nuisance tripping. Nuisance tripping on a safety input is a fault to be found, not a delay to
be added.

**Reset type.** Auto means the effect clears when the cause clears. Manual means an operator
must act. Every safety related cause is manual reset, per ISO 13849-1: a machine that restarts
by itself when a guard is closed is a machine that restarts with someone inside it.

**Master trip.** Where a cause is marked for master trip, all other effects are implied. It is
still listed explicitly, because implied behaviour is untestable behaviour.

## Bypass and override

| Ref | What may be bypassed | Who may authorise | Conditions | Recorded |
|---|---|---|---|---|
| BP-001 | [Signal] | [Role, level 3] | [e.g. maintenance mode only, key switch] | Yes, audit trail |

No safety instrumented function may be bypassed from the operator interface. If a bypass is
required for maintenance, it is key switched, it is alarmed while active, and it is logged.

## Testing

Each X is one test. The test proves the effect happens, and it also proves the blanks: while
testing C-006, confirm the pump does *not* stop. Testing only the marks proves half the matrix.

| Test ref | Cause | Method | Expected | Result | Tester | Date |
|---|---|---|---|---|---|---|
| FAT-IL-001 | C-003 | [Simulate LT-101 above 95%] | [Effects per row] | | | |
