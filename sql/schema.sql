-- SQLite Star Schema Creation Script

-- 1. dim_fund (Fund Dimension)
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_name TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    category TEXT NOT NULL,
    sub_category TEXT NOT NULL,
    risk_grade TEXT NOT NULL,
    launch_date TEXT
);

-- 2. dim_date (Date Dimension)
CREATE TABLE IF NOT EXISTS dim_date (
    date TEXT PRIMARY KEY, -- YYYY-MM-DD
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    day_of_week TEXT NOT NULL,
    is_weekend INTEGER NOT NULL -- 0 or 1
);

-- 3. fact_nav (NAV Daily Fact)
CREATE TABLE IF NOT EXISTS fact_nav (
    amfi_code INTEGER,
    date TEXT,
    nav REAL NOT NULL,
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund (amfi_code),
    FOREIGN KEY (date) REFERENCES dim_date (date)
);

-- 4. fact_transactions (Investor Transactions Fact)
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id TEXT PRIMARY KEY,
    investor_id TEXT NOT NULL,
    investor_name TEXT NOT NULL,
    state TEXT NOT NULL,
    amfi_code INTEGER,
    transaction_date TEXT,
    transaction_type TEXT NOT NULL,
    amount REAL NOT NULL,
    kyc_status TEXT NOT NULL,
    units REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund (amfi_code),
    FOREIGN KEY (transaction_date) REFERENCES dim_date (date)
);

-- 5. fact_performance (Fund Performance Fact)
CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code INTEGER PRIMARY KEY,
    return_1y REAL,
    return_3y REAL,
    return_5y REAL,
    expense_ratio REAL,
    anomaly_flag INTEGER,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund (amfi_code)
);

-- 6. fact_aum (Fund Assets Under Management Fact)
CREATE TABLE IF NOT EXISTS fact_aum (
    amfi_code INTEGER PRIMARY KEY,
    aum_amount REAL NOT NULL,
    last_updated_date TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund (amfi_code),
    FOREIGN KEY (last_updated_date) REFERENCES dim_date (date)
);
