# mcp_client/main_c.py

import os
import requests
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

# MCP Context schema (input)
class QuestionContext(BaseModel):
    country: str = Field(..., description="Country name to ask about")

# MCP Output schema
class AnswerOutput(BaseModel):
    answer: str = Field(..., description="Answer to user question")

# Set MCP server URL (you'll update this when deployed)
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8001")

@app.get("/")
def root():
    return {"message": "MCP Client — Calls MCP Server"}

@app.get("/ask")
def ask(country: str = Query(..., description="Country to ask about")):
    context = QuestionContext(country=country)

    # Call MCP server
    response = requests.post(
        f"{MCP_SERVER_URL}/get-capital",
        json=context.dict()
    )
    data = response.json()

    # Wrap output
    capital = data.get("capital", "Unknown")
    answer = f"The capital of {context.country} is {capital}."
    return AnswerOutput(answer=answer)
