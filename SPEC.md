# RepoPulse Lite - Specification

## 1. Project Purpose
RepoPulse Lite is a full-stack web application designed to evaluate public GitHub repositories. It retrieves repository and commit telemetry, calculates a deterministic 0-100 health score based on multiple heuristic dimensions, leverages an LLM to generate an executive risk/hygiene report, and visualizes the results on an interactive dashboard.

## 2. Architecture
The application follows a client-server architecture.
- **Frontend**: React, Vite, Tailwind CSS, Recharts. Deployed on Vercel.
- **Backend**: Python, FastAPI, Pydantic, httpx. Deployed on Render.
- **External Services**: GitHub REST API (for repository/commit telemetry), OpenAI-compatible LLM API (for executive reporting).

## 3. Data Model

### GitHub Telemetry
- **Repository Info**: Name, Owner, Stars, Forks, Open Issues, Primary Language, Created At, Updated At.
- **Commit History**: List of recent commits including Hash, Author Name, Message, Timestamp, Additions, Deletions, Files Changed.

### Heuristic Engine Metrics
- **Code Churn**: Total additions, total deletions, additions-to-deletions relationship.
- **Commit Hygiene**: Percentage of commits using conventional prefixes, count of vague messages.
- **Cadence**: Total commits in analyzed period, average interval (days), standard deviation of intervals.
- **Contributor Distribution**: Number of contributors, distribution metric (Normalized Shannon Entropy).
- **Anomaly Risk**: Count of very large commits, unusually high deletions, atomic rewrites.

## 4. API Contracts

### `POST /api/analyze`
**Request:**
```json
{
  "repo_url": "https://github.com/owner/repository"
}
```

**Response:**
```json
{
  "repo_meta": {
    "name": "repository",
    "owner": "owner",
    "stars": 120,
    "forks": 15,
    "open_issues": 5,
    "language": "TypeScript"
  },
  "analyzed_commits": 100,
  "metrics": {
    "code_churn": {
      "additions": 15000,
      "deletions": 5000,
      "score": 18
    },
    "commit_hygiene": {
      "conventional_commits": 80,
      "vague_commits": 5,
      "score": 22
    },
    "cadence": {
      "average_interval_hours": 24.5,
      "score": 12
    },
    "author_distribution": {
      "contributor_count": 5,
      "entropy_score": 18
    },
    "anomaly_risk": {
      "anomalies_detected": 2,
      "score": 12
    }
  },
  "anomaly_flags": [
    "Commit abc1234 has > 10,000 additions.",
    "Suspicious atomic rewrite detected on 2026-08-01."
  ],
  "health_score": 82,
  "risk_level": "Low",
  "executive_report": "The LLM generated Markdown report goes here..."
}
```

### `GET /api/health`
**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

## 5. Heuristic Formulas & Weights (Max 100 Points)

The final score is a deterministic weighted sum of 5 dimensions, strictly clamped between 0 and 100.

### 5.1 Code Churn (Weight: 20 points)
Measures the balance and volume of code changes.
- **Score Formula**: `Base (20) - Penalties`.
- **Penalties**: 
  - Penalty applied if `deletions > additions * 3` (e.g., massive purging).
  - Penalty if average additions per commit > 1000 lines (indicating massive undocumented dumps).
- **Edge cases**: Repositories with 0 additions/deletions default to 10 points (neutral).

### 5.2 Commit Hygiene (Weight: 25 points)
Measures discipline in commit messages.
- **Metric**: Ratio of conventional commits (`feat:`, `fix:`, `refactor:`, `docs:`, `chore:`, `test:`) vs. total commits.
- **Base calculation**: `(Conventional Commits / Total Commits) * 25`.
- **Penalties**: -2 points for every vague commit (e.g., `wip`, `update`, `changes`, `fix` without prefix).
- **Score Formula**: Clamped to `[0, 25]`.

### 5.3 Commit Cadence / Velocity (Weight: 15 points)
Measures development consistency and activity.
- **Metric**: Average interval between commits over the analyzed period.
- **Score Formula**: 
  - Optimal cadence (e.g., 1-7 days average interval) scores 15 points.
  - Gradually decays for very slow (e.g., > 14 days) or highly erratic cadences.
  - Score is calculated logarithmically or step-wise to penalize dead projects.

### 5.4 Author Distribution (Weight: 20 points)
Measures dependency on a single author (Bus Factor) using a mathematically defensible concentration metric.
- **Metric**: Normalized Shannon Entropy of commit distribution across authors.
  `H = -SUM(p_i * ln(p_i)) / ln(N)` where `p_i` is the proportion of commits by author `i`, and `N` is the number of authors.
- **Score Formula**: `H * 20`. 
- **Edge cases**: If `N = 1` (a single author), the score is fixed at 10 points (moderate penalty, since personal projects are common, but it presents a higher risk for a corporate dependency).

### 5.5 Anomaly Risk (Weight: 20 points)
Measures stability and detects suspicious behavior.
- **Base Score**: 20 points (assumes no anomalies).
- **Penalties**: 
  - -5 points for any commit with > 50 files changed (excluding first commit).
  - -10 points for suspicious atomic rewrites (very high deletions accompanied by very high additions in single commits).
  - -5 points for very large commits (> 10,000 lines).
- **Score Formula**: `20 - SUM(Penalties)`. Clamped to `[0, 20]`.

### Composite Score
`Final Score = Churn + Hygiene + Cadence + Author Distribution + Anomaly Risk` (Always bounded between 0 and 100)

## 6. Dashboard Requirements
- **Repository Overview**: High-level stats (Stars, Forks, Issues, Language).
- **Overall Health Score**: 0-100 gauge chart, color-coded by Risk Level (e.g., Green for Low Risk, Yellow for Medium, Red for High).
- **Score Breakdown**: Radar or Bar chart showing the 5 dimension scores vs their max points.
- **Commit Analytics**: Visualizing additions/deletions and commit activity over time (via Recharts).
- **Contributor Analytics**: Visual distribution of commits by author.
- **Risk/Anomaly Panel**: Dedicated section highlighting any flags raised by the heuristic engine.
- **AI Executive Report**: Neatly rendered Markdown summary of the LLM's analysis.
- **UX**: Loading skeletons during API calls, elegant error states, empty states before searching, responsive design.

## 7. Error Handling & Defensive Requirements
- **Invalid URLs**: Reject non-GitHub URLs or malformed paths instantly on both frontend and backend.
- **Missing/Private Repositories (GitHub 404)**: Return clear "Repository not found or private" messages.
- **GitHub Rate Limiting (403)**: Detect rate limit headers and return graceful errors asking the user to try again later.
- **Empty Repositories**: Return a specific "Repository is empty / no commits" response instead of triggering division-by-zero math errors.
- **Timeouts & Upstream Failures**: Wrap `httpx` and LLM calls in timeouts; fallback gracefully if LLM is down (return deterministic scores even if LLM fails).
- **Missing Env Vars**: Fail fast on backend startup if `GITHUB_TOKEN` or LLM credentials are missing.

## 8. Testing Strategy
- **URL Validation**: Tests for valid/invalid inputs.
- **External Failures**: Mock GitHub 404s, 403 rate limits, and timeouts.
- **Heuristic Engine Tests**:
  - Test conventional commit regex matching and vague message detection.
  - Test churn and cadence mathematical bounds.
  - Test Normalized Shannon Entropy calculation for 1 author and N authors.
  - Test anomaly detection logic with mock large commits.
  - Verify final composite score never exceeds 100 or drops below 0.
- **Empty Repositories**: Ensure engine safely handles zero commits.
