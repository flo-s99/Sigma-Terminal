CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY, 
    symbol TEXT NOT NULL UNIQUE, 
    company TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stock_price (
    id INTEGER PRIMARY KEY, 
    stock_id INTEGER,
    date NOT NULL,
    open NOT NULL, 
    high NOT NULL, 
    low NOT NULL, 
    close NOT NULL, 
    adjusted_close NOT NULL, 
    volume NOT NULL,
    FOREIGN KEY (stock_id) REFERENCES stock (id)
);

CREATE TABLE IF NOT EXISTS stock_price_minute (
    id INTEGER PRIMARY KEY, 
    stock_id INTEGER,
    datetime NOT NULL,
    open NOT NULL, 
    high NOT NULL,
    low NOT NULL, 
    close NOT NULL, 
    volume NOT NULL,
    FOREIGN KEY (stock_id) REFERENCES stock (id)
)