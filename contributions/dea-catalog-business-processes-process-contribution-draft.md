# Process Contribution Draft: 5G RAN Anomaly Management

Status: PREPARED, awaiting lodging. This draft follows the contribution record shape observed in `technehub-labs/dea-catalog-business-processes` (`contributions/processes/`). On lodging, it is filed through that catalog's own contribution process; the published `processes:process-*` identifier then replaces the declared process gap in `manifests/ran-anomaly.json` and the compiled AOP, per CG-PA-4.

```yaml
# Process Contribution record for the 5G RAN anomaly triage flow.
schema: dea-catalog-processes/contribution/v1
contribution_type: new-entry
contributor: aop-programme
status: draft

# ECF context: the operations domain at the Operate stage, per the
# catalog's area structure (ao-operate).
context_reference:
  context_id: processes:pc-ao-operate
  domain: AgencyAndOrganization   # to be confirmed against the catalog's domain enumeration at lodging
  lifecycle_stage: Operate

proposed_entry:
  id: processes:process-<assigned-by-catalog>
  name: Manage RAN Anomaly Triage
  type: Process
  version: 1.0.0
  lifecycle_status: candidate

  process_intent: operational
  process_audience: <per the catalog's audience enumeration at lodging>
  process_type: operational

  description: |
    Triage, classify and resolve radio access network anomalies on the
    5G estate: validate the raised alarm, classify the anomaly, run the
    KPI diagnostic, apply the bounded recovery (cell restart), notify
    the network operations centre, and escalate or dispatch field
    maintenance on the declared thresholds. Performed by a NOC AI agent
    inside a governed harness with human approvers for high-impact
    dispositions (see the Agentic Operating Procedure exemplar).

  trigger: |
    A cell-level anomaly is raised by the network assurance platform
    for a 5G cell in the monitored estate.

  outcome: |
    The anomaly is resolved, restarted, escalated or dispatched with
    the disposition recorded against the anomaly ticket.

# Activity decomposition per the observed triage flow; the catalog's
# activity and task entity forms apply at lodging.
activities:
  - name: Validate And Classify Anomaly
    tasks: [intake, classification]
  - name: Diagnose KPI Degradation
    tasks: [kpi-diagnostic]
  - name: Apply Bounded Recovery
    tasks: [cell-restart]
  - name: Notify And Escalate Or Dispatch
    tasks: [noc-notification, escalation, field-dispatch]
```
