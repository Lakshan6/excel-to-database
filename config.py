"""
config.py
---------
All environment-specific settings live here. Values are read from
environment variables first, falling back to the defaults below so the
project runs out-of-the-box for local development.

Edit the DB_* defaults to match your local PostgreSQL instance, or export
the equivalent environment variables before running main.py.
"""

import os

# ---------------------------------------------------------------------------
# Database connection
# ---------------------------------------------------------------------------
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "database")

# The schema that contains product / spec / test (per your DDL: "ate")
DB_SCHEMA = os.environ.get("DB_SCHEMA", "ate")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ---------------------------------------------------------------------------
# File paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_EXCEL_PATH = os.path.join(BASE_DIR, "data", "products.xlsx")
MAPPING_FILE_PATH = os.path.join(BASE_DIR, "mappings", "column_mapping.json")
LOG_FILE_PATH = os.path.join(BASE_DIR, "logs", "import.log")
