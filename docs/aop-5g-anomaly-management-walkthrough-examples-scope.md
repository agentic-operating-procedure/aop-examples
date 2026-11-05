# Walkthrough: 5G RAN Anomaly Management, from Classic SOP to Governed Agents (Examples Scope)

The complete worked demonstration of the six-stage playbook (see `aop-adoption`) in the directed scenario: a telecom service provider managing a complex 5G mobile network, with human operators and AI agents working mobile network anomaly management together, converting a classic SOP into an AOP and measuring the result against the human baseline.

**Status: steward-run.** This walkthrough was produced by the programme stewards. The Wave 6 gate requires a pilot migrated by a team other than the stewards; until that happens, this demonstration claims rule fidelity and mechanism correctness, not adoption.

**The corpus is synthetic.** The 45 observed cases are generated deterministically by `corpus/generate_ran_cases.py` under a declared profile mix. The demonstration proves the chain runs and the numbers are computable; it does not prove performance on a live 5G network. The live claim belongs to the adoption pilot.

## 1. The scenario

A 5G radio access network generates cell-level anomalies: KPI degradation, cell outages, hardware suspicions, persistent faults. The classic SOP `RB-RAN-014@v7` describes a linear triage corridor: validate, classify, run the KPI diagnostic, restart the cell, notify the NOC, escalate or dispatch. It was last reviewed before the current anomaly mix, and its escalation prose ("high-severity anomalies are escalated") carries no threshold a machine could apply.

The operating cast, per the DEA actors catalog's vocabulary: `noc-ai-agent` (the AI agent proposing actions), `noc-analyst` (shift log and first-line triage), `ran-operations-engineer` (the approver for high-impact dispositions), `on-call-ran-engineer` (the escalation target for unknown conditions).

## 2. Stage 1 to 3: decomposition, grounding, disposition

- The procedure family is `ran-anomaly-management`; the source SOP is pinned at v7; the enterprise process catalog has no canonical record for RAN anomaly management, so the gap is declared and the contribution draft is prepared (`contributions/`).
- The observed corpus: 45 cases across five profiles, 2 transient, 4 restart-eligible, 1 mass event, 1 hardware-suspected, 1 persistent per ten-case cycle. The documented corridor holds for a minority of cases: 22 of 45 cases deviate from it, which is the happy-path fallacy stated as a number.
- The governance manifest (`manifests/ran-anomaly.json`) carries the owner's dispositions: restart within observed degradation bounds is autonomous; NOC notification during a mass event, high-severity escalation and any field dispatch are approval-required; the agent never touches radio configuration or contacts a customer; the persistence prohibition blocks dispatch and escalation once the restart path is exhausted.

## 3. Stage 4: compilation

```
python3 -m aop_toolkit compile --sop sop/rb-ran-014.md --cases corpus/ran-anomaly-cases.jsonl \
  --manifest manifests/ran-anomaly.json --version v0.1.0 --out compiled/AP-RAN-014.json
python3 -m aop_toolkit lint compiled/AP-RAN-014.json        # LINT PASS
```

The compiled AOP `ran-anomaly-management/AP-RAN-014@v0.1.0` carries five variants with observed frequencies, the exception edge for the 45-minute persistence clock with its target role, the rework loop with its observed bound, and decision rules whose thresholds are values: severity 85, degradation 30 percent, persistence 45 minutes. Every rule carries observed provenance. The prose "escalate high-severity anomalies" became `severity_score >= 85` with its case count, which is the SOP's hypothesis turned into a measurement.

## 4. Stage 5: governed execution

The compiled AOP runs in the reference harness. Decision semantics verified per profile:

| Profile | Restart | Notify NOC | Escalate | Dispatch |
|---|---|---|---|---|
| Transient (clears on diagnostic) | not proposed | autonomous | autonomous | not proposed |
| Restart-eligible | autonomous | autonomous | autonomous | not proposed |
| Mass event (severity 88+, outage) | autonomous | approval-required | approval-required | approval-required |
| Hardware suspected | autonomous | autonomous | autonomous | approval-required |
| Persistent (45 min clock blown) | autonomous | autonomous | prohibited | prohibited |

Every approval-required action dispatched an evidence bundle to the RAN operations engineer and was approved against the rule's observed provenance. Every action appended to the hash-chained case record.

## 5. Stage 6: verification

```
python3 -m aop_evaluation baseline corpus/ran-anomaly-cases.jsonl
python3 -m aop_evaluation shadow --aop compiled/AP-RAN-014.json --cases corpus/ran-anomaly-cases.jsonl --report-dir reports
```

Human baseline from the corpus: MTTR-p50 35 minutes, first-pass resolution 0.889, exception rate 0.111, escalation precision 1.0.

Shadow-mode run: 265 per-action comparisons across 45 cases. Agreement 1.0: zero authority violations (the agent never acted more permissively than the human), 25 conservative deviations (the agent declined where the human acted with approval, concentrated in the mass-event and persistent profiles where the persistence prohibition overlaps the approval routes). The conservative deviations are the work queue for rule refinement: a future manifest may scope the persistence rule by severity, and the shadow run would measure the change.

Read honestly: this is rule fidelity against the corpus the rules were compiled from. It validates compilation and the guardrail's authority fidelity. It does not validate live performance; the live claim is the adoption pilot's, under the reproducibility protocol.

## 6. Metrics and business value

The value measurement is wired, and its honest state is declared:

- **Bound now**: mean time to detect (`dea:metric-mean-time-to-detect`), cell outage rate (`dea:metric-cell-outage-rate`), AI incident escalation compliance (`dea:metric-ai-incident-escalation-compliance`).
- **Lodged gaps**: MTTR-p50 for RAN anomalies and first-pass anomaly resolution have no canonical records; drafts are prepared in `contributions/` and lodge with `dea-catalog-metrics`.
- **Baseline**: the corpus's human values are published as the baseline the pilot will be measured against.
- **The improvement claim is deliberately absent.** The fixture chain proves parity of dispositions, not improvement. The pilot measures the delta on live operations: cycle time against the 35-minute baseline, first-pass against 0.889, escalation precision against 1.0, with the case corpus as the evidence.

## 6a. The held-out cohort run (2026-11-06)

The CR-014 protocol's first real exercise on this exemplar. The corpus was split deterministically (seed `ran-cohort-2026-11`, 25 percent held out): 33 development cases, 12 held-out cases, with every rule family present in the development cohort. The AOP was recompiled from the development cohort alone (`AP-RAN-014@v0.2.0`; the support floor scaled proportionately, 4/45 to 3/33, declared in the evaluation manifest) and shadow-evaluated on cases it has never seen:

| Run | Cohort | Agreement | Authority violations | Claim class |
|---|---|---|---|---|
| Compile corpus | development (33) | 1.0 | 0 | rule-fidelity |
| Unseen cases | held-out (12) | 1.0 | 0 | generalisation (held-out) |

Read honestly, as the protocol requires: the held-out cases did not feed the compile, so the rules transferred to unseen cases, which is a stronger claim than rule fidelity. But the corpus is synthetic and generated from five deterministic profiles, so "unseen" means unseen cases of the same generator, not live 5G traffic. This is the protocol's machinery demonstrated end to end on held-out data; the live prospective cohort remains the adoption pilot's.

## 7. Reproduce

```
python3 gate/reproduce.py
```

runs the whole chain: corpus generation, compilation, lint, registry publication with provenance verification, conformance of the compiled document, governed execution, and the shadow evaluation, printing the gate report.
