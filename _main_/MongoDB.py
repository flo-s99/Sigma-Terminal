from pymongo import MongoClient
import pandas as pd
from collections import defaultdict
import csv

# Connect to Database and Collection within Database
try:
    cluster = MongoClient('mongodb+srv://Flo:<FSMedia99!>@stock-data.rioop.mongodb.net/Stock-Data?retryWrites=true&w=majority')
    print('Connected')
except:
    print('Failed')
db = cluster['Sigma-Terminal']
collection = db['Stock-Prices']

data = {'name': 'Flo',
'stock': ['PLUG','TSLA', 'MSFT', 'AAPL'],
'quantity': ['2', '3','6','1'],
'price': [30.43, 703.01, 1509.93, 2023.23]}
# Upload data
collection.insert_one(data)

