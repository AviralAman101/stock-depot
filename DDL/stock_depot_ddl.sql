/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `balance_sheets` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `report_date` date NOT NULL,
  `report_type` enum('Annual','Quarterly') NOT NULL,
  `cash_and_cash_equivalents` bigint DEFAULT NULL,
  `inventory` bigint DEFAULT NULL,
  `current_assets` bigint DEFAULT NULL,
  `total_assets` bigint DEFAULT NULL,
  `current_liabilities` bigint DEFAULT NULL,
  `total_liabilities` bigint DEFAULT NULL,
  `long_term_debt` bigint DEFAULT NULL,
  `shareholders_equity` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `company_id` (`company_id`,`report_date`,`report_type`),
  CONSTRAINT `balance_sheets_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1123 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cash_flow_statements` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `report_date` date NOT NULL,
  `report_type` enum('Annual','Quarterly') NOT NULL,
  `operating_cash_flow` bigint DEFAULT NULL COMMENT 'Cash generated from operating activities',
  `investing_cash_flow` bigint DEFAULT NULL COMMENT 'Cash generated/used in investing activities',
  `financing_cash_flow` bigint DEFAULT NULL COMMENT 'Cash generated/used in financing activities',
  `capital_expenditure` bigint DEFAULT NULL COMMENT 'Capital expenditure (CapEx)',
  `free_cash_flow` bigint DEFAULT NULL COMMENT 'Free Cash Flow',
  `beginning_cash_position` bigint DEFAULT NULL COMMENT 'Cash balance at beginning of period',
  `end_cash_position` bigint DEFAULT NULL COMMENT 'Cash balance at end of period',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_cashflow` (`company_id`,`report_date`,`report_type`),
  CONSTRAINT `fk_cashflow_company` FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=775 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `companies` (
  `company_id` int NOT NULL AUTO_INCREMENT,
  `ticker` varchar(20) NOT NULL,
  `company_name` varchar(200) NOT NULL,
  `exchange_id` int NOT NULL,
  `isin` varchar(20) DEFAULT NULL,
  `sector` varchar(100) DEFAULT NULL,
  `industry` varchar(100) DEFAULT NULL,
  `market_cap` bigint DEFAULT NULL,
  `shares_outstanding` bigint DEFAULT NULL,
  `listing_date` date DEFAULT NULL,
  `headquarters` varchar(150) DEFAULT NULL,
  `website` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`company_id`),
  UNIQUE KEY `ticker` (`ticker`),
  KEY `exchange_id` (`exchange_id`),
  CONSTRAINT `companies_ibfk_1` FOREIGN KEY (`exchange_id`) REFERENCES `exchanges` (`exchange_id`)
) ENGINE=InnoDB AUTO_INCREMENT=391 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corporate_actions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `action_date` date NOT NULL,
  `action_type` enum('DIVIDEND','STOCK_SPLIT') NOT NULL,
  `amount` decimal(18,6) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `company_id` (`company_id`,`action_date`,`action_type`),
  CONSTRAINT `corporate_actions_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4136 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exchanges` (
  `exchange_id` int NOT NULL AUTO_INCREMENT,
  `exchange_code` varchar(10) NOT NULL,
  `exchange_name` varchar(100) NOT NULL,
  `country` varchar(50) DEFAULT NULL,
  `currency` varchar(10) DEFAULT NULL,
  `timezone` varchar(50) DEFAULT NULL,
  `website` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`exchange_id`),
  UNIQUE KEY `exchange_code` (`exchange_code`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fundamentals` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `snapshot_date` date NOT NULL,
  `market_cap` bigint DEFAULT NULL,
  `enterprise_value` bigint DEFAULT NULL,
  `pe_ratio` decimal(12,2) DEFAULT NULL,
  `forward_pe` decimal(12,2) DEFAULT NULL,
  `peg_ratio` decimal(12,2) DEFAULT NULL,
  `pb_ratio` decimal(12,2) DEFAULT NULL,
  `eps` decimal(12,2) DEFAULT NULL,
  `roe` decimal(12,4) DEFAULT NULL,
  `roa` decimal(12,4) DEFAULT NULL,
  `debt_to_equity` decimal(12,2) DEFAULT NULL,
  `current_ratio` decimal(12,2) DEFAULT NULL,
  `quick_ratio` decimal(12,2) DEFAULT NULL,
  `dividend_yield` decimal(12,4) DEFAULT NULL,
  `beta` decimal(12,4) DEFAULT NULL,
  `fifty_two_week_high` decimal(12,2) DEFAULT NULL,
  `fifty_two_week_low` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `company_id` (`company_id`,`snapshot_date`),
  CONSTRAINT `fundamentals_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=147 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `income_statements` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `report_date` date NOT NULL,
  `report_type` enum('Annual','Quarterly') NOT NULL,
  `total_revenue` bigint DEFAULT NULL,
  `cost_of_revenue` bigint DEFAULT NULL,
  `gross_profit` bigint DEFAULT NULL,
  `operating_income` bigint DEFAULT NULL,
  `pretax_income` bigint DEFAULT NULL,
  `net_income` bigint DEFAULT NULL,
  `basic_eps` decimal(12,4) DEFAULT NULL,
  `diluted_eps` decimal(12,4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `company_id` (`company_id`,`report_date`,`report_type`),
  CONSTRAINT `income_statements_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1490 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_prices_daily` (
  `price_id` bigint NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `trade_date` date NOT NULL,
  `open_price` decimal(12,2) DEFAULT NULL,
  `high_price` decimal(12,2) DEFAULT NULL,
  `low_price` decimal(12,2) DEFAULT NULL,
  `close_price` decimal(12,2) DEFAULT NULL,
  `adjusted_close` decimal(12,2) DEFAULT NULL,
  `volume` bigint DEFAULT NULL,
  PRIMARY KEY (`price_id`),
  UNIQUE KEY `company_id` (`company_id`,`trade_date`),
  CONSTRAINT `stock_prices_daily_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32352 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_prices_intraday` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_id` int DEFAULT NULL,
  `trade_datetime` datetime DEFAULT NULL,
  `interval_minutes` int DEFAULT NULL,
  `open_price` decimal(12,2) DEFAULT NULL,
  `high_price` decimal(12,2) DEFAULT NULL,
  `low_price` decimal(12,2) DEFAULT NULL,
  `close_price` decimal(12,2) DEFAULT NULL,
  `volume` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `company_id` (`company_id`,`trade_datetime`,`interval_minutes`),
  CONSTRAINT `stock_prices_intraday_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19732 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
