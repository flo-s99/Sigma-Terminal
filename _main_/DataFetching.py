import alpha_vantage as av
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.cryptocurrencies import CryptoCurrencies

# Getting Stock-Data: 
# Prices, Volume, Company Fundamental Data
# Simple Moving Average, EMA, RSI, ADX
def getStockDataDaily():
    # My API Credentials
    API_URL = "https://www.alphavantage.co/query"
    # Let User Input Stock Symbols
    symbol = 'MSFT'
    # Query Data from Alpha Vantage into pandas dataframes
    ts = TimeSeries(key='6GBO7IYRXHROK1ZO', output_format='json')
    data, metadata = ts.get_daily_adjusted(symbol=symbol, outputsize='compact')
    print(data)
    # Getting Technical Indicators and Fundamental data
    ti = TechIndicators(key='6GBO7IYRXHROK1ZO', output_format='json')
    dataSMA, metadataSMA = ti.get_sma(symbol=symbol, interval='daily', time_period=200, series_type='close')
    dataEMA, metadataEMA = ti.get_ema(symbol=symbol, interval='daily', time_period=200, series_type='close')
    #dataADX, metadataADX = ti.get_adx(symbol=symbol, interval='daily', time_period=200)   
    dataRSI, metadataRSI = ti.get_rsi(symbol=symbol, interval='daily', time_period=200, series_type='close')
    fd = FundamentalData(key='6GBO7IYRXHROK1ZO', output_format='json')
    dataFundamental, metadataFund = fd.get_company_overview(symbol=symbol)
#getStockDataDaily()

# Getting CryptoCurrency-Data
# Get Crypto Health Index !!!!! API not working atm!!!! 
def getCryptoDataDaily():
    # My API Credentials
    API_URL = "https://www.alphavantage.co/query"
    # Let User Input Stock Symbols
    symbol = 'BTC'
    # Query Data from Alpha Vantage into pandas dataframes or json
    cc = CryptoCurrencies(key='6GBO7IYRXHROK1ZO', output_format='json')
    #dataRating, metadataRating = cc.get_digital_crypto_rating(symbol=symbol)
    dataCrypto, metadataCrypto = cc.get_digital_currency_daily(symbol=symbol, market='USD')
    print(dataCrypto)
getCryptoDataDaily()
    
getStockDataDaily()

def getStockDataIntraday30():
    # My API Credentials
    API_URL = "https://www.alphavantage.co/query"
    # Let User Input Stock Symbols
    symbol = 'MSFT'
    # Query Data from Alpha Vantage into pandas dataframes
    ts = TimeSeries(key='6GBO7IYRXHROK1ZO', output_format='json')
    data, metadata = ts.get_intraday(symbol=symbol, outputsize='compact', interval='30min')
    print(data)
    # Setting Technical Indicators
    ti = TechIndicators(key='6GBO7IYRXHROK1ZO', output_format='json')
    dataSMA, metadataSMA = ti.get_sma(symbol=symbol, interval='30min', time_period=200)
