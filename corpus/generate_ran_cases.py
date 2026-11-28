#!/usr/bin/env python3
"""Generate the observed case corpus for the 5G RAN anomaly management exemplar.

CR-041 3.1: started_at, every step timestamp and ended_at derive from ONE
minutes-from-midnight timeline per case (fmt(start_total + offset));
cycle_time = ended_at - started_at exactly. Step offsets are declared
relative and monotonic per profile. Cases carry origin (CG-S15): the base
corpus models the human-operated era (--agent-fraction 0); post-deployment
observation is generated with --agent-fraction.

Deterministic: fixed seed. Usage:
    python3 corpus/generate_ran_cases.py [--out corpus/ran-anomaly-cases.jsonl] [--n 45] [--agent-fraction 0.0]
"""

import argparse
import json

# Per profile: the ordered steps with their minute offsets from started_at,
# the actor role, whether it is a governed handoff, plus the declared
# decisions, exceptions, outcome and context of the observed path.
PROFILES = {
    "transient": {
        "steps": [
            ("validate-alarm", "network-assurance-platform", 2, "noc-ai-agent", False),
            ("classify-anomaly", "network-assurance-platform", 4, "noc-ai-agent", False),
            ("run-kpi-diagnostic", "kpi-analytics", 9, "noc-ai-agent", False),
            ("handoff-anomaly", "ticketing", 12, "noc-analyst", True),
        ],
        "decisions": [("kpi_degradation_pct <= 30", "degradation {deg} pct")],
        "exceptions": [],
        "outcome": ("achieved", True),
        "cycle": (18, 8),
        "context": {},
    },
    "restart": {
        "steps": [
            ("validate-alarm", "network-assurance-platform", 2, "noc-ai-agent", False),
            ("classify-anomaly", "network-assurance-platform", 4, "noc-ai-agent", False),
            ("run-kpi-diagnostic", "kpi-analytics", 9, "noc-ai-agent", False),
            ("restart-cell", "element-manager", 15, "noc-ai-agent", False),
            ("notify-noc", "noc-dashboard", 22, "noc-ai-agent", False),
            ("handoff-anomaly", "ticketing", 25, "noc-analyst", True),
        ],
        "decisions": [("kpi_degradation_pct <= 30", "degradation {deg} pct")],
        "exceptions": [],
        "outcome": ("achieved", True),
        "cycle": (32, 10),
        "context": {"anomaly_persistence_min": 12},
    },
    "mass-event": {
        "steps": [
            ("validate-alarm", "network-assurance-platform", 2, "noc-ai-agent", False),
            ("classify-anomaly", "network-assurance-platform", 4, "noc-ai-agent", False),
            ("run-kpi-diagnostic", "kpi-analytics", 9, "noc-ai-agent", False),
            ("restart-cell", "element-manager", 15, "noc-ai-agent", False),
            ("notify-noc", "noc-dashboard", 22, "noc-analyst", True),
            ("handoff-anomaly", "ticketing", 28, "ran-operations-engineer", True),
            ("dispatch-field-crew", "field-service", 40, "ran-operations-engineer", True),
        ],
        "decisions": [
            ("severity_score >= 85", "severity {sev}"),
            ("kpi_degradation_pct > 30 and cell_outage == true", "degradation {deg} pct with outage"),
        ],
        "exceptions": [],
        "outcome": ("achieved", True),
        "cycle": (70, 20),
        "context": {"cell_outage": True, "anomaly_persistence_min": 55},
    },
    "hardware": {
        "steps": [
            ("validate-alarm", "network-assurance-platform", 2, "noc-ai-agent", False),
            ("classify-anomaly", "network-assurance-platform", 4, "noc-ai-agent", False),
            ("run-kpi-diagnostic", "kpi-analytics", 9, "noc-ai-agent", False),
            ("restart-cell", "element-manager", 15, "noc-ai-agent", False),
            ("dispatch-field-crew", "field-service", 35, "ran-operations-engineer", True),
            ("notify-noc", "noc-dashboard", 45, "noc-ai-agent", False),
            ("handoff-anomaly", "ticketing", 50, "noc-analyst", True),
        ],
        "decisions": [("hardware_suspected == true", "VSWR alarm on the antenna path")],
        "exceptions": [],
        "outcome": ("achieved", True),
        "cycle": (80, 25),
        "context": {"hardware_suspected": True, "anomaly_persistence_min": 30},
    },
    "persistent": {
        "steps": [
            ("validate-alarm", "network-assurance-platform", 2, "noc-ai-agent", False),
            ("classify-anomaly", "network-assurance-platform", 4, "noc-ai-agent", False),
            ("run-kpi-diagnostic", "kpi-analytics", 9, "noc-ai-agent", False),
            ("restart-cell", "element-manager", 15, "noc-ai-agent", False),
            ("restart-cell", "element-manager", 35, "noc-ai-agent", False),
            ("handoff-anomaly", "ticketing", 50, "ran-operations-engineer", True),
            ("dispatch-field-crew", "field-service", 65, "ran-operations-engineer", True),
        ],
        "decisions": [("anomaly_persistence_min >= 45", "persistent {pers} min")],
        "exceptions": [{
            "condition": "anomaly persists past 45 minutes after restart",
            "class": "technical", "severity": "critical",
            "escalation": {"target_role": "ran-operations-engineer", "reason": "restart path exhausted"},
        }],
        "outcome": ("partially_achieved", False),
        "cycle": (110, 30),
        "context": {},
    },
}


