WITH source_data AS (
    SELECT *
    FROM {{ ref('stg_er_event_log') }}
),

cleaned_data AS (
    SELECT
        case_id,
        patient_id,
        event_id,
        TRIM(activity) AS activity,
        event_timestamp,
        department,
        event_sequence,
        COALESCE(is_repeat, FALSE) AS is_repeat
    FROM source_data
    WHERE case_id IS NOT NULL
      AND activity IS NOT NULL
      AND event_timestamp IS NOT NULL
)

SELECT *
FROM cleaned_data