import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
#%matplotlib inline

from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import plotly.graph_objs as go

print(__version__) # requires version >= 1.9.0

init_notebook_mode(connected=True)

portfolio_df = pd.read_excel('aquisitions.xlsx')

portfolio_df.head(10)


# Date Ranges for SP 500 and for all tickers
# Modify these date ranges each week.

# The below will pull back stock prices from 2010 until end date specified.
start_sp = datetime.datetime(2010, 1, 1)
end_sp = datetime.datetime(2018, 7, 13)

# This variable is used for YTD performance.
end_of_last_year = datetime.datetime(2017, 12, 29)

# These are separate if for some reason want different date range than SP.
stocks_start = datetime.datetime(2010, 1, 1)
stocks_end = datetime.datetime(2018, 7, 13)

from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
yf.pdr_override() # <== that's all it takes :-)

sp500 = pdr.get_data_yahoo('^GSPC', 
                           start_sp,
                             end_sp)
                          
sp500.head()


# Create a dataframe with only the Adj Close column as that's all we need for this analysis.

sp_500_adj_close = sp500[['Adj Close']].reset_index()

# Adj Close for the EOY in 2017 in order to run comparisons versus stocks YTD performances.

sp_500_adj_close_start = sp_500_adj_close[sp_500_adj_close['Date']==end_of_last_year]
sp_500_adj_close_start

# Generate a dynamic list of tickers to pull from Yahoo Finance API based on the imported file with tickers.
tickers = portfolio_df['Ticker'].unique()
tickers


def get(tickers, startdate, enddate):
    def data(ticker):
        return (pdr.get_data_yahoo(ticker, start=startdate, end=enddate))
    datas = map(data, tickers)
    return(pd.concat(datas, keys=tickers, names=['Ticker', 'Date']))
               
all_data = get(tickers, stocks_start, stocks_end)

# Also only pulling the ticker, date and adj. close columns for our tickers.

adj_close = all_data[['Adj Close']].reset_index()
adj_close.head()


# Grabbing the ticker close from the end of last year 
adj_close_start = adj_close[adj_close['Date']==end_of_last_year]
adj_close_start.head()

# Grab the latest stock close price 

adj_close_latest = adj_close[adj_close['Date']==stocks_end]
adj_close_latest.head()

# Merge the portfolio dataframe with the adj close dataframe; they are being joined by the indexes.

merged_portfolio = pd.merge(portfolio_df, adj_close_latest, on='Ticker')
merged_portfolio.head()

# The below creates a new column which is the ticker return; takes the latest adjusted close for each position
# and divides that by the initial share cost.

merged_portfolio['ticker return'] = merged_portfolio['Adj Close'] / merged_portfolio['Unit Cost'] - 1

merged_portfolio.head()
# Above we reset the index to the newly merged dataframe.  This is because we have a flat dataframe for the sp500 returns
# and we merge the the new dataframe with the sp500 adjusted closes since the sp start on acquisition date and sp500 close date.

merged_portfolio_sp = pd.merge(merged_portfolio, sp_500_adj_close, left_on='Acquisition Date', right_on='Date')
# .set_index('Ticker')
# We will delete the additional date column which is created from this merge.
# We then rename columns to Latest Date and then reflect Ticker Adj Close and SP 500 Initial Close.

del merged_portfolio_sp['Date_y']

merged_portfolio_sp.rename(columns={'Date_x': 'Latest Date', 'Adj Close_x': 'Ticker Adj Close'
                                    , 'Adj Close_y': 'SP 500 Initial Close'}, inplace=True)
# This new column is intended to figure out what SP 500 equivalent purchase would have been at purchase date of stock.
merged_portfolio_sp['Equiv SP Shares'] = merged_portfolio_sp['Cost Basis'] / merged_portfolio_sp['SP 500 Initial Close']
merged_portfolio_sp.head()

# We are joining the developing dataframe with the sp500 closes again, this time with the latest close for SP.
merged_portfolio_sp_latest = pd.merge(merged_portfolio_sp, sp_500_adj_close, left_on='Latest Date', right_on='Date')

merged_portfolio_sp_latest.head()

