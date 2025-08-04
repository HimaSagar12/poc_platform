# How to Run the POC Recruitment Platform

This document provides instructions on how to set up and run the backend and frontend services for the POC Recruitment Platform.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.8+ and `pip`
- Node.js 18+ and `npm`

## Backend Setup (FastAPI)

1.  **Navigate to the backend directory:**
    ```bash
    cd poc_recruitment_platform/backend
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

5.  **Run the FastAPI development server:**
    ```bash
    uvicorn main:app --reload
    ```
    The backend API will now be running at `http://127.0.0.1:8000`.

## Frontend Setup (PyReact)

The frontend is now served by the backend.

1.  **Ensure the backend server is running.**

2.  **Open your web browser and navigate to `http://127.0.0.1:8000`**

    The application will load, and you can interact with it through the browser.
