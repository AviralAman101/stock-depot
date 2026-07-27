DB_CONFIG = {
    "host": "localhost",
    "user": "Aviral",
    "password": "Aviral123",
    "database": "stocks_depot"
}


DEFAULT_START_DATE="2026-07-20"

DOWNLOAD_MODE = "INCREMENTAL"
# Options:
# "FULL"        -> Always download from DEFAULT_START_DATE
# "INCREMENTAL" -> Continue from the latest date in the database

INTRADAY_INTERVAL = "5m"

INTRADAY_LOOKBACK_DAYS = 30

# Intraday loader
INTRADAY_INTERVAL = "5m"
INTRADAY_START_DATE = "2026-07-20"