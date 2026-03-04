# import pytest
# import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_tasks_benchmark(benchmark):
    def fetch():
        r = client.get("/tasks")
        assert r.status_code == 200

    benchmark(fetch)
