<div align="center">
  
  # 📈 RepoPulse Lite

  **Deterministic GitHub Repository Health & Risk Analysis Dashboard**
  <br />
  A full-stack application that analyzes GitHub repositories, scores their health deterministically based on engineering metrics, and generates AI-powered executive risk reports.

  [![Live Demo](https://img.shields.io/badge/Live_Demo-Vercel-black?style=for-the-badge&logo=vercel)](https://repopulse-lite-ashen.vercel.app)
  [![API Status](https://img.shields.io/badge/API-Render-blue?style=for-the-badge&logo=render)](https://repopulse-lite-4jml.onrender.com/docs)
  
</div>

---

## 🌟 Features

- **Deterministic Heuristic Engine:** Calculates a 0-100 score based on hard telemetry (not AI hallucination).
  - Code Churn & Volatility
  - Commit Message Hygiene (Conventional Commits)
  - Development Cadence
  - Author Entropy (Bus Factor & Normalized Shannon Entropy)
  - Anomaly Detection (Mega-commits, force-pushes, etc.)
- **LLM Executive Summary:** Integrates with Groq's high-speed AI (Llama 3 / Qwen) to write a detailed markdown report explaining the deterministic score.
- **Beautiful Telemetry Dashboard:** Built with React, Tailwind CSS v4, and Recharts for interactive radar and gauge charts.

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** React 18 (Vite)
- **Styling:** Tailwind CSS v4
- **Charts:** Recharts
- **Icons:** Lucide React
- **Markdown:** React-Markdown + Remark-GFM

### Backend
- **Framework:** FastAPI (Python)
- **HTTP Client:** HTTPX
- **Data Validation:** Pydantic
- **AI Integration:** OpenAI-compatible API (Groq)

---

## 🚀 Live Deployment

- **Frontend Application:** [https://repopulse-lite-ashen.vercel.app](https://repopulse-lite-ashen.vercel.app)
- **Backend API Docs:** [https://repopulse-lite-4jml.onrender.com/docs](https://repopulse-lite-4jml.onrender.com/docs)

---

## 💻 Local Development

If you wish to run RepoPulse Lite locally on your machine, follow these steps:

### Prerequisites
- Python 3.9+
- Node.js 18+
- A GitHub Personal Access Token
- An OpenAI-compatible API Key (e.g., Groq)

### Backend Setup
1. Open a terminal and navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the `backend` directory and add your keys:
   ```env
   GITHUB_TOKEN=your_github_token_here
   LLM_API_KEY=your_groq_api_key_here
   LLM_BASE_URL=https://api.groq.com/openai/v1
   LLM_MODEL=qwen/qwen3.8-27b
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Frontend Setup
1. Open a new terminal and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. Open `http://localhost:5173` in your browser.

---

## 📄 API Endpoints

- `GET /api/health` - Check backend status.
- `POST /api/analyze` - Analyze a GitHub repository.
  - **Body:** `{ "repo_url": "https://github.com/owner/repo" }`

---

*Built for a Technical Assessment.*
