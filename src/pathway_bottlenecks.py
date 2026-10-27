import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def load_and_prepare_data(filepath):
    """Load clinical event log data and sort by case and timestamp."""
    df = pd.read_csv(filepath)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values(by=['Case_ID', 'Timestamp'])
    return df

def calculate_transition_delays(df):
    """Calculate waiting time between consecutive clinical activities per patient."""
    df['next_activity'] = df.groupby('Case_ID')['Activity'].shift(-1)
    df['next_timestamp'] = df.groupby('Case_ID')['Timestamp'].shift(-1)
    
    # Calculate transition delay in minutes
    df['delay_minutes'] = (df['next_timestamp'] - df['Timestamp']).dt.total_seconds() / 60.0
    
    # Create transition label
    df['transition'] = df['Activity'] + ' -> ' + df['next_activity']
    
    # Filter valid transitions
    transitions_df = df.dropna(subset=['next_activity', 'delay_minutes'])
    return transitions_df

def summarize_bottlenecks(transitions_df):
    """Aggregate average delay and count per clinical transition."""
    summary = transitions_df.groupby('transition').agg(
        avg_delay_min=('delay_minutes', 'mean'),
        median_delay_min=('delay_minutes', 'median'),
        total_occurrences=('delay_minutes', 'count')
    ).reset_index()
    
    summary = summary.sort_values(by='avg_delay_min', ascending=False)
    return summary

def plot_bottlenecks(summary_df, output_path='reports/bottleneck_analysis.png'):
    """Generate and save a bar chart of top clinical pathway bottlenecks."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    top_transitions = summary_df.head(10)
    
    plt.barh(top_transitions['transition'], top_transitions['avg_delay_min'], color='#1f77b4')
    plt.xlabel('Average Delay (Minutes)')
    plt.ylabel('Clinical Activity Transition')
    plt.title('Top 10 Clinical Pathway Bottlenecks (Average Waiting Time)')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300)
    print(f"Bottleneck plot successfully saved to {output_path}")

if __name__ == "__main__":
    data_path = "data/raw/careflow_clinical_data.csv"
    
    if os.path.exists(data_path):
        print("Processing clinical event log for bottleneck analysis...")
        df = load_and_prepare_data(data_path)
        transitions = calculate_transition_delays(df)
        bottleneck_summary = summarize_bottlenecks(transitions)
        
        print("\n--- Top Bottlenecks Identified ---")
        print(bottleneck_summary.head(10).to_string(index=False))
        
        plot_bottlenecks(bottleneck_summary)
    else:
        print(f"Data file not found at {data_path}. Please check the file path.")

        
# CareFlow Pathway Bottleneck Analysis Module
# Calculates transition delays between clinical steps and identifies high-latency 
# pathways to assist healthcare operations in resource allocation and workflow optimization.
# Updated for daily process verification.