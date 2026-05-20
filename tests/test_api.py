def test_get_actors_returns_json_by_default(client):
    response = client.get("/actors")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["count"] == 3
    assert payload["actors"][0]["last_name"] == "Aunor"


def test_get_actors_supports_xml_output(client):
    response = client.get("/actors?format=xml")

    assert response.status_code == 200
    assert response.mimetype == "application/xml"
    assert "<actors>" in response.text
    assert "<last_name>Aunor</last_name>" in response.text


def test_get_single_actor_returns_404_for_missing_record(client):
    response = client.get("/actors/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Actor not found."


def test_create_actor_successfully(client):
    response = client.post(
        "/actors",
        json={
            "first_name": "Toshiro",
            "last_name": "Mifune",
            "birth_year": 1920,
            "nationality": "Japanese",
        },
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["first_name"] == "Toshiro"
    assert payload["id"] > 0


def test_create_actor_validates_payload(client):
    response = client.post(
        "/actors",
        json={"first_name": "", "last_name": "Mifune", "birth_year": 1920},
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_update_actor_successfully(client):
    response = client.put(
        "/actors/2",
        json={"nationality": "American / Stage and Screen"},
    )

    assert response.status_code == 200
    assert response.get_json()["nationality"] == "American / Stage and Screen"


def test_update_actor_returns_404_when_missing(client):
    response = client.put("/actors/999", json={"nationality": "Unknown"})

    assert response.status_code == 404
    assert response.get_json()["error"] == "Actor not found."


def test_delete_actor_successfully(client):
    response = client.delete("/actors/3")

    assert response.status_code == 204

    follow_up = client.get("/actors/3")
    assert follow_up.status_code == 404


def test_search_filters_records(client):
    response = client.get("/actors?q=Filip")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["count"] == 2
    assert {actor["last_name"] for actor in payload["actors"]} == {"Aunor", "Salonga"}


def test_invalid_format_returns_400(client):
    response = client.get("/actors?format=yaml")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Unsupported format. Use json or xml."

