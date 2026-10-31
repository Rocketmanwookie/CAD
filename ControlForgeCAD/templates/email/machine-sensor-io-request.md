# Machine, Sensor, and I/O Request

Subject: Machine / Sensor / I/O Information Request - {{project_name}}

Hello {{recipient_name}},

We are preparing the controls package for {{project_name}} and need process, machine, sensor, and I/O information before PLC I/O, wiring, HMI requirements, and panel layout are finalized.

## Machine/process overview

1. Machine or process description:
2. Main sequence of operation:
3. Throughput or cycle-time requirement:
4. Manual mode requirements:
5. Maintenance mode requirements:
6. Known jam/fault conditions:
7. Required operator interactions:

## Motors, actuators, and controlled devices

1. Motor list:
2. VFD/drive requirements:
3. Solenoids/valves:
4. Pneumatic cylinders:
5. Hydraulic devices:
6. Heaters/cooling devices:
7. Other controlled loads:

## Sensors and feedback

1. Sensor list:
2. Sensor type for each location:
3. Signal type for each sensor:
4. Analog scaling requirements:
5. Encoder/high-speed input requirements:
6. Calibration requirements:
7. Preferred connector/cable type:
8. Junction box or remote I/O locations:
9. Spare sensor/I/O requirements:

## Drawings and references

1. Mechanical drawing reference:
2. P&ID reference, if applicable:
3. Existing controls drawing reference:
4. Existing I/O list reference:
5. Field photos or site notes available:
6. Contact for clarification:

## Per-load electrical and operating record

Repeat for every physical load occurrence, including repeated identical devices.
Record a stable occurrence identity, one owning physical machine/panel/location
identity, separate circuit and function references,
tag, quantity basis, nameplate/datasheet reference and revision, voltage/phase/
frequency, rated current or power with units, starting/inrush information,
duty/cycling, and simultaneous operating conditions. Identify the requested
drive/control method (for example direct starter, reversing starter, or VFD)
explicitly; a motor list alone does not select a starter arrangement.

For proposed switching/protection, request utilization/duty evidence, coil
voltage and holding/pickup demand, auxiliary-contact needs, feedback/interlocks,
overload/short-circuit requirements, manufacturer compatibility references,
environmental limits, and the engineering reviewer. Leave unresolved ratings
and settings open rather than copying a typical part.

## Per-point electrical and functional record

Repeat for each actual I/O point: stable signal and field-device identities,
owning load/function, direction/type, electrical level, sourcing/sinking or
contact arrangement, sensor/actuator supply, normal and loss-of-power states,
signal range/units, cable/terminal endpoints, shielding/isolation needs,
diagnostics, response timing, and safety-function reference where applicable.
Include commanded behavior, permissives, interlocks, reset/restart behavior,
feedback, and the approved narrative/function reference needed for each rung.

I/O counts support capacity planning; verified electrical characteristics are
also needed to establish compatible modules and interfaces. Counts alone do
not determine a control power supply or application logic.

## Evidence and review

For each record, identify source/revision, received date, verifier, verification
method/evidence, disposition, open conflicts, and follow-up owner. Supply an
applicable revision for the load list, I/O list, and control narrative so a
change can invalidate affected proposals and drawing/rung instances.

Thank you,

{{requester_name}}
