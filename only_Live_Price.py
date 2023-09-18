import requests as re
from bs4 import BeautifulSoup as bs
import csv


with open('ticker_price.csv', 'w', newline='') as csvfile:
    
    csvwriter = csv.writer(csvfile)
    
    
    csvwriter.writerow(['Ticker', 'Live Price', 'Open Price'])

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
            open = soup.find("td",{'class': 'Ta(end) Fw(600) Lh(14px)'})

            
            live_price = price.text if price else "N/A"
            opening_price = open.text if open else "N/A"

            
            csvwriter.writerow([ticker, live_price, opening_price])

            print(f"{ticker} : Rs.{live_price} : Rs.{opening_price}")
