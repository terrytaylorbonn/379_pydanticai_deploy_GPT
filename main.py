# main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/ask")
def ask(question: str):
    return {"answer": "Hello World"}