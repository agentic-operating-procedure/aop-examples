# dea:metric-mttr-anomaly-p50-ran-operations

Candidate Performance Metric record for **MTTR Anomaly P50 (RAN Operations)** (MTTR-ANOM-P50) in the OpenDEAM Metric catalog.

## 1. Identity

- **Canonical id:** `dea:metric-mttr-anomaly-p50-ran-operations`
- **Name:** MTTR Anomaly P50 (RAN Operations)
- **Type:** Metric
- **Version:** 1.0.0
- **Lifecycle:** candidate
- **Short form:** MTTR-ANOM-P50

## 2. Definition

MTTR Anomaly P50 (RAN Operations) addresses the speed of anomaly resolution and is a fixture of network operations reporting. It provides the day-to-day signal that triage and restoration keep pace with the anomaly load on a 5G radio access network. It is defined as the median over cases of the ticket resolved time minus the ticket created time, for triaged RAN anomalies in the period; the result is stated in minutes. It should be driven down, since lower readings signal healthier restoration performance, read together with the first-pass resolution rate so that speed is not bought with rework.

## 3. Context

The median (rather than the mean) is chosen because anomaly restoration times are heavy-tailed: a minority of hardware-dispatch cases dominates the mean while the p50 tracks the routine triage health the operations centre actually steers by. Read together with the first-pass resolution rate, the pair separates speed from quality so neither is bought with the other. The Agentic Operating Procedure programme's worked exemplar uses this record as the human baseline its governed-agent runs are measured against.

## Provenance

Contributed by the Agentic Operating Procedure programme with its 5G RAN anomaly management exemplar, whose human baseline and evaluation protocol bind to this record. Lodged per the AOP specification's process-alignment rule (NM-INT-5): an AOP binds its baseline metrics to canonical records or declares the gap; this record closes two declared gaps.
