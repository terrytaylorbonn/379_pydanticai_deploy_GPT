# mcp_client/main_c.py

import os
import json
import requests
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

# === CONFIG LOADING ===
def load_mcp_config():
    try:
        with open("mcp_config.json", "r") as f:
            config = json.load(f)
            print(f"Loaded MCP config: {config}") ########
            return config.get("mcp_server_url", "http://127.0.0.1:8001")
    except Exception:
        return "http://127.0.0.1:8001"

MCP_SERVER_URL = load_mcp_config()

# === SCHEMAS ===

class QuestionContext(BaseModel):
    country: str = Field(..., description="Country name to ask about")

class AnswerOutput(BaseModel):
    answer: str = Field(..., description="Answer to user question")

@app.get("/")
def root():
    return {
        "message": "MCP Client — Calls MCP Server",
        "mcp_server_url": MCP_SERVER_URL
    }

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
