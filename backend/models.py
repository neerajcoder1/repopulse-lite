import re
from pydantic import BaseModel, HttpUrl, field_validator

class AnalyzeRequest(BaseModel):
    repo_url: str

    @field_validator("repo_url")
    def validate_github_url(cls, v):
        pattern = r"^https?://(www\.)?github\.com/[\w.-]+/[\w.-]+/?$"
        if not re.match(pattern, v):
            raise ValueError("Invalid GitHub repository URL")
        return v

class RepoMetadata(BaseModel):
    name: str
    owner: str
    stars: int
    forks: int
    open_issues: int
    language: str | None
