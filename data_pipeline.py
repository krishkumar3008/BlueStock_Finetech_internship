import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
import os
import glob
import re

# Ensure directory structure exists
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

# ----------------------------------------------------
# 1. SYNTHESIS OF RAW DATASETS
# ----------------------------------------------------
print("Starting Data Synthesis...")

# A. Synthesize fund_master.csv
fund_master_data = {
    'amfi_code': [118632, 119092, 119551, 120503, 120841, 125497],
    'fund_name': [
        'Nippon India Large Cap Fund',
        'Axis Bluechip Fund',
        'SBI Bluechip Fund',
        'ICICI Prudential Bluechip Fund',
        'Kotak Bluechip Fund',
        'HDFC Top 100 Fund'
    ],
    'fund_house': [
        'Nippon India Mutual Fund',
        'Axis Mutual Fund',
        'SBI Mutual Fund',
        'ICICI Prudential Mutual Fund',
        'Kotak Mahindra Mutual Fund',
        'HDFC Mutual Fund'
    ],
    'category': ['Equity', 'Equity', 'Equity', 'Equity', 'Equity', 'Equity'],
    'sub_category': ['Large Cap', 'Large Cap', 'Large Cap', 'Large Cap', 'Large Cap', 'Large Cap'],
    'risk_grade': ['Very High', 'Very High', 'Very High', 'Very High', 'Very High', 'Very High'],
    'launch_date': ['2013-01-07', '2013-01-05', '2006-02-14', '2008-05-23', '2013-01-01', '2013-01-01'],
    'aum_amount_crores': [25000.50, 32000.75, 41000.20, 48000.60, 7200.45, 30000.30]
}
df_fund_master_raw = pd.DataFrame(fund_master_data)
df_fund_master_raw.to_csv('data/raw/fund_master.csv', index=False)
print("Saved raw fund_master.csv")

# B. Synthesize investor_transactions.csv
np.random.seed(42)
num_txns = 500

states = ['Maharashtra', 'Karnataka', 'Delhi', 'Tamil Nadu', 'Uttar Pradesh', 'Gujarat', 'West Bengal', 'Telangana', 'Haryana', 'Bihar']
investors = [
    ('INV101', 'Aarav Sharma', 'Maharashtra'),
    ('INV102', 'Vihaan Patel', 'Gujarat'),
    ('INV103', 'Aditya Reddy', 'Telangana'),
    ('INV104', 'Sai Krishna', 'Tamil Nadu'),
    ('INV105', 'Arjun Nair', 'Karnataka'),
    ('INV106', 'Diya Sen', 'West Bengal'),
    ('INV107', 'Ananya Gupta', 'Delhi'),
    ('INV108', 'Rahul Verma', 'Uttar Pradesh'),
    ('INV109', 'Ishaan Mishra', 'Bihar'),
    ('INV110', 'Meera Rao', 'Karnataka'),
    ('INV111', 'Kabir Malhotra', 'Haryana'),
    ('INV112', 'Rohan Das', 'West Bengal'),
    ('INV113', 'Neha Joshi', 'Maharashtra'),
    ('INV114', 'Karan Mehta', 'Gujarat'),
    ('INV115', 'Tanvi Bhat', 'Karnataka'),
    ('INV116', 'Yash Singhal', 'Delhi'),
    ('INV117', 'Pranav Kumar', 'Bihar'),
    ('INV118', 'Aanya Saxena', 'Uttar Pradesh'),
    ('INV119', 'Rithvik Choudhury', 'Telangana'),
    ('INV120', 'Aditi Pillai', 'Tamil Nadu')
]

amfi_codes = [118632, 119092, 119551, 120503, 120841, 125497]

# Messy date formats
date_formats = [
    lambda d: d.strftime('%Y-%m-%d'),
    lambda d: d.strftime('%d-%m-%Y'),
    lambda d: d.strftime('%d/%m/%Y'),
    lambda d: d.strftime('%Y/%m/%d')
]

# Messy transaction types
txn_types = ['SIP', 'sip', 'Sip', 'Lumpsum', 'lumpsum', 'LUMP_SUM', 'Redemption', 'redemption', 'Redeem']

# Messy KYC values
kyc_values = ['Y', 'N', 'Yes', 'No', 'Pending', 'Verified', 'FAILED', 'Done', 'verified', 'pending', 'failed']

