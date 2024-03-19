import csv
import os
from data_repository import DatabaseRepository
class CSVDataRepository:
    def __init__(self, db_name='work_tracker.db'):
        self.db_name = db_name
        self.repo = DatabaseRepository(db_name)

    def copy_to_csv(self, csv_filename):
        # Get all workers from the database
        print('here')
        all_workers = self.repo.get_all_rows()
        
        # Define the CSV headers
        headers = ['id', 'date', 'hour_spend_worker', 'timestamp']
        print("Current Working Directory:", os.getcwd())
        # Write data to CSV file
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Write headers to the CSV file
            for worker in all_workers:
                writer.writerow(worker)  # Write each worker's data to the CSV file


