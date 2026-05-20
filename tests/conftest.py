from pathlib import Path
from uuid import uuid4

import pytest

from app import create_app


@pytest.fixture()
def client():
    runtime_dir = Path(__file__).resolve().parent / "_runtime"
    runtime_dir.mkdir(exist_ok=True)
    database_path = runtime_dir / f"test_actors_{uuid4().hex}.db"

    app = create_app(
        {
            "TESTING": True,
            "DATABASE_URL": f"sqlite:///{database_path.as_posix()}",
        }
    )
    seed_records(app)

    try:
        yield app.test_client()
    finally:
        if database_path.exists():
            database_path.unlink()


def seed_records(app):
    db = app.config["DB"]
    records = [
        ("Nora", "Aunor", 1953, "Filipino"),
        ("Viola", "Davis", 1965, "American"),
        ("Lea", "Salonga", 1971, "Filipino"),
    ]

    for record in records:
        db.execute(
            """
            INSERT INTO actors (first_name, last_name, birth_year, nationality)
            VALUES (?, ?, ?, ?)
            """,
            record,
        )

