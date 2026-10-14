
# CareFlow BigQuery Setup

## Purpose

This document describes how the synthetic emergency-room event log is stored in Google BigQuery for CareFlow process mining.

## Google Cloud Configuration

- Project ID: `elegant-poetry-511603-n5`
- Dataset: `careflow`
- Table: `er_event_log`
- Source file: `data/raw/er_event_log.csv`
- Data type: Synthetic emergency-room event data

## Table Contents

The event log contains the following fields:

- `case_id`: Identifies a patient visit.
- `patient_id`: Identifies a synthetic patient.
- `event_id`: Unique identifier for an event.
- `activity`: Activity performed during the visit.
- `timestamp`: Date and time of the activity.
- `department`: Department where the activity occurred.
- `event_sequence`: Order of the activity within the visit.
- `is_repeat`: Indicates a repeated triage activity.

## Upload Procedure

1. Open BigQuery Studio in Google Cloud Console.
2. Select the project `elegant-poetry-511603-n5`.
3. Open the `careflow` dataset.
4. Create a table from the local CSV file `er_event_log.csv`.
5. Select CSV as the source format and review the detected schema.
6. Confirm that the table is named `er_event_log`.

## Verification Query

```sql
SELECT
  COUNT(*) AS total_events,
  COUNT(DISTINCT case_id) AS total_visits,
  COUNT(DISTINCT patient_id) AS unique_patients
FROM `elegant-poetry-511603-n5.careflow.er_event_log`;
```

## Data Privacy

All patient records in this project are synthetic and are not real patient records.