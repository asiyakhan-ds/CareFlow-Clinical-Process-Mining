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