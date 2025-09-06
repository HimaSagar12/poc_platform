import subprocess
import sys
import os
import time
import socket

def wait_for_port(port, host='127.0.0.1', timeout=30.0):
    """Wait until a port starts accepting TCP connections."""
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except (socket.timeout, ConnectionRefusedError):
            time.sleep(0.1)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError(f'Waited too long for the port {port} on host {host} to start accepting connections.')

def main():
    # Get the absolute path to the directory containing run.py
    run_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.join(run_dir, "app")
    log_dir = os.path.join(run_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Open log files
    backend_stdout_log = open(os.path.join(log_dir, "backend_stdout.log"), "w")
    backend_stderr_log = open(os.path.join(log_dir, "backend_stderr.log"), "w")


    # Start the backend (FastAPI)
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=app_dir,
        stdout=backend_stdout_log,
        stderr=backend_stderr_log,
    )

    try:
        # Wait for the backend to be ready
        wait_for_port(8000)

        # Start the frontend (Streamlit)
        frontend_process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "frontend.py"],
            cwd=app_dir,
        )

        # Wait for the processes to complete
        frontend_process.wait()

    except TimeoutError as e:
        print(e)
        print("The backend failed to start. Check the logs in the 'logs' directory for more information.")

    finally:
        # Terminate the backend process when the frontend is closed
        backend_process.terminate()
        backend_process.wait()
        backend_stdout_log.close()
        backend_stderr_log.close()


if __name__ == "__main__":
    main()
