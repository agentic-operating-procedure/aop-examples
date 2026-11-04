#!/usr/bin/env python3
"""Generate the observed case corpus for the 5G RAN anomaly management exemplar.

Synthetic but realistic: five observed profiles covering transient anomalies
(auto-recovery), restart-eligible degradation, mass events with customer
impact, hardware-suspected dispatches, and persistent anomalies that exhaust
the restart path. Deterministic via a fixed seed. Roles are roles, not
persons (CG-1). Cases carry the machine context the guardrail evaluates.

Usage: python3 corpus/generate_ran_cases.py [--out corpus/ran-anomaly-cases.jsonl] [--n 45]
"""

import argparse
import json
import random

random.seed(20261105)

ACTIONS_DOMINANT = ["validate-alarm", "classify-anomaly", "run-kpi-diagnostic", "restart-cell", "notify-noc", "escalate-anomaly"]
ACTIONS_MASS = ["validate-alarm", "classify-anomaly", "run-kpi-diagnostic", "restart-cell", "notify-noc", "escalate-anomaly", "dispatch-field-crew"]


def make_case(index, profile):
    case_id = "RAN-2026-11-%04d" % index
    steps = []
    decisions = []
    outcome = "achieved"
    first_pass = True
    cycle = 30 + index % 20

    def step(action, app, minute, actor="noc-ai-agent", handoff=False, **extra):
        entry = {"action": action, "application": app, "actor_role": actor,
                 "timestamp": "2026-11-05T%02d:%02dZ" % (6 + minute // 60, minute % 60)}
        if handoff:
            entry["handoff"] = True
        entry.update(extra)
        return entry

    severity = 40 + index % 25
    kpi_deg = 10 + index % 20
    context = {"hardware_suspected": False, "cell_outage": False, "anomaly_persistence_min": 0}

    if profile == "transient":
        # The SOP says restart; observation shows the anomaly clears after the
        # KPI diagnostic without a restart: the documented path overreaches.
        steps += [step("validate-alarm", "network-assurance-platform", 2),
                  step("classify-anomaly", "network-assurance-platform", 4),
                  step("run-kpi-diagnostic", "kpi-analytics", 9),
                  step("escalate-anomaly", "ticketing", 12, actor="noc-analyst")]
        decisions.append({"branch_condition": "kpi_degradation_pct <= 30", "evidence": "degradation %d pct" % kpi_deg})
        cycle = 18 + index % 8
    elif profile == "restart":
        steps += [step("validate-alarm", "network-assurance-platform", 2),
                  step("classify-anomaly", "network-assurance-platform", 4),
                  step("run-kpi-diagnostic", "kpi-analytics", 9),
                  step("restart-cell", "element-manager", 15),
                  step("notify-noc", "noc-dashboard", 22),
                  step("escalate-anomaly", "ticketing", 25, actor="noc-analyst")]
        decisions.append({"branch_condition": "kpi_degradation_pct <= 30", "evidence": "degradation %d pct" % kpi_deg})
        cycle = 32 + index % 10
        context["anomaly_persistence_min"] = 12
    elif profile == "mass-event":
        severity = 88 + index % 10
        kpi_deg = 40 + index % 20
        steps += [step("validate-alarm", "network-assurance-platform", 2),
                  step("classify-anomaly", "network-assurance-platform", 4),
                  step("run-kpi-diagnostic", "kpi-analytics", 9),
                  step("restart-cell", "element-manager", 15),
                  step("notify-noc", "noc-dashboard", 22, actor="noc-analyst", handoff=True),
                  step("escalate-anomaly", "ticketing", 28, actor="ran-operations-engineer", handoff=True),
                  step("dispatch-field-crew", "field-service", 40, actor="ran-operations-engineer", handoff=True)]
        decisions.append({"branch_condition": "severity_score >= 85", "evidence": "severity %d" % severity})
        decisions.append({"branch_condition": "kpi_degradation_pct > 30 and cell_outage == true", "evidence": "degradation %d pct with outage" % kpi_deg})
        outcome = "achieved"
        cycle = 70 + index % 20
        context["cell_outage"] = True
        context["anomaly_persistence_min"] = 55
    elif profile == "hardware":
        steps += [step("validate-alarm", "network-assurance-platform", 2),
                  step("classify-anomaly", "network-assurance-platform", 4),
                  step("run-kpi-diagnostic", "kpi-analytics", 9),
                  step("restart-cell", "element-manager", 15),
                  step("dispatch-field-crew", "field-service", 35, actor="ran-operations-engineer", handoff=True),
                  step("notify-noc", "noc-dashboard", 45),
                  step("escalate-anomaly", "ticketing", 50, actor="noc-analyst")]
        decisions.append({"branch_condition": "hardware_suspected == true", "evidence": "VSWR alarm on the antenna path"})
        context["hardware_suspected"] = True
        context["anomaly_persistence_min"] = 30
        cycle = 80 + index % 25
    else:  # persistent
        steps += [step("validate-alarm", "network-assurance-platform", 2),
                  step("classify-anomaly", "network-assurance-platform", 4),
                  step("run-kpi-diagnostic", "kpi-analytics", 9),
                  step("restart-cell", "element-manager", 15),
                  step("restart-cell", "element-manager", 35),
                  step("escalate-anomaly", "ticketing", 50, actor="ran-operations-engineer", handoff=True),
                  step("dispatch-field-crew", "field-service", 65, actor="ran-operations-engineer", handoff=True)]
        steps[3]["exceptions"] = [{"condition": "anomaly persists past 45 minutes after restart",
                                   "class": "technical", "severity": "critical",
                                   "escalation": {"target_role": "ran-operations-engineer", "reason": "restart path exhausted"}}]
        decisions.append({"branch_condition": "anomaly_persistence_min >= 45", "evidence": "persistent %d min" % (50 + index % 20)})
        outcome = "partially_achieved"
        first_pass = False
        context["anomaly_persistence_min"] = 50 + index % 20
        cycle = 110 + index % 30

    context["severity_score"] = severity
    context["kpi_degradation_pct"] = kpi_deg

    case = {
        "case_id": case_id,
        "procedure": "ran-anomaly-management",
        "started_at": "2026-11-05T06:%02dZ" % (index % 60),
        "ended_at": "2026-11-05T08:%02dZ" % (index % 60),
        "tasks": [{"name": "triage-and-restore", "steps": steps}],
        "actor_roles": sorted({s["actor_role"] for s in steps}),
        "outcome": {"result": outcome, "cycle_time": cycle, "first_pass": first_pass},
        "provenance": {
            "stitching_version": "stitch-1.2.0",
            "capture_surface_declaration_version": "csd-2026-11",
            "process_catalog_version": "v1-alpha",
            "correlation_key": "anomaly-ticket:" + case_id,
        },
        "context": context,
    }
    if decisions:
        target = next((s for s in steps if s["action"] in ("restart-cell", "dispatch-field-crew")), steps[-1])
        target["decisions"] = decisions
    return case


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="corpus/ran-anomaly-cases.jsonl")
    ap.add_argument("--n", type=int, default=45)
    args = ap.parse_args()

    profiles = (["transient"] * 2 + ["restart"] * 4 + ["mass-event"] * 1 + ["hardware"] * 1 + ["persistent"] * 1)
    with open(args.out, "w") as handle:
        for i in range(1, args.n + 1):
            profile = profiles[i % len(profiles)]
            handle.write(json.dumps(make_case(i, profile)) + "\n")
    print("wrote %d cases to %s" % (args.n, args.out))


if __name__ == "__main__":
    main()
