# import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_list_tasks_empty():
    r = client.get("/tasks")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_and_get_task():
    payload = {"title": "Test task", "description": "Ceci est un test."}
    r = client.post("/tasks", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    task_id = data["id"]
    r2 = client.get(f"/tasks/{task_id}")
    assert r2.status_code == 200
    assert r2.json()["id"] == task_id


def test_update_and_delete_task():
    payload = {"title": "À modifier", "description": "desc"}
    r = client.post("/tasks", json=payload)
    assert r.status_code == 201
    data = r.json()
    task_id = data["id"]
    # Update
    r2 = client.put(f"/tasks/{task_id}", json={"status": "DONE"})
    assert r2.status_code == 200
    assert r2.json()["status"] == "DONE"
    # Delete
    r3 = client.delete(f"/tasks/{task_id}")
    assert r3.status_code == 204
    # Not found après suppression
    r4 = client.get(f"/tasks/{task_id}")
    assert r4.status_code == 404


def test_create_task_missing_title():
    r = client.post("/tasks", json={"description": "no title"})
    assert r.status_code == 422


def test_update_task_not_found():
    r = client.put("/tasks/99999", json={"status": "DONE"})
    assert r.status_code == 404


def test_delete_task_not_found():
    r = client.delete("/tasks/99999")
    assert r.status_code == 404


def test_admin_stats_unauthorized():
    r = client.get("/admin/stats")
    assert r.status_code == 401


def test_debug_unauthorized():
    r = client.get("/debug")
    assert r.status_code == 401


def test_import_yaml():
    payload = "a: 1\nb: 2"
    r = client.post("/import", json={"payload": payload})
    assert r.status_code == 200
    assert r.json()["imported"] is True
    assert "a" in r.json()["keys"]


def test_import_yaml_invalid():
    # Utilise un YAML vraiment invalide (crochet non fermé)
    payload = "a: [1, 2"
    r = client.post("/import", json={"payload": payload})
    assert r.status_code == 400


def test_search_tasks():
    # Ajoute une tâche pour la recherche
    client.post("/tasks", json={"title": "RechercheTest", "description": "abc"})
    r = client.get("/tasks/search", params={"q": "RechercheTest"})
    assert r.status_code == 200
    assert any("RechercheTest" in t["title"] for t in r.json())


def test_admin_stats_authorized():
    from app.main import API_KEY

    r = client.get("/admin/stats", headers={"x-api-key": API_KEY})
    assert r.status_code == 200
    assert "tasks" in r.json()


def test_debug_authorized():
    from app.main import API_KEY

    r = client.get("/debug", headers={"x-api-key": API_KEY})
    assert r.status_code == 200
    assert "env" in r.json()


def test_create_task_long_title():
    long_title = "a" * 201
    r = client.post("/tasks", json={"title": long_title, "description": "desc"})
    assert r.status_code == 422


def test_create_task_empty_title():
    r = client.post("/tasks", json={"title": "", "description": "desc"})
    assert r.status_code == 422


def test_update_task_invalid_status():
    r = client.post("/tasks", json={"title": "Tâche", "description": "desc"})
    task_id = r.json()["id"]
    r2 = client.put(f"/tasks/{task_id}", json={"status": "INVALID"})
    assert r2.status_code == 422
