import tempfile
import zipfile
from pathlib import Path


def load_local(path_str: str) -> Path:
    path = Path(path_str).resolve()

    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path}")

    if path.is_dir():
        return path

    if path.suffix.lower() == ".zip":
        tmp_dir = Path(tempfile.mkdtemp(prefix="codesentinel_"))
        with zipfile.ZipFile(path, "r") as zf:
            zf.extractall(tmp_dir)
        return tmp_dir

    raise ValueError("Unsupported input. Use a directory or .zip file.")
