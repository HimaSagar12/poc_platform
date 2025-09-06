# How to Run the POC Recruitment Platform

This document provides instructions on how to set up and run the POC Recruitment Platform.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.8+ and `pip`

## Setup and Running the Application

### 1. Create a Virtual Environment (Highly Recommended)

To avoid conflicts with other Python packages on your system, it is highly recommended to use a virtual environment.

- **Navigate to the project directory:**
  ```bash
  cd poc_platform
  ```

- **Create a virtual environment:**
  ```bash
  python -m venv venv
  ```

- **Activate the virtual environment:**
  - On **macOS/Linux**:
    ```bash
    source venv/bin/activate
    ```
  - On **Windows**:
    ```bash
    .\venv\Scripts\activate
    ```

### 2. Install Dependencies

Once your virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python run.py
```

This command will start both the backend and the frontend services.

- The backend API will be running at `http://127.0.0.1:8000`.
- The frontend application will be accessible at `http://localhost:8501`.

If the application fails to start, please check the `logs` directory for error logs.