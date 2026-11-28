# RB-RAN-014: RAN Anomaly Triage Procedure

Version 8. Authority wording reconciled per the Agentic Operating Procedure programme's decision-rights model: escalation to a human is a governed handoff (the agent prepares the evidence bundle and waits; the handoff itself is not an agent-executable action), and only the dispatch of external resources carries an approval requirement. The engaged human owns the decision from that point.

## Objective

Detect, triage and resolve radio access network anomalies on the 5G estate before customer impact materialises, keeping the network within its service availability commitments.

## Outcome

The reported anomaly is validated, classified and either auto-recovered, restarted, notified, escalated through the governed handoff route, or dispatched to field maintenance after approval, with the disposition recorded against the anomaly ticket.

## In scope

- 5G RAN cell-level anomalies raised by the network assurance platform
- Anomalies triaged by the network operations centre

## Out of scope

- Core network anomalies
- Planned maintenance and upgrade windows
- Direct customer communication
- Paging the on-call engineer: the agent never engages on-call staff; persistence beyond the restart path routes through the declared exception edge to the on-call engineer

## Steps

- validate-alarm
- classify-anomaly
- run-kpi-diagnostic
- restart-cell
- notify-noc
- handoff-anomaly (governed handoff: the agent prepares the escalation bundle; the receiving role owns the decision)
- dispatch-field-crew

## Decision rules

- if severity_score >= 85 then dispatch requires human approval [approval-required]
- if kpi_degradation_pct > 30 and cell_outage == true then notify NOC and request human approval before dispatch [approval-required]
- if kpi_degradation_pct <= 30 then restart the affected cell [autonomous]
- if hardware_suspected == true then dispatch requires human approval [approval-required]
- if anomaly_persistence_min >= 45 then the agent must not dispatch or engage the on-call engineer; the case routes through the persistence exception edge [prohibited]
- filing a handoff-anomaly ticket is a governed handoff request, always available to the agent: it is how the agent reaches a human (reversible, no external effect beyond the ticket)

## Exceptions

- anomaly persists past 45 minutes after restart -> governed handoff to ran-operations-engineer (exception edge; not an agent action)

## Escalation

Escalation is a governed handoff through the declared escalation routes. The agent prepares the bundle; the receiving role decides. The agent never pages on-call staff directly.
