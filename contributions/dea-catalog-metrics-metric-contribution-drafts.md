# Metric Contribution Drafts: RAN Anomaly Management

Status: PREPARED, awaiting lodging. Two performance metrics observed in the 5G anomaly management domain have no canonical records in `technehub-labs/dea-catalog-metrics`. Drafts follow the catalog's metric record shape (`id: dea:metric-*`, unit, directionality, calculation and formula definitions, classifications). On lodging, the published `dea:metric-*` identifiers replace the declared gaps in `manifests/ran-anomaly.json` and the compiled AOP, per NM-INT-5.

## Draft 1: MTTR Anomaly P50 (RAN Operations)

```yaml
id: dea:metric-mttr-anomaly-p50-ran-operations
name: MTTR Anomaly P50 (RAN Operations)
type: Metric
description: The median time to restore a triaged 5G RAN anomaly, from anomaly
  ticket creation to the recorded disposition (resolved, escalated, or
  dispatched). Measures the speed of the anomaly management procedure; the
  Agentic Operating Procedure pilot measures agent-run cases against this
  human baseline. Lower is better.
abbreviation: MTTR-ANOM-P50
unit: minute
version: 1.0.0
lifecycle_status: candidate
subject_classification: [network_operations]   # confirm against the catalog's enumeration
purpose_classification: [performance]
scope_classification: [organizational_unit]
directionality: lower_is_better
management_significance: [operational]
measurable_entity_kind: dea:BusinessProcess
reputability_tier: programme_defined
calculation_definition: Median over cases of (ticket resolved_at - ticket created_at) for triaged RAN anomalies in the period
formula_definition:
  formula_id: dea:formula-mttr-anomaly-p50-ran-operations
  expression: MTTR-ANOM-P50 = median(resolved_at_i - created_at_i)
  unit_semantics:
    output_unit: dea:unit-time-minute
source_credit: Agentic Operating Procedure programme, worked exemplar corpus
```

## Draft 2: First-Pass Anomaly Resolution (RAN Operations)

```yaml
id: dea:metric-first-pass-anomaly-resolution-ran-operations
name: First-Pass Anomaly Resolution (RAN Operations)
type: Metric
description: The share of triaged 5G RAN anomalies resolved on the first
  disposition without rework loops firing and without exceptions beyond the
  anticipated set. Measures the quality of the anomaly management procedure's
  first response. Higher is better.
abbreviation: FP-ANOM-RES
unit: ratio
version: 1.0.0
lifecycle_status: candidate
subject_classification: [network_operations]
purpose_classification: [quality]
scope_classification: [organizational_unit]
directionality: higher_is_better
management_significance: [operational]
measurable_entity_kind: dea:BusinessProcess
reputability_tier: programme_defined
calculation_definition: First-pass resolved anomaly cases / total triaged anomaly cases in the period
formula_definition:
  formula_id: dea:formula-first-pass-anomaly-resolution-ran-operations
  expression: FP-ANOM-RES = first_pass_cases / total_cases
  unit_semantics:
    output_unit: dea:unit-ratio-percent
source_credit: Agentic Operating Procedure programme, worked exemplar corpus
```
