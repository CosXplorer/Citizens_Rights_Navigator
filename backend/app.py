from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents import grievance_graph

app = FastAPI()

# ================================
# CORS CONFIGURATION (PRODUCTION SAFE)
# ================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow Vercel, localhost, Postman, etc.
    allow_credentials=True,
    allow_methods=["*"],  # POST, OPTIONS, etc
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
        "raw_query": req.query,
        "query": "",
        "language": "",
        "kb_entry": None,
        "response": ""
    }

    result = grievance_graph.invoke(state)
    return {"response": result["response"]}


# ================================
# HEALTH CHECK
# ================================
@app.get("/")
def root():
    return {"status": "Backend running"}