# Once again need to delete the new Date column added as it's redundant to Latest Date.  
# Modify Adj Close from the sp dataframe to distinguish it by calling it the SP 500 Latest Close.

del merged_portfolio_sp_latest['Date']

merged_portfolio_sp_latest.rename(columns={'Adj Close': 'SP 500 Latest Close'}, inplace=True)

merged_portfolio_sp_latest.head()
# Percent return of SP from acquisition date of position through latest trading day.
merged_portfolio_sp_latest['SP Return'] = merged_portfolio_sp_latest['SP 500 Latest Close'] / merged_portfolio_sp_latest['SP 500 Initial Close'] - 1

# This is a new column which takes the tickers return and subtracts the sp 500 equivalent range return.
merged_portfolio_sp_latest['Abs. Return Compare'] = merged_portfolio_sp_latest['ticker return'] - merged_portfolio_sp_latest['SP Return']

# This is a new column where we calculate the ticker's share value by multiplying the original quantity by the latest close.
merged_portfolio_sp_latest['Ticker Share Value'] = merged_portfolio_sp_latest['Quantity'] * merged_portfolio_sp_latest['Ticker Adj Close']

# We calculate the equivalent SP 500 Value if we take the original SP shares * the latest SP 500 share price.
merged_portfolio_sp_latest['SP 500 Value'] = merged_portfolio_sp_latest['Equiv SP Shares'] * merged_portfolio_sp_latest['SP 500 Latest Close']

# This is a new column where we take the current market value for the shares and subtract the SP 500 value.
merged_portfolio_sp_latest['Abs Value Compare'] = merged_portfolio_sp_latest['Ticker Share Value'] - merged_portfolio_sp_latest['SP 500 Value']

# This column calculates profit / loss for stock position.
merged_portfolio_sp_latest['Stock Gain / (Loss)'] = merged_portfolio_sp_latest['Ticker Share Value'] - merged_portfolio_sp_latest['Cost Basis']

# This column calculates profit / loss for SP 500.
merged_portfolio_sp_latest['SP 500 Gain / (Loss)'] = merged_portfolio_sp_latest['SP 500 Value'] - merged_portfolio_sp_latest['Cost Basis']

merged_portfolio_sp_latest.head()
# Merge the overall dataframe with the adj close start of year dataframe for YTD tracking.

merged_portfolio_sp_latest_YTD = pd.merge(merged_portfolio_sp_latest, adj_close_start, on='Ticker')
merged_portfolio_sp_latest_YTD.head()
# Deleting date again as it's an unnecessary column.  Explaining that new column is the Ticker Start of Year Close.

del merged_portfolio_sp_latest_YTD['Date']

merged_portfolio_sp_latest_YTD.rename(columns={'Adj Close': 'Ticker Start Year Close'}, inplace=True)

merged_portfolio_sp_latest_YTD.head()

# Join the SP 500 start of year with current dataframe.

merged_portfolio_sp_latest_YTD_sp = pd.merge(merged_portfolio_sp_latest_YTD, sp_500_adj_close_start
                                             , left_on='Start of Year', right_on='Date')

# Deleting another unneeded Data column.

del merged_portfolio_sp_latest_YTD_sp['Date']

# Renaming so that it's clear this column is SP 500 start of year close.
merged_portfolio_sp_latest_YTD_sp.rename(columns={'Adj Close': 'SP Start Year Close'}, inplace=True)

# YTD return for portfolio position.
merged_portfolio_sp_latest_YTD_sp['Share YTD'] = merged_portfolio_sp_latest_YTD_sp['Ticker Adj Close'] / merged_portfolio_sp_latest_YTD_sp['Ticker Start Year Close'] - 1

# YTD return for SP to run compares.
merged_portfolio_sp_latest_YTD_sp['SP 500 YTD'] = merged_portfolio_sp_latest_YTD_sp['SP 500 Latest Close'] / merged_portfolio_sp_latest_YTD_sp['SP Start Year Close'] - 1

