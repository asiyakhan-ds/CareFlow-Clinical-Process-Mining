
import pandas as pd
import pm4py
from pathlib import Path

# Load the synthetic EHR event log
DATA_PATH = Path("data/raw/er_event_log.csv")
df = pd.read_csv(DATA_PATH)

# Convert timestamps
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Prepare data for process mining
df = df.rename(columns={
    "case_id": "case:concept:name",
    "activity": "concept:name",
    "timestamp": "time:timestamp"
})

# Sort events in chronological order
df = df.sort_values(
    ["case:concept:name", "time:timestamp"]
)

# Discover the process model
event_log = pm4py.format_dataframe(
    df,
    case_id="case:concept:name",
    activity_key="concept:name",
    timestamp_key="time:timestamp"
)

process_model = pm4py.discover_process_tree_inductive(event_log)

# Export the discovered process model
output_path = Path("process_model.png")
pm4py.save_vis_process_tree(process_model, str(output_path))

print("Process model generated successfully!")
print(f"Saved to: {output_path.resolve()}")
