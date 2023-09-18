import yfinance as yf
import pandas as pd

import datetime

today_date = datetime.date.today()
today = today_date.strftime('%Y-%m-%d')

stock_symbol = "^NSEBANK"
start_date = "2023-09-15"
ticker = 'samriddha'

panda_data = {'Name':[],
              'Open': [],
              'High': [],
              'Low': [],
              'Close': [],
              'Volume': []}

data = yf.download(stock_symbol, start=start_date)
df = pd.DataFrame(panda_data)

df['Open'] = data['Open']
df['High'] = data['High']
df['Low'] = data['Low']
df['Close'] = data['Close']
df['Volume'] = data['Volume']
df['Name'] = ticker

print(df)
