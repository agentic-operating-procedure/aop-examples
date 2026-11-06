# Changelog

All notable changes to this repository are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning is semantic: the major version changes when a walkthrough's meaning changes, the minor version when substantive demonstration content is added, and the patch version for corrections that do not change meaning.

## [Unreleased]

### Lodged (2026-11-07)

- The DEA contributions filed: dea-catalog-metrics PR #17 and dea-catalog-business-processes PR #233, after passing the metrics catalog's seven local gates (schema, MECE, field alignment, dual anchor, formula namespace, measurement conformance, evidence anchors) and regenerating CATALOG.yaml in the change. Two vocabulary corrections at lodging are recorded in the guide.


### Added (2026-11-06)

- The DEA catalog lodgement package, prepared and structurally checked but NOT lodged: CR-MET-023 and two metric records in the catalog's exact format (schema-required fields present; README Definitions verbatim-matched to the YAML descriptions), the process contribution in the BP catalog's template form, and the lodging guide with per-repo steps, CI expectations and maintainer flags. Lodging is the owner's explicit call: opening PRs in the technehub-labs org is outward-facing.


### Added (CR-036)

- Origin tagging across the exemplar corpus (CG-S15): all cases carry origin human (the modelled era); the generator's agent-fraction flag produces post-deployment corpora; the evaluation's exclusion and reservoir reporting demonstrated on a mixed corpus (13 agent-origin cases excluded, the baseline computed from the human-origin set); the held-out exercise re-run unchanged on the tagged corpus (v0.2.1).


## [0.3.0] - 2026-11-06

### Added (CR-033: CR-014 first exercise)

- The held-out cohort run: the corpus split deterministically (33 development, 12 held-out, every rule family in development), the AOP recompiled from development alone with the support floor scaled proportionately and declared, and the held-out shadow evaluation: agreement 1.0, zero authority violations, claim class generalisation (held-out). The walkthrough states the honest limit: unseen cases of the same synthetic generator, not live traffic; the prospective cohort remains the pilot's.
- The cohort files and the evaluation manifest are published alongside the corpus.


## [v0.2.0] - 2026-11-05

### Added (Wave H5: CR-027)

- The optional Pi adapter, labelled EXPERIMENTAL: Pi reasons and proposes; the external guardrail enforces; shell, filesystem, network and credential routes are denied by default; the self-test runs the CR-027 acceptance behaviours (bypass attempts, flood, duplicate delivery) without Pi installed. Not a normative dependency; not rollout-ready until the promotion gates pass.


## [0.1.0] - 2026-11-05

### The worked exemplar

- Published the 5G RAN anomaly management walkthrough: the directed scenario of a telecom service provider managing a complex 5G mobile network with human operators and AI agents, from the classic SOP through all six playbook stages to governed execution and evaluation.
- Published the deterministic 45-case observation corpus across five anomaly profiles, the governance manifest with the owner's autonomy dispositions, and the compiled AP-RAN-014.
- Published the DEA catalog contribution drafts: the process contribution for RAN anomaly management and two metric contribution drafts (MTTR-p50, first-pass resolution), prepared for lodging per CG-PA-5 and NM-INT-5.
- Published the reproduction gate and passed it: corpus determinism, compilation, lint, registry provenance, conformance, governed execution (245 actions, 10 approvals, complete chain-verified records), and shadow agreement 1.0 with zero authority violations and 25 conservative deviations.
- Status stated plainly: steward-run; the corpus is synthetic; the demonstration claims rule fidelity and mechanism correctness, not adoption or live performance.

[Unreleased]: https://github.com/agentic-operating-procedure/aop-examples/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/agentic-operating-procedure/aop-examples/compare/v0.2.0...v0.3.0
[v0.2.0]: https://github.com/agentic-operating-procedure/aop-examples/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/agentic-operating-procedure/aop-examples/releases/tag/v0.1.0
