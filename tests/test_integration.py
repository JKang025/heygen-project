import subprocess
import time
import pytest

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from client_library.client import VideoTranslationClient, AsyncVideoTranslationClient

SERVER_START_DELAY = 3  # In seconds

@pytest.fixture(scope="function")
def start_server():
    """
    Starts the server before each test and terminates it afterward.
    """
    server_process = subprocess.Popen(
        ["python", "server/app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(SERVER_START_DELAY)  
    yield
    server_process.terminate()  
    server_process.wait()

def test_integration_polling_expo_sync(start_server):
    """
    Tests synchronous polling using exponential backoff.
    """
    print("Integration test (sync exponential backoff) started")
    base_url = "http://127.0.0.1:5000"

    client = VideoTranslationClient(base_url)

    def on_status_change(status):
        print(f"Status changed to: {status}")

    try:
        final_status = client.poll_status(
            max_wait=60,
            initial_interval=2,
            strategy="exponential_backoff",
            on_status_change=on_status_change,
        )
        assert final_status == "completed", f"Unexpected final status: {final_status}"
        print("Integration test (sync exponential backoff) passed: Job completed successfully.")
    except TimeoutError:
        print("Integration test failed: Job did not complete in time.")
    except Exception as e:
        print(f"Integration test failed with error: {e}")

def test_integration_polling_fixed_sync(start_server):
    """
    Tests synchronous polling using a fixed interval.
    """
    print("Integration test (sync fixed) started")
    base_url = "http://127.0.0.1:5000"

    client = VideoTranslationClient(base_url)

    def on_status_change(status):
        print(f"Status changed to: {status}")

    try:
        final_status = client.poll_status(
            max_wait=60,
            initial_interval=5,
            strategy="fixed",
            on_status_change=on_status_change,
        )
        assert final_status == "completed", f"Unexpected final status: {final_status}"
        print("Integration test (sync fixed) passed: Job completed successfully.")
    except TimeoutError:
        print("Integration test failed: Job did not complete in time.")
    except Exception as e:
        print(f"Integration test failed with error: {e}")


@pytest.mark.asyncio
async def test_integration_polling_expo_async(start_server):
    """
    Tests asynchronous polling using exponential backoff.
    """
    print("Integration test (async exponential backoff) started")
    base_url = "http://127.0.0.1:5000"

    client = AsyncVideoTranslationClient(base_url)

    async def on_status_change(status):
        print(f"Status changed to: {status}")

    try:
        final_status = await client.poll_status(
            max_wait=60,
            initial_interval=2,
            strategy="exponential_backoff",
            on_status_change=on_status_change,
        )
        assert final_status == "completed", f"Unexpected final status: {final_status}"
        print("Integration test (async: exponential backoff) passed: Job completed successfully.")
    except TimeoutError:
        print("Integration test failed: Job did not complete in time.")
    except Exception as e:
        print(f"Integration test failed with error: {e}")

@pytest.mark.asyncio
async def test_integration_polling_fixed_async(start_server):
    """
    Tests asynchronous polling using a fixed interval.
    """
    print("Integration test (async fixed) started")
    base_url = "http://127.0.0.1:5000"

    client = AsyncVideoTranslationClient(base_url)

    async def on_status_change(status):
        print(f"Status changed to: {status}")

    try:
        final_status = await client.poll_status(
            max_wait=60,
            initial_interval=5,
            strategy="fixed",
            on_status_change=on_status_change,
        )
        assert final_status == "completed", f"Unexpected final status: {final_status}"
        print("Integration test (async fixed) passed: Job completed successfully.")
    except TimeoutError:
        print("Integration test failed: Job did not complete in time.")
    except Exception as e:
        print(f"Integration test failed with error: {e}")
