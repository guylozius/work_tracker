import time
import datetime
from timer import TimeLog
import re
import pygetwindow as gw
from data_repository import DatabaseRepository
from csv_repository import CSVDataRepository

def check_and_update_last_row(repo):
    all_workers = repo.get_all_workers()

    if all_workers:
        last_worker = repo.get_last_worker()
        print("Last Worker:", last_worker)
        return last_worker
    else:
        repo.delete_all_workers()
        today_date = datetime.date.today().strftime("%Y-%m-%d")
        repo.add_worker(today_date, 0)
        new_row = repo.get_last_worker()
        print("Added new row with today's date and zero hours.")
        return new_row



def is_within_timeframe(start_time, end_time, check_time, date, repo):
    lastest = repo.get_last_worker()
    if lastest['date'] == date:
        return True
    else:
        # Check if the time frame crosses midnight
        crosses_midnight = start_time > end_time

        # Parse the check_time string into a datetime object
        check_datetime = datetime.datetime.strptime(check_time, '%Y-%m-%d %I:%M %p')
        
        # If the time frame crosses midnight, adjust end_time to the next day
        if crosses_midnight:
            end_time = (datetime.datetime.strptime(end_time, '%I:%M %p') + datetime.timedelta(days=1)).strftime('%I:%M %p')

        # Create datetime objects for start_time and end_time
        start_datetime = datetime.datetime.strptime(check_datetime.strftime('%Y-%m-%d ') + start_time, '%Y-%m-%d %I:%M %p')
        end_datetime = datetime.datetime.strptime(check_datetime.strftime('%Y-%m-%d ') + end_time, '%Y-%m-%d %I:%M %p')

        # Check if check_time falls within the time frame
        if not crosses_midnight:
            return start_datetime <= check_datetime <= end_datetime
        else:
            return check_datetime >= start_datetime or check_datetime <= end_datetime


def is_app_focused(window_title):
    time.sleep(3)
    active_window = gw.getActiveWindow()
    if active_window is not None:
        if re.search(window_title, active_window.title):
            return True
        else:
            print(f"The focused window is: {active_window.title}")
    return False

def main():
    csvFileName = "work_tracker.csv"
    csvrepo = CSVDataRepository()
    timer = TimeLog()
    app_title = "Visual Studio Code"
    while True:
        if is_app_focused(app_title):
            print(f"The {app_title} window is in focus.")
            repo = DatabaseRepository()
            last_worker = check_and_update_last_row(repo)
            if last_worker:
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p')
                if is_within_timeframe("12:00 PM", "05:00 AM", current_time,last_worker['date'],repo):
                    if is_app_focused(app_title):
                        if timer.is_timer_started():
                            pass
                        else:
                            timer.start_timer()
                    else:
                        timer.stop_timer()
                        last_worker['hour_spend_worker'] = timer.get_hours_spent() + last_worker['hour_spend_worker']
                        repo.edit_worker_by_id(last_worker['hour_spend_worker'], last_worker['id'])
                        csvrepo.copy_to_csv(csvFileName)
                    
                else:
                    repo.add_worker(last_worker['date'], 0)
                    pass
            else:
                print("Failed to get last worker from the database.")
        else:
            print(f"The {app_title} window is not in focus.")

if __name__ == "__main__":
    main()
