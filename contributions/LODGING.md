# DEA Catalog Lodgement Guide

Status: **LODGED 2026-11-07**: dea-catalog-metrics PR #17 (CR-MET-023 + both records; all seven local gates passed before filing) and dea-catalog-business-processes PR #233 (the process contribution). Two corrections were made at lodging against the catalogs' actual vocabularies: `dea:unit-minute` (not `dea:unit-time-minute`) and `reputability_tier: internal_custom` (not `programme_defined`, which their schema gate rejected). The gap-to-reference swap happens when the maintainers publish. Everything needed to lodge is in this directory; the outward-facing step (opening PRs in the technehub-labs org) awaits the programme owner's explicit go, per the estate's rules on outward-facing actions. Nothing here has been published.

## What is prepared

| # | Artefact | Destination repo | Destination path |
|---|---|---|---|
| 1 | `dea-metrics-lodgement/CR-MET-023.md` | `technehub-labs/dea-catalog-metrics` | `change-requests/CR-MET-023.md` |
| 2 | `dea-metrics-lodgement/dea:metric-mttr-anomaly-p50-ran-operations/` | same | `entities/v1-alpha/dea:metric-mttr-anomaly-p50-ran-operations/` |
| 3 | `dea-metrics-lodgement/dea:metric-first-pass-anomaly-resolution-ran-operations/` | same | `entities/v1-alpha/dea:metric-first-pass-anomaly-resolution-ran-operations/` |
| 4 | `dea-bp-lodgement/manage-ran-anomaly-triage.yaml` | `technehub-labs/dea-catalog-business-processes` | `contributions/processes/manage-ran-anomaly-triage.yaml` |

## Lodging steps (metrics)

1. Branch `cr-met-023-ran-anomaly-baseline` off `technehub-labs/dea-catalog-metrics` main.
2. Copy items 1 to 3 to their destination paths above.
3. Regenerate the registry and the subject-concept registry in the same change (the CR-MET-016 pipeline requires it; run the catalog's regeneration script).
4. Open the PR titled `CR-MET-023: contribute the RAN anomaly management baseline metrics (2 records)`. The `validate-metrics` workflow checks: entity schema conformance, the README Definition matching the YAML description verbatim (whitespace-normalised), controlled-vocabulary classification, MECE-unique signature, and source credit presence. The prepared records were written to pass each check; two items are flagged for the maintainer rather than guaranteed: the `unit_ref` values (`dea:unit-time-minute`, `dea:unit-ratio-percent`) must exist in the catalog's unit registry (regenerate or register if absent), and the `reputability_tier: programme_defined` value should be confirmed against the tier vocabulary.

## Lodging steps (business process)

1. Branch `contribution-manage-ran-anomaly-triage` off `technehub-labs/dea-catalog-business-processes` main.
2. Copy item 4 to `contributions/processes/`.
3. Open the PR. The `process-contribution-report` workflow validates the contribution against `schemas/contribution.schema.json`, runs the identity check on the proposed entry (`dea:process-<kebab-case-name>` per PC-008), and posts a reclassification recommendation as a PR comment. A catalog maintainer reviews before anything lands; the contribution does not auto-land.
4. The `context_reference.domain` value is marked "to be confirmed": the maintainer's recommendation will place it against the correct ECF domain enumeration.

## After publication

Per CG-PA-4 and NM-INT-5: replace the declared gaps in `manifests/ran-anomaly.json` (process gap and the two metric gaps) with the published canonical references, recompile the exemplar AOP, and record the swap in the walkthrough. The AOP artefacts then carry references, not gaps, and the loop closes.