merged_portfolio_sp_latest_YTD_sp.head()
merged_portfolio_sp_latest_YTD_sp = merged_portfolio_sp_latest_YTD_sp.sort_values(by='Ticker', ascending=True)
merged_portfolio_sp_latest_YTD_sp.head()
# Cumulative sum of original investment
merged_portfolio_sp_latest_YTD_sp['Cum Invst'] = merged_portfolio_sp_latest_YTD_sp['Cost Basis'].cumsum()

# Cumulative sum of Ticker Share Value (latest FMV based on initial quantity purchased).
merged_portfolio_sp_latest_YTD_sp['Cum Ticker Returns'] = merged_portfolio_sp_latest_YTD_sp['Ticker Share Value'].cumsum()

# Cumulative sum of SP Share Value (latest FMV driven off of initial SP equiv purchase).
merged_portfolio_sp_latest_YTD_sp['Cum SP Returns'] = merged_portfolio_sp_latest_YTD_sp['SP 500 Value'].cumsum()

# Cumulative CoC multiple return for stock investments
merged_portfolio_sp_latest_YTD_sp['Cum Ticker ROI Mult'] = merged_portfolio_sp_latest_YTD_sp['Cum Ticker Returns'] / merged_portfolio_sp_latest_YTD_sp['Cum Invst']
# Need to factor in that some positions were purchased much more recently than others.
# Join adj_close dataframe with portfolio in order to have acquisition date.

adj_close_acq_date = pd.merge(adj_close, portfolio_df, on='Ticker')

adj_close_acq_date.head()

# delete_columns = ['Quantity', 'Unit Cost', 'Cost Basis', 'Start of Year']

del adj_close_acq_date['Quantity']
del adj_close_acq_date['Unit Cost']
del adj_close_acq_date['Cost Basis']
del adj_close_acq_date['Start of Year']

adj_close_acq_date.sort_values(by=['Ticker', 'Acquisition Date', 'Date'], ascending=[True, True, True], inplace=True)
adj_close_acq_date['Date Delta'] = adj_close_acq_date['Date'] - adj_close_acq_date['Acquisition Date']

adj_close_acq_date['Date Delta'] = adj_close_acq_date[['Date Delta']].apply(pd.to_numeric)  

adj_close_acq_date.head()
# Modified the dataframe being evaluated to look at highest close which occurred after Acquisition Date (aka, not prior to purchase).

adj_close_acq_date_modified = adj_close_acq_date[adj_close_acq_date['Date Delta']>=0]
# This pivot table will index on the Ticker and Acquisition Date, and find the max adjusted close.

adj_close_pivot = adj_close_acq_date_modified.pivot_table(index=['Ticker', 'Acquisition Date'], values='Adj Close', aggfunc=np.max)

adj_close_pivot.reset_index(inplace=True)

adj_close_pivot[0:10]
# Merge the adj close pivot table with the adj_close table in order to grab the date of the Adj Close High (good to know).

adj_close_pivot_merged = pd.merge(adj_close_pivot, adj_close
                                             , on=['Ticker', 'Adj Close'])

adj_close_pivot_merged.head()
# Duplicates could be created where the stock had the same high on multiple dates.
# Sorted by latest date and then dropped duplicates, which drops the earlier high from consideration.

adj_close_pivot_merged.sort_values(by=['Ticker', 'Acquisition Date', 'Date'], ascending=[True, True, False], inplace=True)

adj_close_pivot_merged.drop_duplicates(['Ticker', 'Acquisition Date', 'Adj Close'], inplace=True)

adj_close_pivot_merged.head()
# Merge the Adj Close pivot table with the master dataframe to have the closing high since you have owned the stock.

merged_portfolio_sp_latest_YTD_sp_closing_high = pd.merge(merged_portfolio_sp_latest_YTD_sp, adj_close_pivot_merged
                                             , on=['Ticker', 'Acquisition Date'])

# Renaming so that it's clear that the new columns are two year closing high and two year closing high date.
merged_portfolio_sp_latest_YTD_sp_closing_high.rename(columns={'Adj Close': 'Closing High Adj Close', 'Date': 'Closing High Adj Close Date'}, inplace=True)

merged_portfolio_sp_latest_YTD_sp_closing_high['Pct off High'] = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker Adj Close'] / merged_portfolio_sp_latest_YTD_sp_closing_high['Closing High Adj Close'] - 1 

