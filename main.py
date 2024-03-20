from app_focus_tracker import AppFocusTracker
from csv_repository import CSVDataRepository  # Import the AppFocusTracker class to track application usage.
from data_repository import DatabaseRepository  # Class for interacting with the database.

def main():
    app_title = "Visual Studio Code"
    db_name = "work_tracker.db"
    repo = DatabaseRepository(db_name)  
    csv_repo = CSVDataRepository()  # Create an instance of CSVDataRepository
    tracker = AppFocusTracker(app_title, repo, csv_repo)  # Pass the CSVDataRepository instance
    tracker.run_tracker()

if __name__ == "__main__":
    main()
