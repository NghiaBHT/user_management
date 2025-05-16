# User Management API

This is a FastAPI-based User Management API.

## Prerequisites

*   Python 3.1x
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
    DATABASE_URL=postgresql://youruser:yourpassword@localhost:5432/usermanagementdb
    ACCESS_TOKEN_EXPIRE_SECONDS=604800
    SECRET_KEY=your-very-strong-secret-key
    ALGORITHM=HS256
    ```
    Ensure your `DATABASE_URL` points to your database instance.

5.  **Database Migrations**

    Setup connection database at file `alembic.ini`
    ```ini
    sqlalchemy.url = postgresql://youruser:yourpassword@localhost:5432/usermanagementdb
    ```
    This project uses Alembic for database migrations. To set up or update your database schema, run:
    ```bash
    alembic upgrade head
    ```
    If you haven't created the database yet, please create a database named `usermanagementdb` first. Then, run the above command to apply the migrations.

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
