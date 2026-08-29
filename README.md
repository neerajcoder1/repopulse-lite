# RepoPulse Lite

> A full-stack GitHub Repository Health Analyzer that transforms repository and commit telemetry into an explainable 0–100 engineering health score and an AI-generated executive risk report.

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black)](https://github.com/neerajcoder1/repopulse-lite)
<img width="920" height="425" alt="image" src="https://github.com/user-attachments/assets/2912c678-a8bc-48ad-8d0f-a9e3f6259545" />

---

## Live Demo

**Production Application:**  
https://repopulse-lite-ashen.vercel.app

**Backend API:**  
https://repopulse-lite-4jml.onrender.com

### Deployment

- Frontend: Vercel
- Backend: Render
- Source Code: GitHub

---

## About the Project

RepoPulse Lite is a full-stack engineering analytics platform designed to analyze the development health of a public GitHub repository.

The application accepts a public GitHub repository URL, retrieves repository and recent commit telemetry through the GitHub REST API, processes that telemetry using a deterministic heuristic scoring engine, calculates a 0–100 Repository Health Score, identifies potential engineering risks, and uses an OpenAI-compatible LLM to generate an executive-level risk and hygiene report.

The numerical health score is calculated entirely by the deterministic scoring engine. The LLM is used as an interpretation and reporting layer rather than as the source of the numerical score.

---

## Problem Statement

Engineering leads often need actionable visibility into repository momentum, commit quality, code churn, contributor distribution, and potentially risky development patterns without manually reviewing hundreds of Git logs.

RepoPulse Lite addresses this problem by converting raw GitHub repository telemetry into:

- A single Repository Health Score
- Individual engineering-health metrics
- Contributor distribution insights
- Commit-quality analysis
- Code churn analysis
- Development cadence analysis
- Anomaly and risk detection
- An AI-generated executive report

The goal is not to replace engineering judgment, but to provide a fast and explainable first-level assessment of repository health.

---

## Key Features

### GitHub Repository Analysis

- Accepts public GitHub repository URLs
- Validates GitHub repository URLs
- Retrieves repository metadata
- Retrieves recent commit telemetry
- Processes additions, deletions, changed files, authors and commit messages

### Deterministic Health Scoring

RepoPulse Lite calculates a 0–100 score using five dimensions:

1. Code Churn
2. Commit Hygiene
3. Commit Cadence / Velocity
4. Author Entropy / Contributor Distribution
5. Anomaly Risk

### Risk Detection

The system identifies potentially risky development patterns including:

- Very large commits
- Excessive file changes
- High deletion activity
- Massive atomic rewrites
- Contributor concentration
- Poor commit-message hygiene

### AI Executive Audit

An OpenAI-compatible LLM receives the deterministic analysis and produces:

- Executive summary
- Repository strengths
- Major risks
- Engineering concerns
- Recommendations

### Interactive Dashboard

The frontend provides:

- Overall health score
- Score breakdown
- Repository statistics
- Commit analytics
- Contributor analytics
- Risk indicators
- AI executive report
- Loading states
- Error states
- Responsive UI

---

# System Architecture

```text
                         ┌─────────────────────┐
                         │        User         │
                         │ GitHub Repository URL│
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   React Frontend    │
                         │   Analytics UI       │
                         └──────────┬──────────┘
                                    │
                             POST /api/analyze
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   FastAPI Backend   │
                         │ URL Validation      │
                         │ Error Handling      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   GitHub REST API   │
                         │ Repository Telemetry│
                         │ Commit Telemetry    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Telemetry Processor │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │ Deterministic Heuristic Engine│
                    │                               │
                    │ • Code Churn                  │
                    │ • Commit Hygiene              │
                    │ • Cadence / Velocity          │
                    │ • Author Entropy               │
                    │ • Anomaly Detection            │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Health Score 0–100  │
                         └──────────┬──────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                         ▼                     ▼
                ┌─────────────────┐   ┌─────────────────┐
                │ Risk / Anomaly  │   │ OpenAI-         │
                │ Analysis        │   │ Compatible LLM  │
                └─────────────────┘   └────────┬────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │ Executive Audit │
                                      └────────┬────────┘

                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │ React Dashboard │
                                      └─────────────────┘
````
# Submission Information

## Required Deliverables

### GitHub Repository

https://github.com/neerajcoder1/repopulse-lite

### Live Production Application

https://repopulse-lite-ashen.vercel.app

### Backend API

https://repopulse-lite-4jml.onrender.com

### Documentation

- `README.md` — Project documentation, architecture, scoring model, setup and deployment
- `SPEC.md` — System specification and architectural design
- `DEVELOPMENT_LOG.md` — AI-assisted development and engineering audit
