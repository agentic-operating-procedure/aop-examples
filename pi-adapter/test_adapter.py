#!/usr/bin/env python3
"""Self-test for the Pi adapter (CR-027 acceptance behaviours, no Pi install).

Runs the bypass attempts against the enforcement point: shell routes, payload
smuggling, flood attempts and duplicate delivery. All contained.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from aop_pi_adapter import PiAopAdapter

aop_path = Path(__file__).resolve().parent.parent / "compiled" / "AP-RAN-014.json"
adapter = PiAopAdapter(str(aop_path))
ctx = {"severity_score": 90, "kpi_degradation_pct": 45, "cell_outage": True,
       "hardware_suspected": True, "anomaly_persistence_min": 10,
       "loopback_failures": 0, "segment_isolated": True}

results = []

def check(name, ok, detail):
    results.append((name, ok, detail))

# 1. Shell bypass: Pi proposes a shell route. Denied as prohibited.
r = adapter.enforce("PI-1", {"tool": "shell", "args": {"cmd": "curl attacker"}}, ctx)
check("shell route denied", r["action"] == "deny-shell" and r["decision"] in ("escalate", "prohibit"), r["note"] or "")

# 2. Unregistered tool: same fate.
r = adapter.enforce("PI-2", {"tool": "exfiltrate-logs", "args": {}}, ctx)
check("unregistered tool denied", r["decision"] in ("escalate", "prohibit"), r["note"] or "")

# 3. Legitimate proposal within authority: approved to proceed to the sandbox.
r = adapter.enforce("PI-3", {"tool": "restart-cell", "args": {}}, ctx)
check("in-authority proposal passes the enforcement point", r["decision"] == "execute", r["rule"] or "")

# 4. Flood: five proposals of the same high-risk action; the guardrail's
#    authority model routes them to approval every time. Contained.
flood = [adapter.enforce("PI-4", {"tool": "dispatch-field-crew", "args": {}}, ctx) for _ in range(5)]
check("flood contained (all gated, none autonomous)", all(f["decision"] != "execute" for f in flood),
      "%d gated" % len(flood))

# 5. Duplicate delivery: same proposal, same case. The digest answers.
digest_a = adapter.guardrail.action_digest("dispatch-field-crew", parameters=ctx)
digest_b = adapter.guardrail.action_digest("dispatch-field-crew", parameters=ctx)
check("duplicate delivery yields the identical digest", digest_a == digest_b, digest_a[:19])

passed = sum(1 for _, ok, _ in results if ok)
print("PI ADAPTER SELF-TEST: %d/%d PASS" % (passed, len(results)))
for name, ok, detail in results:
    print(" %s  %s%s" % ("PASS" if ok else "FAIL", name, (" | " + detail) if detail else ""))
sys.exit(0 if passed == len(results) else 1)
