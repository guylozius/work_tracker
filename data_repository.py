import sqlite3

class DatabaseRepository:
    _instance = None

    def __new__(cls, db_name='work_tracker.db'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect(db_name)
            cls._instance.cursor = cls._instance.conn.cursor()
            cls._instance.create_table()
        return cls._instance

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS workers 
                            (id INTEGER PRIMARY KEY, date TEXT, mins_spend_worker REAL, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def add_row(self, date, mins_spend_worker):
        self.cursor.execute("INSERT INTO workers (date, mins_spend_worker) VALUES (?, ?)", (date, mins_spend_worker))
        self.conn.commit()

    def edit_row_by_id(self, worker_id, new_mins):
        self.cursor.execute("UPDATE workers SET mins_spend_worker=? WHERE id=?", (new_mins, worker_id))
        self.conn.commit()

    def get_all_rows(self):
        self.cursor.execute("SELECT * FROM workers")
        return self.cursor.fetchall()
    
    def get_last_row(self):
        self.cursor.execute("SELECT * FROM workers ORDER BY id DESC LIMIT 1")
        data = self.cursor.fetchone()
        if data:
            return {'id': data[0], 'date': data[1], 'mins_spend_worker': data[2], 'timestamp': data[3]}
        else:
            return None

    def delete_all_rows(self):
        self.cursor.execute("DELETE FROM workers")
        self.conn.commit()

   

    def close_connection(self):
        self.conn.close()
