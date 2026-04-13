import pandas as pd
import os

# Point to the file we just downloaded
LOCAL_FILE = "tmp/housing_data_raw.csv"

def profile_raw_data():
    if not os.path.exists(LOCAL_FILE):
        print("File not found! Run fetch_data.py first.")
        return

    # Updated logic to handle encoding AND inconsistent row lengths
    try:
        # We add on_bad_lines='skip' so it doesn't crash on metadata rows
        df = pd.read_csv(
            LOCAL_FILE, 
            encoding='ISO-8859-1', 
            on_bad_lines='skip',
            engine='python'
        )
    except Exception as e:
        print(f"Failed to read file: {e}")
        return

    print("--- DATA PROFILE REPORT ---")
    print(f"Total Rows: {len(df)}")
    print(f"Total Columns: {len(df.columns)}")
    
    
    print("\n--- Column Names ---")
    print(df.columns.tolist())

    print("\n--- Missing Values ---")
    print(df.isnull().sum())

    print("\n--- Data Preview (Top 5) ---")
    print(df.head())

if __name__ == "__main__":
    profile_raw_data()