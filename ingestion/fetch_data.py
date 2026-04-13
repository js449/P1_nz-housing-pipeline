import os
import requests
import boto3
import zipfile  
import io
from dotenv import load_dotenv
from datetime import datetime

# 1. Load the handshake credentials
load_dotenv()

# 2. Configuration and Constants
DATA_URL = "https://www.stats.govt.nz/assets/Uploads/Business-price-indexes/Business-price-indexes-December-2025-quarter/Download-data/business-price-indexes-december-2025-quarter.zip"
S3_BUCKET = "powerbi.pjt" 
LOCAL_FILE = "tmp/housing_data_raw.csv"

# 3. Functions to handle downloading, unzipping, and uploading to S3 
def download_from_stats_nz():
    """Downloads the ZIP from Stats NZ, unzips it, and saves the CSV to a local tmp folder."""
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
        
    print(f"--- Starting Download from Stats NZ ---")
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(DATA_URL, headers=headers)
    
    if response.status_code == 200:
        try:
            # treat the response as a ZIP file in memory
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                # Find the first CSV inside the ZIP
                csv_files = [f for f in z.namelist() if f.endswith('.csv')]
                
                if not csv_files:
                    print("No CSV file found inside the ZIP.")
                    return False
                
                # Extract the first CSV found and save it as LOCAL_FILE
                with z.open(csv_files[0]) as source, open(LOCAL_FILE, 'wb') as target:
                    target.write(source.read())
            
            print(f"Successfully unzipped and saved to {LOCAL_FILE}")
            return True
            
        except zipfile.BadZipFile:
            print("Error: The downloaded file is not a valid ZIP file.")
            return False
    else:
        print(f"Failed to download. Status: {response.status_code}")
        return False

def upload_to_s3_raw():
    """Uploads the local file to the 'raw' zone in S3."""
    # create a 'prefix' (folder) using the current date
    # standard practice to track history
    date_str = datetime.now().strftime("%Y-%m-%d")
    s3_path = f"raw/stats_nz/load_date={date_str}/housing_data.csv"
    
    s3 = boto3.client('s3')
    
    try:
        print(f"--- Uploading to S3 Bucket: {S3_BUCKET} ---")
        s3.upload_file(LOCAL_FILE, S3_BUCKET, s3_path)
        print(f"Successfully uploaded to: {s3_path}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

if __name__ == "__main__":
    if download_from_stats_nz():
        upload_to_s3_raw()