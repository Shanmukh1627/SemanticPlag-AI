import sqlite3

# Connect to database (this creates the file if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the reports table to store our scan history
cursor.execute('''
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    score REAL NOT NULL,
    matched_file TEXT,
    status TEXT,
    date_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
print("✅ Database 'database.db' created successfully!")