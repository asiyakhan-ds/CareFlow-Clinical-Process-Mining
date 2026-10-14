# Raw Synthetic Data

## File Description

`er_event_log.csv` contains synthetic emergency room event records
generated for the CareFlow clinical pathway process mining project.

## Dataset Statistics

- Total event records: 3,201
- Unique patient visits: 500
- Unique patients: 215
- Total columns: 8

## Column Definitions

| Column | Description |
|---|---|
| `case_id` | Unique identifier for a patient visit |
| `patient_id` | Identifier for the patient |
| `event_id` | Unique identifier for an event |
| `activity` | Clinical or administrative activity performed |
| `timestamp` | Date and time when the event occurred |
| `department` | Department associated with the event |
| `event_sequence` | Position of the event within the visit |
| `is_repeat` | Indicates whether the activity is a repeated event |

## Validation

Run the following command from the project root:

`python src/validate_event_log.py`

The dataset should pass the validation checks before being used
for further analysis.
