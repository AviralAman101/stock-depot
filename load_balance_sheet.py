import mysql.connector
import pandas as pd
import yfinance as yf

from config import DB_CONFIG

# ---------------------------------------------------------
# CONNECT TO DATABASE
# ---------------------------------------------------------

connection = mysql.connector.connect(**DB_CONFIG)

cursor = connection.cursor(dictionary=True)

# ---------------------------------------------------------
# READ COMPANIES
# ---------------------------------------------------------

cursor.execute("""
SELECT company_id,
       ticker
FROM companies
ORDER BY company_id
""")

companies = cursor.fetchall()

print(f"{len(companies)} companies found.")

# ---------------------------------------------------------
# SQL UPSERT
# ---------------------------------------------------------

UPSERT_SQL = """
INSERT INTO balance_sheets
(
company_id,
report_date,
report_type,
cash_and_cash_equivalents,
inventory,
current_assets,
total_assets,
current_liabilities,
total_liabilities,
long_term_debt,
shareholders_equity
)

VALUES
(
%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
)

ON DUPLICATE KEY UPDATE

cash_and_cash_equivalents = VALUES(cash_and_cash_equivalents),

inventory = VALUES(inventory),

current_assets = VALUES(current_assets),

total_assets = VALUES(total_assets),

current_liabilities = VALUES(current_liabilities),

total_liabilities = VALUES(total_liabilities),

long_term_debt = VALUES(long_term_debt),

shareholders_equity = VALUES(shareholders_equity)
"""

# ---------------------------------------------------------
# SAFE VALUE FUNCTION
# ---------------------------------------------------------

def get_value(df, possible_names, column):

    for name in possible_names:

        if name in df.index:

            value = df.loc[name, column]

            if pd.isna(value):
                return None

            if hasattr(value, "item"):
                return value.item()

            return value

    return None

# ---------------------------------------------------------
# FIELD MAPPINGS
# ---------------------------------------------------------

FIELD_MAP = {

    "cash_and_cash_equivalents": [
        "Cash And Cash Equivalents",
        "Cash Cash Equivalents And Short Term Investments",
        "Cash"
    ],

    "inventory": [
        "Inventory"
    ],

    "current_assets": [
        "Current Assets",
        "Total Current Assets"
    ],

    "total_assets": [
        "Total Assets"
    ],

    "current_liabilities": [
        "Current Liabilities",
        "Total Current Liabilities"
    ],

    "total_liabilities": [
        "Total Liabilities Net Minority Interest",
        "Total Liabilities"
    ],

    "long_term_debt": [
        "Long Term Debt",
        "Long Term Debt And Capital Lease Obligation"
    ],

    "shareholders_equity": [
        "Stockholders Equity",
        "Total Equity Gross Minority Interest",
        "Common Stock Equity"
    ]

}

# ---------------------------------------------------------
# PROCESS ONE DATAFRAME
# ---------------------------------------------------------

def load_dataframe(company_id, report_type, df):

    if df.empty:
        return

    for column in df.columns:

        report_date = pd.to_datetime(column).date()

        values = (

            company_id,

            report_date,

            report_type,

            get_value(df, FIELD_MAP["cash_and_cash_equivalents"], column),

            get_value(df, FIELD_MAP["inventory"], column),

            get_value(df, FIELD_MAP["current_assets"], column),

            get_value(df, FIELD_MAP["total_assets"], column),

            get_value(df, FIELD_MAP["current_liabilities"], column),

            get_value(df, FIELD_MAP["total_liabilities"], column),

            get_value(df, FIELD_MAP["long_term_debt"], column),

            get_value(df, FIELD_MAP["shareholders_equity"], column)

        )

        cursor.execute(UPSERT_SQL, values)

# ---------------------------------------------------------
# LOOP THROUGH COMPANIES
# ---------------------------------------------------------

for company in companies:

    company_id = company["company_id"]

    ticker = company["ticker"]

    print("=" * 60)

    print(ticker)

    try:

        stock = yf.Ticker(ticker)

        annual = stock.balance_sheet

        quarterly = stock.quarterly_balance_sheet

        load_dataframe(company_id, "Annual", annual)

        load_dataframe(company_id, "Quarterly", quarterly)

        connection.commit()

        print("Balance sheets loaded.")

    except Exception as ex:

        print(ex)

connection.close()

print()

print("Finished.")