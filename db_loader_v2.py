import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine, text

def load_db():
    print("Connecting to SQLite database bluestock_mf.db...")
    engine = create_engine('sqlite:///bluestock_mf.db')
    
    # 1. Connect and run schema.sql to reset/initialize core tables
    with sqlite3.connect('bluestock_mf.db') as conn:
        print("Executing schema.sql to initialize tables...")
        with open('sql/schema.sql', 'r') as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)
        
        # Clear existing data in core tables to avoid unique constraint violations
        print("Clearing existing data in core tables...")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fact_aum")
        cursor.execute("DELETE FROM fact_performance")
        cursor.execute("DELETE FROM fact_transactions")
        cursor.execute("DELETE FROM fact_nav")
        cursor.execute("DELETE FROM dim_date")
        cursor.execute("DELETE FROM dim_fund")
        conn.commit()
        
    # 2. Load dim_fund from fund_master.csv
    print("\nLoading dim_fund...")
    df_fund = pd.read_csv('data/processed/fund_master.csv')
    df_dim_fund = df_fund[[
        'amfi_code', 'fund_name', 'fund_house', 'category', 'sub_category', 'risk_grade', 'launch_date'
    ]].copy()
    df_dim_fund.to_sql('dim_fund', con=engine, if_exists='append', index=False)
    
    # 3. Extract and load dim_date
    print("Generating and loading dim_date...")
    df_nav_dates = pd.read_csv('data/processed/nav_history.csv', usecols=['date'])
    df_txn_dates = pd.read_csv('data/processed/investor_transactions.csv', usecols=['transaction_date']).rename(columns={'transaction_date': 'date'})
    
    unique_dates = pd.concat([df_nav_dates, df_txn_dates]).drop_duplicates().dropna().reset_index(drop=True)
    unique_dates['date_dt'] = pd.to_datetime(unique_dates['date'])
    
    df_dim_date = pd.DataFrame({
        'date': unique_dates['date'],
        'day': unique_dates['date_dt'].dt.day,
        'month': unique_dates['date_dt'].dt.month,
        'year': unique_dates['date_dt'].dt.year,
        'quarter': unique_dates['date_dt'].dt.quarter,
        'day_of_week': unique_dates['date_dt'].dt.day_name(),
        'is_weekend': unique_dates['date_dt'].dt.dayofweek.apply(lambda x: 1 if x in (5,6) else 0)
    })
    
    df_dim_date.to_sql('dim_date', con=engine, if_exists='append', index=False)
    
    # 4. Load fact_nav
    print("Loading fact_nav...")
    df_nav = pd.read_csv('data/processed/nav_history.csv')
    df_nav.to_sql('fact_nav', con=engine, if_exists='append', index=False)
    
    # 5. Load fact_transactions
    print("Loading fact_transactions...")
    df_txn = pd.read_csv('data/processed/investor_transactions.csv')
    df_txn.to_sql('fact_transactions', con=engine, if_exists='append', index=False)
    
    # 6. Load fact_performance
    print("Loading fact_performance...")
    df_perf = pd.read_csv('data/processed/scheme_performance.csv')
    df_fact_perf = df_perf[[
        'amfi_code', 'return_1y', 'return_3y', 'return_5y', 'expense_ratio', 'anomaly_flag'
    ]].copy()
    df_fact_perf.to_sql('fact_performance', con=engine, if_exists='append', index=False)
    
    # 7. Load fact_aum
    print("Loading fact_aum...")
    max_nav_date = df_nav['date'].max()
    df_aum = pd.DataFrame()
    df_aum['amfi_code'] = df_fund['amfi_code']
    df_aum['aum_amount'] = df_fund['aum_amount_crores']
    df_aum['last_updated_date'] = max_nav_date
    df_aum.to_sql('fact_aum', con=engine, if_exists='append', index=False)
    
    # 8. Load additional custom tables for analysis
    print("\nLoading additional custom analysis tables...")
    
    print("Loading fact_aum_history...")
    df_aum_hist = pd.read_csv('data/processed/aum_history.csv')
    df_aum_hist.to_sql('fact_aum_history', con=engine, if_exists='replace', index=False)
    
    print("Loading fact_sip_inflows...")
    df_sip = pd.read_csv('data/processed/sip_inflow_history.csv')
    df_sip.to_sql('fact_sip_inflows', con=engine, if_exists='replace', index=False)
    
    print("Loading fact_category_inflows...")
    df_cat_inflow = pd.read_csv('data/processed/category_inflows.csv')
    df_cat_inflow.to_sql('fact_category_inflows', con=engine, if_exists='replace', index=False)
    
    print("Loading dim_investor_demographics...")
    df_demog = pd.read_csv('data/processed/investor_demographics.csv')
    df_demog.to_sql('dim_investor_demographics', con=engine, if_exists='replace', index=False)
    
    print("Loading fact_folio_growth...")
    df_folios = pd.read_csv('data/processed/folio_growth.csv')
    df_folios.to_sql('fact_folio_growth', con=engine, if_exists='replace', index=False)
    
    print("Loading fact_portfolio_holdings...")
    df_holdings = pd.read_csv('data/processed/portfolio_holdings.csv')
    df_holdings.to_sql('fact_portfolio_holdings', con=engine, if_exists='replace', index=False)
    
    print("\nData loading complete!")
    print("="*50)
    print("VERIFICATION OF ROW COUNTS")
    print("="*50)
    
    # Verify counts
    with engine.connect() as conn:
        tables = [
            'dim_fund', 'dim_date', 'fact_nav', 'fact_transactions', 
            'fact_performance', 'fact_aum', 'fact_aum_history', 
            'fact_sip_inflows', 'fact_category_inflows', 
            'dim_investor_demographics', 'fact_folio_growth', 'fact_portfolio_holdings'
        ]
        
        for table in tables:
            res = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            db_count = res.scalar()
            print(f"Table: {table:<28} | DB Rows: {db_count:<8}")
            
if __name__ == "__main__":
    load_db()
