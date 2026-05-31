from sqlalchemy.orm import Session
from collections import deque
from models import Book
from schemas import BookCreate, BookUpdate


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: BookCreate):
    db_book = Book(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_update: BookUpdate):
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    if book_update.title is not None:
        db_book.title = book_update.title
    if book_update.author is not None:
        db_book.author = book_update.author
    if book_update.read is not None:
        db_book.read = book_update.read
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False


def get_books_by_author(db: Session):
    """返回作者名 -> 该书作者的所有书籍列表"""
    books = db.query(Book).all()
    author_map = {}
    for book in books:
        if book.author not in author_map:
            author_map[book.author] = []
        author_map[book.author].append(book)
    return author_map

def recommend_by_bfs(db: Session, book_id: int, max_depth: int = 1):
    target = get_book(db, book_id)
    if not target:
        return []
    
    author_books = get_books_by_author(db)
    all_books = db.query(Book).all()   # 改正点：models.Book → Book
    books_by_id = {b.id: b for b in all_books}
    
    queue = deque()
    queue.append((book_id, 0))
    visited = {book_id}
    recommendations = []
    
    while queue:
        curr_id, dist = queue.popleft()
        if dist > max_depth:
            continue
        if dist > 0:
            recommendations.append((dist, curr_id))
        
        curr_book = books_by_id[curr_id]
        if curr_book.author in author_books:
            for neighbor in author_books[curr_book.author]:
                if neighbor.id not in visited:
                    visited.add(neighbor.id)
                    queue.append((neighbor.id, dist + 1))
    
    recommendations.sort(key=lambda x: (x[0], x[1]))
    return [books_by_id[bid] for _, bid in recommendations]