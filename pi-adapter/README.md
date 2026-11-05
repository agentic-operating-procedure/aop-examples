# AOP Pi Adapter: An Optional Reference Integration (Experimental)

Status: **EXPERIMENTAL**. This adapter is a reference integration with the Pi agent harness (github.com/earendil-works/pi), delivered per CR-027. It is optional, is not a normative dependency of the estate, and is not rollout-ready: the label stands until an independent implementation and a live pilot pass the relevant gates (CR-019's promotion gates).

## The boundary that makes this safe

Pi's own documentation states it provides no built-in filesystem, process, network or credential permission system, and runs with the launching process's permissions. Therefore **a Pi extension cannot be the AOP enforcement boundary**. The architecture is fixed and non-negotiable:

- Pi reasons and proposes. It never executes.
- Every Pi tool proposal is translated into a canonical action and routed through the external guardrail (the same policy decision point and enforcement point as the reference harness).
- Pi's shell, filesystem, process, network and extension routes are denied unless the sandbox profile explicitly mediates them.
- The AOP, the guardrail, the case record and the credential broker sit **outside** Pi's model and extension context.

## What the adapter does

`aop_pi_adapter.py` demonstrates the translation layer against the reference guardrail:

- Loads one immutable AOP version and builds the guardrail from it.
- Maps a Pi tool proposal (`{"tool": ..., "args": ...}`) to a canonical action name and payload.
- Runs the full enforcement sequence for every proposal: trusted-view matching, parameter validation, budget verdicts, authority decision, duplicate delivery, workload identity.
- Returns the decision to Pi as a tool result; approved actions would be executed by the deployment's sandboxed executor, never by Pi itself.

## Self-test

`test_adapter.py` runs the CR-027 acceptance behaviours without Pi installed: bypass attempts (a proposal routed to an unregistered action), payload smuggling, flood attempts and duplicate delivery, each contained by the enforcement point.

## What this adapter is not

- It is not a sandbox. The deployment provides the sandbox profile (filesystem, process, network, credentials) around Pi; the adapter documents the requirement and enforces nothing outside the action path.
- It is not a compile path from raw SOP text to production authority: SOP intake, compilation, linting, conformance, evaluation, approval and publication remain the separate auditable stages they are everywhere else in the estate.
- It is not certified: the adapter reuses the certified guardrail, but the integration itself carries no certificate until the gates pass.
