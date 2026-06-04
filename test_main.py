from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_book():
    resp = client.post("/books", json={"title": "测试书", "author": "李四"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "测试书"
    assert data["author"] == "李四"
    # 不要返回任何东西，或者添加一个断言

def test_get_books():
    resp = client.get("/books")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_book_by_id():
    # 先创建一个
    create_resp = client.post("/books", json={"title": "查ID书", "author": "王五"})
    book_id = create_resp.json()["id"]
    resp = client.get(f"/books/{book_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "查ID书"

def test_update_book():
    create_resp = client.post("/books", json={"title": "原书名", "author": "赵六"})
    book_id = create_resp.json()["id"]
    resp = client.put(f"/books/{book_id}", json={"title": "新书名", "author": "赵六"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "新书名"

def test_delete_book():
    create_resp = client.post("/books", json={"title": "待删", "author": "钱七"})
    book_id = create_resp.json()["id"]
    resp = client.delete(f"/books/{book_id}")
    assert resp.status_code == 204
    get_resp = client.get(f"/books/{book_id}")
    assert get_resp.status_code == 404

def test_get_similar_books():
    # 先创建两个有共同作者的书
    client.post("/books", json={"title": "书A", "author": "共同作者"})
    client.post("/books", json={"title": "书B", "author": "共同作者"})
    # 获取第一本书的推荐
    resp = client.get("/books/1/similar?max_depth=1")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

def test_get_similar_not_found():
    resp = client.get("/books/99999/similar")
    assert resp.status_code == 404

def test_create_book_invalid():
    resp = client.post("/books", json={"title": "", "author": ""})
    assert resp.status_code == 422
