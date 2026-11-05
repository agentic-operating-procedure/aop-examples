"""The reference Pi-to-AOP adapter (CR-027, experimental).

Maps Pi tool proposals to canonical actions and routes every proposal through
the reference guardrail's enforcement sequence. Pi reasons and proposes; the
guardrail disposes; nothing executes here. The sandbox profile is a deployment
obligation this adapter documents but does not provide.

Usage of the reference harness modules: the adapter imports the guardrail,
expression and caserecord modules from the aop-reference-harness checkout the
same way the conformance suite does (never installed).
"""

from __future__ import annotations

import importlib.util
import json
import sys
import types
from pathlib import Path

DEFAULT_HARNESS_HOME = Path(__file__).resolve().parent.parent.parent / "aop-reference-harness"

# Pi tool names the adapter recognises. Anything else is an unregistered
# route: denied unless a deployment profile explicitly mediates it (CR-027).
KNOWN_TOOLS = {
    "shell": "prohibited",       # a shell route is never mediated by default
    "filesystem": "prohibited",
    "network": "prohibited",
    "credentials": "prohibited",
}


def load_guardrail(harness_home: Path = DEFAULT_HARNESS_HOME):
    package = types.ModuleType("aop_harness_pi_adapter")
    package.__path__ = [str(harness_home / "aop_harness")]
    sys.modules["aop_harness_pi_adapter"] = package
    for name in ("expression", "guardrail"):
        spec = importlib.util.spec_from_file_location("aop_harness_pi_adapter.%s" % name,
                                                      harness_home / "aop_harness" / ("%s.py" % name))
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    return sys.modules["aop_harness_pi_adapter.guardrail"]


class PiAopAdapter:
    def __init__(self, aop_path: str, harness_home: Path = DEFAULT_HARNESS_HOME):
        guardrail_m = load_guardrail(Path(harness_home))
        self._guardrail_m = guardrail_m
        aop = json.loads(Path(aop_path).read_text())
        self.aop_ref = "%s@%s" % (aop["aop"], aop["version"])
        self.guardrail = guardrail_m.Guardrail(aop)
        self.aop = aop
        self.denied: list[dict] = []

    def translate(self, pi_proposal: dict) -> tuple[str, dict]:
        """Map a Pi tool proposal to a canonical action and payload.
        Unregistered tools map to a denied sentinel action."""
        tool = pi_proposal.get("tool", "")
        if tool in KNOWN_TOOLS:
            return "deny-" + tool, {}
        return tool, pi_proposal.get("args", {})

    def enforce(self, case_id: str, pi_proposal: dict, context: dict) -> dict:
        """The enforcement sequence for one Pi proposal. Returns the guardrail
        decision; execution happens in the deployment's sandboxed executor,
        never inside Pi."""
        action, params = self.translate(pi_proposal)
        variant, note = self.guardrail.match_variant(self.guardrail.decision_context(context))
        decision = self.guardrail.authorise(variant, action, self.guardrail.decision_context(context))
        pfail = self.guardrail.parameter_verdict(action, params)
        if pfail is not None:
            decision = pfail
        if decision["decision"] in ("escalate", "prohibit"):
            self.denied.append({"case_id": case_id, "proposal": pi_proposal, "note": decision.get("note")})
        return {"case_id": case_id, "action": action, "decision": decision["decision"],
                "rule": (decision.get("rule") or {}).get("if"), "note": decision.get("note")}