def make_case(index, profile):
    spec = PROFILES[profile]
    case_id = "RAN-2026-11-%04d" % index
    start_total = 6 * 60 + (index % 240)   # 06:00 to 09:59, per the shift pattern
    cycle = spec["cycle"][0] + index % spec["cycle"][1]

    ctx = dict(spec["context"])
    sev = 40 + index % 25
    deg = 10 + index % 20
    ctx.setdefault("severity_score", sev)
    ctx.setdefault("kpi_degradation_pct", deg)
    if profile == "mass-event":
        ctx["severity_score"] = 88 + index % 10
        ctx["kpi_degradation_pct"] = 40 + index % 20
    if profile == "persistent":
        ctx["anomaly_persistence_min"] = 50 + index % 20
    ctx.setdefault("anomaly_persistence_min", 0)
    ctx.setdefault("hardware_suspected", False)
    ctx.setdefault("cell_outage", False)
    ctx.setdefault("loopback_failures", 0)

    steps = []
    for (action, app, offset, actor, handoff) in spec["steps"]:
        entry = {
            "action": action,
            "application": app,
            "actor_role": actor,
            "timestamp": "2026-11-05T%02d:%02dZ" % ((start_total + offset) // 60, (start_total + offset) % 60),
        }
        if handoff:
            entry["handoff"] = True
        steps.append(entry)
    # CR-041 3.1: the recorded decisions attach to the step that acted on them.
    if spec["decisions"]:
        target = next((s for s in steps if s["action"] in ("restart-cell", "dispatch-field-crew")), steps[-1])
        target["decisions"] = [
            {"branch_condition": cond.format(sev=ctx["severity_score"], deg=ctx["kpi_degradation_pct"], pers=ctx["anomaly_persistence_min"]),
             "evidence": evidence.format(sev=ctx["severity_score"], deg=ctx["kpi_degradation_pct"], pers=ctx["anomaly_persistence_min"])}
            for cond, evidence in spec["decisions"]
        ]
    if spec["exceptions"]:
        steps[-1]["exceptions"] = [dict(e) for e in spec["exceptions"]]

    result, first_pass = spec["outcome"]
    return {
        "case_id": case_id,
        "origin": "human",
        "procedure": "ran-anomaly-management",
        "started_at": "2026-11-05T%02d:%02dZ" % (start_total // 60, start_total % 60),
        "ended_at": "2026-11-05T%02d:%02dZ" % ((start_total + cycle) // 60, (start_total + cycle) % 60),
        "tasks": [{"name": "triage-and-restore", "steps": steps}],
        "actor_roles": sorted({s["actor_role"] for s in steps}),
        "outcome": {"result": result, "cycle_time": cycle, "first_pass": first_pass},
        "provenance": {
            "stitching_version": "stitch-1.2.0",
            "capture_surface_declaration_version": "csd-2026-11",
            "process_catalog_version": "v1-alpha",
            "correlation_key": "anomaly-ticket:" + case_id,
        },
        "context": ctx,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="corpus/ran-anomaly-cases.jsonl")
    ap.add_argument("--n", type=int, default=45)
    ap.add_argument("--agent-fraction", type=float, default=0.0,
                    help="fraction of cases tagged agent-origin (post-deployment observation); default 0: the human baseline era")
    args = ap.parse_args()

    cycle = ["transient"] * 2 + ["restart"] * 4 + ["mass-event"] * 1 + ["hardware"] * 1 + ["persistent"] * 1
    with open(args.out, "w") as handle:
        for i in range(1, args.n + 1):
            profile = cycle[i % len(cycle)]
            case = make_case(i, profile)
            if args.agent_fraction and (i / args.n) <= args.agent_fraction:
                case["origin"] = "agent"  # post-deployment: the agent's own runs feed back
            handle.write(json.dumps(case) + "\n")
    print("wrote %d cases to %s" % (args.n, args.out))


if __name__ == "__main__":
    main()
