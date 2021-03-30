from pymongo import MongoClient

# Connect to Database and Collection within Database
cluster = MongoClient('mongodb+srv://Flo:<Stanglmeier99>@stock-data.rioop.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster['Sigma-Terminal']
collection = db['Stock-Prices']

# Create a dictionary post to upload data to MongoDB
post = {}

# Upload data
collection.insert_one(post)

