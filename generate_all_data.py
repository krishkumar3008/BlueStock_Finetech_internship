import os
import pandas as pd
import numpy as np
import datetime

# Setup directories
os.makedirs('data/processed', exist_ok=True)
os.makedirs('reports/charts', exist_ok=True)

print("Starting generation of 40 schemes and historical data...")

# Set random seed for reproducibility
np.random.seed(42)

# ----------------------------------------------------
# 1. Scheme Metadata (40 Schemes)
# ----------------------------------------------------
fund_houses = [
    "SBI Mutual Fund", "HDFC Mutual Fund", "ICICI Prudential Mutual Fund",
    "Nippon India Mutual Fund", "Kotak Mahindra Mutual Fund", "Axis Mutual Fund",
    "UTI Mutual Fund", "Aditya Birla Sun Life Mutual Fund"
]

categories_info = {
    "Equity": {
        "sub_categories": ["Large Cap", "Mid Cap", "Small Cap", "Flexi Cap"],
        "risks": ["Very High", "High"],
        "percentage": 0.50 # 20 schemes
    },
    "Debt": {
        "sub_categories": ["Liquid", "Gilt", "Corporate Bond"],
        "risks": ["Low", "Low to Moderate", "Moderate"],
        "percentage": 0.25 # 10 schemes
    },
    "Hybrid": {
        "sub_categories": ["Balanced Advantage", "Aggressive Hybrid"],
        "risks": ["Moderately High", "High"],
        "percentage": 0.15 # 6 schemes
    },
    "Solution Oriented": {
        "sub_categories": ["Retirement Fund", "Childrens Fund"],
        "risks": ["Moderately High", "High"],
        "percentage": 0.05 # 2 schemes
    },
    "ETF/Others": {
        "sub_categories": ["Nifty 50 ETF", "Gold ETF"],
        "risks": ["Very High", "High"],
        "percentage": 0.05 # 2 schemes
    }
}

# Generate 40 schemes
schemes_list = []
scheme_counter = 0

for cat, info in categories_info.items():
    num_schemes = int(40 * info["percentage"])
    for i in range(num_schemes):
        amfi_code = 100001 + scheme_counter
        fh = fund_houses[scheme_counter % len(fund_houses)]
        sub_cat = info["sub_categories"][i % len(info["sub_categories"])]
        risk = info["risks"][i % len(info["risks"])]
        
        # Unique names using AMFI code to avoid duplicate pivot indices
        name_prefix = fh.replace(' Mutual Fund', '')
        if scheme_counter % 2 == 1:
            base_name = f"{name_prefix} {sub_cat} Fund - Direct Growth ({amfi_code})"
        else:
            base_name = f"{name_prefix} {sub_cat} Fund - Regular Growth ({amfi_code})"
            
        launch_yr = np.random.randint(2010, 2021)
        launch_mo = np.random.randint(1, 13)
        launch_day = np.random.randint(1, 28)
        launch_date = f"{launch_yr}-{launch_mo:02d}-{launch_day:02d}"
        
        # 2025 AUM
        if fh == "SBI Mutual Fund":
            aum = round(np.random.uniform(50000, 150000), 2)
        else:
            aum = round(np.random.uniform(5000, 45000), 2)
            
        schemes_list.append({
            "amfi_code": amfi_code,
            "fund_name": base_name,
            "fund_house": fh,
            "category": cat,
            "sub_category": sub_cat,
            "risk_grade": risk,
            "launch_date": launch_date,
            "aum_amount_crores": aum
        })
        scheme_counter += 1

df_fund_master = pd.DataFrame(schemes_list)
df_fund_master.to_csv('data/processed/fund_master.csv', index=False)
print(f"Generated {len(df_fund_master)} schemes in fund_master.csv")

