from datetime import datetime, time
import re
import pygetwindow as gw

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
