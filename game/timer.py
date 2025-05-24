import threading
import time

class GameTimer:
    """
    A repeating timer that invokes a callback function every interval seconds.
    """

    def __init__(self, interval: float, callback):
        """
        Initialize the GameTimer.
        """
        self.interval = interval
        self.callback = callback
        self._running = False

    def _run(self):
        """
        Runs on a separate thread: waits for the interval, then calls the callback repeatedly until stopped.
        """
        while self._running:
            time.sleep(self.interval)
            self.callback(self.interval)

    def start(self):
        """
        Starts the timer, launching a background thread that triggers the callback at each interval.
        """
        self._running = True
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        """
        Stops the timer, preventing any further callback executions.
        """
        self._running = False
