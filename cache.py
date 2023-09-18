import cache_requests
session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'my-program/1.0'
ticker = yf.Ticker('msft', session=session)
# The scraped response will be stored in the cache
ticker.actions