# Mutual Fund Advanced Portfolio & Investor Analytics Report

**Prepared for**: Bluestock Finetech Investment Committee  
**Date**: July 2026  
**Scope**: In-depth risk-return profiling, tail risk, investor cohorts, SIP continuity, and sector concentration analytics of 40 mutual fund schemes.

---

## 1. Executive Summary

This report delivers five advanced quantitative analytics modules to evaluate mutual fund portfolio risk, investor behavioral continuity, cohort demographics, and sector concentration across 40 schemes (representing Equity, Debt, Hybrid, and Solution-Oriented categories). 

### Key Findings:
1.  **Tail Risk**: Equity Small Cap and Mid Cap schemes show the largest tail risk. Daily Historical VaR (95%) shows a threshold of **-1.95%** for small-cap funds, with a Conditional VaR (95%) of **-2.35%** daily loss. Liquid and Gilt debt funds remain extremely safe with VaR (95%) at **-0.16%**.
2.  **Investor Cohorts**: Gross investor inflows peaked in **2024** (1,064 new accounts, INR 4.10 Crore total invested) with a strong preference for Large Cap funds, while **2025** entrants shifted toward Hybrid/Balanced Advantage funds, and **2026** entrants preferred Gilt/Corporate Bond funds.
3.  **SIP Continuity**: Of the 200 investors with long-term SIP accounts (6+ payments), **195 (97.5%)** have missed at least one payment installment (payment gap > 35 days), placing them in the **"At-Risk"** category. The active continuity rate stands at only **2.5%**.
4.  **Portfolio Concentration**: Equity portfolios show highly divergent concentration profiles. **ICICI Pru Small Cap (100011)** is the most sector-concentrated fund (HHI = **2674.57**), while **Axis Mid Cap (100014)** is the most diversified (HHI = **1436.99**).
5.  **Risk-Adjusted Performance**: Rolling 90-day Sharpe ratios peaked above **2.80** for mid/small-cap funds in late 2023, crashed below **-0.50** during 2024 corrections, and stabilized between **0.50 and 1.50** by mid-2026.

---

## 2. Historical Value-at-Risk (VaR) & Conditional VaR (CVaR)

We calculated the Historical VaR (95%) and CVaR (95%) using daily return series derived from the 4.5-year daily NAV dataset (2022–2026).
*   **Historical VaR (95%)**: The 5th percentile of daily returns, indicating the threshold loss that is exceeded only 5% of the time.
*   **CVaR (95%) / Expected Shortfall**: The average loss on days when returns are worse than the VaR threshold.

