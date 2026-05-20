import sqlite3
from contextlib import closing
from pathlib import Path
from urllib.parse import urlparse


SQLITE_SCHEMA = """
CREATE TABLE IF NOT EXISTS actors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birth_year INTEGER NOT NULL,
    nationality TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


class Database:
    def __init__(self, database_url):
        self.database_url = database_url
        parsed = urlparse(database_url)
        self.driver_name = parsed.scheme or "sqlite"

        if self.driver_name == "sqlite":
            raw_path = parsed.path or database_url.replace("sqlite:///", "", 1)
            self.sqlite_path = Path(raw_path.lstrip("/")).resolve()
        elif self.driver_name == "mysql":
            self.mysql_config = {
                "host": parsed.hostname or "localhost",
                "port": parsed.port or 3306,
                "user": parsed.username,
                "password": parsed.password,
                "database": parsed.path.lstrip("/"),
                "cursorclass": None,
                "autocommit": False,
            }
        else:
            raise ValueError(
                "Unsupported DATABASE_URL. Use sqlite:///path/to.db or "
                "mysql://user:password@host:3306/database_name"
            )

    def _connect(self):
        if self.driver_name == "sqlite":
            connection = sqlite3.connect(self.sqlite_path)
            connection.row_factory = sqlite3.Row
            return connection

        try:
            import pymysql
            from pymysql.cursors import DictCursor
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "PyMySQL is required for MySQL connections. Install dependencies "
                "with `pip install -r requirements.txt`."
            ) from exc

        config = dict(self.mysql_config)
        config["cursorclass"] = DictCursor
        return pymysql.connect(**config)

    def _prepare_query(self, query):
        if self.driver_name == "mysql":
            return query.replace("?", "%s")
        return query

    def ensure_sqlite_schema(self):
        if self.driver_name != "sqlite":
            return

        self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection:
            connection.executescript(SQLITE_SCHEMA)
            connection.commit()

    def fetch_all(self, query, params=()):
        sql = self._prepare_query(query)
        with closing(self._connect()) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def fetch_one(self, query, params=()):
        sql = self._prepare_query(query)
        with closing(self._connect()) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, params)
            row = cursor.fetchone()
            return dict(row) if row else None

    def execute(self, query, params=()):
        sql = self._prepare_query(query)
        with closing(self._connect()) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, params)
            connection.commit()
            return cursor.lastrowid, cursor.rowcount

