# integraCAD Open GitHub project setup

Project owner selected GitHub Projects on 2026-10-27, America/New_York.
This supersedes the monday.com destination; the prepared task seed remains
in [the earlier setup document](MONDAY_PROJECT_SETUP.md).

## Destination

- Project: [@Rocketmanwookie's IntegraCAD Open](https://github.com/users/Rocketmanwookie/projects/1).
- Owner: `Rocketmanwookie`; project number `1`.
- Node identity: `PVT_kwHOBlA0Os4Bo5YU`.
- Repository: [Rocketmanwookie/CAD](https://github.com/Rocketmanwookie/CAD).
- Existing visibility: private; preserved during setup.
- Existing PR #5 project item and existing fields are preserved.

## Planning structure

Seventeen draft tasks use stable keys: `IN-01..03`, `DATA-01`, `INST-01..03`,
`PLC-01..02`, `PWR-01..03`, `DWG-01..03`, `QA-01..02`.

The added fields are Workstream, Agent Role, Depends On, Review State, and
Evidence & Limitations. Existing Status, Assignees, Start date and Target date
fields are retained. New draft tasks initially use Todo; Review State records
the more specific review requirement or blocker. No human assignee or date
is invented. Agent Role is responsibility text, not a GitHub user identity.

Depends On records stable task keys as text. It is not a native issue-blocking
relationship or automatic scheduling. Convert drafts to repository issues
and establish issue relationships when those issues enter implementation.

Each draft includes its outcome/acceptance, role, prerequisites, repository,
and evidence boundary. Local uncommitted template/design work is explicitly
identified as local, not misrepresented as a published GitHub artifact. The
project README records the same engineering and acceptance boundaries.

## Operating rules

Check existing keys before adding tasks; reruns must not duplicate them.
Preserve surviving task identities and existing review/assignee/date changes.
No automatic sync between local files and the project is configured. Update
task evidence with exact commits, checks, engineering review and desktop
acceptance before marking work complete. Historical project entries retain
their own status and are not bulk overwritten by this setup.

No paid subscription, Codespace, automation, invitation or notification
schedule is created by this setup. Project planning uses the existing free
GitHub Projects capability.

## Verification

Population is checked by reading the project back: all 17 unique draft keys,
the preserved PR item, required fields and per-item values, valid dependency
keys, repository link, and private visibility. Remote API results establish
configuration; local software tests do not verify a GitHub project setup.

Read-back passed on 2026-10-27: 18 items total (17 unique draft tasks plus the
preserved PR #5), all six populated field values on each draft match the seed,
all prerequisite keys resolve, the repository is linked, the README and
description are populated, and visibility remains private. Existing Backlog,
Monthly roadmap and Quarterly roadmap views are retained. Local whitespace
check passed. No new custom view is claimed.

| Task key | Project item node identity |
|---|---|
| IN-01 | `PVTI_lAHOBlA0Os4Bo5YUzhD39xs` |
| IN-02 | `PVTI_lAHOBlA0Os4Bo5YUzhD391Y` |
| IN-03 | `PVTI_lAHOBlA0Os4Bo5YUzhD395U` |
| DATA-01 | `PVTI_lAHOBlA0Os4Bo5YUzhD398U` |
| INST-01 | `PVTI_lAHOBlA0Os4Bo5YUzhD3-AM` |
| INST-02 | `PVTI_lAHOBlA0Os4Bo5YUzhD3-FQ` |
| INST-03 | `PVTI_lAHOBlA0Os4Bo5YUzhD3-Is` |
| PLC-01 | `PVTI_lAHOBlA0Os4Bo5YUzhD3-Mo` |
| PLC-02 | `PVTI_lAHOBlA0Os4Bo5YUzhD3-SE` |
| PWR-01 | `PVTI_lAHOBlA0Os4Bo5YUzhD3-Yk` |
| PWR-02 | `PVTI_lAHOBlA0Os4Bo5YUzhD3-ec` |
| PWR-03 | `PVTI_lAHOBlA0Os4Bo5YUzhD3-jc` |
| DWG-01 | `PVTI_lAHOBlA0Os4Bo5YUzhD3-oE` |
| DWG-02 | `PVTI_lAHOBlA0Os4Bo5YUzhD3-vs` |
| DWG-03 | `PVTI_lAHOBlA0Os4Bo5YUzhD3-0c` |
| QA-01 | `PVTI_lAHOBlA0Os4Bo5YUzhD3-6E` |
| QA-02 | `PVTI_lAHOBlA0Os4Bo5YUzhD3_AE` |
