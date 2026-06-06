from dotenv import load_dotenv
import os

# 加载 .env 文件（仅开发环境，生产环境应直接使用系统环境变量）
load_dotenv()

# 可选：检查必要环境变量
if not os.getenv("API_KEY"):
    print("WARNING: API_KEY not set, using default (insecure)")

from auth import verify_api_key
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/books", response_model=schemas.BookResponse, status_code=201, dependencies=[Depends(verify_api_key)])
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.create_book(db, book)
    return db_book

@app.get("/books", response_model=list[schemas.BookResponse])
def list_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.get("/books/{book_id}/similar", response_model=list[schemas.BookResponse])
def get_similar_books(book_id: int, max_depth: int = 1, db: Session = Depends(get_db)):
    # 先检查书是否存在
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    similar_books = crud.recommend_by_bfs(db, book_id, max_depth)
    return similar_books

@app.put("/books/{book_id}", response_model=schemas.BookResponse, dependencies=[Depends(verify_api_key)])
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_id, book_update)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/books/{book_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    if not crud.delete_book(db, book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return

@app.get("/books/{book_id}/similar", response_model=list[schemas.BookResponse])
def get_similar_books(book_id: int, max_depth: int = 1, db: Session = Depends(get_db)):
    similar_books = crud.recommend_by_bfs(db, book_id, max_depth)
    return similar_books
