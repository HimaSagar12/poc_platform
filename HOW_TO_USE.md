# How to Run the POC Recruitment Platform

This document provides instructions on how to set up and run the POC Recruitment Platform.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.8+ and `pip`

## Setup and Running the Application

1.  **Navigate to the project directory:**
    ```bash
    cd poc_platform
    ```

2.  **Create a Python virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    - On **macOS/Linux**:
      ```bash
      source venv/bin/activate
      ```
    - On **Windows**:
      ```bash
      .\venv\Scripts\activate
      ```

4.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the application:**
    ```bash
    python run.py
    ```
    This command will start both the backend and the frontend services.

    - The backend API will be running at `http://127.0.0.1:8000`.
    - The frontend application will be accessible at `http://localhost:8501`.
