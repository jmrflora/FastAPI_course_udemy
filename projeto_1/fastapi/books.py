from fastapi import FastAPI

app = FastAPI()

BOOKS =[
    {'title': 'title one', 'author': 'Author one', 'category': 'Science'},
    {'title': 'title two', 'author': 'Author two', 'category': 'Science'},
    {'title': 'title three', 'author': 'Author three', 'category': 'history'},
    {'title': 'title four', 'author': 'Author four', 'category': 'math'},
    {'title': 'title five', 'author': 'Author six', 'category': 'math'},
    {'title': 'title six', 'author': 'Author two', 'category': 'math'}
]

@app.get("/api-endpoint")
async def read_all_books():
    return BOOKS