from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents import grievance_graph

app = FastAPI()

# ================================
# CORS CONFIGURATION (IMPORTANT)
# ================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite frontend
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow POST, OPTIONS, etc.
    allow_headers=["*"],
)

# ================================
# REQUEST SCHEMA
# ================================
class QueryRequest(BaseModel):
    query: str


# ================================
# API ENDPOINT
# ================================
@app.post("/ask")
def ask_grievance(req: QueryRequest):
    state = {
        "raw_query": req.query
    }
    result = grievance_graph.invoke(state)
    return {"response": result["response"]}
@app.get("/")
def root():
    return {"status": "Backend running"}