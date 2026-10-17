SELECT
    CAST(case_id AS STRING) AS case_id,
    CAST(patient_id AS STRING) AS patient_id,
    CAST(event_id AS STRING) AS event_id,
    CAST(activity AS STRING) AS activity,
    SAFE_CAST(`timestamp` AS TIMESTAMP) AS event_timestamp,
    CAST(department AS STRING) AS department,
    SAFE_CAST(event_sequence AS INT64) AS event_sequence,
    SAFE_CAST(is_repeat AS BOOL) AS is_repeat

FROM {{ source('careflow', 'er_event_log') }}