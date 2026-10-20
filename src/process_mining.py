
import pandas as pd
import pm4py
from pathlib import Path

# Resolve paths from the project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "er_event_log.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"
MODEL_PATH = PROJECT_ROOT / "process_model.png"
ACTIVITY_REPORT_PATH = REPORTS_DIR / "activity_frequency.csv"
TRANSITION_REPORT_PATH = REPORTS_DIR / "activity_transitions.csv"

# Required input columns
REQUIRED_COLUMNS = ["case_id", "activity", "timestamp"]


def main():
    # Check that the dataset exists
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Event log not found: {DATA_PATH}"
        )

    # Load the synthetic EHR event log
    df = pd.read_csv(DATA_PATH)

    # Validate the dataset structure
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    original_rows = len(df)

    # Convert timestamps
    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce"
    )

    # Remove records missing essential values
    df = df.dropna(
        subset=["case_id", "activity", "timestamp"]
    ).copy()

    # Clean activity names
    df["activity"] = df["activity"].astype(str).str.strip()
    df = df[df["activity"] != ""].copy()

    dropped_rows = original_rows - len(df)

    if df.empty:
        raise ValueError(
            "No valid events remain after data validation."
        )

    # Sort events by case and timestamp
    df = df.sort_values(
        ["case_id", "timestamp"]
    ).copy()

    # ------------------------------------------
    # 1. Event log statistics
    # ------------------------------------------
    total_cases = df["case_id"].nunique()
    total_events = len(df)
    total_activities = df["activity"].nunique()

    activity_frequency = (
        df["activity"]
        .value_counts()
        .rename_axis("activity")
        .reset_index(name="event_count")
    )

    # Create the reports directory
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Save activity frequency report
    activity_frequency.to_csv(
        ACTIVITY_REPORT_PATH, index=False
    )

    # ------------------------------------------
    # 2. Activity transition analysis
    # ------------------------------------------
    # Find the previous activity and timestamp
    # separately within each patient case.
    df["previous_activity"] = (
        df.groupby("case_id")["activity"].shift(1)
    )

    df["previous_timestamp"] = (
        df.groupby("case_id")["timestamp"].shift(1)
    )

    # The first event in each case has no transition
    transitions = df.dropna(
        subset=["previous_activity"]
    ).copy()

    # Calculate elapsed time between consecutive events
    transitions["minutes_between"] = (
        transitions["timestamp"]
        - transitions["previous_timestamp"]
    ).dt.total_seconds() / 60

    # Summarize how often each transition occurs
    transition_report = (
        transitions.groupby(
            ["previous_activity", "activity"]
        )
        .agg(
            transition_count=("activity", "size"),
            avg_minutes_between=("minutes_between", "mean"),
        )
        .reset_index()
        .rename(
            columns={
                "previous_activity": "from_activity",
                "activity": "to_activity",
            }
        )
    )

    transition_report["avg_minutes_between"] = (
        transition_report["avg_minutes_between"].round(2)
    )

    transition_report = transition_report.sort_values(
        "transition_count",
        ascending=False
    )

    # Save activity transition report
    transition_report.to_csv(
        TRANSITION_REPORT_PATH, index=False
    )

    # ------------------------------------------
    # 3. Process discovery using PM4Py
    # ------------------------------------------
    # Rename columns to PM4Py event-log conventions
    event_log_df = df.rename(
        columns={
            "case_id": "case:concept:name",
            "activity": "concept:name",
            "timestamp": "time:timestamp",
        }
    )

    event_log = pm4py.format_dataframe(
        event_log_df,
        case_id="case:concept:name",
        activity_key="concept:name",
        timestamp_key="time:timestamp",
    )

    # Discover the process tree
    process_model = pm4py.discover_process_tree_inductive(
        event_log
    )

    # Export the process model
    pm4py.save_vis_process_tree(
        process_model, str(MODEL_PATH)
    )

    # ------------------------------------------
    # 4. Display analysis results
    # ------------------------------------------
    print("\nCareFlow Process Mining Summary")
    print("=" * 40)
    print(f"Valid events: {total_events}")
    print(f"Unique cases: {total_cases}")
    print(f"Unique activities: {total_activities}")
    print(f"Records excluded: {dropped_rows}")

    print("\nTop 5 activities by event count:")
    print(activity_frequency.head(5).to_string(index=False))

    print("\nTop 10 activity transitions:")
    if transition_report.empty:
        print("No consecutive activity transitions found.")
    else:
        print(transition_report.head(10).to_string(index=False))

    print(f"\nProcess model saved to: {MODEL_PATH}")
    print(f"Activity report saved to: {ACTIVITY_REPORT_PATH}")
    print(f"Transition report saved to: {TRANSITION_REPORT_PATH}")


if __name__ == "__main__":
    main()
