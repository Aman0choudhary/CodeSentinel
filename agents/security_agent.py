import json
import re
from typing import List, Optional

from tools.file_reader import CodeFile
from tools.pattern_scanner import scan_file_patterns, SECURITY_PATTERNS
from tools.redaction import redact_secrets
from tools.hermes_client import HermesClient


class SecurityAgent:
    def __init__(self, hermes_client: Optional[HermesClient] = None) -> None:
        self.hermes_client = hermes_client
        self.system_prompt = (
            "You are a senior application security engineer. "
            "Analyze code snippets for security vulnerabilities. "
            "Return a JSON array of findings with fields: "
            "line, issue, severity, description, recommendation."
        )

    async def analyze(self, files: List[CodeFile]) -> List[dict]:
        findings: List[dict] = []
        for file in files:
            pattern_matches = scan_file_patterns(file.content, SECURITY_PATTERNS)
            for match in pattern_matches:
                findings.append(
                    {
                        "file": file.path,
                        "line": match.line_number,
                        "issue": match.pattern_name,
                        "severity": match.severity,
                        "description": f"Detected pattern: {match.line_content}",
                        "recommendation": "Review this code for security issues.",
                        "category": "security",
                        "line_content": match.line_content,
                    }
                )

            if not pattern_matches:
                continue

            if self.hermes_client and self.hermes_client.enabled:
                snippet = _build_context(file.content, [m.line_number for m in pattern_matches])
                redacted, _ = redact_secrets(snippet)
                user_prompt = (
                    f"File: {file.path}\n"
                    f"Language: {file.language}\n\n"
                    "Code:\n"
                    f"{redacted}\n\n"
                    "Return a JSON array of findings."
                )
                try:
                    response = self.hermes_client.run(self.system_prompt, user_prompt)
                    findings.extend(_parse_findings(response, file.path))
                except Exception:
                    pass

        return findings


def _build_context(content: str, lines: List[int], radius: int = 6) -> str:
    src = content.splitlines()
    keep = set()
    for n in lines:
        start = max(1, n - radius)
        end = min(len(src), n + radius)
        for i in range(start, end + 1):
            keep.add(i)
    ordered = sorted(keep)
    return "\n".join(f"{i}: {src[i - 1]}" for i in ordered)


def _parse_findings(response: Optional[str], file_path: str) -> List[dict]:
    if not response:
        return []
    match = re.search(r"\[.*\]", response, re.DOTALL)
    if not match:
        return []
    try:
        data = json.loads(match.group())
    except json.JSONDecodeError:
        return []

    findings: List[dict] = []
    for item in data:
        findings.append(
            {
                "file": file_path,
                "line": int(item.get("line", 0)),
                "issue": item.get("issue", "Unknown"),
                "severity": item.get("severity", "MEDIUM"),
                "description": item.get("description", ""),
                "recommendation": item.get("recommendation", ""),
                "category": "security",
            }
        )
    return findings
