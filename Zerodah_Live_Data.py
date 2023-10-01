import requests as re
import json
import time
from datetime import date, datetime
import csv

output_data = []

while True:
    with open('LiveTesting1.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            ticker, Instrument_token = row[0], row[1]
                        
            today = date.today()
            now = datetime.now()
            dt_time = now.strftime("%H-%M-%S")
            today = "2023-09-29"

            
            url = f"https://kite.zerodha.com/oms/instruments/historical/{Instrument_token}/day?user_id=DQ5843&oi=1&from={today}&to={today}"
            
            headers= {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
                'authorization': 'enctoken SfNtPL59Rf7Ywdd205ocv+4oBEab7Y/azHuQdlgKYeuekJAMfuI2cYSEZmXdh1yBLvTPbswEnfb6dXaTaDJxi3rDa5oaF8HHc8TPtBmdpizYUd2GO3Y83Q=='
            }
            
            response = re.get(url,headers=headers)
            
            parsed_data = json.loads(response.text)
            
            candles = parsed_data['data']['candles'][0]
            opens= candles[1]
            high= candles[2]
            low= candles[3]
            live_value= candles[4]
            volume= candles[5]
            
            output_data.append([ticker, today, opens, high, low, live_value, volume, dt_time])
            
            print (ticker + " : " + today + " : " + str(opens) + " : " + str(high) + " : " + str(low) + " : " + str(live_value) + " : " + str(volume) + " : " + dt_time)        
                    
        csv_filename = f"output_data_{dt_time}.csv"
        with open(csv_filename, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Ticker", "YMD", "Open", "High", "Low", "Close", "Volume"])
            csv_writer.writerows(output_data)
        output_data=[]          
        time.sleep(5)            
                