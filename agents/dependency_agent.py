from pathlib import Path
from typing import List

from tools.dep_checker import check_python_deps


class DependencyAgent:
    async def analyze(self, repo_path: Path) -> List[dict]:
        findings: List[dict] = []
        deps = check_python_deps(repo_path)
        for dep in deps:
            findings.append(
                {
                    "file": "requirements.txt",
                    "line": 0,
                    "issue": f"{dep.get('package')} {dep.get('id')}",
                    "severity": dep.get("severity", "HIGH"),
                    "description": dep.get("summary", ""),
                    "recommendation": f"Upgrade {dep.get('package')} to a patched version.",
                    "category": "dependency",
                }
            )
        return findings
