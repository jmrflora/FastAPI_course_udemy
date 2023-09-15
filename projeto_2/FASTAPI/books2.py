from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self. author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
    

class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=180)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1900, lt=2024)
    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'codingwithroby',
                'description': 'A new description of a book',
                'rating': 5,
                'published_date': 2012
            }
        }

BOOKS =[
    Book(1, 'Computer science pro', 'codingwithroby', 'A very nice book!', 5, 2020),
    Book(2, 'Be fast with fastapi', 'codingwithroby', 'A great book', 5, 2012),
    Book(3, 'Master endpoints', 'codingwithroby', 'A awesome book!', 5, 2018),
    Book(4, 'HP1', 'Author 1', 'Book description', 2, 1999),
    Book(5, 'HP2', 'Author 2', 'Book description', 3, 1999),
    Book(6, 'HP3', 'Author', 'Book description', 1, 1999)
]

@app.get("/book", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS
 
@app.get("/book/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int= Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book 
    raise HTTPException(status_code=404, detail="item not found in the server")

@app.get("/book/",status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int= Query(gt=0, lt=6)):
    books_to_return =[]
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/book/publish/",status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_date: int=Query(gt=1900, lt=2024)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return

@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id +1
    else:
        book.id = 1
    return book

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="item not found")
 
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int= Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="item not found")
