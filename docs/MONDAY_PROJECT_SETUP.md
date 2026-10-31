# integraCAD Open monday project setup

Superseded: the project owner selected GitHub Projects on 2026-10-27.
Use [GitHub project setup](GITHUB_PROJECT_SETUP.md) for the active destination.
The task seed below is retained as the source for initial population; no
monday board was created.

Prepared 2026-10-27, America/New_York.

User selected monday.com for project management. Confirmed connection:
[Main workspace](https://whrsdapartys-team.monday.com/workspaces/17540256),
workspace ID `17540256`. Existing `My first project` board was not changed.
No integraCAD board existed in the workspace when checked.

Private board creation returned `USER_UNAUTHORIZED` (403); a prior assisted
creation returned 500 and a direct read confirmed no board was created.
Account tier is unavailable, so the cause cannot be attributed to a plan.
Do not retry creation through another API to bypass this rejection. Obtain
authorization for a Main board or a writable private board supplied by the
owner. Main boards are visible to account members, not anonymous web users.

## Board specification

Name: `integraCAD_OPEN — Engineering & Development`.

Columns: Workflow Status; Owner; Agent Role; Depends On; Acceptance Criteria;
Evidence & Limitations; GitHub; Review State; Target Date.

Workflow labels: Backlog, In progress, Blocked, Needs review, Complete.
Review labels: Not reviewed, Controls review needed, QA review needed,
Owner decision needed, Accepted. Human Owner and Target Date remain empty
until assigned. Agent Role is text, not an invented monday user account.
Depends On initially records stable task keys explicitly; native dependency
scheduling is a later configuration choice, not an implied integration.

GitHub source: https://github.com/Rocketmanwookie/CAD . Repository files
remain authoritative code/design evidence; board status does not establish
engineering approval or replace release acceptance. No automatic repository
sync, notifications, invitations or schedules are configured.

## Initial task seed

All implementation tasks below are Backlog unless a specific current state
is recorded. Reviewed template edits and the proposed design are local,
uncommitted artifacts and must not be linked as already published GitHub files.

| Key | Group | Task | Agent role | Depends on | Acceptance and current evidence |
|---|---|---|---|---|---|
| IN-01 | Intake & verified inputs | Review engineering intake templates | Controls Engineer | — | Needs review: six emails, I/O guide, Engineering Readiness and original draft SAT updated locally; source package approval remains blocked |
| IN-02 | Intake & verified inputs | Capture revision-bound verification in structured intake | Backend / Controls Engineer | IN-01, DATA-01 | Value/unit/source revision/verifier/scope persist; imported Verified text alone cannot authorize derivation |
| IN-03 | Intake & verified inputs | Resolve supplied template provenance and issue disposition | Project owner / Controls Engineer | — | Blocked: source, rights and reviewer evidence remain missing for supplied reference assets |
| DATA-01 | Instance hierarchy & data contracts | Complete JSON-first migration | Backend / Schema | — | JSON project/catalog round trips, legacy XML import only, documented supported versions; existing design is local |
| INST-01 | Instance hierarchy & data contracts | Review ownership and dependency design | Controls Engineer / Project owner | — | Needs review: proposed design and two advisory Controls Engineer reviews; owner agreement on extended hierarchy pending |
| INST-02 | Instance hierarchy & data contracts | Implement verification and ownership foundation | Python / FreeCAD | INST-01, DATA-01 | Reject cycles/ambiguous roots/cross-owner links; stable identities, revision checks, rollback and persistence |
| INST-03 | Instance hierarchy & data contracts | Derive supply and feeder circuit instances | Backend / Controls Engineer | IN-02, INST-02 | Verified infeed creates project-owned draft circuit and missing-data manifest; no inferred protective ratings |
| PLC-01 | PLC & I/O configuration | Verify visible count-configure-define workflow | FreeCAD / QA | — | Needs review: I/O Count restored locally; 286 headless tests passed; actual toolbar and save/reopen acceptance unrun |
| PLC-02 | PLC & I/O configuration | Reconcile reviewed PLC instances with electrical I/O requirements | Controls Engineer / Backend | IN-02, INST-02, PLC-01 | Preserve rack/module/channel identities; actual/spare distinction and electrical compatibility checks |
| PWR-01 | Control power & load protection | Build supply-domain and consumer power budget | Controls Engineer / Python | IN-02, PLC-02 | Source-based demand per consumer/interface/domain; separate backplane, external and field-output demand; no double counting |
| PWR-02 | Control power & load protection | Propose supplies and accepted equipment instances | Controls Engineer / Backend | PWR-01, INST-02 | Reviewed candidates retain demand/derating/inrush evidence and decision references |
| PWR-03 | Control power & load protection | Propose controlled-load switching and protection | Controls Engineer / motor and protection SMEs | IN-02, INST-03 | Explicit drive arrangement; evidence-backed candidates; joint motor/protection consultation before motor sizing approval |
| DWG-01 | Drawings & coordinated package | Implement shared device and symbol occurrence model | Controls Engineer / FreeCAD | INST-02 | Coil/main/aux and split PLC symbols reference one device; separate symbol IDs and pin mapping; one physical BOM occurrence |
| DWG-02 | Drawings & coordinated package | Generate coordinated single-line and three-line views | Controls Engineer / Drawing adapter | INST-03, PWR-02, PWR-03, DWG-01 | Explicit selected view type, shared snapshot, cross-references, phase/neutral/PE and pending decisions |
| DWG-03 | Drawings & coordinated package | Generate low-voltage electrical ladder and I/O interfaces | Controls Engineer / Drawing adapter | PLC-02, PWR-02, DWG-01 | Verified connections and approved functional intent; electrical rungs distinguished from executable PLC logic |
| QA-01 | Acceptance & release | Prove regeneration, persistence and stale dependencies | QA / FreeCAD | INST-03, PLC-02, PWR-02, PWR-03, DWG-02, DWG-03 | Repeated generation has no duplicates; changes invalidate exact dependencies; rollback/save/reopen retain links |
| QA-02 | Acceptance & release | Complete review and release evidence | QA / Controls Engineer / Project owner | QA-01, IN-03 | Required cadence reports, qualified decisions where applicable, real FreeCAD evidence and coordinated exports; no inferred pass |

## Before population

Confirm the actual destination and board visibility. Read board metadata to
obtain real column IDs/labels and check existing task keys before writes.
Populate by stable task key; retain returned item IDs and board URL here.
Verify every item and dependency text after creation. Partial failures must
be reconciled by read-back rather than replaying the whole seed.
