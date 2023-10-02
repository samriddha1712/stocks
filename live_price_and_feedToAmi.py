import requests as re
import json
import time
from datetime import date, datetime
import csv
import os
import sys
import glob
import win32com.client


imp_tbl = [
    {
        'db': r"C:\Program Files\AmiBroker\Zerodah",
        'data': "",  
        'format': r"wizard.format"
    },
]

def ImportData(ab, lst):
    for l in lst:
        print("Loading database {}".format(os.path.split(l['db'])[1]))
        ab.LoadDatabase(l['db'])
        f_lst = sorted(set(glob.glob(l['data'])))
        for f in f_lst:
            try:
                print("Importing datafile {}, using format {}".format(f, l['format']))
                ab.Import(0, f, l['format'])
            except Exception as e:
                print(f"Error importing datafile {f}: {str(e)}")
            else:
                (newpath, filename) = os.path.split(f)
                archive_folder = os.path.join(newpath, "archive")
                os.makedirs(archive_folder, exist_ok=True)
                os.rename(f, os.path.join(archive_folder, filename))
                print("Import complete")

        print("Saving Amibroker")
        ab.RefreshAll()
        ab.SaveDatabase()
        print("OK")

def main():
    while True:
        output_data = []

        with open('LiveTesting1.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                ticker, Instrument_token = row[0], row[1]

                today = date.today()
                now = datetime.now()
                dt_time = now.strftime("%H:%M:%S")
                today = "2023-09-29"
                dt_time1 = now.strftime("%H-%M-%S")

                url = f"https://kite.zerodha.com/oms/instruments/historical/{Instrument_token}/day?user_id=DQ5843&oi=1&from={today}&to={today}"

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
                    'authorization': 'enctoken zCLa2eQgEAeZAp9MTIyU6tCoJFqirIWI4PvP5vO0t7eQwRDAcg3CVc4YVCgn60n8CZgy898SPkrVL1WaagLIhhZihRFbaxRKbUdVmAWvZSlPA07c9yJekg=='
                }

                response = re.get(url, headers=headers)

                parsed_data = json.loads(response.text)

                candles = parsed_data['data']['candles'][0]
                opens = candles[1]
                high = candles[2]
                low = candles[3]
                live_value = candles[4]
                volume = candles[5]

                output_data.append([ticker, today, opens, high, low, live_value, volume, dt_time])

                print(
                    ticker + " : " + today + " : " + str(opens) + " : " + str(high) + " : " + str(low) + " : " + str(
                        live_value) + " : " + str(volume) + " : " + dt_time)

            csv_filename = f"output_data_{dt_time1}.csv"
            imp_tbl[0]['data'] = os.path.join("D:\PythonProjects\Stocks", csv_filename)

            with open(csv_filename, "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Ticker", "Date", "Open", "High", "Low", "Close", "Volume", "Time"])
                csv_writer.writerows(output_data)

            ImportData(oAB, imp_tbl)
            output_data = []
            time.sleep(5)

if __name__ == '__main__':
    oAB = win32com.client.Dispatch("Broker.Application")
    main()
