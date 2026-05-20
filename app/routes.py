from flask import current_app, request

from .formatters import build_response
from .validators import validate_actor_payload


ACTOR_FIELDS = "id, first_name, last_name, birth_year, nationality, created_at"


def register_routes(app):
    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    @app.get("/actors")
    def get_actors():
        db = current_app.config["DB"]
        filters = []
        params = []

        first_name = request.args.get("first_name")
        last_name = request.args.get("last_name")
        nationality = request.args.get("nationality")
        born_after = request.args.get("born_after", type=int)
        born_before = request.args.get("born_before", type=int)
        search_term = request.args.get("q")

        if first_name:
            filters.append("first_name = ?")
            params.append(first_name)
        if last_name:
            filters.append("last_name = ?")
            params.append(last_name)
        if nationality:
            filters.append("nationality = ?")
            params.append(nationality)
        if born_after is not None:
            filters.append("birth_year >= ?")
            params.append(born_after)
        if born_before is not None:
            filters.append("birth_year <= ?")
            params.append(born_before)
        if search_term:
            filters.append("(first_name LIKE ? OR last_name LIKE ? OR nationality LIKE ?)")
            like_value = f"%{search_term}%"
            params.extend([like_value, like_value, like_value])

        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
        actors = db.fetch_all(
            f"SELECT {ACTOR_FIELDS} FROM actors {where_clause} ORDER BY last_name, first_name",
            tuple(params),
        )
        return build_response({"count": len(actors), "actors": actors}, root="actors_response")

    @app.get("/actors/<int:actor_id>")
    def get_actor(actor_id):
        db = current_app.config["DB"]
        actor = db.fetch_one(
            f"SELECT {ACTOR_FIELDS} FROM actors WHERE id = ?",
            (actor_id,),
        )
        if not actor:
            return build_response({"error": "Actor not found."}, status=404, root="error")
        return build_response(actor, root="actor")

    @app.post("/actors")
    def create_actor():
        payload, error = validate_actor_payload(request.get_json(silent=True), partial=False)
        if error:
            return build_response({"error": error}, status=400, root="error")

        db = current_app.config["DB"]
        actor_id, _ = db.execute(
            """
            INSERT INTO actors (first_name, last_name, birth_year, nationality)
            VALUES (?, ?, ?, ?)
            """,
            (
                payload["first_name"],
                payload["last_name"],
                payload["birth_year"],
                payload["nationality"],
            ),
        )
        actor = db.fetch_one(
            f"SELECT {ACTOR_FIELDS} FROM actors WHERE id = ?",
            (actor_id,),
        )
        return build_response(actor, status=201, root="actor")

    @app.put("/actors/<int:actor_id>")
    def update_actor(actor_id):
        payload, error = validate_actor_payload(request.get_json(silent=True), partial=True)
        if error:
            return build_response({"error": error}, status=400, root="error")

        db = current_app.config["DB"]
        existing_actor = db.fetch_one(
            f"SELECT {ACTOR_FIELDS} FROM actors WHERE id = ?",
            (actor_id,),
        )
        if not existing_actor:
            return build_response({"error": "Actor not found."}, status=404, root="error")

        assignments = []
        params = []
        for field, value in payload.items():
            assignments.append(f"{field} = ?")
            params.append(value)
        params.append(actor_id)

        _, rowcount = db.execute(
            f"UPDATE actors SET {', '.join(assignments)} WHERE id = ?",
            tuple(params),
        )
        if rowcount == 0:
            return build_response({"error": "Actor not found."}, status=404, root="error")

        actor = db.fetch_one(
            f"SELECT {ACTOR_FIELDS} FROM actors WHERE id = ?",
            (actor_id,),
        )
        return build_response(actor, root="actor")

    @app.delete("/actors/<int:actor_id>")
    def delete_actor(actor_id):
        db = current_app.config["DB"]
        existing_actor = db.fetch_one("SELECT id FROM actors WHERE id = ?", (actor_id,))
        if not existing_actor:
            return build_response({"error": "Actor not found."}, status=404, root="error")

        db.execute("DELETE FROM actors WHERE id = ?", (actor_id,))
        return ("", 204)

