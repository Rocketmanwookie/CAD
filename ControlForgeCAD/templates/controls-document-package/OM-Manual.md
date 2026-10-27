# Operation and Maintenance Manual
## [Project name]

| | |
|---|---|
| **Document title** | Operation and Maintenance Manual (O&M) |
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

## 1. Safety information

**Read this section before operating or working on the system.**

### 1.1 Residual risks
| Risk | Where | Precaution |
|---|---|---|
| | | |

### 1.2 Isolation
[How to isolate the system safely, including every energy source: electrical, pneumatic,
hydraulic, gravity and stored energy. List them all. The one that is forgotten is the one that
causes the injury.]

| Energy source | Isolation point | Method | Verification |
|---|---|---|---|
| Electrical, 400 V | [Isolator ref] | Lock off | Prove dead |
| Control, 24 V | | | |
| Compressed air | | | Vent and verify zero |
| Stored, [e.g. raised load] | | | |

### 1.3 Personal protective equipment
[What is required, and where.]

---

## 2. System description

[Plain language. What the system does, what the main parts are, and how they relate. A diagram
belongs here. Assume the reader has never seen the machine.]

---

## 3. Operating instructions

### 3.1 Before starting
| # | Check |
|---|---|
| 1 | [Check] |

### 3.2 Starting
1. [Step, with what to expect on the screen]

### 3.3 Normal running
[What the operator watches. What normal looks like, with numbers.]

### 3.4 Stopping
1. [Step]

### 3.5 Emergency stop and recovery
1. [What to do]
2. [How to make safe]
3. [How to reset, and what must be true first]

---

## 4. Alarm response guide

Ordered by the alarm message the operator sees, because that is what they are holding.

| Alarm message | What it means | What to do | If it persists |
|---|---|---|---|
| Feed tank level high high | Level above 95%, feed stopped automatically | Check the outfeed route is clear, then reset | Call maintenance, do not bypass |
| Valve failed to open | No open confirmation within 10 seconds | Check air supply pressure and the limit switch | Call maintenance |

---

## 5. Fault finding

By symptom. The reader knows what they can see, not which subsystem is at fault.

### 5.1 The machine will not start

| Check | How | If not right |
|---|---|---|
| Is an E-stop pressed? | Check all stations, look for the latched button | Release, twist to reset, then press Reset |
| Are all guards closed? | Check the guard status screen | Close and latch the guard shown |
| Is the mode correct? | Check mode indicator | Select Auto |
| Is there a standing alarm? | Check alarm list | Clear the cause, then acknowledge |
| Is control power on? | Check 24 V indicator in panel | Check MCB, check power supply |

### 5.2 The sequence stops part way through

| Check | How | If not right |
|---|---|---|
| Which step is it on? | Sequence screen shows the step number | Compare with the FDS sequence table |
| Is there a step timeout alarm? | Alarm list | The alarm names the step that failed |
| Is the transition condition met? | Check the device the step waits for | Investigate that device |

### 5.3 A value on screen looks wrong

| Check | How | If not right |
|---|---|---|
| Is the reading at the extreme? | Look for 0 or full scale | Suspect a broken wire or a shorted loop |
| Does the local gauge agree? | Compare | If not, suspect the transmitter or its calibration |
| Was it right yesterday? | Check the trend | A step change points at a hardware event |

---

## 6. Routine maintenance

| Task | Interval | Procedure | Skill |
|---|---|---|---|
| | | | |

---

## 7. Parts and consumables

| Part | Number | Used in | Typical life |
|---|---|---|---|
| | | | |
