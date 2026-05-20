from datetime import datetime


ALLOWED_FIELDS = {"first_name", "last_name", "birth_year", "nationality"}
REQUIRED_FIELDS = {"first_name", "last_name", "birth_year", "nationality"}


def validate_actor_payload(payload, partial=False):
    if not isinstance(payload, dict):
        return None, "Request body must be a JSON object."

    extra_fields = sorted(set(payload) - ALLOWED_FIELDS)
    if extra_fields:
        return None, f"Unexpected fields: {', '.join(extra_fields)}."

    missing_fields = sorted(REQUIRED_FIELDS - set(payload))
    if missing_fields and not partial:
        return None, f"Missing required fields: {', '.join(missing_fields)}."

    if partial and not payload:
        return None, "Provide at least one field to update."

    cleaned = {}
    current_year = datetime.now().year

    for field, value in payload.items():
        if field in {"first_name", "last_name", "nationality"}:
            if not isinstance(value, str) or not value.strip():
                return None, f"{field} must be a non-empty string."
            cleaned[field] = value.strip()
        elif field == "birth_year":
            if not isinstance(value, int):
                return None, "birth_year must be an integer."
            if value < 1850 or value > current_year:
                return None, f"birth_year must be between 1850 and {current_year}."
            cleaned[field] = value

    return cleaned, None

