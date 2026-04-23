# check_symbols.py
from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv('BINANCE_API_KEY'),
    os.getenv('BINANCE_API_SECRET'),
    testnet=True
)

# Get exchange info for futures
exchange_info = client.futures_exchange_info()

# Print all USDT-M symbols
print("Available Trading Symbols:\n")
for symbol in exchange_info['symbols']:
    if symbol['symbol'].endswith('USDT'):
        print(f"  ✅ {symbol['symbol']}")

print(f"\nTotal USDT-M pairs: {len([s for s in exchange_info['symbols'] if s['symbol'].endswith('USDT')])}")