### Top 5 Schemes by Tail Risk (Highest VaR/CVaR - Riskiest)
| AMFI Code | Fund Name | Category | Sub-Category | Daily VaR (95%) | Daily CVaR (95%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **100003** | ICICI Prudential Small Cap Fund - Regular Growth | Equity | Small Cap | -1.9547% | -2.3511% |
| **100019** | ICICI Prudential Small Cap Fund - Regular Growth | Equity | Small Cap | -1.9427% | -2.4338% |
| **100001** | SBI Large Cap Fund - Regular Growth | Equity | Large Cap | -1.9284% | -2.4118% |
| **100017** | SBI Large Cap Fund - Regular Growth | Equity | Large Cap | -1.9213% | -2.4101% |
| **100002** | HDFC Mid Cap Fund - Direct Growth | Equity | Mid Cap | -1.9167% | -2.3769% |

### Top 5 Schemes by Capital Preservation (Lowest VaR/CVaR - Safest)
| AMFI Code | Fund Name | Category | Sub-Category | Daily VaR (95%) | Daily CVaR (95%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **100030** | Axis Liquid Fund - Direct Growth | Debt | Liquid | -0.1587% | -0.2016% |
| **100021** | Kotak Mahindra Liquid Fund - Regular Growth | Debt | Liquid | -0.1588% | -0.2030% |
| **100027** | ICICI Prudential Liquid Fund - Regular Growth | Debt | Liquid | -0.1593% | -0.2001% |
| **100025** | SBI Gilt Fund - Regular Growth | Debt | Gilt | -0.1597% | -0.2015% |
| **100028** | Nippon India Gilt Fund - Direct Growth | Debt | Gilt | -0.1599% | -0.2023% |

*The complete list of all 40 funds is exported in [var_cvar_report.csv](file:///d:/BlueStock%20Finetech/var_cvar_report.csv).*

---

## 3. Rolling 90-Day Sharpe Ratio

Rolling 90-day annualized Sharpe ratios were computed for the 5 key funds representing top scorecard rankings. This dynamic measure tracks how the risk-adjusted return changed across bull markets (2023) and corrections (2024).

*   **Mid & Small Cap outperformance (2023)**: Annualized rolling Sharpe ratios rose above **2.80** for the **HDFC Mid Cap Fund** and **ICICI Pru Small Cap Fund** as high returns far compensated daily volatility.
*   **Correction regime (2024)**: During the corrections of Jan-Feb 2024 and June 2024, rolling Sharpe ratios dipped below **-0.50** for all equity funds.
*   **Stabilization (2025-2026)**: Sharpe ratios rebounded and stabilized between **0.50 and 1.50** by early 2026, indicating solid but mature market returns with normalized volatilities.

*The high-resolution visualization is saved at [rolling_sharpe_chart.png](file:///d:/BlueStock%20Finetech/rolling_sharpe_chart.png).*

---

## 4. Investor Cohort Analysis

Investors were grouped by the calendar year of their first transaction (Cohort Year).
*   **Total Invested** represents gross subscriptions (SIP + Lumpsum transaction amounts).
*   **Top Fund Preference** is based on the fund receiving the highest total investment from that cohort.

| Cohort Year | Unique Investors | Average SIP Amount (INR) | Total Gross Invested (INR) | Top Fund Preference (AMFI) | Top Fund Name |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **2024** | 1,064 | 8,054.49 | 41,052,788.84 | 100009 | SBI Large Cap Fund - Regular Growth (100009) |
| **2025** | 300 | 7,929.13 | 7,096,160.00 | 100035 | ICICI Pru Balanced Advantage Fund (100035) |
| **2026** | 55 | 7,949.16 | 1,090,047.20 | 100025 | SBI Gilt Fund - Regular Growth (100025) |

---

## 5. SIP Continuity & Account Risk Profiling

We analyzed payment intervals for accounts with a long-term transaction history (**6+ SIP payments**).
*   We calculated the average and maximum gaps (in calendar days) between successive payments.
*   Accounts with **any gap > 35 days** were flagged as **"At-Risk"** (indicating a missed monthly payment cycle).

### Risk Profile Summary:
*   **Total Qualified Accounts (6+ SIPs)**: 200 accounts
*   **Active Accounts (Zero gaps > 35 days)**: 5 accounts (**2.50%** continuity rate)
*   **At-Risk Accounts (At least one gap > 35 days)**: 195 accounts (**97.50%** risk rate)
*   **Average Gaps**: The average payment gap for active accounts hovered around **30.1 days**, while at-risk accounts had a maximum gap ranging between **58 and 65 days** (representing a missed month's installment).

*Actionable Recommendation: The investor relations team should set up automated alerts when a payment is delayed by more than 33 days to proactively contact the client before the account enters the "At-Risk" state.*

---

## 6. Sector HHI Concentration

The Herfindahl-Hirschman Index (HHI) measures portfolio sector concentration by summing the squared weights of sectors in each fund. 
$$HHI = \sum_{i=1}^N (w_{\text{sector, } i})^2$$
*   **HHI > 2,000 (0.20)**: Highly concentrated portfolio.
*   **HHI < 1,500 (0.15)**: Diversified portfolio.

### Equity Funds Sector Concentration Rankings (Top 5 Concentrated vs. Top 5 Diversified)
| Rank | AMFI Code | Fund Name | Sub-Category | Sector HHI (0-10000) | HHI (Decimal) | Concentration Status |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| **1** | 100011 | ICICI Prudential Small Cap Fund - Regular Growth | Small Cap | 2674.57 | 0.2675 | Highly Concentrated |
| **2** | 100013 | Kotak Mahindra Large Cap Fund - Regular Growth | Large Cap | 2595.74 | 0.2596 | Highly Concentrated |
| **3** | 100004 | Nippon India Flexi Cap Fund - Direct Growth | Flexi Cap | 2519.17 | 0.2519 | Highly Concentrated |
| **4** | 100015 | UTI Small Cap Fund - Regular Growth | Small Cap | 2387.90 | 0.2388 | Highly Concentrated |
| **5** | 100008 | Aditya Birla Sun Life Flexi Cap Fund - Direct Growth | Flexi Cap | 2384.20 | 0.2384 | Highly Concentrated |
| ... | ... | ... | ... | ... | ... | ... |
| **16** | 100012 | Nippon India Flexi Cap Fund - Direct Growth | Flexi Cap | 1557.16 | 0.1557 | Well-Diversified |
| **17** | 100001 | SBI Large Cap Fund - Regular Growth | Large Cap | 1470.09 | 0.1470 | Well-Diversified |
| **18** | 100005 | Kotak Mahindra Large Cap Fund - Regular Growth | Large Cap | 1445.58 | 0.1446 | Well-Diversified |
| **19** | 100009 | SBI Large Cap Fund - Regular Growth | Large Cap | 1441.44 | 0.1441 | Well-Diversified |
| **20** | 100014 | Axis Mid Cap Fund - Direct Growth | Mid Cap | 1436.99 | 0.1437 | Well-Diversified |

---

## 7. Conclusions & Next Steps

1.  **Tail-Risk Shielding**: Advise conservative investors (Low-Moderate risk profiles) to shift assets from small/mid-caps to Balanced Advantage hybrid funds (**ICICI Pru Balanced Advantage (100035)**) to reduce tail risk (VaR reduces from **-1.95%** to **-1.11%** daily).
2.  **Mitigate SIP At-Risk Accounts**: Since 97.5% of long-term SIP investors show at least one missed payment gap, we recommend introducing flexible SIP calendars (e.g. grace periods of 7 days or choosing alternative dates) to reduce administrative churn.
3.  **Portfolio Rebalancing**: Mid/Large cap index funds exhibit HHI concentration above 2,500 due to Financials/IT concentration. Active managers should seek tactical exposure in Construction, Power, and Automobile sectors to bring HHI closer to 1,500.
