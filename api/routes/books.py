from typing import OrderedDict
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from api.db.schemas import Book, Genre, InMemoryDB

# Initialize the router
router = APIRouter()

# Initialize InMemoryDB with some sample books
db = InMemoryDB()
db.books = {
    1: Book(
        id=1,
        title="The Hobbit",
        author="J.R.R. Tolkien",
        publication_year=1937,
        genre=Genre.SCI_FI,
    ),
    2: Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        publication_year=1954,
        genre=Genre.FANTASY,
    ),
    3: Book(
        id=3,
        title="The Return of the King",
        author="J.R.R. Tolkien",
        publication_year=1955,
        genre=Genre.FANTASY,
    ),
}

# Existing POST route for creating a book
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    db.add_book(book)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=book.model_dump()
    )

# Existing GET route for getting all books
@router.get("/", response_model=OrderedDict[int, Book], status_code=status.HTTP_200_OK)
async def get_books() -> OrderedDict[int, Book]:
    return db.get_books()

# Existing PUT route for updating a book
@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: Book) -> Book:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=db.update_book(book_id, book).model_dump(),
    )

# New GET route for getting a book by ID
@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int):
    """Retrieve a book by its ID"""
    book = db.get_book(book_id)
    
    if not book:
        raise HTTPException(
            status_code=404, detail=f"Book with ID {book_id} not found"
        )
    
    return book

