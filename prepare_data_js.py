import pandas as pd
import json
import os

def prepare_data_js():
    print("Preparing dashboard/data.js...")
    os.makedirs('dashboard', exist_ok=True)
    
    # Read files
    df_fund = pd.read_csv('data/processed/fund_master.csv')
    df_sip = pd.read_csv('data/processed/sip_inflow_history.csv')
    df_folio = pd.read_csv('data/processed/folio_growth.csv')
    df_cat_inflow = pd.read_csv('data/processed/category_inflows.csv')
    df_perf = pd.read_csv('data/processed/scheme_performance.csv')
    df_aum_hist = pd.read_csv('data/processed/aum_history.csv')
    df_demog = pd.read_csv('data/processed/investor_demographics.csv')
    df_txn = pd.read_csv('data/processed/investor_transactions.csv')
    df_nifty = pd.read_csv('data/processed/nifty50_history.csv')
    df_nav = pd.read_csv('data/processed/nav_history.csv')
    
    # Export to dicts
    data = {
        'fundMaster': df_fund.to_dict(orient='records'),
        'sipInflows': df_sip.to_dict(orient='records'),
        'folioGrowth': df_folio.to_dict(orient='records'),
        'categoryInflows': df_cat_inflow.to_dict(orient='records'),
        'schemePerformance': df_perf.to_dict(orient='records'),
        'aumHistory': df_aum_hist.to_dict(orient='records'),
        'investorDemographics': df_demog.to_dict(orient='records'),
        'investorTransactions': df_txn.to_dict(orient='records'),
        'nifty50History': df_nifty.to_dict(orient='records'),
        'navHistory': df_nav.to_dict(orient='records')
    }
    
    # Write to data.js
    with open('dashboard/data.js', 'w', encoding='utf-8') as f:
        f.write("// Bluestock Mutual Fund Dashboard Data Store\n")
        f.write("// Generated automatically to bypass local browser CORS policy\n\n")
        for key, val in data.items():
            f.write(f"const {key}Data = {json.dumps(val, indent=2)};\n\n")
            
    print("Data preparation complete: dashboard/data.js created successfully.")

if __name__ == '__main__':
    prepare_data_js()