# ----------------------------------------------------
# 2. Daily NAV History (2022–2026) for 40 schemes
# ----------------------------------------------------
print("Generating NAV history with 2023 Bull Run and 2024 Corrections...")
start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2026, 6, 15)
date_range = pd.date_range(start_date, end_date)

# Base NAV for each scheme
base_navs = {row["amfi_code"]: np.random.uniform(10.0, 350.0) for idx, row in df_fund_master.iterrows()}
cat_map = df_fund_master.set_index("amfi_code")["category"].to_dict()

nav_rows = []

# Generate daily returns with specific trends
# 2022: Volatile/Flat (-2% to +2% avg)
# 2023: Bull Run (+25% to +35% avg for Equity)
# 2024: Corrections:
#       - Dip 1: Jan 15 to Feb 29 (Equity drops ~12% overall)
#       - Dip 2: June 1 to June 15 (Equity drops ~8% overall)
#       - Recovery in other months, ending slightly positive
# 2025: Smooth upward trend (+15% to +20%)
# 2026: Flat/Moderate (+5% to +10%)

daily_navs = {amfi: [base_navs[amfi]] for amfi in base_navs}

for d in date_range[1:]:
    year = d.year
    month = d.month
    day = d.day
    
    # Check if correction period
    is_correction = False
    corr_factor = 0.0
    
    if year == 2024:
        # Correction 1: Jan 15 - Feb 29
        if (month == 1 and day >= 15) or (month == 2):
            is_correction = True
            corr_factor = -0.003 # Daily drag
        # Correction 2: June 1 - June 15
        elif month == 6 and day <= 15:
            is_correction = True
            corr_factor = -0.005 # Stronger daily drag
            
    for amfi_code, navs in daily_navs.items():
        cat = cat_map[amfi_code]
        prev_nav = navs[-1]
        
        # Determine drift and volatility based on year and category
        if cat == "Equity":
            vol = 0.012
            if year == 2022:
                drift = 0.00005
            elif year == 2023:
                drift = 0.0009 # Strong bull run
            elif year == 2024:
                drift = -0.0015 if is_correction else 0.0008
            elif year == 2025:
                drift = 0.0006
            else: # 2026
                drift = 0.0003
                
        elif cat == "Debt":
            vol = 0.001
            drift = 0.0002 # Stable yield
            if is_correction:
                drift = 0.00015 # Very minor impact
                
        elif cat == "Hybrid":
            vol = 0.007
            if year == 2022:
                drift = 0.00005
            elif year == 2023:
                drift = 0.0006
            elif year == 2024:
                drift = -0.0009 if is_correction else 0.0005
            elif year == 2025:
                drift = 0.0004
            else: # 2026
                drift = 0.00025
                
        elif cat == "Solution Oriented":
            vol = 0.008
            if year == 2022:
                drift = 0.00005
            elif year == 2023:
                drift = 0.0006
            elif year == 2024:
                drift = -0.0010 if is_correction else 0.0005
            elif year == 2025:
                drift = 0.0004
            else:
                drift = 0.00025
                
        else: # ETF/Others (Nifty 50 or Gold)
            vol = 0.015
            if year == 2022:
                drift = -0.0001
            elif year == 2023:
                drift = 0.0010
            elif year == 2024:
                drift = -0.0018 if is_correction else 0.0008
            elif year == 2025:
                drift = 0.0007
            else:
                drift = 0.0003
                
        # Generate daily return
        daily_ret = np.random.normal(drift, vol)
        new_nav = max(1.0, prev_nav * (1.0 + daily_ret))
        navs.append(new_nav)

# Compile into dataframe
for idx, row in df_fund_master.iterrows():
    amfi_code = row["amfi_code"]
    navs = daily_navs[amfi_code]
    for d, nav in zip(date_range, navs):
        nav_rows.append({
            "amfi_code": amfi_code,
            "date": d.strftime('%Y-%m-%d'),
            "nav": round(nav, 4)
        })

