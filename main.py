# main.py GPT6

import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

load_dotenv()

# Create OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Define output schema
class AnswerOutput(BaseModel):
    answer: str

@app.get("/")
def read_root():
    return {"message": "Hello from PydanticAI + OpenAI (new API) GPT6"}

@app.get("/ask")
def ask(question: str):
    # Call OpenAI API (new style)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        temperature=0
    )
    answer_text = response.choices[0].message.content.strip()

    # Validate response using Pydantic
    validated = AnswerOutput(answer=answer_text)
    return validated