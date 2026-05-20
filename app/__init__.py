import os

from flask import Flask

from .db import Database
from .routes import register_routes


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE_URL=os.getenv("DATABASE_URL", "sqlite:///actors.db"),
        JSON_SORT_KEYS=False,
    )

    if test_config:
        app.config.update(test_config)

    app.config["DB"] = Database(app.config["DATABASE_URL"])

    if app.config["DB"].driver_name == "sqlite":
        app.config["DB"].ensure_sqlite_schema()

    register_routes(app)
    return app

