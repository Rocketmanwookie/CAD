# Governing product documents

This directory holds product-level governing material that establishes what
IntegraCAD Open is intended to do. It is distinct from the repository's
contributor process, release-gate, and agent-operation records in the parent
`docs/` directory.

## Design basis

[`INTEGRACAD_OPEN_SCOPE.md`](INTEGRACAD_OPEN_SCOPE.md) is the supplied design
basis for the workbench. It defines the intended control-system workflow,
supported document set, boundaries with other FreeCAD workbenches, and the
initial platform assumptions. It is a planning and product-scope input; it is
not evidence that the described engineering, safety, compliance, or document
generation capabilities have been implemented or verified.

## Supporting document package

The [workbench workflow](WORKBENCH_WORKFLOW.md) records the owner's revised
plant-questionnaire → I/O sizing → PLC configuration → I/O definition → CAD →
controls circuit → safety circuit → shared cabinet → BOM/drawings → combined
wire-schedule sequence and its delivery order.

The reusable document and drawing package governed by this scope is located in
[`ControlForgeCAD/templates/controls-document-package`](../../ControlForgeCAD/templates/controls-document-package).
It contains editable Markdown and CSV templates as well as reference PDF and
DXF assets. The package is intentionally stored alongside the workbench rather
than here, because it is a future input/output asset collection rather than a
repository-governance policy.

## Deliberate coverage gap

The scope lists a Site Acceptance Test Protocol (SAT), but no SAT template was
provided in the supplied package. Do not represent SAT as available until a
reviewed source template is added.
