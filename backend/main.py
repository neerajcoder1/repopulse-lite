from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import re
from models import AnalyzeRequest
from services.github import GitHubService
from services.heuristic_engine import HeuristicEngine
from services.llm import LLMService

app = FastAPI(title="RepoPulse Lite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

github_service = GitHubService()
llm_service = LLMService()

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/api/analyze")
async def analyze_repo(request: AnalyzeRequest):
    # Parse owner and repo from URL
    match = re.search(r"github\.com/([\w.-]+)/([\w.-]+)/?$", request.repo_url)
    if not match:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL format")
        
    owner, repo = match.groups()
    
    # 1. Fetch metadata
    repo_meta = await github_service.get_repo_metadata(owner, repo)
    
    # 2. Fetch commits
    commits = await github_service.get_recent_commits(owner, repo, limit=15)
    
    # 3. Heuristic Engine
    engine = HeuristicEngine(commits)
    analysis = engine.analyze()
    
    # 4. LLM Executive Report
    report = await llm_service.generate_executive_report(
        repo_meta=repo_meta.model_dump(),
        metrics=analysis["metrics"],
        anomaly_flags=analysis["anomaly_flags"],
        health_score=analysis["health_score"],
        risk_level=analysis["risk_level"]
    )
    
    return {
        "repo_meta": repo_meta.model_dump(),
        "analyzed_commits": len(commits),
        "metrics": analysis["metrics"],
        "anomaly_flags": analysis["anomaly_flags"],
        "health_score": analysis["health_score"],
        "risk_level": analysis["risk_level"],
        "executive_report": report
    }
