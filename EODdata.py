import requests as re
import json
import time
import csv
import os
import threading
from datetime import datetime
import win32com.client as wcl
import pythoncom
import random 
import subprocess
import multiprocessing
import glob

# ab = wcl.Dispatch("Broker.Application")
Date = datetime.now().strftime('%Y/%m/%d')
interval = 5




def live_price(ticker, instrument):
    # today = datetime.now().strftime('%Y-%m-%d')
    today = "2023-11-10"
    url = f"https://kite.zerodha.com/oms/instruments/historical/{instrument}/minute?user_id=DQ5843&oi=1&from={today}&to={today}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
        'authorization': 'enctoken 06mUkdY0vXGhVeYrFfuVgRvh3S4UED1Us1DLtTXrS1BV30bksp5zkhvpOxPR8O6+b7BINzgJeT57GKvc6aBOzO9+XPoZV+6n+foerfMWCEKMKtzM8h6p3w=='
    }

    response = re.get(url, headers=headers)

    parsed_data = json.loads(response.text)
    
    candles = parsed_data['data']['candles']
    
    
    
    csv_filename = f'output_{ticker}.csv'
    
    
    with open(csv_filename, 'w', newline='') as csv_file:
        fieldnames = ['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Time']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Write candle data to CSV
        for candle in candles:
            timestamp = datetime.strptime(candle[0], "%Y-%m-%dT%H:%M:%S%z")
            formatted_time = timestamp.strftime("%H:%M:%S")

            writer.writerow({
                'Ticker' : ticker,
                'Date' : Date,
                'Open': candle[1],
                'High': candle[2],
                'Low': candle[3],
                'Close': candle[4],
                'Volume' : candle[5],
                'Time': formatted_time,
            })
            
        
        subprocess.call(["python", "connectionAmi.py", csv_filename])



def main():
    
    with open('result.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            ticker, instrument_token = row[0], row[2]
            live_price(ticker, instrument_token)
  
main()