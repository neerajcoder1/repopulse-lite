# Development Log

## Overview
This log documents the AI-assisted development of the RepoPulse Lite application. 

### Tools and IDE
- **Agent**: Gemini 3.1 Pro (High) via Antigravity 2.0
- **Development Environment**: Local terminal via `default_api:run_command`, file manipulations via `default_api:write_to_file`.

### Process
1. **Phase 1**: Inspected workspace, created `repopulse-lite` repo, generated `SPEC.md` documenting architecture, metrics, and contracts.
2. **Phase 2-3**: Initialized Vite React frontend and FastAPI backend concurrently. Encountered minor issues with Vite CLI arguments in PowerShell, resolved using `Remove-Item` and strict npm create formatting.
3. **Phase 4**: Implemented `models.py` with URL validation for GitHub URLs. Implemented `github.py` telemetry service taking care of edge cases (rate limiting, 404s, timeouts) utilizing `httpx`.
4. **Phase 5**: Implemented `heuristic_engine.py` using math-based scoring logic. Specifically used Shannon Entropy for contributor concentration analysis. 
5. **Phase 7**: Built `llm.py` to consume the heuristics results and prompt the LLM for a summarized risk report.
6. **Phase 8**: Built the frontend `Dashboard.tsx` utilizing Lucide icons and Recharts for a clean overview.
7. **Testing**: Built `test_heuristics.py` to assert mathematical integrity.

### Engineering Decisions
- Separated GitHub fetching and Heuristic Logic into two distinct modules to allow simple isolated unit testing.
- Used Recharts for frontend visualizations due to ease of integration and radar chart availability.
- Handled empty repositories explicitly at the top of the heuristic engine to avoid division-by-zero math errors.
