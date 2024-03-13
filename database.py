import sqlite3
import random
import datetime

class Database:

    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()
        self.setup()

    def setup(self): # Create Database
        self.c.executescript('''
                        CREATE TABLE IF NOT EXISTS applications (
                        job_title TEXT,
                        company TEXT,
                        location TEXT,
                        date DATE,
                        status TEXT NOT NULL,
                        id INTEGER NOT NULL,
                        PRIMARY KEY(id)
                        )
                        ''')
        self.conn.commit()

    def insert_app_db(self, conn, job_title, company, location):

        today = datetime.date.today() # Set today's date
        status = 'Active' # Set application status to active
        id = random.randint(1,1000) # Generate random job id

        self.c.execute('''INSERT INTO applications (job_title, company, location, date, status, id)
                VALUES (?, ?, ?, ?, ?, ?);
                ''', (job_title, company, location, today, status, id))
        self.conn.commit()

    def remove_app_db(self, id):
        self.c.execute('''DELETE
                       FROM applications
                       WHERE id = ?;
                       ''', (id,))
        self.conn.commit()
    
    def display_all_db(self):
        self.c.execute('''SELECT * 
                       FROM applications''')
        rows = self.c.fetchall()
        return rows
