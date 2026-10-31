# Safety Requirements Request

Subject: Safety Requirements Request - {{project_name}}

Hello {{recipient_name}},

We are preparing the controls package for {{project_name}} and need the current safety requirements and related references. Please identify which items are confirmed, assumed, or still under review.

## Safety documentation

1. Risk assessment available:
2. Safety requirements specification available:
3. Required customer safety standard:
4. Required site safety standard:
5. Required machine or process standard references:
6. Contact responsible for safety approval:

## Safety devices and functions

1. E-stop locations/zones:
2. Guard doors or access gates:
3. Light curtains or scanners:
4. Safety mats or presence sensing:
5. Required safety relay or safety controller preference:
6. Required STO circuits:
7. Reset type and reset locations:
8. Feedback/monitoring contact requirements:
9. Manual/maintenance mode requirements:
10. Lockout/tagout considerations:

## Controls integration

1. Safety status points needed in PLC/HMI:
2. Alarm or event logging requirements:
3. Required safety validation or checkout documentation:
4. Required field test or commissioning witness:
5. Open safety decisions:

## Verification and instance references

For each safety function, record its stable identity, zone and controlled
load/interface identities, required response, supplied PL/SIL/category or other
performance requirement where applicable, requirement source/revision, and
responsible safety reviewer. Record required channel architecture, diagnostics,
reset/restart, feedback, power-loss behavior, and validation evidence separately
from ordinary PLC status points and I/O capacity/spare policy.

Identify shared physical devices and terminals through existing occurrence
identities. Record the function's verification/approval scope, date, reviewer,
open decisions, and references to the safety circuit and independent validation
plan. A response, diagram, NO/NC designation, or generated rung is not evidence
of achieved safety performance. Changes to requirements or shared interfaces
must reopen review of dependent circuits, logic, and tests.

Thank you,

{{requester_name}}
