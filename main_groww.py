import requests as re

response = re.get("https://groww.in/v1/api/stocks_data/v1/accord_points/exchange/NSE/segment/CASH/latest_prices_ohlc/20MICRONS.NS")
data = response.json()
live = data["ltp"]
print(live)