import pandas as pd
import sys

def get_recommendations(risk_appetite):
    # 1. Load datasets
    try:
        df_scorecard = pd.read_csv("fund_scorecard.csv")
    except Exception as e:
        print(f"Error loading fund_scorecard.csv: {e}")
        return None
        
    try:
        df_funds = pd.read_csv("data/processed/fund_master.csv")
    except Exception as e:
        print(f"Error loading data/processed/fund_master.csv: {e}")
        return None
        
    # 2. Join datasets on amfi_code
    df_merged = pd.merge(df_scorecard[['amfi_code', 'sharpe']], 
                         df_funds[['amfi_code', 'fund_name', 'category', 'sub_category', 'risk_grade', 'aum_amount_crores']], 
                         on='amfi_code')
    
    # 3. Map risk appetite to risk grades
    risk_mapping = {
        'low': ['Low', 'Low to Moderate'],
        'moderate': ['Moderate', 'Moderately High'],
        'high': ['High', 'Very High']
    }
    
    appetite_clean = risk_appetite.strip().lower()
    if appetite_clean not in risk_mapping:
        print(f"Invalid risk appetite input: '{risk_appetite}'. Please choose from Low, Moderate, or High.")
        return None
        
    target_grades = risk_mapping[appetite_clean]
    
    # 4. Filter and sort
    df_filtered = df_merged[df_merged['risk_grade'].isin(target_grades)]
    df_recommended = df_filtered.sort_values(by='sharpe', ascending=False).head(3)
    
    return df_recommended

def print_table(df):
    if df is None or len(df) == 0:
        print("No recommendations found.")
        return
        
    print("\n" + "="*95)
    print(f"{'AMFI':<8} | {'Fund Name':<45} | {'Category':<10} | {'Risk Grade':<15} | {'Sharpe':<8}")
    print("="*95)
    for idx, row in df.iterrows():
        # Trim long fund names
        name = row['fund_name']
        if len(name) > 45:
            name = name[:42] + "..."
        print(f"{row['amfi_code']:<8} | {name:<45} | {row['category']:<10} | {row['risk_grade']:<15} | {row['sharpe']:<8.4f}")
    print("="*95 + "\n")

def main():
    print("="*50)
    print("    BLUESTOCK FINETECH - MUTUAL FUND RECOMMENDER    ")
    print("="*50)
    
    if len(sys.argv) > 1:
        # Command line argument provided
        risk_input = sys.argv[1]
        print(f"Risk Appetite Selected: {risk_input}")
    else:
        # Prompt user
        print("Choose your risk appetite to receive top-ranked fund recommendations.")
        print("Options: Low | Moderate | High")
        try:
            risk_input = input("Enter risk appetite: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting recommender.")
            return
            
    df_rec = get_recommendations(risk_input)
    if df_rec is not None:
        print(f"\nTop 3 Recommended Funds for '{risk_input.capitalize()}' Risk Profile:")
        print_table(df_rec)

if __name__ == "__main__":
    main()
