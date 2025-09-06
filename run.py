import subprocess
import sys
import os

def main():
    # Get the absolute path to the directory containing run.py
    run_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.join(run_dir, "app")

    # Start the backend (FastAPI)
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=app_dir,
    )

    # Start the frontend (Streamlit)
    # We add a small delay to ensure the backend is up before the frontend starts
    try:
        import time
        time.sleep(5)
    except ImportError:
        pass # If time module is not available for some reason, just continue

    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend.py"],
        cwd=app_dir,
    )

    # Wait for the processes to complete
    backend_process.wait()
    frontend_process.wait()

if __name__ == "__main__":
    main()
