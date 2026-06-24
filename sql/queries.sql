-- 10 Analytical SQL Queries for Bluestock Mutual Fund Database

-- Query 1: Top 5 funds by AUM
-- Lists mutual fund schemes sorted by Assets Under Management (AUM) in crores.
SELECT 
    f.fund_name, 
    f.fund_house, 
    a.aum_amount AS aum_crores
FROM fact_aum a
JOIN dim_fund f ON a.amfi_code = f.amfi_code
ORDER BY a.aum_amount DESC
LIMIT 5;

-- Query 2: Average NAV per month
-- Calculates monthly average NAV values to track historic price movement of each fund.
SELECT 
    f.fund_name,
    d.year,
    d.month,
    ROUND(AVG(n.nav), 4) AS avg_nav
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
JOIN dim_date d ON n.date = d.date
GROUP BY f.amfi_code, d.year, d.month
ORDER BY f.fund_name, d.year, d.month;

-- Query 3: SIP YoY growth
-- Compares annual SIP transaction amounts to evaluate growth trends.
WITH sip_by_year AS (
    SELECT 
        d.year,
        SUM(t.amount) AS total_sip_amount
    FROM fact_transactions t
    JOIN dim_date d ON t.transaction_date = d.date
    WHERE t.transaction_type = 'SIP'
    GROUP BY d.year
)
SELECT 
    curr.year,
    curr.total_sip_amount AS current_year_sip,
    prev.total_sip_amount AS prev_year_sip,
    ROUND(((curr.total_sip_amount - prev.total_sip_amount) / prev.total_sip_amount) * 100, 2) || '%' AS yoy_growth_pct
FROM sip_by_year curr
LEFT JOIN sip_by_year prev ON curr.year = prev.year + 1
ORDER BY curr.year;

-- Query 4: Transactions by state
-- Aggregates transaction counts and volume to see which states lead in investments.
SELECT 
    state,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_volume
FROM fact_transactions
GROUP BY state
ORDER BY total_volume DESC;

-- Query 5: Funds with expense_ratio < 1%
-- Retrieves schemes with cost-efficient management (expense ratio less than 1.0%).
SELECT 
    f.fund_name, 
    p.expense_ratio AS expense_ratio_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio < 1.0;

-- Query 6: Total net units held per fund
-- Subtracts redemption units from subscription units to calculate the net holdings per fund.
SELECT 
    f.fund_name,
    ROUND(SUM(CASE WHEN t.transaction_type = 'Redemption' THEN -t.units ELSE t.units END), 4) AS net_units_held
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.amfi_code
GROUP BY f.fund_name
ORDER BY net_units_held DESC;

-- Query 7: KYC compliance rate by state
-- Shows percentage of transactions made by KYC Verified accounts across different states.
SELECT 
    state,
    COUNT(CASE WHEN kyc_status = 'Verified' THEN 1 END) AS verified_txns,
    COUNT(*) AS total_txns,
    ROUND((COUNT(CASE WHEN kyc_status = 'Verified' THEN 1 END) * 100.0) / COUNT(*), 2) || '%' AS kyc_compliance_rate
FROM fact_transactions
GROUP BY state
ORDER BY (COUNT(CASE WHEN kyc_status = 'Verified' THEN 1 END) * 100.0) / COUNT(*) DESC;

-- Query 8: Peak NAV achieved by each fund
-- Identifies the maximum NAV ever recorded for each scheme and the date of achievement.
WITH ranked_navs AS (
    SELECT 
        amfi_code,
        date,
        nav,
        ROW_NUMBER() OVER (PARTITION BY amfi_code ORDER BY nav DESC, date DESC) as rn
    FROM fact_nav
)
SELECT 
    f.fund_name,
    r.date AS peak_date,
    r.nav AS peak_nav
FROM ranked_navs r
JOIN dim_fund f ON r.amfi_code = f.amfi_code
WHERE r.rn = 1
ORDER BY peak_nav DESC;

-- Query 9: Monthly Investment Volume (Excluding Redemptions)
-- Shows aggregate monthly inflow (SIP + Lumpsum) to observe seasonal behaviors.
SELECT 
    d.year,
    d.month,
    COUNT(*) AS investment_count,
    ROUND(SUM(t.amount), 2) AS total_investment_amount
FROM fact_transactions t
JOIN dim_date d ON t.transaction_date = d.date
WHERE t.transaction_type IN ('SIP', 'Lumpsum')
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- Query 10: Aggregated Performance and AUM summary per Fund House
-- Summarizes fund houses by count, total AUM, average 1-year returns, and average expense ratios.
SELECT 
    f.fund_house,
    COUNT(DISTINCT f.amfi_code) AS schemes_count,
    ROUND(SUM(a.aum_amount), 2) AS total_aum_crores,
    ROUND(AVG(p.return_1y), 2) AS avg_return_1y_pct,
    ROUND(AVG(p.expense_ratio), 2) AS avg_expense_ratio_pct
FROM dim_fund f
JOIN fact_aum a ON f.amfi_code = a.amfi_code
JOIN fact_performance p ON f.amfi_code = p.amfi_code
GROUP BY f.fund_house
ORDER BY total_aum_crores DESC;
