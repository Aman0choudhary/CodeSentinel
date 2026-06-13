from dataclasses import dataclass, field
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


def _env(key: str, default: str = "") -> str:
    return os.getenv(key, default)


def _bool_env(key: str, default: str = "false") -> bool:
    return _env(key, default).strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    hermes_base_url: str = _env("HERMES_BASE_URL", "")
    hermes_api_key: str = _env("HERMES_API_KEY", "")
    hermes_api_path: str = _env("HERMES_API_PATH", "/v1/chat/completions")
    hermes_model: str = _env("HERMES_MODEL", "hermes-3-llama-3.1-70b")
    hermes_timeout_seconds: int = int(_env("HERMES_TIMEOUT_SECONDS", "30"))
    hermes_enabled: bool = _bool_env("HERMES_ENABLED", "false")

    github_token: str = _env("GITHUB_TOKEN", "")

    max_file_size_kb: int = int(_env("MAX_FILE_SIZE_KB", "500"))
    max_files_per_repo: int = int(_env("MAX_FILES_PER_REPO", "1000"))
    supported_extensions: List[str] = field(
        default_factory=lambda: [
            ".py", ".js", ".ts", ".java", ".go",
            ".rb", ".php", ".cs", ".cpp", ".c"
        ]
    )

    output_dir: str = _env("OUTPUT_DIR", "./codesentinel-reports")
    respect_gitignore: bool = _bool_env("RESPECT_GITIGNORE", "true")


settings = Settings()
