
import pandas as pd
import pm4py
from pathlib import Path

# Resolve paths from the project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "er_event_log.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"
MODEL_PATH = PROJECT_ROOT / "process_model.png"
ACTIVITY_REPORT_PATH = REPORTS_DIR / "activity_frequency.csv"

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

    # Convert timestamps and identify invalid records
    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce"
    )

    # Remove records missing essential process-mining values
    df = df.dropna(
        subset=["case_id", "activity", "timestamp"]
    ).copy()


    if df.empty:
        raise ValueError(
            "No valid events remain after data validation."
        )

    # Normalize activity names and remove blank values
    df["activity"] = df["activity"].astype(str).str.strip()
    df = df[df["activity"] != ""].copy()
    dropped_rows = original_rows - len(df)

    if df.empty:
        raise ValueError("No valid activities found in the event log.")

    # Prepare data for PM4Py
    df = df.rename(
        columns={
            "case_id": "case:concept:name",
            "activity": "concept:name",
            "timestamp": "time:timestamp",
        }
    )

    # Sort events chronologically within each case
    df = df.sort_values(
        ["case:concept:name", "time:timestamp"]
    )

    # Summarize event-log statistics
    total_cases = df["case:concept:name"].nunique()
    total_events = len(df)
    total_activities = df["concept:name"].nunique()

    activity_frequency = (
        df["concept:name"]
        .value_counts()
        .rename_axis("activity")
        .reset_index(name="event_count")
    )

    # Create the reports directory if necessary
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Export activity-frequency report
    activity_frequency.to_csv(
        ACTIVITY_REPORT_PATH, index=False
    )

    # Format the event log for PM4Py
    event_log = pm4py.format_dataframe(
        df,
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

    # Display a summary of the analysis
    print("\nCareFlow Process Mining Summary")
    print("=" * 35)
    print(f"Valid events: {total_events}")
    print(f"Unique cases: {total_cases}")
    print(f"Unique activities: {total_activities}")
    print(f"Records excluded: {dropped_rows}")

    print("\nTop 5 activities by event count:")
    print(activity_frequency.head(5).to_string(index=False))

    print(f"\nProcess model saved to: {MODEL_PATH}")
    print(f"Activity report saved to: {ACTIVITY_REPORT_PATH}")


if __name__ == "__main__":
    main()
