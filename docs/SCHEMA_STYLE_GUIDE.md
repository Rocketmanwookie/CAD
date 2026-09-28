# CEProject schema style guide

- Version each public XML schema in both filename and `schemaVersion`.
- Use explicit namespaces and stable, descriptive element/attribute names.
- Give every addressable project fact a stable ID; references must use IDs, not
  display labels or mutable positions.
- Represent unknown, assumed, estimated, verified, approved, rejected, and
  superseded facts distinctly. Never serialize an assumption as a verified fact.
- Document backwards-compatibility and migration behavior before changing a
  persisted public contract.
- Provide a valid fixture, an invalid fixture, and round-trip coverage for each
  new schema surface.
- Keep vendor-specific formats behind adapters; CEProject remains
  vendor-neutral source data.
