# Software Design Specification
## [Project name]

| | |
|---|---|
| **Document title** | Software Design Specification (SDS) |
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

## 1. Program organisation

| POU | Type | Language | Called from | Interval | Purpose |
|---|---|---|---|---|---|
| Main | Program | LD | Cyclic task | 10 ms | Coordination and calls |
| Safety | Program | LD | Safety task | 10 ms | Safety logic only |
| Sequence | Function block | SFC | Main | | Step sequencing |
| Alarms | Function block | ST | Main | | Alarm evaluation |
| Analog | Function block | ST | Main | 100 ms | Scaling and filtering |
| Comms | Function block | ST | Main | 100 ms | External interfaces |

**Task allocation.** [State why each POU is where it is. Anything that must react to a fast
event goes in the fast task; anything that does not, does not, because scan time is a budget.]

---

## 2. Naming conventions

The convention matters less than the consistency. Pick one, write it here, and hold to it.

| Object | Pattern | Example | Notes |
|---|---|---|---|
| Digital input | `XX_nnn_FUNC` | `XV_101_ZSO` | Device, number, function |
| Digital output | `XX_nnn_CMD` | `MTR_101_RUN` | |
| Analog input | `XT_nnn` | `FT_101` | ISA-5.1 letters |
| Internal flag | `b` prefix | `bSequenceRunning` | |
| Timer | `t` prefix | `tValveTimeout` | |
| Counter | `c` prefix | `cCyclesComplete` | |
| Constant | Upper snake | `MAX_TEMP` | |
| Function block instance | `fb` prefix | `fbFeedPump` | |
| Step number | `STEP_` | `STEP_FILL` | Named, never a bare integer |

**Forbidden.** Single letter names, names that differ only by case, names that encode the
address (`I0_0`), and any name that requires the comment to be readable.

---

## 3. Standard function blocks

The library used on this project. Each block is tested once and reused, rather than the logic
being retyped per device.

| Block | Purpose | Inputs | Outputs | Notes |
|---|---|---|---|---|
| `FB_Motor` | Motor start, stop, fault, run hours | Cmd, Fbk, Interlock, Reset | Run, Fault, Hours | Feedback timeout configurable |
| `FB_Valve` | Two position valve with limits | Cmd, ZSO, ZSC, Interlock | Sol, Fault, Position | Travel timeout per instance |
| `FB_AnalogIn` | Scale, filter, range check, alarm | Raw, RangeLo, RangeHi | Value, Fault, AlmL, AlmH | Detects out of range both ends |
| `FB_Alarm` | Alarm with delay, deadband, ack | Trigger, Ack | Active, Unack, Latched | |
| `FB_Sequence` | Step engine with timeout | Enable, StepDone | Step, Timeout | |

**Rule.** A block is either general or it is not used. A "general" block with an `if
device = 3` inside it is two blocks pretending to be one.

---

## 4. Memory and addressing

| Area | Range | Use | Retentive |
|---|---|---|---|
| Inputs | | Physical inputs | No |
| Outputs | | Physical outputs | No |
| Markers | | Internal flags | Partly |
| Retentive | | Counters, run hours, recipe | Yes |
| Data blocks | | Structured data | Per block |

**Retentive data.** [List exactly what survives a power cycle and why. Anything retentive needs
a defined behaviour on first run after a memory clear.]

---

## 5. State machine pattern

Every sequence uses the same shape, so that any engineer reading any sequence recognises it.

```
STEP:
  entry action, executed once
  running action, executed every scan while in step
  transition condition -> next step
  timeout -> alarm and hold
```

**Rules.**

- A step is only left through a defined transition or a timeout. There is no other exit.
- Every step has a timeout. A step without one can hang forever, and the operator's report will
  be "it just stopped".
- Step numbers are named constants, never bare integers.
- The current step number is exposed to the HMI. Diagnosing a stuck sequence without it means
  going online with the programming software.

---

## 6. Coding rules

| # | Rule | Reason |
|---|---|---|
| 1 | One coil per tag, in one place | Two coils on one tag means the last rung wins and the first is invisible |
| 2 | No duplicated logic, use a block | Two copies drift apart |
| 3 | No jumps backwards | Unreadable and can create loops |
| 4 | Every rung commented with intent, not restatement | "Start latches" not "XIC Start OTE Run" |
| 5 | No online edits without a change record | Undocumented online edits are how a program stops matching its printout |
| 6 | Safety logic in the safety task only | Mixing them defeats the safety certification |
| 7 | No forces left in the delivered program | A force is a temporary tool, not a fix |
| 8 | Timers use named presets, not literals | A literal 5000 explains nothing |
| 9 | Analog values checked for range before use | An out of range value used in a calculation propagates silently |
| 10 | First scan initialisation is explicit | Relying on default zero is relying on the vendor |

---

## 7. Version control and change record

| Version | Date | Author | Change | Reason | Tested | Approved |
|---|---|---|---|---|---|---|
| 1.0 | [Date] | [Author] | First issue | | | |

**Backup.** Source and compiled program archived at [location] after every change. Checksum
recorded in the handover pack.
