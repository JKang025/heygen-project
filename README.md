# Video Translation Client Library

This repository contains a client library to interact with a simulated video translation backend. The server implements a `/status` API to return the status of a video translation job.

## Bells and Whistles

1. The client library includes trivial fixed polling alongside more intelligent exponential backoff polling, both of which are configurable.
2. The client library supports both synchronous and asynchronous approaches.
3. The client library provides an optional callback function that triggers once the status changes.
4. The client library includes robust exception handling to gracefully manage network errors, timeouts, and unexpected server responses.
5. The client library includes a basic get_status function for customers who wish to build their own custom polling function.
6. The client library has clear logging using a logger.
7. The server simulation is comprehensive and customizable. It is easy to edit the server configuration to simulate fixed, uniform, or Gaussian delay and error probabilities.
8. The project uses pytest to set up a robust testing framework that currently implements four integration tests but can be easily expanded to fit customer needs.

## Setup
1. Clone the repository:
   ```bash
   git clone git@github.com:JKang025/heygen-project.git
   ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run integration tests:
    ```bash
    pytest -s tests/test_integration.py
    ```
## Documentation
### Synchronous Client

**Initalization**
```
from video_translation_client import VideoTranslationClient

client = VideoTranslationClient(base_url="http://your-api-url.com", timeout=5)
```
* base_url (str): The base URL of the video translation server
* timeout (int, optional): Request timeout in seconds. Default is 5


**Get Status:**
Retrieve the current status of a video translation job.
```
status = client.get_status()
print(f"Current status: {status}")
```
* Returns: str — The current job status.
* Raises: ServerError if the server response is invalid.


**Poll Status:**
Continuously poll the job status until it completes or fails.
```
final_status = client.poll_status(
    max_wait=300,
    initial_interval=1,
    strategy='fixed',
    on_status_change=handle_status_change
)
```
* Parameters:
    * max_wait (int, optional): Maximum total wait time in seconds. Default is 300.
    * initial_interval (int, optional): Initial polling interval in seconds. Default is 1.
    * strategy (str, optional): Polling strategy ('fixed' or 'exponential_backoff'). Default is 'fixed'.
    * max_interval (int, optional): Maximum interval for exponential backoff. Default is 60.
    * backoff_factor (int, optional): Backoff multiplier. Default is 2.
    * on_status_change (callable, optional): Callback function when status changes.
* Returns: str — Final job status ('completed' or 'error').
* Raises:
    * TimeoutError if the job doesn't complete within max_wait.
    * ValueError if an invalid strategy is provided.
    * ServerError if there's an issue fetching the status.

**Example**
```
def handle_status_change(new_status):
    print(f"Status changed to: {new_status}")

try:
    final_status = client.poll_status(
        max_wait=300,
        initial_interval=1,
        strategy='exponential_backoff',
        on_status_change=handle_status_change
    )
    print(f"Final status: {final_status}")
except TimeoutError as e:
    print(f"Timeout Error: {e}")
except ServerError as e:
    print(f"Server Error: {e}")
```

### Asynchronous Client

**Initalization**
```
from video_translation_client import AsyncVideoTranslationClient

client = AsyncVideoTranslationClient(base_url="http://your-api-url.com", timeout=5)
```
* base_url (str): The base URL of the video translation server
* timeout (int, optional): Request timeout in seconds. Default is 5


**Get Status:**
Retrieve the current status of a video translation job.
```
import asyncio

async def get_status():
    status = await async_client.get_status()
    print(f"Current status: {status}")

asyncio.run(get_status())
```
* Returns: str — The current job status.
* Raises: ServerError if the server response is invalid.


**Poll Status:**
Continuously poll the job status until it completes or fails.
```
async def handle_status_change(new_status):
    print(f"Status changed to: {new_status}")

async def poll_status():
    try:
        final_status = await async_client.poll_status(
            max_wait=300,
            initial_interval=1,
            strategy='fixed',
            on_status_change=handle_status_change
        )
        print(f"Final status: {final_status}")
    except TimeoutError as e:
        print(f"Timeout Error: {e}")
    except ServerError as e:
        print(f"Server Error: {e}")

asyncio.run(poll_status())
```
* Parameters:
    * max_wait (int, optional): Maximum total wait time in seconds. Default is 300.
    * initial_interval (int, optional): Initial polling interval in seconds. Default is 1.
    * strategy (str, optional): Polling strategy ('fixed' or 'exponential_backoff'). Default is 'fixed'.
    * max_interval (int, optional): Maximum interval for exponential backoff. Default is 60.
    * backoff_factor (int, optional): Backoff multiplier. Default is 2.
    * on_status_change (callable, optional): Callback function when status changes.
* Returns: str — Final job status ('completed' or 'error').
* Raises:
    * TimeoutError if the job doesn't complete within max_wait.
    * ValueError if an invalid strategy is provided.
    * ServerError if there's an issue fetching the status.

**Example**
```
def handle_status_change(new_status):
    print(f"Status changed to: {new_status}")

try:
    final_status = client.poll_status(
        max_wait=300,
        initial_interval=1,
        strategy='exponential_backoff',
        on_status_change=handle_status_change
    )
    print(f"Final status: {final_status}")
except TimeoutError as e:
    print(f"Timeout Error: {e}")
except ServerError as e:
    print(f"Server Error: {e}")
```

## Testing
### Testing Options
To change the server's settings regarding it's probablity of returning an error and time for delay, alter these options in config.py. The default is set to 0% error and delay time between [15.0s, 30.0s]
```
DELAY_CONFIG = {
    'model': 'uniform',  # Choose between 'fixed', 'uniform', or 'gaussian'
    'params': {
        'delay': 20.0,  # Used for 'fixed'
        'min_delay': 15.0,  # Used for 'uniform'
        'max_delay': 30.0,  # Used for 'uniform'
        'mean_delay': 10.0,  # Used for 'gaussian'
        'stddev_delay': 2.0,  # Used for 'gaussian'
    }
}

ERROR_CONFIG = {
    'model': 'fixed',  # Choose between 'fixed', 'uniform', or 'gaussian'
    'params': {
        'probability': 0.0,  # Used for 'fixed'
        'min_probability': 0.05,  # Used for 'uniform'
        'max_probability': 0.15,  # Used for 'uniform'
        'mean_probability': 0.1,  # Used for 'gaussian'
        'stddev_probability': 0.02,  # Used for 'gaussian'
    }
}
```
### Integration Tests
Within test/test_integration.py, it contains four independent integration tests for async fixed polling, async exponential polling, sync fixed polling, and sync exponential polling. The server follows default config stated aboved
```
pytest -s tests/test_integration.py
```

