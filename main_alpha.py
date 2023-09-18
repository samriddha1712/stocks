import requests

# Replace with your AlphaVantage API key
API_KEY = 'DFBCA1UQ8Z5PZHC4'
SYMBOL = 'IBM'  # Replace with the symbol of the stock you want to track

# Make a request to get real-time stock data
url = f'https://www.alphavantage.co/query'
params = {
    'function': 'TIME_SERIES_INTRADAY',
    'symbol': SYMBOL,
    'interval': '1min',  # Adjust the interval as needed (e.g., 1min, 5min, 15min)
    'apikey': API_KEY,
}

response = requests.get(url, params=params)
data = response.json()

# Print the most recent data point
latest_time = max(data['Time Series (1min)'].keys())
latest_price = float(data['Time Series (1min)'][latest_time]['1. open'])

print(f'Latest real-time price for {SYMBOL}: ${latest_price:.2f}')