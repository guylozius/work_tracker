import time

class TimeLog:
    def __init__(self):
        self.hours_spent = []
        self.start_time = None

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        if self.start_time is not None:
            end_time = time.time()
            elapsed_time = end_time - self.start_time
            self.hours_spent.append(elapsed_time)
            self.start_time = None
            return elapsed_time
        else:
            return 0

    def clear_hours_spent(self):
        self.hours_spent = []

    def get_hours_spent(self):
        return sum(self.hours_spent)
    def is_timer_started(self):
        return self.start_time is not None