df_nav_history = pd.DataFrame(nav_rows)
df_nav_history.to_csv('data/processed/nav_history.csv', index=False)
print(f"Generated {len(df_nav_history)} daily NAV records in nav_history.csv")

# ----------------------------------------------------
# 3. AUM Growth History (2022–2025)
# ----------------------------------------------------
print("Generating AUM history by fund house...")
aum_history_rows = []
for fh in fund_houses:
    # Set 2025 base AUM
    if fh == "SBI Mutual Fund":
        aum_2025 = 1250000.0 # Exactly 12.5L Cr
    elif fh == "HDFC Mutual Fund":
        aum_2025 = 780000.0
    elif fh == "ICICI Prudential Mutual Fund":
        aum_2025 = 820000.0
    elif fh == "Nippon India Mutual Fund":
        aum_2025 = 480000.0
    elif fh == "Kotak Mahindra Mutual Fund":
        aum_2025 = 440000.0
    elif fh == "Axis Mutual Fund":
        aum_2025 = 320000.0
    elif fh == "UTI Mutual Fund":
        aum_2025 = 300000.0
    else: # Aditya Birla Sun Life Mutual Fund
        aum_2025 = 350000.0
        
    # Scale back to 2022
    aum_2024 = aum_2025 * np.random.uniform(0.80, 0.85)
    aum_2023 = aum_2024 * np.random.uniform(0.80, 0.85)
    aum_2022 = aum_2023 * np.random.uniform(0.75, 0.82)
    
    aum_history_rows.append({"year": 2022, "fund_house": fh, "aum_amount_crores": round(aum_2022, 2)})
    aum_history_rows.append({"year": 2023, "fund_house": fh, "aum_amount_crores": round(aum_2023, 2)})
    aum_history_rows.append({"year": 2024, "fund_house": fh, "aum_amount_crores": round(aum_2024, 2)})
    aum_history_rows.append({"year": 2025, "fund_house": fh, "aum_amount_crores": round(aum_2025, 2)})

df_aum_history = pd.DataFrame(aum_history_rows)
df_aum_history.to_csv('data/processed/aum_history.csv', index=False)
print("Saved aum_history.csv")

# ----------------------------------------------------
# 4. SIP Inflows (Jan 2022 – Dec 2025)
# ----------------------------------------------------
print("Generating SIP Inflows time-series...")
months_range = pd.date_range('2022-01-01', '2025-12-01', freq='MS')
sip_inflows = []

start_sip = 11305.0 # Starting SIP
target_sip = 31002.0 # Target in Dec 2025 (48th month)

# Generate smooth growth curve
for t, m in enumerate(months_range):
    pct = t / (len(months_range) - 1)
    # Exponential growth model
    sip_val = start_sip * np.exp(np.log(target_sip / start_sip) * pct)
    # Add minor noise
    if t < len(months_range) - 1:
        sip_val += np.random.uniform(-400, 400)
    else:
        sip_val = target_sip # Ensure exactly target
        
    sip_inflows.append({
        "month": m.strftime('%Y-%m'),
        "sip_amount_crores": round(sip_val, 2)
    })

df_sip_inflows = pd.DataFrame(sip_inflows)
df_sip_inflows.to_csv('data/processed/sip_inflow_history.csv', index=False)
print("Saved sip_inflow_history.csv")

# ----------------------------------------------------
# 5. Category Inflows Heatmap Data (2022–2025)
# ----------------------------------------------------
print("Generating Category Inflows...")
category_inflows_rows = []
categories = ["Equity", "Debt", "Hybrid", "Solution Oriented", "Others"]

