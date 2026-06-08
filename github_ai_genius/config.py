from __future__ import annotations

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration. Secrets are read from the environment, never hard-coded."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    github_token: str = Field(default="", alias="GITHUB_TOKEN")
    github_api_url: str = Field(default="https://api.github.com", alias="GITHUB_API_URL")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="qwen2.5-coder:14b", alias="OLLAMA_MODEL")
    workspace_dir: Path = Field(default=Path(".genius/workspaces"), alias="GENIUS_WORKSPACE_DIR")
    index_path: Path = Field(default=Path(".genius/index.sqlite3"), alias="GENIUS_INDEX_PATH")
    max_file_bytes: int = Field(default=350_000, alias="GENIUS_MAX_FILE_BYTES")
    max_repo_files: int = Field(default=8_000, alias="GENIUS_MAX_REPO_FILES")
    request_timeout_seconds: int = Field(default=60, alias="GENIUS_REQUEST_TIMEOUT_SECONDS")
    allow_incompatible_license_copy: bool = Field(default=False, alias="GENIUS_ALLOW_INCOMPATIBLE_LICENSE_COPY")
    allow_security_exploit_generation: bool = Field(default=False, alias="GENIUS_ALLOW_SECURITY_EXPLOIT_GENERATION")

    def require_github_token(self) -> str:
        if not self.github_token:
            raise RuntimeError("GITHUB_TOKEN is required for authenticated GitHub operations")
        return self.github_token


def get_settings() -> Settings:
    return Settings()
