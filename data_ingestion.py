import pandas as pd
import glob
import os

def load_and_explore_datasets(data_dir="data/raw"):
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    
    if not csv_files:
        print(f"No CSV datasets found in '{data_dir}'. Please place the 10 provided datasets there.")
        return {}
        
    datasets = {}
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            filename = os.path.basename(file)
            datasets[filename] = df
            
            print(f"\n{'-'*40}")
            print(f"--- Dataset: {filename} ---")
            print(f"{'-'*40}")
            print(f"Shape: {df.shape}")
            print("\nData Types:")
            print(df.dtypes)
            print("\nHead:")
            print(df.head())
            
            # Simple anomaly check: null values
            null_counts = df.isnull().sum()
            if null_counts.any():
                print("\nAnomalies Detected (Null Values):")
                print(null_counts[null_counts > 0])
            else:
                print("\nNo null values detected in initial scan.")
                
        except Exception as e:
            print(f"Error loading {file}: {e}")
            
    return datasets

def explore_fund_master(df):
    print("\n" + "="*40)
    print("=== Exploring Fund Master ===")
    print("="*40)
    
    if 'fund_house' in df.columns:
        print("\nUnique Fund Houses:", df['fund_house'].nunique())
        print(df['fund_house'].unique()[:5], "...") # Print first 5
        
    if 'category' in df.columns:
        print("\nUnique Categories:", df['category'].nunique())
        print(df['category'].unique())
        
    if 'sub_category' in df.columns:
        print("\nUnique Sub-Categories:", df['sub_category'].nunique())
        print(df['sub_category'].unique()[:5], "...")
        
    if 'risk_grade' in df.columns:
        print("\nUnique Risk Grades:")
        print(df['risk_grade'].unique())
        
    if 'scheme_code' in df.columns:
        print("\nAMFI Scheme Code Structure Note:")
        print("AMFI scheme codes are typically 6-digit numeric identifiers assigned by AMFI to uniquely identify mutual fund schemes in India.")

def validate_amfi_codes(fund_master, nav_history):
    print("\n" + "="*40)
    print("=== Validating AMFI Codes ===")
    print("="*40)
    
    if 'scheme_code' not in fund_master.columns or 'scheme_code' not in nav_history.columns:
        print("Error: 'scheme_code' column missing in one or both datasets.")
        return
        
    master_codes = set(fund_master['scheme_code'].unique())
    history_codes = set(nav_history['scheme_code'].unique())
    
    missing_in_history = master_codes - history_codes
    
    print("\n--- Data Quality Summary ---")
    print(f"Total unique scheme codes in fund_master: {len(master_codes)}")
    print(f"Total unique scheme codes in nav_history: {len(history_codes)}")
    
    if len(missing_in_history) == 0:
        print("Validation Successful: Every scheme code in fund_master exists in nav_history.")
    else:
        print(f"Validation Failed: {len(missing_in_history)} scheme codes from fund_master are missing in nav_history.")
        print("Sample missing codes:", list(missing_in_history)[:5])

if __name__ == "__main__":
    print("Starting Data Ingestion Process...")
    datasets = load_and_explore_datasets()
    
    # Try to find fund_master and nav_history by approximate names if available
    fund_master_key = next((k for k in datasets.keys() if 'fund_master' in k.lower()), None)
    nav_history_key = next((k for k in datasets.keys() if 'nav_history' in k.lower()), None)
    
    if fund_master_key:
        explore_fund_master(datasets[fund_master_key])
    else:
        print("\n'fund_master.csv' not found among loaded datasets. Skipping fund master exploration.")
        
    if fund_master_key and nav_history_key:
        validate_amfi_codes(datasets[fund_master_key], datasets[nav_history_key])
    else:
        print("\nBoth 'fund_master.csv' and 'nav_history.csv' are required for AMFI code validation. Skipping.")
