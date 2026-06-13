from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import pathspec

from config import settings


@dataclass
class CodeFile:
    path: str
    content: str
    language: str
    line_count: int


EXTENSION_TO_LANG = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".go": "go",
    ".rb": "ruby",
    ".php": "php",
    ".cs": "csharp",
    ".cpp": "cpp",
    ".c": "c",
}

DEFAULT_SKIP_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    "vendor",
}


def _load_patterns(path: Path) -> List[str]:
    patterns = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def build_ignore_spec(root: Path, respect_gitignore: bool) -> Optional[pathspec.PathSpec]:
    if not respect_gitignore:
        return None

    patterns: List[str] = []
    for name in [".gitignore", ".codesentinelignore"]:
        p = root / name
        if p.exists():
            patterns.extend(_load_patterns(p))

    if not patterns:
        return None

    return pathspec.PathSpec.from_lines("gitwildmatch", patterns)


def build_spec(patterns: List[str]) -> Optional[pathspec.PathSpec]:
    if not patterns:
        return None
    return pathspec.PathSpec.from_lines("gitwildmatch", patterns)


def read_codebase(
    root: Path,
    include_globs: List[str],
    exclude_globs: List[str],
    respect_gitignore: bool,
) -> List[CodeFile]:
    files: List[CodeFile] = []
    root = Path(root)

    ignore_spec = build_ignore_spec(root, respect_gitignore)
    include_spec = build_spec(include_globs)
    exclude_spec = build_spec(exclude_globs)

    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue

        if any(part in DEFAULT_SKIP_DIRS for part in file_path.parts):
            continue

        rel_path = file_path.relative_to(root).as_posix()
        if ignore_spec and ignore_spec.match_file(rel_path):
            continue
        if exclude_spec and exclude_spec.match_file(rel_path):
            continue
        if include_spec and not include_spec.match_file(rel_path):
            continue

        ext = file_path.suffix.lower()
        if ext not in settings.supported_extensions:
            continue

        size_kb = file_path.stat().st_size / 1024
        if size_kb > settings.max_file_size_kb:
            continue

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        files.append(
            CodeFile(
                path=rel_path,
                content=content,
                language=EXTENSION_TO_LANG.get(ext, "unknown"),
                line_count=len(content.splitlines()),
            )
        )

        if len(files) >= settings.max_files_per_repo:
            break

    return files
