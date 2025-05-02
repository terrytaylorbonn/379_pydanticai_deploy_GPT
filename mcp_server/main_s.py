# mcp_server/main_s.py

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# MCP Input schema
class ToolInput(BaseModel):
    country: str = Field(..., description="Name of the country")

# MCP Output schema
class ToolOutput(BaseModel):
    capital: str = Field(..., description="Capital of the country")

@app.get("/")
def root():
    return {"message": "MCP Server — Fake Tool"}

@app.post("/get-capital", response_model=ToolOutput)
def get_capital(input: ToolInput):
    # Dummy logic (hardcoded)
    capitals = {
        "France": "Paris",
        "Germany": "Berlin",
        "Japan": "Tokyo"
    }
    capital = capitals.get(input.country, "Unknown")
    return ToolOutput(capital=capital)
