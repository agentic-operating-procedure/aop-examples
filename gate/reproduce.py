#!/usr/bin/env python3
"""The Wave 6 reproduction gate for the 5G exemplar.

Runs the whole chain from published artefacts alone, per the reproducibility
protocol: corpus generation, compilation, lint, registry publication with
provenance verification, conformance of the compiled document, governed
execution in the harness, and the shadow evaluation. Prints the gate report.

The gate reports STEWARD-RUN: the Wave 6 exit condition (a pilot migrated by
a team other than the programme stewards) is not yet met, and this report
says so rather than implying it.

Exit 0 with GATE PASS, 1 otherwise.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXAMPLES_HOME = HERE.parent
AOP_HOME = EXAMPLES_HOME.parent
TOOLKIT_HOME = AOP_HOME / "aop-toolkit"
EVAL_HOME = AOP_HOME / "aop-evaluation"
CONF_HOME = AOP_HOME / "aop-conformance"
REGISTRY_HOME = AOP_HOME / "aop-registry"
HARNESS_HOME = AOP_HOME / "aop-reference-harness"

sys.path.insert(0, str(EVAL_HOME))
sys.path.insert(0, str(REGISTRY_HOME))
sys.path.insert(0, str(HARNESS_HOME))

from aop_evaluation.shadow import shadow_evaluate, compare_with_baseline          # noqa: E402
from aop_evaluation.metrics import baseline                                       # noqa: E402
from aop_harness.agent import ScriptedAgent                                       # noqa: E402
from aop_harness.caserecord import CaseRecordStore                                # noqa: E402
from aop_harness.runtime import Runtime                                           # noqa: E402
from aop_registry.catalogue import Registry                                       # noqa: E402

MANDATORY_FIELDS = ["inputs", "context_snapshot", "rule", "provenance", "decision", "approver", "outcome"]


def run(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def main() -> int:
    report: list[tuple[str, bool, str]] = []
    work = tempfile.mkdtemp(prefix="aop-wave6-gate-")
    cases = EXAMPLES_HOME / "corpus" / "ran-anomaly-cases.jsonl"
    compiled = Path(work) / "AP-RAN-014.json"
    record_path = Path(work) / "case-record.jsonl"

    # 1. Corpus regeneration is deterministic.
    result = run([sys.executable, "corpus/generate_ran_cases.py", "--out", str(Path(work) / "regen.jsonl")], cwd=str(EXAMPLES_HOME))
    same = result.returncode == 0 and (Path(work) / "regen.jsonl").read_bytes() == cases.read_bytes()
    report.append(("corpus: regeneration is deterministic (45 cases)", same, result.stdout.strip() or result.stderr.strip()[:100]))

    # 2. Compile.
    result = run([sys.executable, "-m", "aop_toolkit", "compile",
                  "--sop", str(EXAMPLES_HOME / "sop/rb-ran-014.md"),
                  "--cases", str(cases),
                  "--manifest", str(EXAMPLES_HOME / "manifests/ran-anomaly.json"),
                  "--version", "v0.1.0", "--out", str(compiled)], cwd=str(TOOLKIT_HOME))
    ok = result.returncode == 0 and compiled.exists()
    report.append(("compile: classic SOP + corpus + manifest -> AP-RAN-014", ok, result.stderr.strip()[:100]))

    # 3. Lint.
    result = run([sys.executable, "-m", "aop_toolkit", "lint", str(compiled)], cwd=str(TOOLKIT_HOME))
    report.append(("lint: validates against aop-spec schema and clauses", result.returncode == 0, result.stdout.strip()[:100]))

    # 4. Registry: publish, resolve, verify provenance.
    registry = Registry(Path(work) / "registry")
    entry = registry.publish(str(compiled))
    chain = registry.provenance_chain(entry["ref"], str(cases))
    report.append(("registry: published %s, provenance chain holds" % entry["ref"], chain["holds"], json.dumps(chain["derived_from"])))

    # 5. Conformance of the compiled document.
    result = run([sys.executable, "-m", "aop_conformance", "documents", str(compiled)], cwd=str(CONF_HOME))
    report.append(("conformance: profile AOP-DOC-1 on the compiled AOP", result.returncode == 0, result.stdout.strip().splitlines()[0][:80] if result.stdout else ""))

    # 6. Governed execution.
    aop = json.loads(compiled.read_text())
    runtime = Runtime(aop, str(record_path))
    agent = ScriptedAgent()
    case_list = [json.loads(l) for l in cases.read_text().splitlines() if l.strip()]
    for case in case_list:
        runtime.run_case(case, agent)
    stats = dict(runtime.stats)
    store = CaseRecordStore(str(record_path))
    entries = store.read_all()
    incomplete = [e["seq"] for e in entries if any(f not in e for f in MANDATORY_FIELDS)]
    intact, _ = store.verify_chain()
    report.append(("harness: %d cases executed under the guardrail" % len(case_list), stats["runs"] == len(case_list), json.dumps(stats)))
    report.append(("case record: complete fields, chain intact", not incomplete and intact, "%d entries" % len(entries)))

    # 7. Shadow evaluation against the human baseline.
    bl = baseline(case_list)
    shadow = shadow_evaluate(str(compiled), str(cases), str(HARNESS_HOME))
    reading = compare_with_baseline(shadow, bl)
    report.append(("shadow: agreement %s against the human baseline (band 0.85)" % shadow["agreement_rate"],
                   reading["within_band"],
                   "violations %d, conservative deviations %d" % (len(shadow["authority_violations"]), len(shadow["conservative_deviations"]))))

    # Save the shadow report with the published reports.
    out = EXAMPLES_HOME / "reports" / "shadow-latest.json"
    out.write_text(json.dumps(shadow, indent=2) + "\n")

    # 8. The honest status line.
    passed = all(ok for _, ok, _ in report)
    print("WAVE 6 REPRODUCTION GATE: 5G RAN ANOMALY MANAGEMENT EXEMPLAR")
    print("=" * 72)
    for name, ok, detail in report:
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
        if detail:
            print("      %s" % detail[:110])
    print("=" * 72)
    print("STATUS: STEWARD-RUN. The Wave 6 exit condition (a pilot migrated by")
    print("a team other than the programme stewards) is not yet met; this")
    print("demonstration claims rule fidelity and mechanism correctness, not")
    print("adoption or live performance.")
    print("GATE %s" % ("PASS" if passed else "FAIL"))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
