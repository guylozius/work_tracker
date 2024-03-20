from app_focus_tracker import AppFocusTracker
from csv_repository import CSVDataRepository  # Import the AppFocusTracker class to track application usage.
from data_repository import DatabaseRepository  # Class for interacting with the database.

def main():
    app_title = "Visual Studio Code"
    db_name = "work_tracker.db"
    csv_file_name = "work_tracker.csv"
    repo = DatabaseRepository(db_name)  
    csv_repo = CSVDataRepository(csv_file_name)  # Create an instance of CSVDataRepository
    tracker = AppFocusTracker(app_title, repo, csv_repo)  # Pass the CSVDataRepository instance
    tracker.run_tracker()

if __name__ == "__main__":
    main()
