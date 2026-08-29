import httpx
from fastapi import HTTPException
from ..config import settings

class LLMService:
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.base_url = settings.LLM_BASE_URL or "https://api.openai.com/v1"
        self.model = settings.LLM_MODEL or "gpt-4"

    async def generate_executive_report(self, repo_meta: dict, metrics: dict, anomaly_flags: list, health_score: int, risk_level: str) -> str:
        if not self.api_key:
            return "LLM integration is not configured. Missing API key."

        prompt = (
            f"Analyze the following GitHub repository telemetry and generate a concise executive risk and hygiene report (Markdown).\n\n"
            f"Repository: {repo_meta['name']} (Owner: {repo_meta['owner']})\n"
            f"Health Score: {health_score}/100 (Risk: {risk_level})\n"
            f"Metrics: {metrics}\n"
            f"Anomaly Flags: {anomaly_flags}\n\n"
            f"Explain the score and highlight the biggest risks. Do not recalculate the score."
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a senior technical auditor."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.2
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers, timeout=15.0)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except httpx.RequestError as e:
                return f"LLM generation failed due to network error: {e}"
            except httpx.HTTPStatusError as e:
                return f"LLM API returned an error: {e.response.status_code}"
            except Exception as e:
                return f"An unexpected error occurred during LLM generation: {e}"