for m in months_range:
    m_str = m.strftime('%Y-%m')
    for cat in categories:
        if cat == "Equity":
            # Higher inflows during 2023 bull run and late 2025
            base = 12000.0 if m.year == 2023 else 9000.0
            if m.year == 2025:
                base = 15000.0
            inflow = base + np.random.uniform(-1500, 2000)
        elif cat == "Debt":
            # Volatile inflows, outflows in some months
            inflow = np.random.uniform(-2000, 3000)
        elif cat == "Hybrid":
            inflow = np.random.uniform(1000, 4000)
        elif cat == "Solution Oriented":
            inflow = np.random.uniform(200, 800)
        else: # Others
            inflow = np.random.uniform(500, 1500)
            
        category_inflows_rows.append({
            "month": m_str,
            "category": cat,
            "net_inflow_crores": round(inflow, 2)
        })

df_category_inflows = pd.DataFrame(category_inflows_rows)
df_category_inflows.to_csv('data/processed/category_inflows.csv', index=False)
print("Saved category_inflows.csv")

# ----------------------------------------------------
# 6. Investor Demographics
# ----------------------------------------------------
print("Generating Investor Demographics...")
states = ['Maharashtra', 'Gujarat', 'Karnataka', 'Tamil Nadu', 'Delhi', 'Uttar Pradesh', 'West Bengal', 'Telangana', 'Haryana', 'Bihar']
state_probs = [0.22, 0.15, 0.12, 0.10, 0.08, 0.08, 0.07, 0.06, 0.06, 0.06]

investor_records = []
age_groups = ["Under 25", "25-34", "35-44", "45-54", "55+"]
age_group_probs = [0.10, 0.35, 0.30, 0.15, 0.10]

for i in range(1500):
    inv_id = f"INV{10000 + i}"
    state = np.random.choice(states, p=state_probs)
    city_tier = np.random.choice(["T30", "B30"], p=[0.65, 0.35])
    gender = np.random.choice(["Male", "Female", "Other"], p=[0.60, 0.38, 0.02])
    
    # Pick age group first
    age_gp = np.random.choice(age_groups, p=age_group_probs)
    if age_gp == "Under 25":
        age = int(np.random.randint(18, 25))
        sip_amount = round(float(np.random.lognormal(mean=7.5, sigma=0.5)), 2) # ~$2000
    elif age_gp == "25-34":
        age = int(np.random.randint(25, 35))
        sip_amount = round(float(np.random.lognormal(mean=8.8, sigma=0.6)), 2) # ~$7000
    elif age_gp == "35-44":
        age = int(np.random.randint(35, 45))
        sip_amount = round(float(np.random.lognormal(mean=9.5, sigma=0.6)), 2) # ~$14000
    elif age_gp == "45-54":
        age = int(np.random.randint(45, 55))
        sip_amount = round(float(np.random.lognormal(mean=9.7, sigma=0.6)), 2) # ~$17000
    else: # 55+
        age = int(np.random.randint(55, 76))
        sip_amount = round(float(np.random.lognormal(mean=9.2, sigma=0.6)), 2) # ~$10000
        
    # Scale SIP amount to be realistic (min 500, max 100000)
    sip_amount = max(500.0, min(100000.0, sip_amount))
    lumpsum_amount = round(sip_amount * np.random.uniform(2, 8), 2)
    
    investor_records.append({
        "investor_id": inv_id,
        "investor_name": f"Investor_{i}",
        "age": age,
        "age_group": age_gp,
        "gender": gender,
        "state": state,
        "city_tier": city_tier,
        "sip_amount": sip_amount,
        "lumpsum_amount": lumpsum_amount
    })

df_demographics = pd.DataFrame(investor_records)
df_demographics.to_csv('data/processed/investor_demographics.csv', index=False)
print("Saved investor_demographics.csv")

# ----------------------------------------------------
# 7. Folio Count Growth
# ----------------------------------------------------
print("Generating Folio Growth data...")
folio_growth_rows = []
start_folios = 13.26 # Jan 2022
target_folios = 26.12 # Dec 2025

