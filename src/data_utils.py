import pandas as pd
import os
import sys

# Ensure src directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import RAW_DATA_PATH

def load_and_clean_data(filepath):
    """
    Loads raw survey data and cleans it by standardizing column names
    and dropping missing values/duplicates.
    
    Args:
        filepath (str): Path to the raw CSV file.
        
    Returns:
        pd.DataFrame: A clean pandas DataFrame.
    """
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Clean data operations
    initial_shape = df.shape
    df_clean = df.dropna().drop_duplicates()
    final_shape = df_clean.shape
    
    print(f"Data cleaned! Rows dropped: {initial_shape[0] - final_shape[0]}")
    return df_clean

if __name__ == "__main__":
    # Test the function if script is run directly
    df = load_and_clean_data(RAW_DATA_PATH)
    print("Clean Data Sample:")
    print(df.head())
