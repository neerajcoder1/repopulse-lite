# RepoPulse Lite

RepoPulse Lite is a full-stack web application designed to evaluate public GitHub repositories. It calculates a deterministic 0-100 health score based on multiple heuristic dimensions and leverages an LLM to generate an executive risk report.

## Architecture & Technology Stack
- **Frontend**: React, Vite, Tailwind CSS, Recharts
- **Backend**: Python, FastAPI, Pydantic, httpx
- **External Services**: GitHub REST API, OpenAI-compatible LLM

## Heuristic Scoring Engine
The deterministic Python engine evaluates 5 dimensions:
1. **Code Churn** (20 pts): Penalizes massive undocumented code dumps or excessive purging.
2. **Commit Hygiene** (25 pts): Rewards conventional commits and penalizes vague messages.
3. **Cadence** (15 pts): Rewards healthy commit intervals (1-7 days) and penalizes erratic or dead activity.
4. **Author Entropy** (20 pts): Calculates Normalized Shannon Entropy to determine "bus factor" risk.
5. **Anomaly Risk** (20 pts): Deducts points for suspicious atomic rewrites or highly impactful untested commits.

## Local Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/Scripts/activate # Windows
pip install -r requirements.txt
```
Create `.env` inside `backend/`:
```env
GITHUB_TOKEN=your_personal_access_token
LLM_API_KEY=your_llm_api_key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4
```
Run Server:
```bash
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints
- `GET /api/health` - Health check endpoint.
- `POST /api/analyze` - Analyzes a given GitHub repository URL.
