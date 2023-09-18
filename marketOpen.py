import pandas_market_calendars as mcal
from datetime import datetime

def market_is_open(date):
    result = mcal.get_calendar("NYSE").schedule(start_date=date, end_date=date)
    return result.empty == False

# check if market is open today
is_open = market_is_open(datetime.now().strftime("%Y-%m-%d"))
print(is_open)

# check if market was open 2023-04-16 (False)
was_open = market_is_open('2023-09-10')
print(was_open)