merged_portfolio_sp_latest_YTD_sp_closing_high.head()

merged_portfolio_sp_latest_YTD_sp_closing_high['Counts'] = merged_portfolio_sp_latest_YTD_sp_closing_high.index

merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker #'] = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker'].map(str) + ' ' + merged_portfolio_sp_latest_YTD_sp_closing_high['Counts'].map(str)

merged_portfolio_sp_latest_YTD_sp_closing_high.head()
trace1 = go.Bar(
    x = merged_portfolio_sp_latest_YTD_sp['Ticker'][0:10],
    y = merged_portfolio_sp_latest_YTD_sp['Share YTD'][0:10],
    name = 'Ticker YTD')

trace2 = go.Scatter(
    x = merged_portfolio_sp_latest_YTD_sp['Ticker'][0:10],
    y = merged_portfolio_sp_latest_YTD_sp['SP 500 YTD'][0:10],
    name = 'SP500 YTD')
    
data = [trace1, trace2]

layout = go.Layout(title = 'Total Return vs S&P 500, YTD'
    , barmode = 'group'
    , yaxis=dict(title='Returns', tickformat=".2%")
    , xaxis=dict(title='Ticker')
    , legend=dict(x=0.8,y=1.2)
    )

fig = go.Figure(data=data, layout=layout)
iplot(fig)
trace1 = go.Bar(
    x = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker #'][0:10],
    y = merged_portfolio_sp_latest_YTD_sp_closing_high['ticker return'][0:10],
    name = 'Ticker Total Return')

trace2 = go.Scatter(
    x = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker #'][0:10],
    y = merged_portfolio_sp_latest_YTD_sp_closing_high['SP Return'][0:10],
    name = 'SP500 Total Return')
    
data = [trace1, trace2]

layout = go.Layout(title = 'Total Return vs S&P 500'
    , barmode = 'group'
    , yaxis=dict(title='Returns', tickformat=".2%")
    , xaxis=dict(title='Ticker')
    , legend=dict(x=.8,y=1.2)
    )

fig = go.Figure(data=data, layout=layout)
iplot(fig)

trace1 = go.Bar(
    x = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker #'][0:10],
    y = merged_portfolio_sp_latest_YTD_sp_closing_high['Stock Gain / (Loss)'][0:10],
    name = 'Ticker Total Return ($)')

trace2 = go.Bar(
    x = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker #'][0:10],
    y = merged_portfolio_sp_latest_YTD_sp_closing_high['SP 500 Gain / (Loss)'][0:10],
    name = 'SP 500 Total Return ($)')

trace3 = go.Scatter(
    x = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker #'][0:10],
    y = merged_portfolio_sp_latest_YTD_sp_closing_high['ticker return'][0:10],
    name = 'Ticker Total Return %',
    yaxis='y2')

data = [trace1, trace2, trace3]
#, , trace4

layout = go.Layout(title = 'Gain / (Loss) and Total Return vs S&P 500'
    , barmode = 'group'
    , yaxis=dict(title='Gain / (Loss) ($)')
    , yaxis2=dict(title='Ticker Return', overlaying='y', side='right', tickformat=".1%") 
    , xaxis=dict(title='Ticker')
    , legend=dict(x=.75,y=1.2)
    )

fig = go.Figure(data=data, layout=layout)
iplot(fig)
trace1 = go.Scatter(
    x = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker #'],
    y = merged_portfolio_sp_latest_YTD_sp_closing_high['Cum Invst'],
    mode = 'lines+markers',
    name = 'Cum Invst')

trace2 = go.Scatter(
    x = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker #'],
    y = merged_portfolio_sp_latest_YTD_sp_closing_high['Cum Ticker Returns'],
    mode = 'lines+markers',
    name = 'Cum Ticker Returns')

trace3 = go.Scatter(
    x = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker #'],
    y = merged_portfolio_sp_latest_YTD_sp_closing_high['Cum SP Returns'],
    mode = 'lines+markers',
    name = 'Cum SP500 Returns')

