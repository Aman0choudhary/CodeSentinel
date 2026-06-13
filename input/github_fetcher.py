import tempfile
import shutil
from pathlib import Path
from git import Repo

from config import settings


def fetch_github_repo(url: str) -> Path:
    tmp_dir = Path(tempfile.mkdtemp(prefix="codesentinel_"))
    clone_url = url

    if settings.github_token and url.startswith("https://"):
        clone_url = url.replace("https://", f"https://{settings.github_token}@", 1)

    try:
        Repo.clone_from(clone_url, tmp_dir, depth=1)
    except Exception as exc:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise RuntimeError(f"Failed to clone repo: {exc}")

    return tmp_dir


def cleanup(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)
