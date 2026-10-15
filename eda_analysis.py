import pandas as pd
import numpy as np

def load_data(file_path):
    """Load clinical pathway data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully with shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def inspect_dataset(df):
    """Inspect dataset columns, data types, and sample records."""
    if df is None:
        print("No DataFrame to inspect.")
        return
    print("\n--- Dataset Info ---")
    print(df.info())
    print("\n--- First 5 Rows ---")
    print(df.head())

def check_missing_values(df):
    """Check for missing values across columns."""
    if df is None:
        return
    missing = df.isnull().sum()
    print("\n--- Missing Values Count ---")
    print(missing[missing > 0] if missing.sum() > 0 else "No missing values found.")
    return missing

if __name__ == "__main__":
    data_path = "data/raw_data.csv"
    df = load_data(data_path)
    if df is not None:
        inspect_dataset(df)
        check_missing_values(df)
        summary_statistics(df)
        check_duplicates(df)

def summary_statistics(df):
    """Generate summary statistics for numerical columns."""
    print("\n--- Summary Statistics ---")
    print(df.describe())
    return df.describe()

def check_duplicates(df):
    """Check and display duplicate rows in the dataset."""
    duplicates = df.duplicated().sum()
    print(f"\n--- Duplicate Rows ---")
    print(f"Total duplicate rows: {duplicates}")
    return duplicates

    def prepare_event_log_schema(df, case_col='patient_id', activity_col='activity_name', timestamp_col='timestamp'):
    """
    Standardizes the dataset columns into process mining event log schema:
    - case_id: Unique trace identifier for patient journey
    - activity: Standardized event name
    - timestamp: Datetime format for temporal ordering
    """
    event_log = df.copy()
    
    # Map raw columns to standardized schema
    column_mapping = {
        case_col: 'case_id',
        activity_col: 'activity',
        timestamp_col: 'timestamp'
    }
    
    # Verify required columns exist
    missing_cols = [col for col in column_mapping.keys() if col not in event_log.columns]
    if missing_cols:
        raise KeyError(f"Missing required schema columns in dataset: {missing_cols}")
        
    # Rename and select standardized event log attributes
    event_log = event_log.rename(columns=column_mapping)
    
    # Standardize data types
    event_log['case_id'] = event_log['case_id'].astype(str)
    event_log['activity'] = event_log['activity'].astype(str)
    event_log['timestamp'] = pd.to_datetime(event_log['timestamp'], errors='coerce')
    
    print("--- Event Log Schema Summary ---")
    print(f"Total Events: {len(event_log)}")
    print(f"Unique Cases: {event_log['case_id'].nunique()}")
    print(f"Unique Activities: {event_log['activity'].nunique()}")
    
    return event_log