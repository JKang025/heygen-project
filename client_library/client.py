import requests
import logging
from .exceptions import ServerError
import time

class VideoTranslationClient:
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url
        self.timeout = timeout

         # Set up logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)  

        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)

            self.logger.addHandler(console_handler)

    def get_status(self):
        response = requests.get(f"{self.base_url}/status", timeout=self.timeout)
        if response.status_code != 200:
            raise ServerError("Failed to fetch status.")
        return response.json()["result"]

    def poll_status(
        self,
        max_wait=300,
        initial_interval=5,
        strategy='fixed',  # 'fixed' or 'exponential_backoff'
        max_interval=60,
        backoff_factor=2,
        on_status_change=None  # Optional callback function
        ):
        """
        Polls the status of a job until it is completed or an error occurs.

        Parameters:
            max_wait (int): Maximum time to wait for the job to complete (in seconds).
            initial_interval (int): Initial interval between polls (in seconds).
            strategy (str): Polling strategy to use ('fixed' or 'exponential_backoff').
            max_interval (int): Maximum interval between polls when using exponential backoff.
            backoff_factor (int): Factor by which the interval increases in exponential backoff.
            on_status_change (callable, optional): Function to call when status changes.

        Returns:
            str: The final status of the job ('completed' or 'error').

        Raises:
            TimeoutError: If the job does not complete within the max_wait time.
            ValueError: If an invalid strategy is provided.
            ServerError: If there is an issue fetching the status from the server.
        """
        start_time = time.time()
        current_interval = initial_interval
        previous_status = None  # Initialize previous status

        while (time.time() - start_time) < max_wait:
            try:
                status = self.get_status()
                self.logger.debug(f"Polled status: {status}")

                # Check if status has changed
                if status != previous_status:
                    if on_status_change is not None:
                        on_status_change(status)
                    previous_status = status

                if status in ['completed', 'error']:
                    self.logger.info(f"Job status: {status}")
                    return status

            except Exception as e:
                self.logger.error(f"Error while fetching status: {e}")
                raise

            self.logger.debug(f"Waiting for {current_interval} seconds before next poll.")
            time.sleep(current_interval)

            # Update interval based on strategy
            if strategy == 'fixed':
                current_interval = initial_interval  # Keep interval constant
            elif strategy == 'exponential_backoff':
                current_interval = min(current_interval * backoff_factor, max_interval)
            else:
                raise ValueError("Invalid strategy. Choose 'fixed' or 'exponential_backoff'.")

        # If we reach here, the polling has timed out
        self.logger.warning(f"Job did not complete within {max_wait} seconds.")
        raise TimeoutError(f"Job did not complete within {max_wait} seconds.")