data = [trace1, trace2, trace3]

layout = go.Layout(title = 'Total Investment Comparisons by Ticker'
    , barmode = 'group'
    , yaxis=dict(title='Returns')
    , xaxis=dict(title='Ticker')
    , legend=dict(x=1,y=1)
    )

fig = go.Figure(data=data, layout=layout)
iplot(fig)
trace1 = go.Bar(
    x = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker'],
    y = merged_portfolio_sp_latest_YTD_sp_closing_high['Cum Invst'],
    # mode = 'lines+markers',
    name = 'Cum Invst')

trace2 = go.Bar(
    x = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker'],
    y = merged_portfolio_sp_latest_YTD_sp_closing_high['Cum SP Returns'],
    # mode = 'lines+markers',
    name = 'Cum SP500 Returns')

trace3 = go.Bar(
    x = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker'],
    y = merged_portfolio_sp_latest_YTD_sp_closing_high['Cum Ticker Returns'],
    # mode = 'lines+markers',
    name = 'Cum Ticker Returns')

trace4 = go.Scatter(
    x = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker'],
    y = merged_portfolio_sp_latest_YTD_sp_closing_high['Cum Ticker ROI Mult'],
    # mode = 'lines+markers',
    name = 'Cum ROI Mult'
    , yaxis='y2')


data = [trace1, trace2, trace3, trace4]

layout = go.Layout(title = 'Total Cumulative Investments Over Time'
    , barmode = 'group'
    , yaxis=dict(title='Returns')
    , xaxis=dict(title='Ticker')
    , legend=dict(x=.4,y=1)
    , yaxis2=dict(title='Cum ROI Mult', overlaying='y', side='right')               
    )
fig = go.Figure(data=data, layout=layout)
iplot(fig)

trace1 = go.Bar(
    x = merged_portfolio_sp_latest_YTD_sp_closing_high['Ticker #'][0:10],
    y = merged_portfolio_sp_latest_YTD_sp_closing_high['Pct off High'][0:10],
    name = 'Pct off High')

data = [trace1]

layout = go.Layout(title = 'Adj Close % off of High Since Purchased'
    , barmode = 'group'
    , yaxis=dict(title='% Below Adj Close High Since Purchased', tickformat=".2%")
    , xaxis=dict(title='Ticker')
    , legend=dict(x=.8,y=1)
    )

fig = go.Figure(data=data, layout=layout)
iplot(fig)
# Generate a dynamic list of tickers to pull from Yahoo Finance API based on the imported file with tickers.

chart_tickers = portfolio_df['Ticker'].unique()

chart_tickers = chart_tickers.tolist()

chart_tickers.append('^GSPC')

chart_tickers = np.array(chart_tickers)
# The below will pull back stock prices from chart start date until end date specified.

chart_start = datetime.datetime(2017, 1, 4)

chart_end = datetime.datetime(2018, 7, 13)
# Run the same function as above, but for a different date range and including the SP500.
               
chart_data = get(chart_tickers, chart_start, chart_end)
chart_data_eval = chart_data[['Close']]

chart_data_eval.reset_index(inplace=True)

chart_data_eval.head()
chart_data_eval_pivot = pd.pivot_table(chart_data_eval, index='Date', columns='Ticker', values = 'Close')

chart_data_eval_pivot.reset_index(inplace=True)

chart_data_eval_pivot.head()
trace1 = go.Scatter(
    x = chart_data_eval_pivot['Date'],
    y = chart_data_eval_pivot['^GSPC'],
    mode = 'lines',
    name = 'SP Prices')

trace2 = go.Scatter(
    x = chart_data_eval_pivot['Date'],
    y = chart_data_eval_pivot['AAPL'],
    mode = 'lines',
    name = 'AAPL Returns')

trace3 = go.Scatter(
    x = chart_data_eval_pivot['Date'],
    y = chart_data_eval_pivot['NFLX'],
    mode = 'lines',
    name = 'NFLX Returns')

data = [trace1, trace2, trace3]

layout = go.Layout(title = 'Share Price Returns by Ticker'
    , barmode = 'group'
    , yaxis=dict(title='Returns')
    , xaxis=dict(title='Ticker')
    , legend=dict(x=1,y=1)
    )

