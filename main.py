import datetime
from function import check_and_update_last_row, is_app_focused, is_within_timeframe
from timer import TimeLog
from data_repository import DatabaseRepository
from csv_repository import CSVDataRepository


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
                        repo.edit_row_by_id(last_worker['hour_spend_worker'], last_worker['id'])
                        csvrepo.copy_to_csv(csvFileName)
                    
                else:
                    repo.add_row(last_worker['date'], 0)
                    pass
            else:
                print("Failed to get last worker from the database.")
        else:
            print(f"The {app_title} window is not in focus.")

if __name__ == "__main__":
    main()
