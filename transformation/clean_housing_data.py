import pandas as pd
import os
import sys
from dotenv import load_dotenv

# 1. Load the credentials from your .env file
load_dotenv()

# 2. Add the project root to sys.path so it can find 'utils'
sys.path.append(os.getcwd())
from utils.s3_tools import upload_to_s3


RAW_FILE = "tmp/housing_data_raw.csv"
SILVER_FILE = "tmp/housing_data_silver.csv"

def transform_to_silver():
    print("--- Starting Silver Transformation ---")
    
    # 1. Load with the encoding we discovered
    df = pd.read_csv(RAW_FILE, encoding='ISO-8859-1', low_memory=False)

    # 2. Drop completely empty columns
    cols_to_drop = ['Series_title_3', 'Series_title_4', 'Series_title_5']
    df = df.drop(columns=cols_to_drop)

    # 3. Clean Missing Data
    # Remove rows where Data_value is null
    df = df.dropna(subset=['Data_value'])

    # 4. Date Transformation (The 'Period' fix)
    # We turn 2025.12 into 2025-12-01
    df['Period'] = df['Period'].astype(str).str.replace(r'\.', '-', regex=True)
    df['Period'] = df['Period'] + "-01"
    
    # 5. Filter for Housing/Construction only
    # Let's see what's in 'Group' to narrow it down later
    # For now, we'll just keep everything that isn't empty
    
    print(f"Cleaning complete. Rows remaining: {len(df)}")
    
    # Save the 'Silver' version locally
    df.to_csv(SILVER_FILE, index=False)
    print(f"Silver file saved to {SILVER_FILE}")

if __name__ == "__main__":
    transform_to_silver()
    # NEW: Upload the cleaned data to the Silver zone
    upload_to_s3(
        local_file="tmp/housing_data_silver.csv", 
        bucket="powerbi.pjt", 
        folder="silver/stats_nz"
    )