for t, m in enumerate(months_range):
    pct = t / (len(months_range) - 1)
    # Smooth growth curve
    folio_val = start_folios + (target_folios - start_folios) * pct + np.random.uniform(-0.1, 0.1)
    if t == len(months_range) - 1:
        folio_val = target_folios
        
    folio_growth_rows.append({
        "month": m.strftime('%Y-%m'),
        "folio_count_crores": round(folio_val, 4)
    })

df_folio_growth = pd.DataFrame(folio_growth_rows)
df_folio_growth.to_csv('data/processed/folio_growth.csv', index=False)
print("Saved folio_growth.csv")

# ----------------------------------------------------
# 8. Portfolio Holdings & Sectors
# ----------------------------------------------------
print("Generating Portfolio Holdings for Equity Funds...")
sectors = [
    "Financial Services", "Information Technology", "Oil & Gas",
    "Healthcare", "Automobile", "Consumer Goods", "Construction",
    "Telecom", "Metals", "Power", "Services"
]
sector_probs = [0.28, 0.16, 0.11, 0.08, 0.07, 0.09, 0.06, 0.05, 0.04, 0.03, 0.03]

stocks_by_sector = {
    "Financial Services": ["HDFC Bank", "ICICI Bank", "SBI", "Axis Bank", "Kotak Mahindra Bank", "Bajaj Finance"],
    "Information Technology": ["Infosys", "TCS", "Wipro", "HCL Tech", "Tech Mahindra", "LTIMindtree"],
    "Oil & Gas": ["Reliance Industries", "ONGC", "BPCL", "IOC", "GAIL"],
    "Healthcare": ["Sun Pharma", "Cipla", "Dr Reddys", "Apollo Hospitals", "Max Healthcare"],
    "Automobile": ["Tata Motors", "Mahindra & Mahindra", "Maruti Suzuki", "Bajaj Auto", "Eicher Motors"],
    "Consumer Goods": ["ITC", "Hindustan Unilever", "Nestle India", "Asian Paints", "Titan Company"],
    "Construction": ["L&T", "DLF", "UltraTech Cement", "Grasim Industries"],
    "Telecom": ["Bharti Airtel", "Tata Communications"],
    "Metals": ["Tata Steel", "JSW Steel", "Hindalco", "Coal India"],
    "Power": ["NTPC", "Power Grid", "Tata Power", "Adani Green"],
    "Services": ["Adani Ports", "InterGlobe Aviation", "Zomato", "Delhivery"]
}

holdings_rows = []
equity_schemes = df_fund_master[df_fund_master["category"] == "Equity"]

for idx, row in equity_schemes.iterrows():
    amfi_code = row["amfi_code"]
    fund_name = row["fund_name"]
    
    # Pick 15-20 random stocks
    num_stocks = np.random.randint(15, 25)
    
    # Choose sectors based on probability distribution
    selected_sectors = np.random.choice(sectors, size=num_stocks, p=sector_probs)
    
    # Pick stocks for those sectors
    chosen_stocks = []
    for sec in selected_sectors:
        stk = np.random.choice(stocks_by_sector[sec])
        chosen_stocks.append((stk, sec))
        
    # Remove duplicates
    chosen_stocks = list(set(chosen_stocks))
    
    # Generate weights
    raw_weights = np.random.exponential(scale=1.0, size=len(chosen_stocks))
    weights = (raw_weights / sum(raw_weights)) * 100.0
    
    for (stk, sec), w in zip(chosen_stocks, weights):
        holdings_rows.append({
            "amfi_code": amfi_code,
            "fund_name": fund_name,
            "stock_name": stk,
            "sector": sec,
            "weight_pct": round(w, 4)
        })

df_portfolio_holdings = pd.DataFrame(holdings_rows)
df_portfolio_holdings.to_csv('data/processed/portfolio_holdings.csv', index=False)
print(f"Generated portfolio holdings in portfolio_holdings.csv across {len(equity_schemes)} equity funds")

