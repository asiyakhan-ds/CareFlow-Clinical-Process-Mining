
# CareFlow — dbt Transformation

## 1. Overview

CareFlow is a Clinical Pathway Process Mining project that analyzes synthetic Emergency Room (ER) patient journeys to identify workflow patterns, delays, and potential bottlenecks.

This module uses **dbt (data build tool)** to transform raw Electronic Health Record (EHR) event logs stored in Google BigQuery into a clean, standardized event log suitable for process mining and downstream analytics.

## 2. Objectives

- Transform raw EHR event data into a consistent structure.
- Standardize column names and data types.
- Handle missing or invalid values where appropriate.
- Maintain a clear and reusable SQL transformation pipeline.
- Prepare event logs for process discovery using PM4Py.
- Support downstream analysis and Power BI visualization.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| dbt Core | SQL-based data transformation |
| Google BigQuery | Cloud data warehouse |
| SQL | Data cleaning and transformation |
| Python | Data validation and process mining |
| PM4Py | Process discovery and analysis |
| Power BI | Dashboard and visualization |

## 4. Data Source

The raw event log is stored in BigQuery.

- **Project ID:** `elegant-poetry-511603-n5`
- **Dataset:** `careflow`
- **Source table:** `er_event_log`

Fully qualified source table:

`elegant-poetry-511603-n5.careflow.er_event_log`

The dataset was generated using the project's synthetic EHR data generator.

### Raw Event Log Columns

| Column | Description |
|---|---|
| `case_id` | Unique identifier for a patient visit |
| `patient_id` | Synthetic patient identifier |
| `event_id` | Unique identifier for an event |
| `activity` | Clinical or administrative activity |
| `timestamp` | Time at which the event occurred |
| `department` | Department associated with the event |
| `event_sequence` | Position of the event within a visit |
| `is_repeat` | Indicates whether an activity is repeated |

## 5. Transformation Architecture

The planned dbt workflow is:

```text
Raw EHR Event Log
        |
        v
Google BigQuery
        |
        v
stg_er_event_log
(Staging and data cleaning)
        |
        v
standardized_event_log
(Standardized event structure)
        |
        v
PM4Py Process Discovery
        |
        v
Process Maps and Bottleneck Analysis
```

The staging model prepares the source data for transformation. The standardized model provides a consistent event-log structure for downstream process mining.

## 6. dbt Models

### 6.1 Staging Model

**File:** `models/staging/stg_er_event_log.sql`

Purpose:

- Read data from the raw BigQuery event-log table.
- Standardize column names.
- Cast columns to appropriate data types.
- Apply appropriate handling for missing values.
- Prepare the data for downstream transformations.

Expected output: a cleaned staging event log.

### 6.2 Standardized Event Log

**File:** `models/marts/standardized_event_log.sql`

Purpose:

- Select the required fields from the staging model.
- Provide a consistent schema for process mining.
- Preserve the relationship between visits, activities, and event timestamps.
- Provide data in a form suitable for PM4Py.

The standardized output should contain, at minimum:

- `case_id`
- `activity`
- `event_timestamp`

Additional fields such as `patient_id`, `department`, `event_id`, `event_sequence`, and `is_repeat` may be retained for analysis and validation.

**Important:** The final model's column names and SQL logic must match the implemented SQL files.

## 7. Project Structure

```text
dbt/
├── README.md
├── dbt_project.yml
├── profiles.yml
└── models/
    ├── staging/
    │   └── stg_er_event_log.sql
    └── marts/
        └── standardized_event_log.sql
```

- `dbt_project.yml`: Defines the dbt project configuration.
- `profiles.yml`: Defines the BigQuery connection profile.
- `stg_er_event_log.sql`: Defines the staging transformation.
- `standardized_event_log.sql`: Defines the standardized output model.

## 8. Setup and Execution

### Prerequisites

- Python installed.
- Access to the CareFlow Google Cloud project.
- BigQuery permissions to query the source table and create model outputs.
- dbt Core and the appropriate BigQuery adapter installed.
- Google Cloud authentication configured.

### Install dbt

Install dbt Core with the BigQuery adapter in your Python environment:

```bash
pip install dbt-core dbt-bigquery
```

Verify the installation:

```bash
dbt --version
```

### Configure the Project

1. Configure the project settings in `dbt_project.yml`.
2. Configure the BigQuery connection in `profiles.yml`.
3. Set the Google Cloud project, dataset, authentication method, and required permissions.
4. Define the raw BigQuery table as a dbt source.
5. Configure the staging and standardized models.

Use an appropriate authentication method and avoid committing service-account keys, access tokens, or other credentials to GitHub.

### Validate the Connection

Run these commands from the directory containing `dbt_project.yml`:

```bash
dbt debug
```

This checks the dbt project and connection configuration.

### Run the Models

```bash
dbt run
```

This executes the configured dbt models.

### Test the Models

```bash
dbt test
```

This runs the tests defined for the project.

**Note:** These commands should be run after the configuration and SQL models have been implemented. A successful command should be verified from its actual output.

## 9. Data Quality and Validation

The transformation pipeline should be checked for:

- Required columns being present.
- Valid case identifiers and activity names.
- Correct timestamp data types.
- Missing values in essential fields.
- Duplicate events, where uniqueness is expected.
- Consistent event ordering within each visit.
- Successful generation of the standardized output.

The original event log contains 3,201 events across 500 visits. The existing raw-data validation script can be used to verify the source dataset.

Additional dbt tests and standardized-log validation should be run once their implementations are complete.

## 10. Integration with Process Mining

The standardized event log will serve as the input for PM4Py.

Process mining uses three essential concepts:

- **Case ID:** Identifies a patient visit.
- **Activity:** Identifies an event in the visit.
- **Timestamp:** Establishes the chronological order of events.

PM4Py can use these fields to discover the observed clinical workflow, identify repeated activities, and support bottleneck analysis.

Example patient pathway:

`Registration → Triage → Doctor Consultation → X-Ray → Treatment → Discharge`

Actual pathways are derived from the event-log data and may vary between visits.

## 11. Expected Outcome

The dbt transformation module is intended to provide:

- A repeatable SQL transformation pipeline.
- A clean and standardized event log in BigQuery.
- Consistent inputs for process discovery.
- Better traceability and maintainability of data transformations.
- A foundation for downstream analytics and visualization.

## 12. Implementation Status

Update this section as each task is completed and verified.

- [ ] Configure dbt Core and the BigQuery adapter.
- [ ] Configure the dbt project and BigQuery profile.
- [ ] Define the raw event-log source.
- [ ] Implement the staging model.
- [ ] Implement the standardized event-log model.
- [ ] Add data quality tests.
- [ ] Run `dbt debug`, `dbt run`, and `dbt test`.
- [ ] Validate the standardized output.
- [ ] Document successful execution and validation results.

---

**Project:** CareFlow — Clinical Pathway Process Mining  
**Module:** Week 2 — dbt Transformation  
**Data Warehouse:** Google BigQuery