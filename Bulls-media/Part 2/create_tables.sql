CREATE DATABASE IF NOT EXISTS macro_analytics;
USE macro_analytics;

-- a. Table of the exchange rates
CREATE TABLE IF NOT EXISTS exchange_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rate_date DATE NOT NULL,
    base_currency VARCHAR(3) NOT NULL,
    target_currency VARCHAR(3) NOT NULL,
    rate DECIMAL(18, 6) NOT NULL CHECK (rate > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_exchange_rate UNIQUE (rate_date, base_currency, target_currency)
);

-- b. Table of the GDP
CREATE TABLE IF NOT EXISTS gdp (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL CHECK (year BETWEEN 1900 AND 2100),
    country VARCHAR(100) NOT NULL,
    gdp_in_usd DECIMAL(20, 2) NOT NULL CHECK (gdp_in_usd >= 0),
    CONSTRAINT unique_country_year_gdp UNIQUE (country, year)
);

-- c. Table of the population
CREATE TABLE IF NOT EXISTS population (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL CHECK (year BETWEEN 1900 AND 2100),
    country VARCHAR(100) NOT NULL,
    population BIGINT NOT NULL CHECK (population >= 0),
    CONSTRAINT unique_country_year_pop UNIQUE (country, year)
);

-- d. Dimensional table of the country and its currency
CREATE TABLE IF NOT EXISTS dim_country_currency (
    country VARCHAR(100) PRIMARY KEY,
    currency_code VARCHAR(3) NOT NULL,
    country_code_alpha2 VARCHAR(2) NULL
);