txn_records = []
start_date = pd.to_datetime('2024-01-01')
end_date = pd.to_datetime('2026-06-15')
date_range = pd.date_range(start_date, end_date)

for i in range(num_txns):
    txn_id = f"TXN{10000 + i}"
    inv = investors[np.random.randint(len(investors))]
    inv_id, inv_name, state = inv
    amfi = int(np.random.choice(amfi_codes))
    
    dt = pd.Timestamp(np.random.choice(date_range))
    # Apply random date format
    dt_str = date_formats[np.random.randint(len(date_formats))](dt)
    
    txn_type = np.random.choice(txn_types)
    
    # Amount with anomalies (0, negative, null, normal)
    rand_val = np.random.rand()
    if rand_val < 0.02:
        amount = 0
    elif rand_val < 0.04:
        amount = -5000.0
    elif rand_val < 0.06:
        amount = np.nan
    else:
        amount = round(float(np.random.uniform(500.0, 100000.0)), 2)
        
    kyc = np.random.choice(kyc_values)
    
    txn_records.append({
        'transaction_id': txn_id,
        'investor_id': inv_id,
        'investor_name': inv_name,
        'state': state,
        'amfi_code': amfi,
        'transaction_date': dt_str,
        'transaction_type': txn_type,
        'amount': amount,
        'kyc_status': kyc
    })

df_txn_raw = pd.DataFrame(txn_records)
df_txn_raw.to_csv('data/raw/investor_transactions.csv', index=False)
print("Saved raw investor_transactions.csv")

# C. Synthesize scheme_performance.csv
# Introduce some string return values, N/As, high return anomalies, and expense ratios out of bounds.
scheme_performance_data = {
    'amfi_code': [118632, 119092, 119551, 120503, 120841, 125497],
    'scheme_name': [
        'Nippon India Large Cap Fund',
        'Axis Bluechip Fund',
        'SBI Bluechip Fund',
        'ICICI Prudential Bluechip Fund',
        'Kotak Bluechip Fund',
        'HDFC Top 100 Fund'
    ],
    'return_1y': ['18.5%', '12.3%', 'N/A', '16.8%', '14.2%', '135.0%'], # 135% return is an anomaly, N/A is text
    'return_3y': [15.2, 11.8, 14.5, 15.6, '13.9%', 12.4],
    'return_5y': [14.1, 10.9, 13.2, 14.8, 12.5, 11.7],
    'expense_ratio': ['0.85%', '2.10%', '0.05%', '1.45%', '3.10%', '1.20%'] # 0.05% and 3.10% are out of range [0.1%, 2.5%]
}
df_perf_raw = pd.DataFrame(scheme_performance_data)
df_perf_raw.to_csv('data/raw/scheme_performance.csv', index=False)
print("Saved raw scheme_performance.csv")

# D. Merge raw schemes to raw nav_history.csv
raw_files = [f for f in glob.glob("data/raw/*.csv") if os.path.basename(f).split('_')[0].isdigit()]
print(f"Merging {len(raw_files)} scheme NAV files into raw nav_history.csv...")
merged_nav = []
for file in raw_files:
    filename = os.path.basename(file)
    # Extract amfi_code from filename prefix
    amfi_code = int(filename.split('_')[0])
    df = pd.read_csv(file)
    df['amfi_code'] = amfi_code
    merged_nav.append(df)

df_nav_raw = pd.concat(merged_nav, ignore_index=True)
# Add some duplicate rows to test duplicate cleaning
df_nav_raw = pd.concat([df_nav_raw, df_nav_raw.head(20)], ignore_index=True)
df_nav_raw.to_csv('data/raw/nav_history.csv', index=False)
print("Saved raw nav_history.csv")


# ----------------------------------------------------
# 2. DATA CLEANING PIPELINE
# ----------------------------------------------------
print("\nStarting Cleaning Pipeline...")

# A. Clean nav_history.csv and individual NAV files
print("\n--- Cleaning NAV History ---")
df_nav = pd.read_csv('data/raw/nav_history.csv')

# Parse dates using dayfirst=True since format is DD-MM-YYYY
df_nav['date'] = pd.to_datetime(df_nav['date'], dayfirst=True)

# Validate NAV > 0
df_nav = df_nav[df_nav['nav'] > 0]