# ----------------------------------------------------
# 9. Scheme Performance Trailing Returns
# ----------------------------------------------------
print("Generating performance trailing returns...")
perf_rows = []
for idx, row in df_fund_master.iterrows():
    amfi_code = row["amfi_code"]
    cat = row["category"]
    
    # Returns based on category
    if cat == "Equity":
        r1 = round(np.random.normal(16.5, 4.0), 2)
        r3 = round(np.random.normal(14.0, 2.5), 2)
        r5 = round(np.random.normal(12.5, 1.8), 2)
        er = round(np.random.uniform(0.75, 2.20), 2)
    elif cat == "Debt":
        r1 = round(np.random.normal(6.8, 0.8), 2)
        r3 = round(np.random.normal(6.5, 0.5), 2)
        r5 = round(np.random.normal(6.2, 0.4), 2)
        er = round(np.random.uniform(0.15, 0.85), 2)
    elif cat == "Hybrid":
        r1 = round(np.random.normal(12.5, 2.0), 2)
        r3 = round(np.random.normal(11.0, 1.5), 2)
        r5 = round(np.random.normal(10.2, 1.2), 2)
        er = round(np.random.uniform(0.65, 1.80), 2)
    elif cat == "Solution Oriented":
        r1 = round(np.random.normal(11.5, 1.8), 2)
        r3 = round(np.random.normal(10.5, 1.2), 2)
        r5 = round(np.random.normal(9.8, 1.0), 2)
        er = round(np.random.uniform(0.85, 2.00), 2)
    else: # ETF
        r1 = round(np.random.normal(15.0, 3.5), 2)
        r3 = round(np.random.normal(13.2, 2.0), 2)
        r5 = round(np.random.normal(12.0, 1.5), 2)
        er = round(np.random.uniform(0.05, 0.40), 2)
        
    perf_rows.append({
        "amfi_code": amfi_code,
        "scheme_name": row["fund_name"],
        "return_1y": r1,
        "return_3y": r3,
        "return_5y": r5,
        "expense_ratio": er,
        "anomaly_flag": 0
    })

df_scheme_perf = pd.DataFrame(perf_rows)
# Add some outliers/anomalies (e.g. 100%+ returns, or empty return metrics)
df_scheme_perf.loc[df_scheme_perf["amfi_code"] == 100005, "return_1y"] = 112.5 # Anomaly returns
df_scheme_perf.loc[df_scheme_perf["amfi_code"] == 100005, "anomaly_flag"] = 1
df_scheme_perf.loc[df_scheme_perf["amfi_code"] == 100018, "return_3y"] = np.nan # Missing return
df_scheme_perf.loc[df_scheme_perf["amfi_code"] == 100018, "anomaly_flag"] = 1

df_scheme_perf.to_csv('data/processed/scheme_performance.csv', index=False)
print("Saved scheme_performance.csv")

# ----------------------------------------------------
# 10. Investor Transactions
# ----------------------------------------------------
print("Generating Investor Transactions...")
txn_records = []
states = ['Maharashtra', 'Gujarat', 'Karnataka', 'Tamil Nadu', 'Delhi', 'Uttar Pradesh', 'West Bengal', 'Telangana', 'Haryana', 'Bihar']
states_prob = [0.22, 0.15, 0.12, 0.10, 0.08, 0.08, 0.07, 0.06, 0.06, 0.06]

amfi_codes = df_fund_master["amfi_code"].tolist()
nav_dict = df_nav_history.set_index(['amfi_code', 'date'])['nav'].to_dict()

# We'll generate regular monthly SIPs for investors INV10000 to INV10199 (200 investors)
regular_sip_investors = 200
txn_counter = 0

