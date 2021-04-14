import sqlite3

# Run script once to create local database

connection = sqlite3.connect("/Users/user/Dev/Sigma-Terminal/database.db")

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_price (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        date NOT NULL,
        open NOT NULL, 
        high NOT NULL, 
        low NOT NULL, 
        close NOT NULL, 
        volume NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
    )
""")

connection.commit()