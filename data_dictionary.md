 # Data Dictionary - Clinical Process Mining

This document describes the schema and field definitions for `careflow_clinical_data.csv`.

| Field Name | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `Patient_ID` | String / Categorical | Unique anonymized identifier for each patient trajectory | `P-101` |
| `Case_ID` | String | Identifier mapping unique clinical admission/encounter | `C-1001` |
| `Activity` | Categorical | The clinical step or event recorded in the pathway | `Triage`, `Consultation` |
| `Timestamp` | Datetime (`YYYY-MM-DD HH:MM:SS`) | Precise timestamp when the activity occurred | `2026-10-01 08:30:00` |
| `Department` | Categorical | Hospital unit handling the activity | `Emergency`, `Radiology` |
| `Resource` | String | Anonymized ID of the medical staff/doctor | `Doc_12`, `Nurse_01` |
| `Cost` | Numeric | Associated unit cost for the event/activity | `150.00` |

## Notes
- Raw data stored in `/data/raw/careflow_clinical_data.csv`.
- Processed data outputs will be exported to `/data/processed/`.
