from datetime import datetime, time
import pandas as pd
import pandas_datareader as web
import yfinance

tick = ['TSLA','PLUG','MSFT']
price_data = web.get_data_yahoo(tick,
                           start = '2018-01-01',
                           end = datetime.now())['Adj Close']
price_data.to_excel('_data_/stock_prices.xlsx')

# ,'BABA', 'BTC-USD','NIO','INDA','EEM','^GSPC', 'NUAN', 'XRP-USD', 'ETH-USD', 'XRX', 'ARKK','ARKX', 'VOO', 'IBB','MCHI','IRBO'