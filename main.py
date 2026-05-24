from fastapi import FastAPI, HTTPException
from models import Book
from schemas import BookCreate, BookResponse

app = FastAPI()

books_db = []
counter = 1

@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate):
    global counter
    new_book = Book(title=book.title, author=book.author)
    new_book.id = counter
    books_db.append(new_book)
    counter += 1
    return BookResponse(
        id=new_book.id,
        title=new_book.title,
        author=new_book.author,
        read=new_book.read
    )

@app.get("/books", response_model=list[BookResponse])
def list_books():
    return [BookResponse(id=b.id, title=b.title, author=b.author, read=b.read) for b in books_db]

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    for b in books_db:
        if b.id == book_id:
            return BookResponse(id=b.id, title=b.title, author=b.author, read=b.read)
    raise HTTPException(status_code=404, detail="Book not found")
