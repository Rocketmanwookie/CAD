# ADR 0002: Catalog feasibility is not engineering approval

- Status: accepted
- Date: 2026-09-28
- Owners: Controls Engineer Guy, Vendor Catalog SME, QA Guy

## Context

The workbench can recommend and allocate supported catalog PLC configurations
from typed I/O demand. Catalog records, placeholder geometry, and normalized
asset metadata are useful planning inputs, but they cannot establish final
hardware selection, safety, code compliance, procurement suitability, or
manufacturer-project compatibility.

## Decision

Present catalog results as explicit feasibility recommendations requiring user
approval. Keep authoritative allocation, vendor assets, source provenance, and
project-specific engineering decisions separate. A public claim of
manufacturer-accurate geometry, vendor compatibility, code compliance, or
final engineering approval requires the corresponding source and qualified
review evidence.

## Alternatives considered

- Automatically promote a catalog recommendation to a final selection.
- Allow bare or generic geometry to stand in for terminal-bearing assets.
- Scatter vendor-specific identifiers through the core domain model.

## Consequences

The product remains honest about starter catalog scope and can expand through
neutral adapters. Acquisition and validation take longer, but unsafe or
misleading claims are avoided. Asset intake follows the Layer 2 registry and
the relevant SME receipt.

## Evidence

- [Architecture status](../ARCHITECTURE.md)
- [External asset policy](../EXTERNAL_ASSET_POLICY.md)
- [Technical document registry](../../ControlForgeCAD/controls_wb/resources/hardware/technical_document_registry.xml)
