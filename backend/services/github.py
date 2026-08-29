import httpx
from fastapi import HTTPException
from config import settings
from models import RepoMetadata

class GitHubService:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if settings.GITHUB_TOKEN:
            self.headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

    async def get_repo_metadata(self, owner: str, repo: str) -> RepoMetadata:
        url = f"{self.base_url}/repos/{owner}/{repo}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=10.0)
            except httpx.RequestError as e:
                raise HTTPException(status_code=503, detail=f"GitHub API request failed: {e}")

            self._handle_errors(response)

            data = response.json()
            return RepoMetadata(
                name=data["name"],
                owner=data["owner"]["login"],
                stars=data["stargazers_count"],
                forks=data["forks_count"],
                open_issues=data["open_issues_count"],
                language=data.get("language")
            )

    def _handle_errors(self, response: httpx.Response):
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Repository not found or private")
        elif response.status_code == 403:
            # Check for rate limiting
            if response.headers.get("x-ratelimit-remaining") == "0":
                reset_time = response.headers.get("x-ratelimit-reset")
                raise HTTPException(status_code=429, detail=f"GitHub API rate limit exceeded. Reset at {reset_time}")
            raise HTTPException(status_code=403, detail="Forbidden access to GitHub API")
        elif response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data from GitHub")

    async def get_recent_commits(self, owner: str, repo: str, limit: int = 30) -> list[dict]:
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        params = {"per_page": min(limit, 100)}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, params=params, timeout=10.0)
            except httpx.RequestError as e:
                raise HTTPException(status_code=503, detail=f"GitHub API request failed: {e}")

            self._handle_errors(response)
            commits_summary = response.json()
            if not commits_summary:
                return []

            detailed_commits = []
            for c in commits_summary:
                sha = c["sha"]
                commit_url = f"{self.base_url}/repos/{owner}/{repo}/commits/{sha}"
                try:
                    c_resp = await client.get(commit_url, headers=self.headers, timeout=10.0)
                    self._handle_errors(c_resp)
                    detailed_commits.append(c_resp.json())
                except httpx.RequestError as e:
                    continue # Skip if individual commit fetch fails due to timeout
            
            return detailed_commits

