import ast
from typing import List

from tools.file_reader import CodeFile


class ArchitectureAgent:
    async def analyze(self, files: List[CodeFile]) -> List[dict]:
        findings: List[dict] = []
        for file in files:
            if file.line_count > 500:
                findings.append(
                    {
                        "file": file.path,
                        "line": 0,
                        "issue": "Large file",
                        "severity": "MEDIUM",
                        "description": f"File has {file.line_count} lines",
                        "recommendation": "Consider splitting into smaller modules.",
                        "category": "architecture",
                    }
                )

            if file.language == "python":
                findings.extend(_analyze_python(file))

        return findings


def _analyze_python(file: CodeFile) -> List[dict]:
    findings: List[dict] = []
    try:
        tree = ast.parse(file.content)
    except SyntaxError:
        return findings

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = [
                n for n in node.body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            if len(methods) > 20:
                findings.append(
                    {
                        "file": file.path,
                        "line": getattr(node, "lineno", 0),
                        "issue": "Large class",
                        "severity": "MEDIUM",
                        "description": f"Class '{node.name}' has {len(methods)} methods",
                        "recommendation": "Refactor into smaller classes.",
                        "category": "architecture",
                    }
                )

    return findings
