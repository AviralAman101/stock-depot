# stock-depot

# 📈 Stock Market Data Warehouse using MySQL & Python

## Overview

This project implements a complete Stock Market Data Warehouse using **MySQL** as the database and **Python** as the ETL (Extract, Transform, Load) engine.

The objective of the project is to automatically fetch stock market data for multiple companies from online financial APIs, transform the data into a relational format, and store it in a normalized SQL database.

The system is designed as a daily ETL pipeline that can be executed repeatedly without creating duplicate records.

---

# Project Objectives

- Build a normalized SQL database for stock market data
- Download historical and latest market data automatically
- Support incremental daily updates
- Prevent duplicate records using UPSERT logic
- Store both historical and current financial statements
- Generate an ER Diagram for the complete database
- Enable SQL-based financial analysis and reporting

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python 3.x |
| Database | MySQL 8.x |
| Database Tool | DBeaver |
| Data Source | Yahoo Finance (yfinance) |
| Python Libraries | yfinance, pandas, mysql-connector-python |
| Version Control | Git / GitHub |

---

# Project Structure

```
StockMarketETL/

│
├── config.py
│
├── load_master_data.py
├── load_daily_prices.py
├── load_intraday_prices.py
├── load_fundamentals.py
├── load_income_statements.py
├── balance_sheet.py
├── cash_flow.py
├── corporate_actions.py
│
├── main.py
│
├── README.md
│
└── sql/
    ├── schema.sql
    └── sample_queries.sql
```

---

# Database Design

The project uses a normalized relational schema.

```
Exchange
    │
    │
Companies
    │
    ├───────────────┐
    │               │
    │               │
Daily Prices        Intraday Prices
    │
    │
Fundamentals
    │
Income Statements
    │
Balance Sheets
    │
Cash Flow Statements
    │
Corporate Actions
```

---

# Database Tables

## 1. Exchanges

Stores stock exchange information.

Example:

- NSE
- BSE
- NASDAQ
- NYSE

---

## 2. Companies

Stores master information about companies.

Examples:

- Ticker
- Company Name
- Sector
- Industry
- Exchange

---

## 3. Stock Prices (Daily)

Stores daily OHLCV market data.

Columns include

- Open
- High
- Low
- Close
- Adjusted Close
- Volume

Supports historical data for multiple years.

Primary ETL Script

```
load_daily_prices.py
```

Features

- Incremental loading
- Configurable start date
- UPSERT support
- Duplicate prevention

---

## 4. Stock Prices (Intraday)

Stores intraday market prices.

Supported intervals include

- 1 Minute
- 5 Minute
- 15 Minute
- 30 Minute
- 60 Minute

Primary ETL Script

```
load_intraday_prices.py
```

Features

- Configurable interval
- Configurable start date
- UPSERT support

---

## 5. Fundamentals

Stores current valuation and financial ratios.

Example metrics

- Market Cap
- Enterprise Value
- PE Ratio
- Forward PE
- PEG Ratio
- Price to Book
- EPS
- ROE
- ROA
- Current Ratio
- Debt to Equity
- Beta
- Dividend Yield

Primary Script

```
load_fundamentals.py
```

---

## 6. Income Statements

Stores annual and quarterly income statements.

Example metrics

- Revenue
- Gross Profit
- Operating Income
- Pretax Income
- Net Income
- EPS

Primary Script

```
load_income_statements.py
```

---

## 7. Balance Sheets

Stores annual and quarterly balance sheets.

Example metrics

- Total Assets
- Total Liabilities
- Shareholders Equity
- Cash & Cash Equivalents
- Inventory
- Current Assets
- Current Liabilities
- Long Term Debt

Primary Script

```
balance_sheet.py
```

---

## 8. Cash Flow Statements

Stores annual and quarterly cash flow statements.

Example metrics

- Operating Cash Flow
- Investing Cash Flow
- Financing Cash Flow
- Capital Expenditure
- Free Cash Flow
- Beginning Cash Position
- Ending Cash Position

Primary Script

```
cash_flow.py
```

---

## 9. Corporate Actions

Stores important corporate events.

Currently supported

- Dividends
- Stock Splits

Primary Script

```
corporate_actions.py
```

---

# ETL Workflow

The ETL process follows the workflow below.

```
Read Companies

        │

        ▼

Connect to Yahoo Finance API

        │

        ▼

Download Dataset

        │

        ▼

Transform Data

        │

        ▼

Generate SQL INSERT / UPSERT

        │

        ▼

Store into MySQL

        │

        ▼

Commit Transaction

        │

        ▼

Process Next Company
```

---

# Incremental Loading Strategy

The project supports incremental updates.

For every execution,

1. Read latest data available in MySQL.
2. Download only new records (or a configurable date range).
3. Execute UPSERT statements.
4. Prevent duplicate records.

This allows the scripts to be executed daily without manual intervention.

---

# Duplicate Prevention

Duplicate records are prevented using

```sql
UNIQUE (...)
```

combined with

```sql
INSERT ...

ON DUPLICATE KEY UPDATE
```

This ensures

- First execution → INSERT
- Subsequent executions → UPDATE

---

# Data Source

Financial data is downloaded from

Yahoo Finance

using the Python package

```
yfinance
```

The project currently supports approximately 50 configurable companies.

---

# Configuration

Project settings are stored inside

```
config.py
```

Example

```python
DB_CONFIG = {

    "host":"localhost",

    "user":"root",

    "password":"password",

    "database":"stocks_depot"

}

DEFAULT_START_DATE="2021-01-01"

INTRADAY_INTERVAL="5m"

INTRADAY_START_DATE="2026-06-01"
```

---

# Running the Project

Run individual ETL scripts

```bash
python load_master_data.py

python load_daily_prices.py

python load_intraday_prices.py

python load_fundamentals.py

python load_income_statements.py

python balance_sheet.py

python cash_flow.py

python corporate_actions.py
```

Or execute everything together

```bash
python main.py
```

---

# Features Implemented

- Normalized relational database
- Configurable ETL pipeline
- Historical data loading
- Daily incremental loading
- Annual financial statements
- Quarterly financial statements
- Corporate actions
- UPSERT logic
- Duplicate prevention
- Modular Python architecture
- MySQL integration
- DBeaver compatible

---

# Future Enhancements

The following modules can be added in future versions.

- Technical Indicators
- Insider Transactions
- Institutional Holdings
- Mutual Fund Holdings
- Analyst Recommendations
- Earnings Calendar
- Economic Indicators
- News Sentiment Analysis
- Portfolio Analytics Dashboard
- Power BI Integration
- Tableau Dashboard
- Machine Learning based Stock Prediction

---

Executive MBA (Analytics)

Indian Institute of Management Kashipur

---

# Disclaimer

This project is intended for academic and educational purposes.

Financial data is sourced from publicly available APIs and should not be considered financial advice.
