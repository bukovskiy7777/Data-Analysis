import json
import mysql.connector
import requests


def load_config(config_path="config.json"):
    """Load API credentials and Database configuration from JSON file."""
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{config_path}'.")
        return None


def fetch_exchange_rates(api_key, date="latest", symbols="", base="USD"):
    """Fetch exchange rates from APILayer Exchange Rates Data API endpoint."""
    url = f"https://api.apilayer.com/exchangerates_data/{date}"

    # Pass base and symbols via query parameters if provided
    params = {}
    if symbols:
        params["symbols"] = symbols
    if base:
        params["base"] = base

    headers = {"apikey": api_key}

    try:
        # Request data using the specified APILayer code pattern
        response = requests.request("GET", url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        if data.get("success"):
            return data
        else:
            print("API returned unsuccessful response:", data)
            return None

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None


def save_to_mysql(data, db_config):
    """Save fetched currency exchange rates into MySQL database."""
    if not data:
        return

    base_currency = data.get("base")
    rate_date = data.get("date")
    rates = data.get("rates", {})

    try:
        # Establish database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Upsert query to prevent duplicate records for the same date/currency pair
        insert_query = """
            INSERT INTO exchange_rates (rate_date, base_currency, target_currency, rate)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE rate = VALUES(rate);
        """

        # Prepare batch payload for efficient insertion
        records_to_insert = [
            (rate_date, base_currency, target_curr, float(rate_val))
            for target_curr, rate_val in rates.items()
        ]

        # Execute bulk insert
        cursor.executemany(insert_query, records_to_insert)
        conn.commit()

        print(
            f"Successfully saved {len(records_to_insert)} rates for date {rate_date}."
        )

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if "conn" in locals() and conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    # Load settings from external config
    config = load_config("config.json")

    if config:
        api_key = config.get("API_KEY")
        db_config = config.get("DB_CONFIG")

        # Fetch exchange rates for all currencies and specific date
        rates_data = fetch_exchange_rates(api_key, date="2025-12-31", base="USD")

        # Save results to MySQL DB
        if rates_data:
            save_to_mysql(rates_data, db_config)