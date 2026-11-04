# RB-RAN-014: RAN Anomaly Triage Procedure

## Objective

Detect, triage and resolve radio access network anomalies on the 5G estate before customer impact materialises, keeping the network within its service availability commitments.

## Outcome

The reported anomaly is validated, classified and either auto-recovered, restarted, escalated to the RAN operations engineer, or dispatched to field maintenance, with the disposition recorded against the anomaly ticket.

## In scope

- 5G RAN cell-level anomalies raised by the network assurance platform
- Anomalies triaged by the network operations centre

## Out of scope

- Core network anomalies
- Planned maintenance and upgrade windows
- Direct customer communication

## Steps

- validate-alarm
- classify-anomaly
- run-kpi-diagnostic
- restart-cell
- notify-noc
- escalate-anomaly
- dispatch-field-crew

## Decision rules

- if severity_score >= 85 then escalate to RAN operations engineer [approval-required]
- if kpi_degradation_pct > 30 and cell_outage == true then notify NOC and request approval before dispatch [approval-required]
- if kpi_degradation_pct <= 30 then restart the affected cell [autonomous]
- if hardware_suspected == true then dispatch field maintenance crew [approval-required]
- if anomaly_persistence_min >= 45 then escalate to RAN operations engineer [prohibited]

## Exceptions

- anomaly persists past 45 minutes after restart -> escalate to ran-operations-engineer

## Escalation

High-severity anomalies are escalated to the RAN operations engineer.
