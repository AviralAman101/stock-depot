import mysql.connector
import pandas as pd
import yfinance as yf

from config import DB_CONFIG

# --------------------------------------------------------
# CONNECT
# --------------------------------------------------------

connection = mysql.connector.connect(**DB_CONFIG)
cursor = connection.cursor(dictionary=True)

# --------------------------------------------------------
# GET COMPANIES
# --------------------------------------------------------

cursor.execute("""
SELECT company_id,
       ticker
FROM companies
ORDER BY company_id
""")

companies = cursor.fetchall()

# --------------------------------------------------------
# UPSERT SQL
# --------------------------------------------------------

UPSERT_SQL = """
INSERT INTO income_statements
(
company_id,
report_date,
report_type,
total_revenue,
cost_of_revenue,
gross_profit,
operating_income,
pretax_income,
net_income,
basic_eps,
diluted_eps
)

VALUES
(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

ON DUPLICATE KEY UPDATE

total_revenue=VALUES(total_revenue),
cost_of_revenue=VALUES(cost_of_revenue),
gross_profit=VALUES(gross_profit),
operating_income=VALUES(operating_income),
pretax_income=VALUES(pretax_income),
net_income=VALUES(net_income),
basic_eps=VALUES(basic_eps),
diluted_eps=VALUES(diluted_eps)
"""

# --------------------------------------------------------
# Helper
# --------------------------------------------------------

def safe_value(df, metric, column):
    try:
        if metric in df.index:
            value = df.loc[metric, column]
            if pd.isna(value):
                return None
            return value.item() if hasattr(value, "item") else value
    except Exception:
        pass

    return None

# --------------------------------------------------------
# Process each company
# --------------------------------------------------------

for company in companies:

    company_id = company["company_id"]
    ticker = company["ticker"]

    print("=" * 60)
    print(ticker)

    stock = yf.Ticker(ticker)

    datasets = [
        ("Annual", stock.financials),
        ("Quarterly", stock.quarterly_financials)
    ]

    for report_type, df in datasets:

        if df.empty:
            continue

        for column in df.columns:

            report_date = pd.to_datetime(column).date()

            values = (

                company_id,

                report_date,

                report_type,

                safe_value(df, "Total Revenue", column),

                safe_value(df, "Cost Of Revenue", column),

                safe_value(df, "Gross Profit", column),

                safe_value(df, "Operating Income", column),

                safe_value(df, "Pretax Income", column),

                safe_value(df, "Net Income", column),

                safe_value(df, "Basic EPS", column),

                safe_value(df, "Diluted EPS", column)

            )

            cursor.execute(UPSERT_SQL, values)

    connection.commit()

cursor.close()
connection.close()

print("Income statements loaded.")