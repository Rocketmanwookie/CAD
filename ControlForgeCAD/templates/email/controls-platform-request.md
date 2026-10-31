# Controls Platform Standards Request

Subject: Controls Platform Standards Request - {{project_name}}

Hello {{recipient_name}},

We are preparing the controls package for {{project_name}} and need the controls-platform requirements before finalizing PLC I/O, HMI requirements, cabinet layout, wiring, and project documentation.

## Required information

1. Preferred PLC manufacturer/platform:
2. Preferred PLC software/version:
3. Preferred HMI/SCADA platform:
4. Required industrial network protocol:
5. Tag naming standard:
6. Drawing/documentation standard:
7. Required spare I/O percentage:
8. Remote access requirement or restriction:
9. Backup/restore expectation:
10. Approved vendor list:
11. Prohibited vendors or product lines:
12. Required data collection, historian, or reporting points:
13. Alarm philosophy or alarm standard:
14. Cybersecurity/network requirements:
15. Customer standard drawings/templates available:
16. Contact for controls clarification:

Please identify which values are standards, preferences, assumptions, or open decisions.

## PLC and control-power proposal prerequisites

Provide the CPU/module/firmware compatibility references; backplane and field
power demands and limits; per-channel and grouped-output ratings; required
special/high-speed functions; network topology; and local/remote rack ownership.
Keep actual demand, required spare capacity, and installed capacity separate.
Unused physical channels are spare channels, not invented field devices.

For every control-power domain, list the PLC, modules, HMI, network equipment,
sensors, relays/contactors, valves, and other consumers with source revisions,
voltage/tolerance, continuous and startup/pickup demand, simultaneity assumptions,
and domain/source/return assignments. Identify external supplies and prevent
double-counting field loads already included in an equipment specification.
Request ambient/altitude derating references, reserve policy, redundancy/hold-up
requirements, distribution protection, and the reviewer's recorded decision.

Record stable controller/rack/module/channel occurrence identities and their
parent links. Module replacement or changed I/O electrical requirements must
trigger review of channel mappings, power budget, interfaces, and drawings.
Catalog feasibility and a calculated power budget are proposals until their
required engineering decisions have an explicit disposition.

Thank you,

{{requester_name}}
