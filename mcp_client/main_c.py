# mcp_client/main.py GPT15

import os
import json
import requests
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

# === CONFIG ===
def load_mcp_config():
    try:
        with open("mcp_config.json", "r") as f:
            config = json.load(f)
            return config.get("mcp_server_url", "http://127.0.0.1:8001")
    except Exception:
        return "http://127.0.0.1:8001"

MCP_SERVER_URL = load_mcp_config()

# === SCHEMAS ===
class QuestionContext(BaseModel):
    question: str = Field(..., description="User's question")

class AnswerOutput(BaseModel):
    answer: str = Field(..., description="Answer to user's question")

# === DUMMY LLM FUNCTION ===
def dummy_model_decide(question: str) -> dict:
    """Return dict {use_tool: bool, country: str or None}"""
    keywords = ["capital", "Capital", "capital city"]
    countries = ["France", "Germany", "Japan"]  # very simple matcher

    if any(k in question for k in keywords):
        for c in countries:
            if c in question:
                return {"use_tool": True, "country": c}
    return {"use_tool": False, "country": None}

@app.get("/")
def root():
    return {
        "message": "MCP Client — Uses LLM + Tool (if needed)",
        "mcp_server_url": MCP_SERVER_URL
    }

@app.get("/ask")
def ask(question: str = Query(..., description="User question")):
    context = QuestionContext(question=question)

    # === LLM decides ===
    decision = dummy_model_decide(context.question)

    if decision["use_tool"]:
        # Call MCP tool server
        response = requests.post(
            f"{MCP_SERVER_URL}/get-capital",
            json={"country": decision["country"]}
        )
        data = response.json()
        capital = data.get("capital", "Unknown")
        answer = f"The capital of {decision['country']} is {capital}."
    else:
        # LLM answers directly (dummy)
        answer = "I'm not sure, but I'll get back to you!"

    return AnswerOutput(answer=answer)
