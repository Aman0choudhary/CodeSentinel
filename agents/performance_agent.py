import re
from typing import List

from tools.file_reader import CodeFile


class PerformanceAgent:
    async def analyze(self, files: List[CodeFile]) -> List[dict]:
        findings: List[dict] = []
        for file in files:
            lines = file.content.splitlines()

            for i, line in enumerate(lines):
                if "time.sleep(" in line:
                    if _is_inside_async(lines, i):
                        findings.append(
                            _make_finding(
                                file.path,
                                i + 1,
                                "Blocking sleep in async context",
                                "MEDIUM",
                                "time.sleep used inside async function",
                                "Use asyncio.sleep in async contexts.",
                                line.strip(),
                            )
                        )

                if re.search(r"^\s*for\s+\w+\s+in\s+.*:\s*$", line):
                    if _db_call_in_window(lines, i, window=6):
                        findings.append(
                            _make_finding(
                                file.path,
                                i + 1,
                                "Possible N+1 query pattern",
                                "HIGH",
                                "Database call inside loop",
                                "Batch queries or prefetch related data.",
                                line.strip(),
                            )
                        )

                if "open(" in line and "with " not in line:
                    findings.append(
                        _make_finding(
                            file.path,
                            i + 1,
                            "File open without context manager",
                            "MEDIUM",
                            "File opened without a with block",
                            "Use with open(...) to ensure closure.",
                            line.strip(),
                        )
                    )

        return findings


def _is_inside_async(lines: List[str], idx: int) -> bool:
    start = max(0, idx - 20)
    for j in range(idx, start - 1, -1):
        if re.search(r"^\s*async\s+def\s+", lines[j]):
            return True
    return False


def _db_call_in_window(lines: List[str], idx: int, window: int = 5) -> bool:
    for j in range(idx + 1, min(len(lines), idx + window + 1)):
        if re.search(r"\.(filter|get|query|execute|select)\(", lines[j]):
            return True
    return False


def _make_finding(
    file_path: str,
    line: int,
    issue: str,
    severity: str,
    description: str,
    recommendation: str,
    line_content: str,
) -> dict:
    return {
        "file": file_path,
        "line": line,
        "issue": issue,
        "severity": severity,
        "description": description,
        "recommendation": recommendation,
        "category": "performance",
        "line_content": line_content,
    }
