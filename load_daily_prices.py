import mysql.connector
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

from config import DB_CONFIG, DEFAULT_START_DATE

# --------------------------------------------------------
# CONNECT TO MYSQL
# --------------------------------------------------------

connection = mysql.connector.connect(**DB_CONFIG)

cursor = connection.cursor(dictionary=True)

# --------------------------------------------------------
# GET ALL COMPANIES
# --------------------------------------------------------

cursor.execute("""
SELECT company_id,
       ticker
FROM companies
ORDER BY company_id
""")

companies = cursor.fetchall()

print(f"Found {len(companies)} companies.")

# --------------------------------------------------------
# SQL FOR UPSERT
# --------------------------------------------------------

UPSERT_SQL = """
INSERT INTO stock_prices_daily
(
company_id,
trade_date,
open_price,
high_price,
low_price,
close_price,
adjusted_close,
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
adjusted_close=VALUES(adjusted_close),
volume=VALUES(volume)
"""

# --------------------------------------------------------
# LOOP THROUGH COMPANIES
# --------------------------------------------------------

for company in companies:

    company_id = company["company_id"]
    ticker = company["ticker"]

    print()
    print("=" * 60)
    print(f"Processing {ticker}")

    # ---------------------------------------------
    # FIND LAST STORED DATE
    # ---------------------------------------------

    cursor.execute("""
    SELECT MAX(trade_date) AS last_date
    FROM stock_prices_daily
    WHERE company_id=%s
    """, (company_id,))

    row = cursor.fetchone()

    if row["last_date"] is None:

        start_date = DEFAULT_START_DATE

        print("No previous data found.")
        print("Downloading complete history...")

    else:

        start_date = row["last_date"] + timedelta(days=1)

        print("Latest stored date:", row["last_date"])
        print("Downloading from:", start_date)

    end_date = datetime.today().strftime("%Y-%m-%d")

    # ---------------------------------------------
    # DOWNLOAD FROM YAHOO
    # ---------------------------------------------

    try:

        df = yf.download(
            tickers=ticker,
            start=str(start_date),
            end=end_date,
            interval="1d",
            auto_adjust=False,
            progress=False,
            threads=False
        )
        # Flatten MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
    except Exception as ex:

        print("Download failed.")
        print(ex)
        continue

    if df.empty:

        print("Already up-to-date.")
        continue

    # ---------------------------------------------
    # RESET INDEX
    # ---------------------------------------------

    df.reset_index(inplace=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    # ---------------------------------------------
    # LOOP THROUGH DATAFRAME
    # ---------------------------------------------

    inserted = 0

    for _, record in df.iterrows():

        values = (

            company_id,

            record["Date"].date(),

            None if pd.isna(record["Open"]) else float(record["Open"]),

            None if pd.isna(record["High"]) else float(record["High"]),

            None if pd.isna(record["Low"]) else float(record["Low"]),

            None if pd.isna(record["Close"]) else float(record["Close"]),

            None if pd.isna(record["Adj Close"]) else float(record["Adj Close"]),

            0 if pd.isna(record["Volume"]) else int(record["Volume"])

        )

        cursor.execute(UPSERT_SQL, values)

        inserted += 1

    connection.commit()

    print(f"{inserted} rows inserted/updated.")

# --------------------------------------------------------
# CLOSE CONNECTION
# --------------------------------------------------------

cursor.close()

connection.close()

print()
print("Daily price loading completed successfully.")
print(yf.__version__)