# Remove duplicates
before_dedup = len(df_nav)
df_nav = df_nav.drop_duplicates(subset=['amfi_code', 'date'])
print(f"Removed {before_dedup - len(df_nav)} duplicate NAV rows")

# Forward-fill missing NAV for holidays/weekends
# To do this correctly, we will group by amfi_code, create a daily date range, reindex, and ffill
cleaned_nav_dfs = []
for amfi_code, group in df_nav.groupby('amfi_code'):
    group = group.sort_values('date')
    min_date = group['date'].min()
    max_date = group['date'].max()
    all_dates = pd.date_range(start=min_date, end=max_date, freq='D')
    
    # Set date as index to reindex
    group = group.set_index('date')
    group_reindexed = group.reindex(all_dates)
    group_reindexed['amfi_code'] = amfi_code
    group_reindexed['nav'] = group_reindexed['nav'].ffill()
    
    # Reset index and rename date column
    group_reindexed = group_reindexed.reset_index().rename(columns={'index': 'date'})
    cleaned_nav_dfs.append(group_reindexed)

df_nav_cleaned = pd.concat(cleaned_nav_dfs, ignore_index=True)

# Sort by amfi_code + date
df_nav_cleaned = df_nav_cleaned.sort_values(by=['amfi_code', 'date']).reset_index(drop=True)

# Convert date to standard YYYY-MM-DD string format
df_nav_cleaned['date'] = df_nav_cleaned['date'].dt.strftime('%Y-%m-%d')

# Save main cleaned nav_history.csv
df_nav_cleaned.to_csv('data/processed/nav_history.csv', index=False)
print(f"Saved cleaned nav_history.csv. Shape: {df_nav_cleaned.shape}")

# Save individual cleaned scheme CSV files (6 of them)
fund_names_map = df_fund_master_raw.set_index('amfi_code')['fund_name'].to_dict()
for amfi_code, group in df_nav_cleaned.groupby('amfi_code'):
    clean_name = fund_names_map[amfi_code].replace(' ', '_')
    filename = f"data/processed/{amfi_code}_{clean_name}.csv"
    # Keep only date and nav columns for individual files
    df_scheme_nav = group[['date', 'nav']].copy()
    df_scheme_nav.to_csv(filename, index=False)
    print(f"Saved cleaned individual file: {filename}. Rows: {len(group)}")


# B. Clean investor_transactions.csv
print("\n--- Cleaning Investor Transactions ---")
df_txn = pd.read_csv('data/raw/investor_transactions.csv')

# Clean date formats
def parse_messy_date(val):
    if pd.isna(val):
        return pd.NaT
    val = str(val).strip()
    # Try different formats
    for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d'):
        try:
            return pd.to_datetime(val, format=fmt)
        except ValueError:
            continue
    # Fallback to dateutil/pandas general parser
    try:
        return pd.to_datetime(val)
    except:
        return pd.NaT

df_txn['transaction_date'] = df_txn['transaction_date'].apply(parse_messy_date)

# Drop rows with invalid dates
null_dates_count = df_txn['transaction_date'].isna().sum()
if null_dates_count > 0:
    print(f"Dropping {null_dates_count} transactions with invalid dates")
    df_txn = df_txn.dropna(subset=['transaction_date'])

# Standardise date to YYYY-MM-DD
df_txn['transaction_date_str'] = df_txn['transaction_date'].dt.strftime('%Y-%m-%d')

# Standardise transaction_type
def standardise_txn_type(val):
    if pd.isna(val):
        return 'Lumpsum' # Default fallback
    val = str(val).strip().lower().replace('_', '')
    if 'sip' in val:
        return 'SIP'
    elif 'redemption' in val or 'redeem' in val:
        return 'Redemption'
    else:
        return 'Lumpsum'

df_txn['transaction_type'] = df_txn['transaction_type'].apply(standardise_txn_type)

# Validate amount > 0
before_amount_filter = len(df_txn)
df_txn = df_txn.dropna(subset=['amount'])
df_txn = df_txn[df_txn['amount'] > 0]
dropped_amount = before_amount_filter - len(df_txn)
print(f"Dropped {dropped_amount} transaction rows due to invalid amount (<= 0 or null)")

# Check and standardise KYC status enum values (Verified, Pending, Failed)
def standardise_kyc(val):
    if pd.isna(val):
        return 'Pending'
    val = str(val).strip().lower()
    if val in ('y', 'yes', 'verified', 'done'):
        return 'Verified'
    elif val in ('n', 'no', 'failed'):
        return 'Failed'
    else:
        return 'Pending'

