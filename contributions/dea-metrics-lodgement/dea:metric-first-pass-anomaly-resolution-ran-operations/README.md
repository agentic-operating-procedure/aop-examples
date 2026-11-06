# dea:metric-first-pass-anomaly-resolution-ran-operations

Candidate Performance Metric record for **First-Pass Anomaly Resolution (RAN Operations)** (FP-ANOM-RES) in the OpenDEAM Metric catalog.

## 1. Identity

- **Canonical id:** `dea:metric-first-pass-anomaly-resolution-ran-operations`
- **Name:** First-Pass Anomaly Resolution (RAN Operations)
- **Type:** Metric
- **Version:** 1.0.0
- **Lifecycle:** candidate
- **Short form:** FP-ANOM-RES

## 2. Definition

First-Pass Anomaly Resolution (RAN Operations) addresses the quality of first response and is a fixture of network operations reporting. It provides the standing signal that the first disposition resolves the anomaly without rework loops or unanticipated exceptions. It is defined as first-pass resolved anomaly cases divided by total triaged anomaly cases in the period; the result is stated as a percentage. It should be driven up, since higher readings signal healthier triage quality, read together with the restoration time metric so that quality is not bought with delay.

## 3. Context

First-pass resolution counts a case resolved on the first disposition without rework loops firing and without exceptions beyond the anticipated set. It is the quality counterpart of the restoration-time metric: a triage operation can raise speed by escalating everything or dispatching early, and this record is the number that exposes the trade. The Agentic Operating Procedure programme's worked exemplar uses this record as the human baseline its governed-agent runs are measured against.

## Provenance

Contributed by the Agentic Operating Procedure programme with its 5G RAN anomaly management exemplar, whose human baseline and evaluation protocol bind to this record. Lodged per the AOP specification's process-alignment rule (NM-INT-5): an AOP binds its baseline metrics to canonical records or declares the gap; this record closes two declared gaps.
