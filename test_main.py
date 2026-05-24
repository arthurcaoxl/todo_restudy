from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_book():
    resp = client.post("/books", json={"title": "测试书", "author": "李四"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "测试书"
    assert data["author"] == "李四"
    assert data["read"] == False
    assert "id" in data

def test_list_books():
    resp = client.get("/books")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_book():
    post_resp = client.post("/books", json={"title": "单独获取", "author": "王五"})
    book_id = post_resp.json()["id"]
    get_resp = client.get(f"/books/{book_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "单独获取"

def test_not_found():
    resp = client.get("/books/99999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Book not found"
