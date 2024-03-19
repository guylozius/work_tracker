import time

class TimeLog:
    def __init__(self):
        self.minutes_spent = []  # Changed from hours_spent to minutes_spent
        self.start_time = None

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        if self.start_time is not None:
            end_time = time.time()
            elapsed_time = end_time - self.start_time
            elapsed_minutes = elapsed_time / 60  # Convert seconds to minutes
            self.minutes_spent.append(elapsed_minutes)
            self.start_time = None
            return elapsed_minutes
        else:
            return 0

    def clear_minutes_spent(self):
        self.minutes_spent = []

    def get_minutes_spent(self):
        return sum(self.minutes_spent)
    
    def is_timer_started(self):
        return self.start_time is not None
