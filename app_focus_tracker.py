import time
from datetime import datetime, timedelta
import re
import pygetwindow as gw
from csv_repository import CSVDataRepository
from timer import Timer

class AppFocusTracker:
    def __init__(self, app_title, repo, csv_repo):
        # Initializes the AppFocusTracker with specific application to track,
        # a repository for data storage, and a CSV repository instance for exporting data.
        self.app_title = app_title  # The title of the application window to track.
        self.repo = repo  # The database repository instance for storing tracking data.
        self.csv_repo = csv_repo  # The CSVDataRepository instance for data export.

        self.timer = Timer()  # A Timer instance to track focused time.

    def is_app_focused(self):
        """Checks if the specified application window is currently focused."""
        time.sleep(3)  # Delay to ensure accurate active window detection.
        active_window = gw.getActiveWindow()  # Get the current active window.
        # Check if the active window's title matches the specified application title.
        if active_window and re.search(self.app_title, active_window.title, re.IGNORECASE):
            return True  # The specified app is in focus.
        else:
            # The specified app is not in focus; print the current active window for debugging.
            print(f"The focused window is: {active_window.title if active_window else 'None'}")
            return False

    def check_and_update_last_row(self):
        """Checks and updates the last entry in the database for continuity."""
        all_workers = self.repo.get_all_rows()  # Retrieve all rows from the database.
        if all_workers:
            # If there are existing entries, fetch the last worker's data.
            last_worker = self.repo.get_last_row()
            print("Last Worker:", last_worker)
            return last_worker
        else:
            # If no entries exist, reset the database and add a new initial row.
            self.repo.delete_all_rows()
            today_date = datetime.today().strftime("%Y-%m-%d")
            self.repo.add_row(today_date, 0)
            new_row = self.repo.get_last_row()
            print("Added new row with today's date and zero hours.")
            return new_row

    def is_within_timeframe(self, start_time, end_time, check_time, date):
        """Determines if the current time is within specified working hours."""
        last_worker = self.repo.get_last_row()
        if last_worker['date'] == date:
            return True  # The check is for the same day as the last worker's entry.
        else:
            crosses_midnight = start_time > end_time  # Determine if the timeframe crosses midnight.
            check_datetime = datetime.strptime(check_time, '%Y-%m-%d %I:%M %p')
            # Adjust times for comparison based on whether the timeframe crosses midnight.
            if crosses_midnight:
                end_time = (datetime.strptime(end_time, '%I:%M %p') + timedelta(days=1)).time()
            start_datetime = datetime.combine(check_datetime.date(), datetime.strptime(start_time, '%I:%M %p').time())
            end_datetime = datetime.combine(check_datetime.date(), end_time)
            # Determine if the check_datetime falls within the start and end datetime range.
            if crosses_midnight:
                return check_datetime >= start_datetime or check_datetime <= end_datetime
            else:
                return start_datetime <= check_datetime <= end_datetime

    def save_data(self, updated_minutes, worker_id):
        """Saves the updated minutes spent in the database and CSV file."""
        # Update the database
        self.repo.edit_row_by_id(worker_id, updated_minutes)
        print(f"Updated worker {worker_id} in the database with {updated_minutes} minutes spent.")

        # Export the updated database to CSV using the csv_repo instance
        self.csv_repo.copy_to_csv()  # Adjusted to use the instance directly
        print(f"Appended updated data for worker {worker_id} to CSV.")

    def run_tracker(self):
        """Main loop to monitor application focus and update work time accordingly."""
        while True:
            if self.is_app_focused():
                print(f"The {self.app_title} window is in focus.")
                last_worker = self.check_and_update_last_row()
                current_time = datetime.now().strftime('%Y-%m-%d %I:%M %p')
                if last_worker and self.is_within_timeframe("12:00 PM", "05:00 AM", current_time, last_worker['date']):
                    if not self.timer.is_started():
                        self.timer.start()  # Start the timer if the app is focused and not already started.
                else:
                    if self.timer.is_started():
                        # If the app
                        elapsed_minutes = self.timer.stop()  # Stop the timer and get elapsed minutes.
                        updated_minutes = elapsed_minutes + last_worker['mins_spend_worker']  # Update total minutes.
                        self.save_data(updated_minutes, last_worker['id'])  # Persist updated data.
                        print(f"Saved data for worker {last_worker['id']} with {updated_minutes} minutes spent.")
            else:
                if self.timer.is_started():
                    elapsed_minutes = self.timer.stop()  # Stop the timer if the app loses focus.
                    last_worker = self.check_and_update_last_row()  # Refresh last_worker data.
                    updated_minutes = elapsed_minutes + last_worker['mins_spend_worker']
                    self.save_data(updated_minutes, last_worker['id'])  # Save the updated data.
                    print(f"Saved data for worker {last_worker['id']} with {updated_minutes} minutes spent.")
                print(f"The {self.app_title} window is not in focus.")
            time.sleep(60)  # Pause for 60 seconds before checking again.
  