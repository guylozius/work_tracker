import csv
import os
from data_repository import DatabaseRepository

class CSVDataRepository:
    def __init__(self, db_name='work_tracker.db'):
        # Constructor for the CSVDataRepository class.
        # Initializes the class with the name of the database file.
        # It also creates an instance of the DatabaseRepository to interact with the SQLite database.
        self.db_name = db_name
        self.repo = DatabaseRepository(db_name)

    def copy_to_csv(self, csv_filename):
        # This method exports all worker data from the SQLite database to a CSV file.
        # csv_filename: The name of the CSV file to which the data will be written.

        # Retrieve all workers' data from the database using the DatabaseRepository instance.
        all_workers = self.repo.get_all_rows()
        
        # Define the headers for the CSV file. These should match the columns in the database.
        headers = ['id', 'date', 'mins_spend_worker', 'timestamp']  # Updated 'hour_spend_worker' to 'mins_spend_worker' to reflect your previous changes

        # Print the current working directory to help in locating the CSV file.
        print("Current Working Directory:", os.getcwd())
        
        # Open (or create if it doesn't exist) the CSV file in write mode.
        with open(csv_filename, mode='w', newline='') as file:
            # Create a csv.writer object to write data into the file.
            writer = csv.writer(file)
            # Write the headers row to the CSV file.
            writer.writerow(headers)
            # Iterate over each worker's data retrieved from the database.
            for worker in all_workers:
                # Write each worker's data as a row in the CSV file.
                writer.writerow(worker)
