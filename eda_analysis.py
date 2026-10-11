print("Starting Exploratory Data Analysi...")
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

if __name__ == "__main__":
    # Load dataset
    data_path = "data/raw_data.csv"
    df = load_data(data_path)