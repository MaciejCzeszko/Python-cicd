import os
import threading

os.environ.setdefault("DATABASE_URL", "sqlite:///app_test.db")

import pytest
from fastapi.testclient import TestClient

from app import main
from app.database import Base, SessionLocal, engine
from app.main import app
from app.models import Score

Base.metadata.create_all(engine)


@pytest.fixture(autouse=True)
def reset_state():
    db = SessionLocal()
    db.query(Score).delete()
    db.commit()
    db.close()
    main.count = 0
    yield
    db = SessionLocal()
    db.query(Score).delete()
    db.commit()
    db.close()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_index_page(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "<html" in r.text.lower()


def test_click_increments(client):
    r1 = client.post("/api/click")
    assert r1.status_code == 200
    r2 = client.post("/api/click")
    assert r2.json()["count"] == r1.json()["count"] + 1


def test_save_resets_count(client):
    client.post("/api/click")
    client.post("/api/click")
    r = client.post("/api/save", json={"name": "alice"})
    assert r.status_code == 200
    assert r.json()["count"] == 0
    assert client.post("/api/click").json()["count"] == 1


def test_save_returns_row(client):
    r = client.post("/api/save", json={"name": "bob"})
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "bob"
    assert "id" in data and "score" in data


def test_scores_includes_saved_rows(client):
    client.post("/api/save", json={"name": "carol"})
    r = client.get("/api/scores")
    assert r.status_code == 200
    assert any(row["name"] == "carol" for row in r.json())


def test_scores_ordered_desc():
    db = SessionLocal()
    db.add_all([Score(name="low", score=1), Score(name="high", score=99)])
    db.commit()
    db.close()
    scores = TestClient(app).get("/api/scores").json()
    assert all(
        scores[i]["score"] >= scores[i + 1]["score"]
        for i in range(len(scores) - 1)
    )


def test_concurrent_clicks_all_counted():
    main.count = 0
    with TestClient(app) as client:
        threads = [
            threading.Thread(target=client.post, args=("/api/click",))
            for _ in range(10)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    assert main.count == 10
