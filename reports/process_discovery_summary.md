# CareFlow – PM4Py Process Discovery Summary

## 1. Objective

The objective of process discovery is to understand patient journeys by analyzing event logs and discovering process flows followed during clinical visits.

## 2. Dataset Overview

The analysis uses a synthetic EHR event log created for the CareFlow project.

- Total event records: 3,201
- Total clinical visits: 500
- Unique patients: 215
- Different activities: 9
- Repeated activity records: 84

The dataset contains synthetic data and no real patient information.

## 3. Process Discovery Methodology

PM4Py is used to discover a process model from the event log.

The workflow includes:

1. Loading the event log using Pandas.
2. Converting timestamps into datetime format.
3. Mapping columns to the format required by PM4Py.
4. Sorting events by case and timestamp.
5. Converting the dataset into a PM4Py event log.
6. Applying the Inductive Miner algorithm to discover a process tree.
7. Exporting the process model as an image.

## 4. Initial Findings

- Registration, triage, and doctor consultation are frequently occurring activities.
- Treatment is recorded in 500 visits.
- Lab tests and X-rays occur in fewer visits.
- Repeated triage events occur in 84 visits.
- Each visit contains between 5 and 10 event records, with an average of approximately 6.4 events.

## 5. Project Outputs

- Process discovery script: `src/process_mining.py`
- Discovered process model: `process_model.png`

## 6. Future Work

- Examine common and alternative patient pathways.
- Analyze transitions between consecutive activities.
- Investigate repeated activities and unusual process paths.
- Identify potential bottlenecks for further investigation.
- Compare observed behavior with a reference process when available.

## 7. Limitations

The findings are based on synthetic data. Elapsed time between event timestamps should not automatically be treated as actual patient waiting time without confirming the meaning of the timestamps.