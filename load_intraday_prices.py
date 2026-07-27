import mysql.connector
import pandas as pd
import yfinance as yf

from datetime import datetime

from config import (
    DB_CONFIG,
    INTRADAY_START_DATE,
    INTRADAY_INTERVAL
)

# ----------------------------------------------------
# CONNECT
# ----------------------------------------------------

connection = mysql.connector.connect(**DB_CONFIG)

cursor = connection.cursor(dictionary=True)

# ----------------------------------------------------
# GET COMPANIES
# ----------------------------------------------------

cursor.execute("""
SELECT company_id,
       ticker
FROM companies
ORDER BY company_id
""")

companies = cursor.fetchall()

print(f"Found {len(companies)} companies.")

# ----------------------------------------------------
# UPSERT SQL
# ----------------------------------------------------

UPSERT_SQL = """
INSERT INTO stock_prices_intraday
(
company_id,
trade_datetime,
interval_minutes,
open_price,
high_price,
low_price,
close_price,
volume
)

VALUES
(
%s,%s,%s,%s,%s,%s,%s,%s
)

ON DUPLICATE KEY UPDATE

open_price=VALUES(open_price),

high_price=VALUES(high_price),

low_price=VALUES(low_price),

close_price=VALUES(close_price),

volume=VALUES(volume)
"""

# ----------------------------------------------------
# interval string -> minutes
# ----------------------------------------------------

interval_map = {
    "1m":1,
    "2m":2,
    "5m":5,
    "15m":15,
    "30m":30,
    "60m":60,
    "90m":90
}

interval_minutes = interval_map[INTRADAY_INTERVAL]

# ----------------------------------------------------
# LOOP
# ----------------------------------------------------

for company in companies:

    company_id = company["company_id"]
    ticker = company["ticker"]

    print()
    print("=" * 60)
    print(ticker)

    try:

        stock = yf.Ticker(ticker)

        df = stock.history(

            start=INTRADAY_START_DATE,

            end=datetime.today(),

            interval=INTRADAY_INTERVAL,

            auto_adjust=False,

            actions=False

        )

    except Exception as ex:

        print(ex)

        continue

    if df.empty:

        print("No data returned.")

        continue

    df.reset_index(inplace=True)

    inserted = 0

    for _, record in df.iterrows():

        if pd.isna(record["Close"]):
            continue

        values = (

            company_id,

            record["Datetime"].to_pydatetime(),

            interval_minutes,

            float(record["Open"]),

            float(record["High"]),

            float(record["Low"]),

            float(record["Close"]),

            int(record["Volume"])

        )

        cursor.execute(UPSERT_SQL, values)

        inserted += 1

    connection.commit()

    print(f"{inserted} rows inserted/updated.")

cursor.close()

connection.close()

print()
print("Intraday loading complete.")