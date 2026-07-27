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
# UPSERT SQL
# ---------------------------------------------------------

UPSERT_SQL = """
INSERT INTO cash_flow_statements
(
company_id,
report_date,
report_type,
operating_cash_flow,
investing_cash_flow,
financing_cash_flow,
capital_expenditure,
free_cash_flow,
beginning_cash_position,
end_cash_position
)

VALUES
(
%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
)

ON DUPLICATE KEY UPDATE

operating_cash_flow = VALUES(operating_cash_flow),

investing_cash_flow = VALUES(investing_cash_flow),

financing_cash_flow = VALUES(financing_cash_flow),

capital_expenditure = VALUES(capital_expenditure),

free_cash_flow = VALUES(free_cash_flow),

beginning_cash_position = VALUES(beginning_cash_position),

end_cash_position = VALUES(end_cash_position)
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
# FIELD MAP
# ---------------------------------------------------------

FIELD_MAP = {

    "operating_cash_flow": [
        "Operating Cash Flow",
        "Cash Flow From Continuing Operating Activities"
    ],

    "investing_cash_flow": [
        "Investing Cash Flow",
        "Cash Flow From Continuing Investing Activities"
    ],

    "financing_cash_flow": [
        "Financing Cash Flow",
        "Cash Flow From Continuing Financing Activities"
    ],

    "capital_expenditure": [
        "Capital Expenditure",
        "Capital Expenditure Reported"
    ],

    "free_cash_flow": [
        "Free Cash Flow"
    ],

    "beginning_cash_position": [
        "Beginning Cash Position"
    ],

    "end_cash_position": [
        "End Cash Position"
    ]

}

# ---------------------------------------------------------
# LOAD ONE DATAFRAME
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

            get_value(df, FIELD_MAP["operating_cash_flow"], column),

            get_value(df, FIELD_MAP["investing_cash_flow"], column),

            get_value(df, FIELD_MAP["financing_cash_flow"], column),

            get_value(df, FIELD_MAP["capital_expenditure"], column),

            get_value(df, FIELD_MAP["free_cash_flow"], column),

            get_value(df, FIELD_MAP["beginning_cash_position"], column),

            get_value(df, FIELD_MAP["end_cash_position"], column)

        )

        cursor.execute(UPSERT_SQL, values)

# ---------------------------------------------------------
# PROCESS ALL COMPANIES
# ---------------------------------------------------------

for company in companies:

    company_id = company["company_id"]
    ticker = company["ticker"]

    print("=" * 60)
    print(ticker)

    try:

        stock = yf.Ticker(ticker)

        annual = stock.cashflow

        quarterly = stock.quarterly_cashflow

        load_dataframe(company_id, "Annual", annual)

        load_dataframe(company_id, "Quarterly", quarterly)

        connection.commit()

        print("Cash flow statements loaded.")

    except Exception as ex:

        print(ex)

cursor.close()
connection.close()

print("\nFinished.")