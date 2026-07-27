import mysql.connector
import yfinance as yf
from datetime import date

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

print(f"Found {len(companies)} companies.")

# --------------------------------------------------------
# UPSERT SQL
# --------------------------------------------------------

UPSERT_SQL = """
INSERT INTO fundamentals
(
company_id,
snapshot_date,
market_cap,
enterprise_value,
pe_ratio,
forward_pe,
peg_ratio,
pb_ratio,
eps,
roe,
roa,
debt_to_equity,
current_ratio,
quick_ratio,
dividend_yield,
beta,
fifty_two_week_high,
fifty_two_week_low
)

VALUES
(
%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
)

ON DUPLICATE KEY UPDATE

market_cap = VALUES(market_cap),

enterprise_value = VALUES(enterprise_value),

pe_ratio = VALUES(pe_ratio),

forward_pe = VALUES(forward_pe),

peg_ratio = VALUES(peg_ratio),

pb_ratio = VALUES(pb_ratio),

eps = VALUES(eps),

roe = VALUES(roe),

roa = VALUES(roa),

debt_to_equity = VALUES(debt_to_equity),

current_ratio = VALUES(current_ratio),

quick_ratio = VALUES(quick_ratio),

dividend_yield = VALUES(dividend_yield),

beta = VALUES(beta),

fifty_two_week_high = VALUES(fifty_two_week_high),

fifty_two_week_low = VALUES(fifty_two_week_low)
"""

# --------------------------------------------------------
# LOOP
# --------------------------------------------------------

today = date.today()

for company in companies:

    company_id = company["company_id"]
    ticker = company["ticker"]

    print("=" * 60)
    print(ticker)

    try:

        stock = yf.Ticker(ticker)

        info = stock.info

    except Exception as ex:

        print(ex)
        continue

    values = (

        company_id,

        today,

        info.get("marketCap"),

        info.get("enterpriseValue"),

        info.get("trailingPE"),

        info.get("forwardPE"),

        info.get("pegRatio"),

        info.get("priceToBook"),

        info.get("trailingEps"),

        info.get("returnOnEquity"),

        info.get("returnOnAssets"),

        info.get("debtToEquity"),

        info.get("currentRatio"),

        info.get("quickRatio"),

        info.get("dividendYield"),

        info.get("beta"),

        info.get("fiftyTwoWeekHigh"),

        info.get("fiftyTwoWeekLow")

    )

    try:

        cursor.execute(UPSERT_SQL, values)

        connection.commit()

        print("Updated")

    except Exception as ex:

        print(ex)

cursor.close()

connection.close()

print("Fundamentals loading completed.")