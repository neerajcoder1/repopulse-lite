from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from .models import AnalyzeRequest

app = FastAPI(title="RepoPulse Lite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/api/analyze")
async def analyze_repo(request: AnalyzeRequest):
    # TODO: Implement GitHub ingestion and heuristic engine
    return {"message": "Valid URL received", "url": request.repo_url}
