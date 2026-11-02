```python
import sqlite3
from pathlib import Path
from contextlib import contextmanager


# Database location
DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "leads.db"
)


@contextmanager
def get_connection():
    """
    Create and safely close a database connection.
    """

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(
        DB_PATH,
        timeout=10
    )

    conn.row_factory = sqlite3.Row

    try:
        conn.execute("PRAGMA busy_timeout = 10000")
        conn.execute("PRAGMA foreign_keys = ON")

        yield conn

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def initialize_database():
    """
    Create database table if it does not exist.
    """

    with get_connection() as conn:

        conn.execute("PRAGMA journal_mode = WAL")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                email TEXT NOT NULL UNIQUE,

                phone TEXT NOT NULL,

                company TEXT NOT NULL,

                requirement TEXT NOT NULL,

                category TEXT NOT NULL,

                status TEXT NOT NULL,

                received_at TEXT NOT NULL

            )
        """)


def insert_lead(lead: dict):
    """
    Insert a new lead into the database.
    """

    with get_connection() as conn:

        cursor = conn.execute("""
            INSERT INTO leads (
                name,
                email,
                phone,
                company,
                requirement,
                category,
                status,
                received_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lead["name"],
            lead["email"],
            lead["phone"],
            lead["company"],
            lead["requirement"],
            lead["category"],
            lead["status"],
            lead["received_at"]
        ))

        return cursor.lastrowid


def fetch_leads(limit: int = 100):
    """
    Retrieve leads from the database.
    """

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT *
            FROM leads
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

        return [dict(row) for row in rows]


def email_exists(email: str) -> bool:
    """
    Check whether an email already exists.
    """

    with get_connection() as conn:

        row = conn.execute(
            "SELECT 1 FROM leads WHERE email = ?",
            (email,)
        ).fetchone()

        return row is not None
```
