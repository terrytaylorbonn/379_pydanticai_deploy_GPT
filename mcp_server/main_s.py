# mcp_server/main_s.py GPT16a

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class ToolInput(BaseModel):
    country: str = Field(..., description="Name of the country")

class ToolOutput(BaseModel):
    capital: str = Field(..., description="Capital of the country")

@app.get("/")
def root():
    return {"message": "MCP Server — Capital Tool"}

@app.post("/get-capital", response_model=ToolOutput)
def get_capital(input: ToolInput):
    capitals = {
        "France": "Paris (from tool)",
        "Germany": "Berlin (from tool)",
        "Japan": "Tokyo (from tool)"
    }
    capital = capitals.get(input.country, "Unknown")
    return ToolOutput(capital=capital)

@app.get("/metadata")
def metadata():
    return {
        "tool_name": "get-capital",
        "description": "Given a country name, returns the capital city.",
        "endpoint": "/get-capital",
        "method": "POST",
        "input_schema": {
            "country": "Name of the country (str)"
        },
        "output_schema": {
            "capital": "Capital city of the country (str)"
        }
    }
