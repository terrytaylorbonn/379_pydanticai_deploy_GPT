# main.py br1

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a simple output schema using Pydantic
class AnswerOutput(BaseModel):
    answer: str

@app.get("/")
def read_root():
    return {"message": "Hello World get / br1"}

@app.get("/ask")
def ask(question: str):
    # Create validated response using Pydantic model
    response = AnswerOutput(answer="Hello World get /ask br1")
    return response