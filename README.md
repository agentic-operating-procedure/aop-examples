# AOP Examples

`aop-examples` is the single authority for complete worked demonstrations: a procedure taken end to end from a classic SOP through compilation to governed, audited agent execution, reproducible from the published artefacts alone.

| Field | Value |
|---|---|
| Authority | The complete, reproducible demonstration |
| Tier | Adoption |
| Landing wave | 6 |
| Version | 0.2.0 |
| Status | Stable |
| Licence | MIT |

## What this repository owns

- The worked exemplar: **5G RAN anomaly management**, the directed scenario. A telecom service provider managing a complex 5G mobile network, with human operators and AI agents working mobile network anomaly management together.
- The reproduction gate (`gate/reproduce.py`): the whole chain, from corpus regeneration to the shadow report, in one command.
- The DEA catalog contribution drafts (`contributions/`): the process contribution for RAN anomaly management (no canonical record exists yet) and two metric contribution drafts (MTTR-p50, first-pass resolution), prepared for lodging with `technehub-labs/dea-catalog-business-processes` and `dea-catalog-metrics`.

## What this repository does not own

- Any reusable component, which belongs upstream: the toolchain (`aop-toolkit`), the runtime (`aop-reference-harness`), the substrate semantics (`aop-context-graph`), the evaluation method (`aop-evaluation`).

## Status, stated plainly

**Steward-run.** The Wave 6 exit condition, a pilot migrated by a team other than the programme stewards, is not yet met. The demonstration claims rule fidelity and mechanism correctness; it does not claim adoption or live performance. The observation corpus is synthetic and deterministic.

## The exemplar at a glance

| Stage | Result |
|---|---|
| Classic SOP | `RB-RAN-014@v7`, linear corridor, prose escalation, reviewed before the current anomaly mix |
| Observed corpus | 45 cases, 5 profiles; the documented path holds for 23 of 45: the happy-path fallacy stated as a number |
| Compiled AOP | `ran-anomaly-management/AP-RAN-014@v0.1.0`: 5 variants with frequencies, thresholds at severity 85, degradation 30 percent, persistence 45 minutes, every rule provenance-backed |
| Governed execution | 45 cases in the harness: 245 actions, 10 approvals with evidence bundles, 20 prohibited, complete hash-chained case record |
| Shadow evaluation | Agreement 1.0, zero authority violations, 25 conservative deviations surfaced for rule refinement |
| Human baseline | MTTR-p50 35 min, first-pass 0.889, escalation precision 1.0 |
| Metric bindings | 3 canonical `dea:metric-*` references; 2 lodged gap drafts; the improvement claim deliberately absent until the live pilot |

## Reproduce

```
python3 gate/reproduce.py
```

## Documents

| Document | Scope |
|---|---|
| [The 5G walkthrough](./docs/aop-5g-anomaly-management-walkthrough-examples-scope.md) | The complete narrated walkthrough across all six playbook stages |
