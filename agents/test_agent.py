import re
from pathlib import Path
from typing import List, Set

from tools.file_reader import CodeFile


class TestAgent:
    async def analyze(self, files: List[CodeFile]) -> List[dict]:
        findings: List[dict] = []
        test_files = _collect_test_files(files)

        for file in files:
            if _is_test_file(file.path):
                continue

            if file.path.endswith(".py") and not _has_matching_test(file.path, test_files):
                findings.append(
                    {
                        "file": file.path,
                        "line": 0,
                        "issue": "Missing tests",
                        "severity": "LOW",
                        "description": "No matching test file found",
                        "recommendation": "Add unit tests for this module.",
                        "category": "test",
                    }
                )

            findings.extend(_find_bare_excepts(file))

        return findings


def _collect_test_files(files: List[CodeFile]) -> Set[str]:
    names = set()
    for f in files:
        name = Path(f.path).name
        if "test" in name or f.path.startswith("tests/"):
            names.add(name)
    return names


def _is_test_file(path_str: str) -> bool:
    name = Path(path_str).name
    return "test" in name or path_str.startswith("tests/")


def _has_matching_test(path_str: str, test_files: Set[str]) -> bool:
    stem = Path(path_str).stem
    candidates = {f"test_{stem}.py", f"{stem}_test.py"}
    return any(c in test_files for c in candidates)


def _find_bare_excepts(file: CodeFile) -> List[dict]:
    findings: List[dict] = []
    for i, line in enumerate(file.content.splitlines(), start=1):
        if re.match(r"^\s*except\s*:\s*$", line):
            findings.append(
                {
                    "file": file.path,
                    "line": i,
                    "issue": "Bare except",
                    "severity": "MEDIUM",
                    "description": "Bare except clause can hide errors",
                    "recommendation": "Catch specific exception types.",
                    "category": "test",
                    "line_content": line.strip(),
                }
            )
    return findings
