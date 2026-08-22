-- dim_exchange_rates
SELECT rate_date, base_currency, target_currency, rate
FROM macro_analytics.exchange_rates 
where month(rate_date) = 12 and day(rate_date) = 31;

-- dim_country_currency
select country, currency_code, country_code_alpha2 from macro_analytics.dim_country_currency;

-- fact_gdp_population
SELECT 
    g.year,
    g.country,
    c.currency_code AS native_currency,
    p.population,
    g.gdp_in_usd,
    (g.gdp_in_usd / p.population) AS gdp_per_capita_usd
FROM macro_analytics.gdp g
JOIN macro_analytics.population p ON g.country = p.country AND g.year = p.year
LEFT JOIN macro_analytics.dim_country_currency c ON g.country = c.country;