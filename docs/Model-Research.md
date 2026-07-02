# Model Research and Design – AI-Assisted Threat Detection Dashboard

## 1. Introduction and Overview

This document presents the model research and design framework for the AI-Assisted Threat Detection Dashboard, a cybersecurity monitoring platform built to help security analysts identify, prioritize, and respond to threats faster and more accurately. The system is designed as a multi-agent AI architecture that combines anomaly detection, threat classification, alert correlation, risk scoring, and natural-language query capabilities into a unified analyst-facing dashboard.

The project addresses one of the most persistent challenges in modern cybersecurity operations: organizations generate enormous volumes of security alerts from firewalls, endpoint tools, authentication systems, and network sensors, but analysts often struggle to distinguish genuine threats from routine noise. This leads to alert fatigue, delayed responses, and missed incidents. The AI-Assisted Threat Detection Dashboard is designed to reduce that burden by combining automated detection models with an interactive analyst interface that prioritizes incidents by risk and presents findings in a clear, actionable format.

## 2. Project Objectives

The model research for this project is guided by the following core objectives:

- Detect suspicious and abnormal security behavior using unsupervised machine learning without relying only on pre-defined attack signatures.
- Classify suspicious events into interpretable threat categories that analysts can act on directly from the dashboard.
- Assign composite risk scores to each event so the dashboard can surface the most critical incidents first.
- Produce structured model outputs that integrate cleanly into the multi-agent architecture, especially the anomaly detection, classification, correlation, and dashboard orchestration agents.
- Support analyst workflows by providing not just detections but also context: severity, affected asset, anomaly score, and risk ranking.

## 3. Dataset Design

The prototype implementation uses a synthetic but realistic cybersecurity event dataset. Each row in the dataset represents a single security event or normalized network session. This approach is appropriate for the prototype stage because it allows controlled injection of attack patterns, consistent schema design, and repeatable evaluation before connecting to real enterprise telemetry such as Zeek, Suricata, or Elasticsearch logs.

The dataset schema includes the following fields:

| Field | Description |
|---|---|
| event_id | Unique identifier for each event |
| timestamp | Time of event occurrence |
| source_ip | Origin IP address |
| destination_ip | Target system IP |
| source_port | Originating port |
| destination_port | Target port |
| protocol | TCP, UDP, ICMP, HTTP, HTTPS, SSH |
| bytes_sent | Outbound data volume |
| bytes_received | Inbound data volume |
| packet_count | Session packet count |
| failed_login_count_last_10min | Authentication pressure indicator |
| asset_criticality | Target importance on a 1 to 5 scale |
| geo_risk_score | Source country risk proxy 0 to 10 |
| label | Threat category for supervised learning |

The threat label space includes five categories: **Normal**, **BruteForce**, **DataExfiltration**, **MalwareBeacon**, and **SuspiciousScan**.

## 4. Anomaly Detection Model Research

Anomaly detection is the first modeling layer in the dashboard. Its purpose is to identify events that deviate significantly from normal behavior without requiring labeled attack data.

| Model | Type | Strength | Limitation | Fit |
|---|---|---|---|---|
| Isolation Forest | Unsupervised | Fast, scalable, no labels needed | Limited interpretability | Strong |
| Local Outlier Factor | Unsupervised | Captures local deviations | Sensitive to parameters | Moderate |
| One-Class SVM | Semi-supervised | Useful with only normal data | Computationally expensive | Low |

**Selected Model: Isolation Forest**

Isolation Forest is selected as the primary anomaly detection model. It provides the best combination of scalability, practical usability, and fit for the unlabeled synthetic dataset used in the prototype stage.

## 5. Classification Model Research

The classification layer assigns meaningful threat labels to suspicious events after anomaly detection.

| Model | Strength | Limitation | Fit |
|---|---|---|---|
| Random Forest | High accuracy, feature importance, robust | Requires labeled data | Strong |
| Decision Tree | Interpretable, visualizable | Overfits easily | Baseline |
| Logistic Regression | Fast, transparent | Weak on non-linear patterns | Baseline |
| XGBoost | Very strong performance | Complex tuning | Stretch goal |

**Selected Model: Random Forest**

Random Forest is selected as the primary classification model. A Decision Tree will be retained as an interpretable baseline to support explanation panels in the dashboard.

## 6. Risk Scoring Design

A composite risk score is calculated for each event to provide a single, sortable measure of priority for the dashboard.

**Formula:**

```
Risk Score = 0.4 x Threat Severity + 0.3 x Asset Criticality + 0.2 x Vulnerability Exposure + 0.1 x Anomaly Score
```

- **Threat Severity**: Derived from the classifier output, mapped to 0-10 scale.
- **Asset Criticality**: From dataset field reflecting target system importance (1-5).
- **Vulnerability Exposure**: Contextual risk from source or target context (0-5).
- **Anomaly Score**: Normalized Isolation Forest output (0-10).

The risk score is stored with each event record and used by the SQL task to filter high-risk events and by the dashboard to drive color-coded alerts and sorted incident queues.

## 7. Integration with Multi-Agent Architecture

| Project Agent | Role of Selected Models |
|---|---|
| Data Ingestion and Normalization Agent | Supplies clean structured event data to downstream models |
| Network Traffic Monitoring Agent | Produces traffic features consumed by anomaly detection |
| Anomaly Detection Agent | Runs Isolation Forest to score and flag unusual events |
| Threat Classification and Severity Agent | Applies Random Forest to assign threat labels and severity |
| Risk Prioritization Module | Combines outputs into composite risk scores |
| Dashboard Orchestration Agent | Displays risk-ranked incidents and anomaly trends |

## 8. Evaluation Plan

The Python notebook implementation evaluates both modeling stages:

- **Anomaly Detection**: Overall anomaly rate, average anomaly score by label, proportion of known attack rows flagged. No formal precision/recall since the model is unsupervised.
- **Classification**: Accuracy, per-class precision, recall, F1 score using scikit-learn classification report. Confusion matrix to identify misclassification patterns.
- **Risk Scoring**: Distribution of risk scores by label to confirm attack events consistently score higher than Normal events.

## 9. Conclusion and Next Steps

The selected strategy combines **Isolation Forest** for unsupervised anomaly detection with **Random Forest** for supervised threat classification, supported by a four-component weighted risk scoring formula that drives dashboard prioritization.

The two companion deliverables for this document are:
1. A **Python notebook** implementing data generation, pandas analysis, anomaly detection, classification, and risk scoring.
2. A **SQL notebook** demonstrating filtering, grouping, aggregation, and join-based queries on the processed threat event data.

Future versions could incorporate deep learning autoencoders for anomaly detection, XAI frameworks like SHAP for explainability, federated learning for privacy-preserving training, and real-time streaming pipelines from production security infrastructure.