df_txn['kyc_status'] = df_txn['kyc_status'].apply(standardise_kyc)

# Calculate units based on NAV on transaction_date
# We need to map amfi_code and transaction_date to the nav_history.csv
nav_dict = df_nav_cleaned.set_index(['amfi_code', 'date'])['nav'].to_dict()

def calculate_units(row):
    amfi = int(row['amfi_code'])
    dt_str = row['transaction_date_str']
    nav = nav_dict.get((amfi, dt_str))
    if nav is not None and nav > 0:
        return round(row['amount'] / nav, 4)
    else:
        return np.nan

df_txn['units'] = df_txn.apply(calculate_units, axis=1)

# Drop transaction_date intermediate columns and rename transaction_date_str
df_txn = df_txn.drop(columns=['transaction_date'])
df_txn = df_txn.rename(columns={'transaction_date_str': 'transaction_date'})

# Save cleaned investor_transactions.csv
df_txn.to_csv('data/processed/investor_transactions.csv', index=False)
print(f"Saved cleaned investor_transactions.csv. Shape: {df_txn.shape}")


# C. Clean scheme_performance.csv
print("\n--- Cleaning Scheme Performance ---")
df_perf = pd.read_csv('data/raw/scheme_performance.csv')

# Clean return values and convert to numeric
def clean_return(val):
    if pd.isna(val):
        return np.nan
    val_str = str(val).strip().replace('%', '')
    if val_str.lower() in ('n/a', 'na', 'null', ''):
        return np.nan
    try:
        return float(val_str)
    except ValueError:
        return np.nan

for col in ('return_1y', 'return_3y', 'return_5y'):
    df_perf[col] = df_perf[col].apply(clean_return)

# Flag return anomalies (e.g. return > 100% or < -50% in return_1y)
df_perf['anomaly_flag'] = 0
df_perf.loc[(df_perf['return_1y'] > 100.0) | (df_perf['return_1y'] < -50.0), 'anomaly_flag'] = 1
df_perf.loc[df_perf['return_1y'].isna() | df_perf['return_3y'].isna() | df_perf['return_5y'].isna(), 'anomaly_flag'] = 1

anomalies = df_perf[df_perf['anomaly_flag'] == 1]
print(f"Flagged {len(anomalies)} performance anomalies:")
for idx, row in anomalies.iterrows():
    print(f"  - Fund: {row['scheme_name']} (1y return: {row['return_1y']}%)")

# Clean and check expense_ratio range (0.1% – 2.5%)
def clean_expense_ratio(val):
    if pd.isna(val):
        return np.nan
    val_str = str(val).strip().replace('%', '')
    try:
        return float(val_str)
    except ValueError:
        return np.nan

df_perf['expense_ratio'] = df_perf['expense_ratio'].apply(clean_expense_ratio)

# Check range and print warning/flag
out_of_range_er = df_perf[(df_perf['expense_ratio'] < 0.1) | (df_perf['expense_ratio'] > 2.5)]
if not out_of_range_er.empty:
    print(f"Found {len(out_of_range_er)} funds with expense ratio out of range (0.1% - 2.5%):")
    for idx, row in out_of_range_er.iterrows():
        print(f"  - Fund: {row['scheme_name']} (Expense Ratio: {row['expense_ratio']}%)")

# Save cleaned scheme_performance.csv
df_perf.to_csv('data/processed/scheme_performance.csv', index=False)
print(f"Saved cleaned scheme_performance.csv. Shape: {df_perf.shape}")


# D. Clean fund_master.csv
print("\n--- Cleaning Fund Master ---")
df_master = pd.read_csv('data/raw/fund_master.csv')
# fund_master is already clean from synthesis, but we ensure proper types
df_master['amfi_code'] = df_master['amfi_code'].astype(int)
df_master['launch_date'] = pd.to_datetime(df_master['launch_date']).dt.strftime('%Y-%m-%d')
df_master.to_csv('data/processed/fund_master.csv', index=False)
print("Saved cleaned fund_master.csv")

print("\nAll datasets cleaned successfully!")
# List files in data/processed
processed_files = glob.glob("data/processed/*.csv")
print(f"Total processed files generated: {len(processed_files)}")
for file in processed_files:
    print(f"  - {os.path.basename(file)}")
