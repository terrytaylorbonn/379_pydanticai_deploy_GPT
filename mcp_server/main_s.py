# mcp_server/main_s.py GPT15

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# === SCHEMAS ===
class ToolInput(BaseModel):
    country: str = Field(..., description="Name of the country")

class ToolOutput(BaseModel):
    capital: str = Field(..., description="Capital of the country")

# === ROUTES ===
@app.get("/")
def root():
    return {"message": "MCP Server — Fake Tool"}

@app.post("/get-capital", response_model=ToolOutput)
def get_capital(input: ToolInput):
    capitals = {
        "France": "Paris",
        "Germany": "Berlin",
        "Japan": "Tokyo"
    }
    capital = capitals.get(input.country, "Unknown")
    return ToolOutput(capital=capital)

# === TOOL METADATA ===
@app.get("/metadata")
def metadata():
    return {
        "tool_name": "get-capital",
        "description": "Given a country name, returns the capital city.",
        "input_schema": {"country": "Name of the country (str)"},
        "output_schema": {"capital": "Capital city of the country (str)"}
    }