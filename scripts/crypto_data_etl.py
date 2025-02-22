import os
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

CMC_API_KEY = os.getenv("CMC_API_KEY")
DB_HOST = "localhost"
DB_NAME = "crypto_data_db"
DB_USER = "user"
DB_PASS = "pass"

API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
HEADERS = {"X-CMC_PRO_API_KEY": CMC_API_KEY}

def fetch_crypto_data():
    response = requests.get(API_URL, headers=HEADERS, params={"limit": 100, "convert": "USD"})
    data = response.json()
    return data["data"]

def save_to_db(data):
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cursor = conn.cursor()
    
    for crypto in data:
        cursor.execute(
            "INSERT INTO crypto_data (symbol, price, volume, market_cap) VALUES (%s, %s, %s, %s)",
            (crypto["symbol"], crypto["quote"]["USD"]["price"], crypto["quote"]["USD"]["volume_24h"], crypto["quote"]["USD"]["market_cap"])
        )
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    crypto_data = fetch_crypto_data()
    save_to_db(crypto_data)
