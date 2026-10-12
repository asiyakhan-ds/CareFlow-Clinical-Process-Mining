
from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/raw/er_event_log.csv")

REQUIRED_COLUMNS = [
    "case_id",
    "patient_id",
    "event_id",
    "activity",
    "timestamp",
    "department",
    "event_sequence",
    "is_repeat",
]


def validate_event_log(path=DATA_PATH):
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)

    errors = []

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(f"Missing columns: {missing_columns}")
        print("\n".join(errors))
        return False

    if df.empty:
        errors.append("Dataset is empty")

    important_columns = [
        "case_id",
        "patient_id",
        "event_id",
        "activity",
        "timestamp",
        "department",
        "event_sequence",
        "is_repeat",
    ]

    missing_values = df[important_columns].isnull().sum()
    missing_values = missing_values[missing_values > 0]

    if not missing_values.empty:
        errors.append(f"Missing values:\n{missing_values}")

    if df["event_id"].duplicated().any():
        errors.append("Duplicate event IDs found")

    parsed_time = pd.to_datetime(df["timestamp"], errors="coerce")

    if parsed_time.isnull().any():
        errors.append("Invalid timestamps found")

    if not df["is_repeat"].isin([True, False]).all():
        errors.append("Invalid values found in is_repeat")

    if not errors:
        ordered = df.assign(_timestamp=parsed_time)

        ordered = ordered.sort_values(
            ["case_id", "event_sequence"]
        )

        time_diff = ordered.groupby("case_id")["_timestamp"].diff()

        if (time_diff.dropna() < pd.Timedelta(0)).any():
            errors.append(
                "Events are not chronological within one or more cases"
            )

    print(f"Dataset rows: {len(df)}")
    print(f"Unique visits: {df['case_id'].nunique()}")
    print(f"Unique patients: {df['patient_id'].nunique()}")

    if errors:
        print("\nVALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return False

    print("\nVALIDATION PASSED")
    print("All required columns and data-quality checks passed.")
    return True


if __name__ == "__main__":
    success = validate_event_log()
    if not success:
        raise SystemExit(1)