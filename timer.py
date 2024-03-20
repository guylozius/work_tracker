import time

class Timer:
    def __init__(self):
        # Initialize the total minutes spent and the start time.
        # The start time is set to None to indicate that the timer is not running.
        self.minutes_spent = 0.0  # Total minutes spent, accumulated over multiple starts/stops.
        self._start_time = None  # The exact time the timer was started; None means the timer is not currently running.

    def start(self) -> None:
        # Start the timer by recording the current time.
        # This uses `time.perf_counter()` for high resolution timing,
        # suitable for measuring short durations.
        self._start_time = time.perf_counter()

    def stop(self) -> float:
        # Stop the timer and calculate the elapsed time since it was started.
        # Returns the number of minutes spent during this timer session.
        end_time = time.perf_counter()  # Record the time when the timer is stopped.

        if self._start_time is None:
            return 0.0  # If the timer was not started, return 0.0 minutes.
        
        elapsed_time = end_time - self._start_time  # Calculate elapsed time in seconds.
        elapsed_minutes = elapsed_time / 60  # Convert seconds to minutes.
        self.minutes_spent += elapsed_minutes  # Add the elapsed minutes to the total minutes spent.

        self._start_time = None  # Reset the start time to None to indicate the timer is not running.

        return elapsed_minutes  # Return the number of minutes spent in the latest session.

    def clear(self) -> None:
        # Reset the timer by clearing the total minutes spent.
        # This does not affect the start time as it only resets the accumulated time.
        self.minutes_spent = 0.0
    
    def is_started(self) -> bool:
        # Check if the timer is currently running.
        # Returns True if the timer has been started and not yet stopped, False otherwise.
        return self._start_time is not None  # True if `_start_time` is not None, indicating the timer is running.
