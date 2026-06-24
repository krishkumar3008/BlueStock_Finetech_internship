import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine, text

def load_db():
    print("Connecting to SQLite database bluestock_mf.db...")
    # Using SQLAlchemy engine
    engine = create_engine('sqlite:///bluestock_mf.db')
    
    # Connect and run schema.sql
    with sqlite3.connect('bluestock_mf.db') as conn:
        print("Executing schema.sql to initialize tables...")
        with open('sql/schema.sql', 'r') as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)
    
    # 1. Load dim_fund from fund_master.csv
    print("\nLoading dim_fund...")
    df_fund = pd.read_csv('data/processed/fund_master.csv')
    df_dim_fund = df_fund[[
        'amfi_code', 'fund_name', 'fund_house', 'category', 'sub_category', 'risk_grade', 'launch_date'
    ]].copy()
    
    df_dim_fund.to_sql('dim_fund', con=engine, if_exists='append', index=False)
    
    # 2. Extract and load dim_date
    print("Generating and loading dim_date...")
    # Collect unique dates from nav_history and transactions
    df_nav_dates = pd.read_csv('data/processed/nav_history.csv', usecols=['date'])
    df_txn_dates = pd.read_csv('data/processed/investor_transactions.csv', usecols=['transaction_date']).rename(columns={'transaction_date': 'date'})
    
    unique_dates = pd.concat([df_nav_dates, df_txn_dates]).drop_duplicates().dropna()
    unique_dates['date_dt'] = pd.to_datetime(unique_dates['date'])
    
    df_dim_date = pd.DataFrame()
    df_dim_date['date'] = unique_dates['date']
    df_dim_date['day'] = unique_dates['date_dt'].dt.day
    df_dim_date['month'] = unique_dates['date_dt'].dt.month
    df_dim_date['year'] = unique_dates['date_dt'].dt.year
    df_dim_date['quarter'] = unique_dates['date_dt'].dt.quarter
    df_dim_date['day_of_week'] = unique_dates['date_dt'].dt.day_name()
    df_dim_date['is_weekend'] = unique_dates['date_dt'].dt.dayofweek.apply(lambda x: 1 if x in (5,6) else 0)
    
    df_dim_date.to_sql('dim_date', con=engine, if_exists='append', index=False)
    
    # 3. Load fact_nav
    print("Loading fact_nav...")
    df_nav = pd.read_csv('data/processed/nav_history.csv')
    df_nav.to_sql('fact_nav', con=engine, if_exists='append', index=False)
    
    # 4. Load fact_transactions
    print("Loading fact_transactions...")
    df_txn = pd.read_csv('data/processed/investor_transactions.csv')
    df_txn.to_sql('fact_transactions', con=engine, if_exists='append', index=False)
    
    # 5. Load fact_performance
    print("Loading fact_performance...")
    df_perf = pd.read_csv('data/processed/scheme_performance.csv')
    df_fact_perf = df_perf[[
        'amfi_code', 'return_1y', 'return_3y', 'return_5y', 'expense_ratio', 'anomaly_flag'
    ]].copy()
    df_fact_perf.to_sql('fact_performance', con=engine, if_exists='append', index=False)
    
    # 6. Load fact_aum
    print("Loading fact_aum...")
    # Get AUM from fund_master
    max_nav_date = df_nav['date'].max() # Use the latest date in NAV history as last updated date for AUM
    df_aum = pd.DataFrame()
    df_aum['amfi_code'] = df_fund['amfi_code']
    df_aum['aum_amount'] = df_fund['aum_amount_crores']
    df_aum['last_updated_date'] = max_nav_date
    
    df_aum.to_sql('fact_aum', con=engine, if_exists='append', index=False)
    
    print("\nData loading complete!")
    print("="*50)
    print("VERIFICATION OF ROW COUNTS")
    print("="*50)
    
    # Verify counts
    with engine.connect() as conn:
        tables = ['dim_fund', 'dim_date', 'fact_nav', 'fact_transactions', 'fact_performance', 'fact_aum']
        csv_counts = {
            'dim_fund': len(df_dim_fund),
            'dim_date': len(df_dim_date),
            'fact_nav': len(df_nav),
            'fact_transactions': len(df_txn),
            'fact_performance': len(df_fact_perf),
            'fact_aum': len(df_aum)
        }
        
        mismatches = 0
        for table in tables:
            res = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            db_count = res.scalar()
            csv_count = csv_counts[table]
            print(f"Table: {table:<20} | CSV Rows: {csv_count:<8} | DB Rows: {db_count:<8}")
            if csv_count != db_count:
                mismatches += 1
                
        if mismatches == 0:
            print("\nVerification SUCCESSFUL: All row counts match exactly!")
        else:
            print(f"\nVerification FAILED: Found {mismatches} mismatching tables.")

if __name__ == "__main__":
    load_db()
