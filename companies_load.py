import mysql.connector
import yfinance as yf

# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "Aviral",
    "password": "Aviral123",
    "database": "stocks_depot"
}

# ==========================================================
# EXCHANGES
# ==========================================================

EXCHANGES = [

    ("NSE", "National Stock Exchange", "India", "INR", "Asia/Kolkata",
     "https://www.nseindia.com"),

    ("BSE", "Bombay Stock Exchange", "India", "INR", "Asia/Kolkata",
     "https://www.bseindia.com")

]

# ==========================================================
# SAMPLE 50 NSE COMPANIES
# ==========================================================

COMPANIES = [

"RELIANCE.NS",
"TCS.NS",
"INFY.NS",
"HDFCBANK.NS",
"ICICIBANK.NS",
"SBIN.NS",
"LT.NS",
"ITC.NS",
"BHARTIARTL.NS",
"KOTAKBANK.NS",

"AXISBANK.NS",
"ASIANPAINT.NS",
"MARUTI.NS",
"BAJFINANCE.NS",
"HCLTECH.NS",
"ULTRACEMCO.NS",
"SUNPHARMA.NS",
"TITAN.NS",
"WIPRO.NS",
"NESTLEIND.NS",

"POWERGRID.NS",
"ONGC.NS",
"NTPC.NS",
"TATAMOTORS.NS",
"ADANIENT.NS",
"ADANIPORTS.NS",
"TECHM.NS",
"COALINDIA.NS",
"BAJAJFINSV.NS",
"BAJAJ-AUTO.NS",

"INDUSINDBK.NS",
"JSWSTEEL.NS",
"HINDALCO.NS",
"DRREDDY.NS",
"CIPLA.NS",
"EICHERMOT.NS",
"DIVISLAB.NS",
"GRASIM.NS",
"HEROMOTOCO.NS",
"BPCL.NS",

"BRITANNIA.NS",
"SHREECEM.NS",
"TATASTEEL.NS",
"APOLLOHOSP.NS",
"HDFCLIFE.NS",
"SBILIFE.NS",
"PIDILITIND.NS",
"DABUR.NS",
"ICICIPRULI.NS",
"BEL.NS"

]

# ==========================================================
# CONNECT
# ==========================================================

connection = mysql.connector.connect(**DB_CONFIG)

cursor = connection.cursor()

# ==========================================================
# INSERT EXCHANGES
# ==========================================================

exchange_sql = """
INSERT INTO exchanges
(
exchange_code,
exchange_name,
country,
currency,
timezone,
website
)

VALUES
(%s,%s,%s,%s,%s,%s)

ON DUPLICATE KEY UPDATE

exchange_name=VALUES(exchange_name),
country=VALUES(country),
currency=VALUES(currency),
timezone=VALUES(timezone),
website=VALUES(website)
"""

for exchange in EXCHANGES:

    cursor.execute(exchange_sql, exchange)

connection.commit()

print("Exchange table populated.")

# ==========================================================
# GET NSE EXCHANGE ID
# ==========================================================

cursor.execute(
"""
SELECT exchange_id
FROM exchanges
WHERE exchange_code='NSE'
"""
)

exchange_id = cursor.fetchone()[0]

# ==========================================================
# COMPANY INSERT SQL
# ==========================================================

company_sql = """

INSERT INTO companies
(

ticker,

company_name,

exchange_id,

sector,

industry,

market_cap,

shares_outstanding,

website

)

VALUES

(%s,%s,%s,%s,%s,%s,%s,%s)

ON DUPLICATE KEY UPDATE

company_name=VALUES(company_name),

sector=VALUES(sector),

industry=VALUES(industry),

market_cap=VALUES(market_cap),

shares_outstanding=VALUES(shares_outstanding),

website=VALUES(website)

"""

# ==========================================================
# DOWNLOAD COMPANY INFORMATION
# ==========================================================

for ticker in COMPANIES:

    try:

        print(f"Downloading {ticker}")

        stock = yf.Ticker(ticker)

        info = stock.info

        values = (

            ticker,

            info.get("longName"),

            exchange_id,

            info.get("sector"),

            info.get("industry"),

            info.get("marketCap"),

            info.get("sharesOutstanding"),

            info.get("website")

        )

        cursor.execute(company_sql, values)

        connection.commit()

        print("Inserted:", ticker)

    except Exception as ex:

        print("Failed:", ticker)

        print(ex)

cursor.close()

connection.close()

print()

print("Master data loading completed.")