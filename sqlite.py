import sqlite3

def setup_db():
    # setup database
    conn = sqlite3.connect('content.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS content
                (id INTEGER PRIMARY KEY, text TEXT)''')

    return conn, c
