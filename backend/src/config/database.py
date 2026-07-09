import pyodbc
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()


def _build_conn_str() -> str:
    return (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER', 'localhost')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
        f"TrustServerCertificate=yes;"
    )


@contextmanager
def get_pyodbc_connection():
    conn = pyodbc.connect(_build_conn_str(), timeout=10)
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
