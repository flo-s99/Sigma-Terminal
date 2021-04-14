import sqlite3
import alpaca_trade_api as tradeapi

connection = sqlite3.connect("/Users/user/Dev/Sigma-Terminal/database.db")
connection.row_factory = sqlite3.Row
##############################################
## GETTING THE SYMBOL DATA
##############################################
cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, name FROM stock
""")

rows = cursor.fetchall()

symbols = [row['symbol'] for row in rows] # list comprehension

api = tradeapi.REST('PKHAU88ODFLYVR0U4ZK5', 'dZX4vdVPI3XdA8s91cNcWDXyBH7saEMyMDu8cesf',
base_url='https://paper-api.alpaca.markets')
assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"Added a new stock {asset.symbol} {asset.name}")
            cursor.execute("INSERT INTO stock (symbol, name) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)
    
connection.commit()
