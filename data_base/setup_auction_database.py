import sqlite3

# Connect to the database (creates auction.db if it doesn't exist)
conn = sqlite3.connect('data_base/auction.db')

# Create a cursor object
cursor = conn.cursor()


# Create a table for auctions
cursor.execute('''
    CREATE TABLE IF NOT EXISTS auctions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        description TEXT,
        starting_bid REAL NOT NULL,
        current_bid REAL,
        auction_end_date TEXT NOT NULL,
        seller_id INTEGER NOT NULL,
        FOREIGN KEY (seller_id) REFERENCES users (id)
    )
''')

# Create a table for bids
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bids (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        auction_id INTEGER NOT NULL,
        bidder_id INTEGER NOT NULL,
        bid_amount REAL NOT NULL,
        bid_time TEXT NOT NULL,
        FOREIGN KEY (auction_id) REFERENCES auctions (id),
        FOREIGN KEY (bidder_id) REFERENCES users (id)
    )
''')

# Create a table for auction history (to track completed auctions)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS auction_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        auction_id INTEGER NOT NULL,
        winner_id INTEGER,
        final_bid REAL,
        auction_end_date TEXT NOT NULL,
        FOREIGN KEY (auction_id) REFERENCES auctions (id),
        FOREIGN KEY (winner_id) REFERENCES users (id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("auction.db has been created successfully!")
