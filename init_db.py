import sqlite3

con = sqlite3.connect("library.db")
cur = con.cursor()

cur.execute("""
    CREATE TABLE book (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL
    );
""")

cur.execute("""
    CREATE TABLE reader(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL        
    );
""")

cur.execute("""
    CREATE TABLE loan(
        id INTEGER PRIMARY KEY,
        reader_id INTEGER,
        book_id INTEGER,
        loan_date TEXT NOT NULL,
        return_date TEXT,

        FOREIGN KEY (reader_id) REFERENCES reader(id),
        FOREIGN KEY (book_id) REFERENCES book(id)       
    );
""")

cur.close()
con.close()