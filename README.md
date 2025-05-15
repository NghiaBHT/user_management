# User Management API

This is a FastAPI-based User Management API.

## Prerequisites

*   Python 3.9+
*   pip (Python package installer)
*   PostgreSQL (or your configured database)

## Setup Instructions

1.  **Clone the Repository**
    ```bash
    # git clone <your-repository-url>
    # cd <your-project-directory>
    ```

2.  **Create and Activate a Virtual Environment**

    *   On macOS and Linux:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv .venv
        .venv\Scripts\activate
        ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**

    Create a `.env` file in the project root. You can copy the structure from the default settings in `app/core/config.py` or use the example below, adjusting the values as necessary:

    ```env
    DATABASE_URL=postgresql://youruser:yourpassword@localhost:5432/yourdatabasename
    ACCESS_TOKEN_EXPIRE_SECONDS=604800
    SECRET_KEY=your-very-strong-secret-key
    ALGORITHM=HS256
    ```
    Ensure your `DATABASE_URL` points to your database instance.

5.  **Database Migrations**

    This project uses Alembic for database migrations. To set up or update your database schema, run:
    ```bash
    alembic upgrade head
    ```
    (If this is the first time, you might need to initialize Alembic if it hasn't been done yet. Refer to Alembic documentation if `alembic.ini` and the migrations directory are not present.)

## Running the Application

To run the FastAPI application locally using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The application will typically be available at `http://127.0.0.1:8000`.

## Running Tests

This project uses `pytest` for testing. To run the tests:

```bash
pytest
```

Make sure your test database (if different) is configured and accessible. 