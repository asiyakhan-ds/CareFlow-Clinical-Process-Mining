# Project Data

This directory contains datasets used in the CareFlow clinical pathway
process mining project.

## Directory Structure

- `raw/`: Contains the original synthetic EHR event log.
- `raw/er_event_log.csv`: Synthetic emergency room patient event records.

## Dataset Overview

The event log contains 3,201 records representing 500 patient visits
and 215 unique patients.

The dataset was generated using the project's synthetic EHR generator.
It is intended for healthcare workflow analysis and process mining.

## Data Privacy

The dataset contains synthetic records and is not intended to represent
real patient medical records.

## Validation

Run the following command from the project root to validate the dataset:

`python src/validate_event_log.py`
