# CR-MET-023 -- Contribute the RAN Anomaly Management Baseline Metrics (2 Records)

| Field | Value |
|---|---|
| Status | Proposed (this document) |
| Target repository | `technehub-labs/dea-catalog-metrics` |
| Author | Emmanuel A. Otchere |
| Date | 2026-11-06 |
| Depends on | CR-MET-009 (catalog establishment); CR-MET-014 (description field); CR-MET-015 (field dimensions); CR-MET-016 (seed-scale pipeline rules) |
| Blocks | none |
| Cardinal authority | dea-catalog-metrics (catalog); dea-metamodel (canonical semantics) |

## 1. Background and problem statement

The Agentic Operating Procedure programme (github.com/agentic-operating-procedure) operates a worked 5G RAN anomaly management exemplar whose evaluation protocol binds its human baseline to canonical metric records. Two of its baseline metrics have no adequate record in this catalog, and are currently carried as declared gaps in the programme's artefacts (per its specification's process-alignment rule, which prohibits inventing identifiers). This CR contributes both through the normal admission pipeline.

The records: `dea:metric-mttr-anomaly-p50-ran-operations` (median restoration time for triaged RAN anomalies) and `dea:metric-first-pass-anomaly-resolution-ran-operations` (first-pass resolution rate). Both are bound to `dea:BusinessProcess` and accompany a sibling process contribution to `dea-catalog-business-processes` (Manage RAN Anomaly Triage), filed separately through that catalog's contribution process.

## 2. Records

- `entities/v1-alpha/dea:metric-mttr-anomaly-p50-ran-operations/` (YAML + README)
- `entities/v1-alpha/dea:metric-first-pass-anomaly-resolution-ran-operations/` (YAML + README)

## 3. Pipeline compliance

- Records satisfy `schemas/entity.schema.json`; all required fields present.
- The README `Definition` matches the YAML `description` verbatim (whitespace-normalised).
- Classification axes use the controlled vocabularies: subject `operations`; purposes `efficiency` and `effectiveness`; scope `organizational_unit`.
- Signatures are MECE-unique: no existing record carries these constructs (verified against the catalog tree 2026-11-06; nearest neighbours `dea:metric-average-resolution-time` and `dea:metric-mean-time-to-detect` differ in construct: mean-based and non-RAN, detection-side, respectively).
- `source_credit` appears in the record; `reputability_tier: programme_defined` (per the seed-scale pipeline's tier vocabulary).
- Registry regeneration: the PR regenerates the registry and subject-concept registry in the same change.

## 4. Notes for the reviewing maintainer

- The percentile construct (p50) is deliberate: RAN anomaly restoration is heavy-tailed and the operations centre steers by the median; the existing `average-resolution-time` record is mean-based, so the constructs do not collide.
- `programme_defined` reputability reflects an honest tier: the records are contributed from a programme's worked exemplar, not an industry standards body. If the maintainer prefers `industry_standard` on the strength of TMForum-adjacent NOC practice, the contributor accepts the reclassification.
