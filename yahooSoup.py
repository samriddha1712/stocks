import requests as re
from bs4 import BeautifulSoup as bs
import yfinance as yf
import datetime
import pandas as pd
import pandas_market_calendars as mcal


def market_is_open(date):
    result = mcal.get_calendar("NYSE").schedule(start_date=date, end_date=date)
    return result.empty == False

# check if market is open today





def market_open():
    current_time = datetime.datetime.now().time()
    market_open = datetime.time(9, 15)  
    market_close = datetime.time(15, 30)
    
    if market_open <= current_time <= market_close:
        return True
    else:
        return False


today_date = datetime.date.today()
today = today_date.strftime('%Y-%m-%d')
day_name = today_date.strftime('%A')

past_data = {'Ticker':[],
              'Open':[],
              'High':[],
              'Low':[],
              'Close':[],
              'Volume':[]}

live_data = {'Ticker':[],
              'Live':[],
              'Open':[],
              'High':[],
              'Low':[],
              'Volume':[]}

with open('ticker_price.txt', 'r') as file:
    df_live = pd.DataFrame(live_data)
    df_past = pd.DataFrame(past_data)
    for line in file:
        ticker = line.strip()
        # print(ticker)
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
                        # print(f"{ticker} : Rs.{price.text} : {data.Open} : {data.High} : {data.Low} : {data.Close} : {data.Volume}")
                        df_live['Ticker'] = ticker
                        df_live['Live'] = price.text
                        df_live['Open'] = data['Open']
                        df_live['High'] = data['High']
                        df_live['Low'] = data['Low']
                        df_live['Volume'] = data['Volume']
                        print(df_live)
                        
                            
                    else:
                        if (datetime.time(9, 15) < datetime.datetime.now().time()):
                            df_past['Ticker'] = ticker
                            df_past['Close'] = data['Close']
                            df_past['Open'] = data['Open']
                            df_past['High'] = data['High']
                            df_past['Low'] = data['Low']
                            df_past['Volume'] = data['Volume']
                            print(df_past)
                        else:
                            if (day_name == "Monday"):
                                result = datetime.date.today() - datetime.timedelta(days=2)
                                result_str = result.strftime('%Y-%m-%d')
                                data = yf.download(ticker, start=result_str)
                                df_past['Ticker'] = ticker
                                df_past['Close'] = data['Close']
                                df_past['Open'] = data['Open']
                                df_past['High'] = data['High']
                                df_past['Low'] = data['Low']
                                df_past['Volume'] = data['Volume']
                                print(df_past)
                            else:
                                result = datetime.date.today() - datetime.timedelta(days=1)
                                result_str = result.strftime('%Y-%m-%d')
                                data = yf.download(ticker, start=result_str)
                                df_past['Ticker'] = ticker
                                df_past['Close'] = data['Close']
                                df_past['Open'] = data['Open']
                                df_past['High'] = data['High']
                                df_past['Low'] = data['Low']
                                df_past['Volume'] = data['Volume']
                                print(df_past)
                else:
                    if (day_name == "Monday"):
                        result = datetime.date.today() - datetime.timedelta(days=2)
                        result_str = result.strftime('%Y-%m-%d')
                        data = yf.download(ticker, start=result_str)
                        df_past['Ticker'] = ticker
                        df_past['Close'] = data['Close']
                        df_past['Open'] = data['Open']
                        df_past['High'] = data['High']
                        df_past['Low'] = data['Low']
                        df_past['Volume'] = data['Volume']
                        print(df_past)
                    else:
                        result = datetime.date.today() - datetime.timedelta(days=1)
                        result_str = result.strftime('%Y-%m-%d')
                        data = yf.download(ticker, start=result_str)
                        df_past['Ticker'] = ticker
                        df_past['Close'] = data['Close']
                        df_past['Open'] = data['Open']
                        df_past['High'] = data['High']
                        df_past['Low'] = data['Low']
                        df_past['Volume'] = data['Volume']
                        print(df_past)
            else:
                print(f"Price not found for {ticker}")

        except Exception as e:
            print(f"Error for {ticker}: {e}")
