import os
import json

def build_pbip():
    print("Building Power BI Project (.pbip) folder structure...")
    
    # Define directories
    report_dir = "bluestock_mf_dashboard.Report"
    model_dir = "bluestock_mf_dashboard.SemanticModel"
    
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    
    # 1. Create bluestock_mf_dashboard.pbip
    pbip_content = {
        "version": "1.0",
        "settings": {
            "locale": "en-US"
        },
        "report": {
            "path": f"./{report_dir}"
        }
    }
    with open("bluestock_mf_dashboard.pbip", "w", encoding="utf-8") as f:
        json.dump(pbip_content, f, indent=2)
        
    # 2. Create definition.pbir
    pbir_content = {
        "version": "1.0",
        "datasetReference": {
            "byPath": f"../{model_dir}"
        }
    }
    with open(os.path.join(report_dir, "definition.pbir"), "w", encoding="utf-8") as f:
        json.dump(pbir_content, f, indent=2)
        
    # 3. Create item.config.json
    config_content = {
        "version": "1.0",
        "settings": {
            "locale": "en-US"
        }
    }
    with open(os.path.join(report_dir, "item.config.json"), "w", encoding="utf-8") as f:
        json.dump(config_content, f, indent=2)
        
    # 4. Create definition.pbid
    pbid_content = {
        "version": "1.0",
        "connection": {
            "type": "SQLite",
            "details": {
                "database": "bluestock_mf.db"
            }
        }
    }
    with open(os.path.join(model_dir, "definition.pbid"), "w", encoding="utf-8") as f:
        json.dump(pbid_content, f, indent=2)
        
    # 5. Create model.bim
    # This defines the tables, columns, measures, and relationships
    model_bim = {
        "name": "bluestock_mf_dashboard",
        "compatibilityLevel": 1560,
        "model": {
            "culture": "en-US",
            "dataSources": [
                {
                    "type": "Structured",
                    "name": "SQLiteDatabase",
                    "connectionDetails": {
                        "path": "bluestock_mf.db"
                    }
                }
            ],
            "tables": [
                {
                    "name": "dim_fund",
                    "columns": [
                        {"name": "amfi_code", "dataType": "int64", "sourceColumn": "amfi_code"},
                        {"name": "fund_name", "dataType": "string", "sourceColumn": "fund_name"},
                        {"name": "fund_house", "dataType": "string", "sourceColumn": "fund_house"},
                        {"name": "category", "dataType": "string", "sourceColumn": "category"},
                        {"name": "sub_category", "dataType": "string", "sourceColumn": "sub_category"},
                        {"name": "risk_grade", "dataType": "string", "sourceColumn": "risk_grade"},
                        {"name": "launch_date", "dataType": "dateTime", "sourceColumn": "launch_date"}
                    ]
                },
                {
                    "name": "dim_date",
                    "columns": [
                        {"name": "date", "dataType": "string", "sourceColumn": "date"},
                        {"name": "day", "dataType": "int64", "sourceColumn": "day"},
                        {"name": "month", "dataType": "int64", "sourceColumn": "month"},
                        {"name": "year", "dataType": "int64", "sourceColumn": "year"},
                        {"name": "quarter", "dataType": "int64", "sourceColumn": "quarter"},
                        {"name": "day_of_week", "dataType": "string", "sourceColumn": "day_of_week"},
                        {"name": "is_weekend", "dataType": "int64", "sourceColumn": "is_weekend"}
                    ]
                },
                {
                    "name": "fact_nav",
                    "columns": [
                        {"name": "amfi_code", "dataType": "int64", "sourceColumn": "amfi_code"},
                        {"name": "date", "dataType": "string", "sourceColumn": "date"},
                        {"name": "nav", "dataType": "double", "sourceColumn": "nav"}
                    ]
                },
                {
                    "name": "fact_transactions",
                    "columns": [
                        {"name": "transaction_id", "dataType": "string", "sourceColumn": "transaction_id"},
                        {"name": "investor_id", "dataType": "string", "sourceColumn": "investor_id"},
                        {"name": "investor_name", "dataType": "string", "sourceColumn": "investor_name"},
                        {"name": "state", "dataType": "string", "sourceColumn": "state"},
                        {"name": "amfi_code", "dataType": "int64", "sourceColumn": "amfi_code"},
                        {"name": "transaction_date", "dataType": "string", "sourceColumn": "transaction_date"},
                        {"name": "transaction_type", "dataType": "string", "sourceColumn": "transaction_type"},
                        {"name": "amount", "dataType": "double", "sourceColumn": "amount"},
                        {"name": "kyc_status", "dataType": "string", "sourceColumn": "kyc_status"},
                        {"name": "units", "dataType": "double", "sourceColumn": "units"}
                    ]
                },
                {
                    "name": "fact_performance",
                    "columns": [
                        {"name": "amfi_code", "dataType": "int64", "sourceColumn": "amfi_code"},
                        {"name": "return_1y", "dataType": "double", "sourceColumn": "return_1y"},
                        {"name": "return_3y", "dataType": "double", "sourceColumn": "return_3y"},
                        {"name": "return_5y", "dataType": "double", "sourceColumn": "return_5y"},
                        {"name": "expense_ratio", "dataType": "double", "sourceColumn": "expense_ratio"},
                        {"name": "anomaly_flag", "dataType": "int64", "sourceColumn": "anomaly_flag"}
                    ]
                },
                {
                    "name": "fact_aum",
                    "columns": [
                        {"name": "amfi_code", "dataType": "int64", "sourceColumn": "amfi_code"},
                        {"name": "aum_amount", "dataType": "double", "sourceColumn": "aum_amount"},
                        {"name": "last_updated_date", "dataType": "string", "sourceColumn": "last_updated_date"}
                    ]
                },
                {
                    "name": "fact_aum_history",
                    "columns": [
                        {"name": "year", "dataType": "int64", "sourceColumn": "year"},
                        {"name": "fund_house", "dataType": "string", "sourceColumn": "fund_house"},
                        {"name": "aum_amount_crores", "dataType": "double", "sourceColumn": "aum_amount_crores"}
                    ]
                },
                {
                    "name": "fact_sip_inflows",
                    "columns": [
                        {"name": "month", "dataType": "string", "sourceColumn": "month"},
                        {"name": "sip_amount_crores", "dataType": "double", "sourceColumn": "sip_amount_crores"}
                    ]
                }
            ],
            "relationships": [
                {
                    "name": "rel_fund_nav",
                    "fromTable": "fact_nav",
                    "fromColumn": "amfi_code",
                    "toTable": "dim_fund",
                    "toColumn": "amfi_code"
                },
                {
                    "name": "rel_fund_txn",
                    "fromTable": "fact_transactions",
                    "fromColumn": "amfi_code",
                    "toTable": "dim_fund",
                    "toColumn": "amfi_code"
                },
                {
                    "name": "rel_fund_perf",
                    "fromTable": "fact_performance",
                    "fromColumn": "amfi_code",
                    "toTable": "dim_fund",
                    "toColumn": "amfi_code"
                },
                {
                    "name": "rel_fund_aum",
                    "fromTable": "fact_aum",
                    "fromColumn": "amfi_code",
                    "toTable": "dim_fund",
                    "toColumn": "amfi_code"
                },
                {
                    "name": "rel_date_nav",
                    "fromTable": "fact_nav",
                    "fromColumn": "date",
                    "toTable": "dim_date",
                    "toColumn": "date"
                },
                {
                    "name": "rel_date_txn",
                    "fromTable": "fact_transactions",
                    "fromColumn": "transaction_date",
                    "toTable": "dim_date",
                    "toColumn": "date"
                },
                {
                    "name": "rel_date_aum",
                    "fromTable": "fact_aum",
                    "fromColumn": "last_updated_date",
                    "toTable": "dim_date",
                    "toColumn": "date"
                }
            ]
        }
    }
    with open(os.path.join(model_dir, "model.bim"), "w", encoding="utf-8") as f:
        json.dump(model_bim, f, indent=2)
        
    # 6. Generate bluestock_mf_dashboard.Report/layout.json
    # Defines standard canvas sizes, settings, theme
    layout_content = {
        "version": "1.0",
        "theme": "BluestockTheme",
        "settings": {
            "layoutType": "Custom",
            "customWidth": 1280,
            "customHeight": 720
        },
        "pages": [
            {
                "name": "Page1",
                "displayName": "Industry Overview",
                "visualTemplates": ["AUM Line Chart", "AUM by AMC Bar Chart", "KPI Cards"]
            },
            {
                "name": "Page2",
                "displayName": "Fund Performance",
                "visualTemplates": ["Risk-Return Scatter Plot", "Scorecard Table", "NAV vs Benchmark"]
            },
            {
                "name": "Page3",
                "displayName": "Investor Analytics",
                "visualTemplates": ["Geographic Bar Chart", "SIP/Lumpsum Donut", "Age Group Avg Bar"]
            },
            {
                "name": "Page4",
                "displayName": "SIP & Market Trends",
                "visualTemplates": ["SIP vs Nifty Dual-Axis", "Category Heatmap", "Top 5 Categories"]
            }
        ]
    }
    with open(os.path.join(report_dir, "layout.json"), "w", encoding="utf-8") as f:
        json.dump(layout_content, f, indent=2)
        
    print("Power BI Project (.pbip) folder structure successfully generated!")

if __name__ == '__main__':
    build_pbip()