for j in range(regular_sip_investors):
    inv_id = f"INV{10000 + j}"
    inv_name = f"Investor_{j}"
    state = np.random.choice(states, p=states_prob)
    amfi = int(np.random.choice(amfi_codes))
    
    # Choose a fixed monthly SIP amount
    sip_amount = round(float(np.random.uniform(1000.0, 15000.0)), 2)
    
    # Start date in early 2024 (first 150 days)
    start_days_offset = np.random.randint(0, 150)
    curr_date = pd.Timestamp('2024-01-01') + pd.Timedelta(days=start_days_offset)
    end_date_limit = pd.Timestamp('2026-06-15')
    
    kyc = np.random.choice(['Verified', 'Pending', 'Failed'], p=[0.88, 0.10, 0.02])
    
    while curr_date <= end_date_limit:
        t_date_str = curr_date.strftime('%Y-%m-%d')
        
        # Look up NAV
        nav = nav_dict.get((amfi, t_date_str))
        if nav is None or nav <= 0:
            nav = base_navs[amfi]
            
        units = round(sip_amount / nav, 4)
        
        txn_id = f"TXN{20000 + txn_counter}"
        txn_records.append({
            "transaction_id": txn_id,
            "investor_id": inv_id,
            "investor_name": inv_name,
            "state": state,
            "amfi_code": amfi,
            "transaction_date": t_date_str,
            "transaction_type": "SIP",
            "amount": sip_amount,
            "kyc_status": kyc,
            "units": units
        })
        txn_counter += 1
        
        # Next monthly transaction date: normal monthly gap is ~30 days.
        # Missed month with 12% probability
        if np.random.rand() < 0.12:
            gap_days = np.random.randint(58, 65) # missed a month
        else:
            gap_days = np.random.randint(28, 33) # regular monthly
            
        curr_date = curr_date + pd.Timedelta(days=gap_days)

print(f"Generated {txn_counter} regular SIP transactions for {regular_sip_investors} investors.")

# Now for the remaining investors INV10200 to INV11499 (1300 investors),
# let's generate random lumpsum and redemptions, and some occasional SIPs.
# We will generate about 3,500 random transactions to maintain data size.
txn_dates = pd.date_range('2024-01-01', '2026-06-15')

for k in range(3500):
    inv_idx = np.random.randint(200, 1500) # INV10200 to INV11499
    inv_id = f"INV{10000 + inv_idx}"
    inv_name = f"Investor_{inv_idx}"
    state = np.random.choice(states, p=states_prob)
    amfi = int(np.random.choice(amfi_codes))
    
    t_date = np.random.choice(txn_dates)
    t_date_str = pd.Timestamp(t_date).strftime('%Y-%m-%d')
    
    txn_type = np.random.choice(['SIP', 'Lumpsum', 'Redemption'], p=[0.40, 0.40, 0.20])
    
    if txn_type == 'SIP':
        amount = round(float(np.random.uniform(500.0, 15000.0)), 2)
    elif txn_type == 'Lumpsum':
        amount = round(float(np.random.uniform(5000.0, 100000.0)), 2)
    else: # Redemption
        amount = round(float(np.random.uniform(2000.0, 50000.0)), 2)
        
    kyc = np.random.choice(['Verified', 'Pending', 'Failed'], p=[0.85, 0.12, 0.03])
    
    nav = nav_dict.get((amfi, t_date_str))
    if nav is None or nav <= 0:
        nav = base_navs[amfi]
        
    units = round(amount / nav, 4)
    
    txn_id = f"TXN{20000 + txn_counter}"
    txn_records.append({
        "transaction_id": txn_id,
        "investor_id": inv_id,
        "investor_name": inv_name,
        "state": state,
        "amfi_code": amfi,
        "transaction_date": t_date_str,
        "transaction_type": txn_type,
        "amount": amount,
        "kyc_status": kyc,
        "units": units
    })
    txn_counter += 1

df_txn = pd.DataFrame(txn_records)
df_txn.to_csv('data/processed/investor_transactions.csv', index=False)
print(f"Generated {len(df_txn)} investor transactions in investor_transactions.csv")

print("\nData synthesis complete! All processed files saved in data/processed/")
