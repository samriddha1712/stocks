import requests as re
from bs4 import BeautifulSoup as bs
import yfinance as yf
import datetime
import pandas as pd
import pandas_market_calendars as mcal

def market_is_open(date):
    result = mcal.get_calendar("NYSE").schedule(start_date=date, end_date=date)
    return not result.empty



def market_open():
    current_time = datetime.datetime.now().time()
    market_open = datetime.time(9, 15)
    market_close = datetime.time(15, 30)

    return market_open <= current_time <= market_close

today_date = datetime.date.today()
today = today_date.strftime('%Y-%m-%d')
day_name = today_date.strftime('%A')


data_list = []

with open('ticker_price.txt', 'r') as file:
    for line in file:
        ticker = line.strip()
        
        url = f"https://finance.yahoo.com/quote/{ticker}"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
        }
        response = re.get(url=url, headers=headers)

        soup = bs(response.text, 'html.parser')

        price = soup.find("fin-streamer", {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'})

        try:
            if price:
                if market_is_open(today):
                    if market_open():
                        data = yf.download(ticker, start=today)
                        if not data.empty:  
                            data['Live'] = price.text
                            data['Ticker'] = ticker
                            data = data.drop(['Close'], axis=1)
                            data = data.drop(['Adj Close'], axis=1)
                            data_list.append(data)
                        else:
                            print(f"Rest of data not available for {ticker}")
                    else:
                        if datetime.time(9, 15) < datetime.datetime.now().time():
                            data = yf.download(ticker, start=today)
                            if not data.empty:
                                data['Ticker'] = ticker
                                data_list.append(data)
                            else:
                                print(f"No data available for {ticker}")
                        else:
                            if day_name == "Monday":
                                result = datetime.date.today() - datetime.timedelta(days=2)
                            else:
                                result = datetime.date.today() - datetime.timedelta(days=1)
                                result_str = result.strftime('%Y-%m-%d')
                                data = yf.download(ticker, start=result_str)
                                if not data.empty:  
                                    data['Ticker'] = ticker
                                    data_list.append(data)
                                else:
                                    print(f"No data available for {ticker}")
                else:
                    if day_name == "Monday":
                        result = datetime.date.today() - datetime.timedelta(days=2)
                    else:
                        result = datetime.date.today() - datetime.timedelta(days=1)
                        result_str = result.strftime('%Y-%m-%d')
                        data = yf.download(ticker, start=result_str)
                        if not data.empty:  
                            data['Ticker'] = ticker
                            data_list.append(data)
                        else:
                            print(f"No data available for {ticker}")
            else:
                print(f"Price not found for {ticker}")

        except Exception as e:
            print(f"Error for {ticker}: {e}")


df = pd.concat(data_list, ignore_index=True)


print(df)