fig = go.Figure(data=data, layout=layout)
iplot(fig)
chart_data_eval_pivot_relative = pd.pivot_table(chart_data_eval, index='Date', columns='Ticker', values = 'Close')

chart_data_eval_pivot_relative.tail()
chart_data_eval_pivot_relative_first = chart_data_eval_pivot_relative.iloc[0,:]

chart_data_eval_pivot_relative_first.head()
chart_data_eval_pivot_relative = (chart_data_eval_pivot_relative.divide(chart_data_eval_pivot_relative_first, axis=1))-1

chart_data_eval_pivot_relative.reset_index(inplace=True)

chart_data_eval_pivot_relative.head()
trace1 = go.Scatter(
    x = chart_data_eval_pivot_relative['Date'],
    y = chart_data_eval_pivot_relative['^GSPC'],
    mode = 'lines',
    name = 'SP Return')

trace2 = go.Scatter(
    x = chart_data_eval_pivot_relative['Date'],
    y = chart_data_eval_pivot_relative['AAPL'],
    mode = 'lines',
    name = 'AAPL Return')

trace3 = go.Scatter(
    x = chart_data_eval_pivot_relative['Date'],
    y = chart_data_eval_pivot_relative['NFLX'],
    mode = 'lines',
    name = 'NFLX Return')

trace4 = go.Scatter(
    x = chart_data_eval_pivot_relative['Date'],
    y = chart_data_eval_pivot_relative['MTCH'],
    mode = 'lines',
    name = 'MTCH Return')

data = [trace1, trace2, trace3, trace4]

layout = go.Layout(title = 'Return Comparisons by Ticker'
    , barmode = 'group'
    , yaxis=dict(title='Relative Returns', tickformat=".1%")
    , xaxis=dict(title='Ticker')
    , legend=dict(x=1,y=1)
    )

fig = go.Figure(data=data, layout=layout)
iplot(fig)
# Generate the base file that will be used for Dash dashboard.

merged_portfolio_sp_latest_YTD_sp_closing_high.to_csv('analyzed_portfolio.csv')
merged_portfolio_sp_latest_YTD_sp_closing_high.head()

merged_portfolio_sp_latest_YTD_sp_closing_high_tickers = merged_portfolio_sp_latest_YTD_sp_closing_high[['Ticker']]

merged_portfolio_sp_latest_YTD_sp_closing_high_tickers = merged_portfolio_sp_latest_YTD_sp_closing_high_tickers.drop_duplicates(['Ticker'], keep='first')

# merged_portfolio_sp_latest_YTD_sp_closing_high_tickers.head()

merged_portfolio_sp_latest_YTD_sp_closing_high_tickers = merged_portfolio_sp_latest_YTD_sp_closing_high_tickers['Ticker'].unique()

merged_portfolio_sp_latest_YTD_sp_closing_high_tickers = merged_portfolio_sp_latest_YTD_sp_closing_high_tickers.tolist()

merged_portfolio_sp_latest_YTD_sp_closing_high_tickers.append('SPY')

merged_portfolio_sp_latest_YTD_sp_closing_high_tickers = pd.DataFrame(data=merged_portfolio_sp_latest_YTD_sp_closing_high_tickers, columns=['Ticker'])

merged_portfolio_sp_latest_YTD_sp_closing_high_tickers.sort_values(by='Ticker', ascending=True, inplace=True)

merged_portfolio_sp_latest_YTD_sp_closing_high_tickers.head()

merged_portfolio_sp_latest_YTD_sp_closing_high_tickers.to_csv('tickers.csv')
# The below generates the tickers that will be used in the Dash ticker dropdown.

merged_portfolio_sp_latest_YTD_sp_closing_high_tickers = merged_portfolio_sp_latest_YTD_sp_closing_high_tickers['Ticker'].unique()

merged_portfolio_sp_latest_YTD_sp_closing_high_tickers = merged_portfolio_sp_latest_YTD_sp_closing_high_tickers.tolist()

merged_portfolio_sp_latest_YTD_sp_closing_high_tickers