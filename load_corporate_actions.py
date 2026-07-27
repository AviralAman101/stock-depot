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
INSERT INTO corporate_actions
(
company_id,
action_date,
action_type,
amount,
description
)

VALUES
(
%s,%s,%s,%s,%s
)

ON DUPLICATE KEY UPDATE

amount=VALUES(amount),

description=VALUES(description)
"""

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

        actions = stock.actions

    except Exception as ex:

        print(ex)
        continue

    if actions.empty:

        print("No corporate actions found.")

        continue

    actions.reset_index(inplace=True)

    inserted = 0

    for _, row in actions.iterrows():

        action_date = row["Date"].date()

        # -------------------------
        # Dividend
        # -------------------------

        if "Dividends" in actions.columns:

            dividend = row["Dividends"]

            if pd.notna(dividend) and dividend != 0:

                values = (

                    company_id,

                    action_date,

                    "DIVIDEND",

                    float(dividend),

                    "Dividend"

                )

                cursor.execute(UPSERT_SQL, values)

                inserted += 1

        # -------------------------
        # Stock Split
        # -------------------------

        if "Stock Splits" in actions.columns:

            split = row["Stock Splits"]

            if pd.notna(split) and split != 0:

                values = (

                    company_id,

                    action_date,

                    "STOCK_SPLIT",

                    float(split),

                    f"Split Ratio {split}"

                )

                cursor.execute(UPSERT_SQL, values)

                inserted += 1

    connection.commit()

    print(f"{inserted} corporate actions inserted/updated.")

cursor.close()

connection.close()

print("\nFinished.")