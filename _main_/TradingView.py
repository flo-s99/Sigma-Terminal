import requests
from bs4 import BeautifulSoup
import re

r = requests.get('https://www.tradingview.com/markets/cryptocurrencies/prices-all/')
soup = BeautifulSoup(r.text, 'html.parser')
links = soup.findAll('td', class_='tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big')

formatted_links = []

html_content = float

m = re.match(' <td class="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big">', html_content)
if m:
	print(m.group(1))

print(links)