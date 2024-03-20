import sqlite3

class DatabaseRepository:
    _instance = None  # Class-level attribute to hold the singleton instance.

    def __new__(cls, db_name='work_tracker.db'):
        # A custom __new__ method to implement the singleton design pattern.
        # This ensures that only one instance of the DatabaseRepository class is ever created.
        if cls._instance is None:  # If no instance has been created yet,
            cls._instance = super().__new__(cls)  # Create a new instance.
            # Establish a connection to the specified SQLite database.
            cls._instance.conn = sqlite3.connect(db_name)
            # Create a cursor object to interact with the database.
            cls._instance.cursor = cls._instance.conn.cursor()
            # Call the method to ensure the workers table exists.
            cls._instance.create_table()
        return cls._instance  # Return the singleton instance.

    def create_table(self):
        # Creates the 'workers' table in the database if it doesn't already exist.
        # The table includes an ID, date, minutes spent by the worker, and a timestamp.
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS workers 
                            (id INTEGER PRIMARY KEY, date TEXT, mins_spend_worker REAL, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()  # Commit the changes to the database.

    def add_row(self, date, mins_spend_worker):
        # Inserts a new row into the 'workers' table with the specified date and minutes spent.
        self.cursor.execute("INSERT INTO workers (date, mins_spend_worker) VALUES (?, ?)", (date, mins_spend_worker))
        self.conn.commit()  # Commit the changes to the database.

    def edit_row_by_id(self, worker_id, new_mins):
        # Updates the minutes spent for a specific worker identified by worker_id.
        self.cursor.execute("UPDATE workers SET mins_spend_worker=? WHERE id=?", (new_mins, worker_id))
        self.conn.commit()  # Commit the changes to the database.

    def get_all_rows(self):
        # Retrieves all rows from the 'workers' table.
        self.cursor.execute("SELECT * FROM workers")
        return self.cursor.fetchall()  # Return all fetched rows.

    def get_last_row(self):
        # Retrieves the most recent row added to the 'workers' table.
        self.cursor.execute("SELECT * FROM workers ORDER BY id DESC LIMIT 1")
        data = self.cursor.fetchone()  # Fetch the last row.
        if data:
            # Return a dictionary representing the last row if it exists.
            return {'id': data[0], 'date': data[1], 'mins_spend_worker': data[2], 'timestamp': data[3]}
        else:
            return None  # Return None if the table is empty.

    def delete_all_rows(self):
        # Deletes all rows from the 'workers' table.
        self.cursor.execute("DELETE FROM workers")
        self.conn.commit()  # Commit the changes to the database.

    def close_connection(self):
        # Closes the connection to the SQLite database.
        self.conn.close()
