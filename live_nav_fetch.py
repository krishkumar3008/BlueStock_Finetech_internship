import requests
import pandas as pd
import os

def fetch_and_save_nav(scheme_code, name):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"Fetching data for {name} ({scheme_code})...")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            df = pd.DataFrame(data['data'])
            # Save as raw CSV
            filename = f"data/raw/{scheme_code}_{name.replace(' ', '_')}.csv"
            df.to_csv(filename, index=False)
            print(f"Saved {name} NAV to {filename}")
        else:
            print(f"No NAV data found for {name} ({scheme_code})")
    else:
        print(f"Failed to fetch {name} ({scheme_code}): HTTP {response.status_code}")

if __name__ == "__main__":
    # Ensure data/raw directory exists
    os.makedirs('data/raw', exist_ok=True)
    
    # 1. HDFC Top 100 Direct
    fetch_and_save_nav(125497, "HDFC_Top_100")
    
    # 2. 5 key schemes
    key_schemes = {
        119551: "SBI_Bluechip",
        120503: "ICICI_Bluechip",
        118632: "Nippon_Large_Cap",
        119092: "Axis_Bluechip",
        120841: "Kotak_Bluechip"
    }
    
    for code, name in key_schemes.items():
        fetch_and_save_nav(code, name)
