from backend.services.heuristic_engine import HeuristicEngine

def test_empty_repository():
    engine = HeuristicEngine([])
    result = engine.analyze()
    assert result["health_score"] == 0
    assert result["risk_level"] == "High"
    assert "Repository is empty" in result["anomaly_flags"][0]

def test_perfect_score():
    # Construct a perfect commit history
    commits = []
    for i in range(10):
        commits.append({
            "sha": f"abc{i}",
            "commit": {
                "message": "feat: add perfect feature\n\nbody",
                "author": {"name": f"Author {i}", "date": f"2026-08-0{i+1}T12:00:00Z"}
            },
            "stats": {"additions": 100, "deletions": 50},
            "files": [{"filename": "src/perfect.py"}]
        })
        
    engine = HeuristicEngine(commits)
    result = engine.analyze()
    
    # Churn: 20
    # Hygiene: 25 (all feats)
    # Cadence: 15 (1 day interval)
    # Entropy: 20 (10 distinct authors)
    # Anomaly: 20 (no anomalies)
    assert result["health_score"] == 100
    assert result["risk_level"] == "Low"

def test_anomalies_and_penalties():
    commits = [
        {
            "sha": "xyz",
            "commit": {
                "message": "wip",
                "author": {"name": "Single Author", "date": "2026-08-01T12:00:00Z"}
            },
            "stats": {"additions": 20000, "deletions": 20000},
            "files": [{} for _ in range(60)] # 60 files changed
        },
        {
            "sha": "xyz2",
            "commit": {
                "message": "wip",
                "author": {"name": "Single Author", "date": "2026-08-01T12:00:05Z"}
            },
            "stats": {"additions": 20000, "deletions": 20000},
            "files": [{} for _ in range(60)] # 60 files changed
        }
    ]
    
    engine = HeuristicEngine(commits)
    result = engine.analyze()
    
    # Hygiene: 0 (all vague)
    # Cadence: penalized for too fast (<0.1 days)
    # Entropy: 10 (single author)
    # Anomaly: penalties for size and files
    assert result["health_score"] < 50
    assert result["risk_level"] == "High"
