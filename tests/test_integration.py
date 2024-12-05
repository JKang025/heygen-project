import subprocess
import time
import pytest
from client_library.client import VideoTranslationClient

SERVER_START_DELAY = 3  # Time to wait for the server to start in seconds

@pytest.fixture(scope="module")
def start_server():
    server_process = subprocess.Popen(
        ["python", "server/app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    time.sleep(SERVER_START_DELAY)  
    yield
    server_process.terminate() 
    server_process.wait()


def test_integration_polling(start_server):
    base_url = "http://127.0.0.1:5000"

    client = VideoTranslationClient(base_url)

    def on_status_change(status):
        print(f"Status changed to: {status}")

    try:
        final_status = client.poll_status(
            max_wait=30,
            initial_interval=2,
            strategy="exponential_backoff",
            on_status_change=on_status_change,
        )
        assert final_status == "completed", f"Unexpected final status: {final_status}"
        print("Integration test passed: Job completed successfully.")
    except TimeoutError:
        print("Integration test failed: Job did not complete in time.")
    except Exception as e:
        print(f"Integration test failed with error: {e}")
