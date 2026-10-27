# Tool and dependency registry

This registry is the durable Layer 2 record for tools that affect a project
artifact, verification result, or external integration. It complements—not
replaces—the package metadata, CI workflow, external-asset policy, or a
software bill of materials generated for a release candidate.

## Operating rules

- Integration Scout owns discovery and provenance; QA Guy verifies a tool used
  as a quality gate; Tony CAD records the milestone decision.
- Before adding a tool or dependency, record its purpose, approved source,
  version constraint or immutable revision, license/provenance check, security
  review, owner, and recheck date.
- Do not store credentials, tokens, proprietary packages, or vendor assets in
  this registry.
- A row marked **pending first resolution** is not an approval to add the tool
  to runtime dependencies. Resolve it in CI or a controlled environment and
  update the row with the exact result.

## Current verification inventory

| Tool | Scope and purpose | Approved source / version control | Provenance and license status | Security review | Owner | Recheck |
|---|---|---|---|---|---|---|
| Python | CI interpreter and pure-Python verification | `actions/setup-python@v5`; Python 3.11 in [quality workflow](../.github/workflows/quality.yml) | GitHub Action and CPython release metadata; runtime remains Python >=3.10 | CI image maintenance; review action major version before change | Integration Scout | Each CI-image or action-major update |
| pytest | Regression suite | PyPI resolution constrained in `requirements-ci.txt` (`>=9.0.3,<10` after the initial audit found a fixed advisory in the former 8.x range) | Pending first resolved-package/license capture | `pip-audit` scans resolved CI requirements | QA Guy | Each dependency update |
| Ruff | Syntax/undefined-name and future lint ratchet | PyPI resolution constrained in `requirements-ci.txt` | Pending first resolved-package/license capture | `pip-audit` scans resolved CI requirements | QA Guy | Each dependency update |
| lxml | Required CEProject XML test coverage | PyPI resolution constrained in `requirements-ci.txt` | Pending first resolved-package/license capture | `pip-audit` scans resolved CI requirements | Schema Guy + QA Guy | Each dependency update |
| pip-audit | CI dependency vulnerability scan | PyPI resolution constrained in `requirements-ci.txt` | Pending first resolved-package/license capture | Self-audited through CI invocation; review scanner advisories | Integration Scout + QA Guy | Each dependency update |
| detect-secrets | CI tracked-file secret scan | PyPI resolution constrained in `requirements-ci.txt` | Pending first resolved-package/license capture | Fails CI when a potential secret is detected. Generic hex-entropy detection is disabled because source-backed catalog checksums are intentional; specialized token/key detectors remain enabled. | Integration Scout + QA Guy | Each dependency update |

## Candidate asset or SDK intake

For an external SDK, FreeCAD add-on, vendor API, or CAD asset pipeline, add a
row before use with: exact source URL or authorized catalog locator, version or
revision, access terms, redistribution/license decision, checksum where
practical, vulnerability review, removal path, owning role, and recheck date.
Use [the SME consultation receipt](SME_CONSULTATION_RECEIPT.md) when the
candidate triggers a vendor, standards, or engineering review.
