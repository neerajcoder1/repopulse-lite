import math
from datetime import datetime
from collections import defaultdict
import re

class HeuristicEngine:
    def __init__(self, commits: list[dict]):
        self.commits = commits

    def analyze(self):
        if not self.commits:
            return {
                "health_score": 0,
                "risk_level": "High",
                "metrics": {},
                "anomaly_flags": ["Repository is empty or no commits found"]
            }

        churn = self._calculate_churn()
        hygiene = self._calculate_hygiene()
        cadence = self._calculate_cadence()
        entropy = self._calculate_author_entropy()
        anomaly = self._calculate_anomaly_risk()

        health_score = max(0, min(100, churn["score"] + hygiene["score"] + cadence["score"] + entropy["score"] + anomaly["score"]))
        
        if health_score >= 80:
            risk_level = "Low"
        elif health_score >= 50:
            risk_level = "Medium"
        else:
            risk_level = "High"

        return {
            "health_score": int(health_score),
            "risk_level": risk_level,
            "metrics": {
                "code_churn": churn,
                "commit_hygiene": hygiene,
                "cadence": cadence,
                "author_distribution": entropy,
                "anomaly_risk": anomaly,
            },
            "anomaly_flags": anomaly["flags"]
        }

    def _calculate_churn(self):
        # Max 20 points
        total_additions = sum(c.get("stats", {}).get("additions", 0) for c in self.commits)
        total_deletions = sum(c.get("stats", {}).get("deletions", 0) for c in self.commits)
        
        if total_additions == 0 and total_deletions == 0:
            return {"additions": 0, "deletions": 0, "score": 10}
            
        score = 20
        # Penalty if deletions > additions * 3
        if total_deletions > total_additions * 3:
            score -= 5
            
        # Penalty if average additions per commit > 1000
        avg_additions = total_additions / len(self.commits)
        if avg_additions > 1000:
            score -= 5
            
        return {
            "additions": total_additions,
            "deletions": total_deletions,
            "score": max(0, int(score))
        }

    def _calculate_hygiene(self):
        # Max 25 points
        conventional_prefixes = ("feat:", "fix:", "refactor:", "docs:", "chore:", "test:", "style:", "perf:", "ci:", "build:")
        vague_messages = ("wip", "update", "changes", "fix", "test")
        
        conventional_count = 0
        vague_count = 0
        
        for c in self.commits:
            msg = c.get("commit", {}).get("message", "").lower().strip()
            first_line = msg.split("\n")[0]
            
            if first_line.startswith(conventional_prefixes):
                conventional_count += 1
            if first_line in vague_messages:
                vague_count += 1
                
        base_score = (conventional_count / len(self.commits)) * 25
        score = base_score - (vague_count * 2)
        
        return {
            "conventional_commits": conventional_count,
            "vague_commits": vague_count,
            "score": max(0, min(25, int(score)))
        }

    def _calculate_cadence(self):
        # Max 15 points
        if len(self.commits) < 2:
            return {"average_interval_hours": 0, "score": 10}
            
        timestamps = []
        for c in self.commits:
            date_str = c.get("commit", {}).get("author", {}).get("date")
            if date_str:
                # Handle ISO 8601 strings, sometimes ending with Z
                date_str = date_str.replace("Z", "+00:00")
                try:
                    timestamps.append(datetime.fromisoformat(date_str))
                except ValueError:
                    pass
                    
        timestamps.sort()
        intervals = [(timestamps[i] - timestamps[i-1]).total_seconds() for i in range(1, len(timestamps))]
        
        if not intervals:
            return {"average_interval_hours": 0, "score": 10}
            
        avg_seconds = sum(intervals) / len(intervals)
        avg_hours = avg_seconds / 3600
        avg_days = avg_hours / 24
        
        score = 15
        if avg_days > 14:
            score -= min(10, (avg_days - 14) / 7) # -1 point for every week over 14 days
        elif avg_days < 0.1:
            score -= 5 # too erratic/fast, maybe automated
            
        return {
            "average_interval_hours": round(avg_hours, 2),
            "score": max(0, min(15, int(score)))
        }

    def _calculate_author_entropy(self):
        # Max 20 points
        authors = defaultdict(int)
        for c in self.commits:
            author = c.get("commit", {}).get("author", {}).get("name", "Unknown")
            authors[author] += 1
            
        n = len(authors)
        if n == 1:
            return {"contributor_count": 1, "score": 10}
            
        total = sum(authors.values())
        entropy = 0
        for count in authors.values():
            p = count / total
            entropy -= p * math.log(p)
            
        normalized_entropy = entropy / math.log(n)
        score = normalized_entropy * 20
        
        return {
            "contributor_count": n,
            "score": max(0, min(20, int(score)))
        }

    def _calculate_anomaly_risk(self):
        # Max 20 points
        score = 20
        flags = []
        
        for idx, c in enumerate(self.commits):
            stats = c.get("stats", {})
            additions = stats.get("additions", 0)
            deletions = stats.get("deletions", 0)
            files = c.get("files", [])
            sha = c.get("sha", "")[:7]
            
            # Not initial commit and high files changed
            if idx < len(self.commits) - 1 and len(files) > 50:
                score -= 5
                flags.append(f"Commit {sha} changed > 50 files.")
                
            # Atomic rewrite
            if additions > 5000 and deletions > 5000:
                score -= 10
                flags.append(f"Commit {sha} is a suspicious atomic rewrite (>5k additions and deletions).")
                
            # Very large commit
            if additions > 10000:
                score -= 5
                flags.append(f"Commit {sha} has > 10,000 additions.")
                
        return {
            "anomalies_detected": len(flags),
            "score": max(0, min(20, int(score))),
            "flags": flags
        }
