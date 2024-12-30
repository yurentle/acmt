import sys
import threading
import itertools
import time

class Spinner:
    """A simple spinner class for command line interfaces."""
    
    def __init__(self, message="Loading...", delay=0.1):
        """Initialize the spinner with a message and delay."""
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.delay = delay
        self.message = message
        self.running = False
        self.spinner_thread = None

    def _spin(self):
        """Internal method to update the spinner animation."""
        while self.running:
            sys.stdout.write(f"\r{next(self.spinner)} {self.message}")
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b' * (len(self.message) + 2))

    def __enter__(self):
        """Start the spinner when entering the context."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop the spinner when exiting the context."""
        self.stop()

    def start(self):
        """Start the spinner animation."""
        if not self.running:
            self.running = True
            self.spinner_thread = threading.Thread(target=self._spin)
            self.spinner_thread.daemon = True
            self.spinner_thread.start()

    def stop(self):
        """Stop the spinner animation and clear the line."""
        self.running = False
        if self.spinner_thread is not None:
            self.spinner_thread.join()
        sys.stdout.write('\r' + ' ' * (len(self.message) + 2) + '\r')
        sys.stdout.flush()
