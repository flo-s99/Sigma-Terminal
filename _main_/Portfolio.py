import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
from datetime import datetime, time

tick = ['TSLA', 'TDOC', 'TSM', 'PLUG']
price_data = web.get_data_yahoo(tick,
                           start = '2018-01-01',
                           end = datetime.now())['Adj Close']

log_ret = np.log(price_data/price_data.shift(1))
# Derive Covariance Matrix
cov_mat = log_ret.cov() * 252
print(cov_mat)
# Simulating 5000 portfolios
num_port = 5000
# Creating an empty array to store portfolio weights
all_wts = np.zeros((num_port, len(price_data.columns)))
# Creating an empty array to store portfolio returns
port_returns = np.zeros((num_port))
# Creating an empty array to store portfolio risks
port_risk = np.zeros((num_port))
# Creating an empty array to store portfolio sharpe ratio
sharpe_ratio = np.zeros((num_port))

for i in range(num_port):
  wts = np.random.uniform(size = len(price_data.columns))
  wts = wts/np.sum(wts)
  
  # saving weights in the array
  all_wts[i,:] = wts
  
  # Portfolio Returns
  port_ret = np.sum(log_ret.mean() * wts)
  port_ret = (port_ret + 1) ** 252 - 1
  
  # Saving Portfolio returns
  port_returns[i] = port_ret
  
  # Portfolio Risk
  port_sd = np.sqrt(np.dot(wts.T, np.dot(cov_mat, wts)))
  port_risk[i] = port_sd
  
  # Portfolio Sharpe Ratio
  # Assuming 0% Risk Free Rate
  sr = port_ret / port_sd
  sharpe_ratio[i] = sr

names = price_data.columns
# Minimum Variance Combination
min_var = all_wts[port_risk.argmin()]
print(min_var)
# Maximum Sharpe Ratio Combination
max_sr = all_wts[sharpe_ratio.argmax()]
print(max_sr)
print(sharpe_ratio.max())
print(port_risk.min())

# Plot Minimum-Variance-Portfolio
min_var = pd.Series(min_var, index=names)
min_var = min_var.sort_values()
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
ax1.set_xlabel('Asset')
ax1.set_ylabel("Weights")
ax1.set_title("Minimum Variance Portfolio weights")
min_var.plot(kind = 'bar')
plt.show()

# Plot Tangency Portfolio Combination
max_sr = pd.Series(max_sr, index=names)
max_sr = max_sr.sort_values()
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
ax1.set_xlabel('Asset')
ax1.set_ylabel("Weights")
ax1.set_title("Tangency Portfolio weights")
max_sr.plot(kind = 'bar')
plt.show()

# Plot Efficient Frontier Scatterplot
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
ax1.set_xlabel('Risk')
ax1.set_ylabel("Returns")
ax1.set_title("Portfolio optimization and Efficient Frontier")
plt.scatter(port_risk, port_returns)
plt.show();