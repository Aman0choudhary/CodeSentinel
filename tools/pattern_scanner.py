import re
from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class PatternMatch:
    pattern_name: str
    line_number: int
    line_content: str
    severity: str


SECURITY_PATTERNS: Dict[str, Tuple[str, str]] = {
    "hardcoded_password": (
        r"(?i)(password|passwd|pwd)\s*=\s*['\"][^'\"]{4,}['\"]",
        "HIGH",
    ),
    "hardcoded_api_key": (
        r"(?i)(api_key|apikey|api-key)\s*=\s*['\"][a-zA-Z0-9]{16,}['\"]",
        "CRITICAL",
    ),
    "hardcoded_secret": (
        r"(?i)(secret|token)\s*=\s*['\"][^'\"]{8,}['\"]",
        "HIGH",
    ),
    "aws_access_key": (r"AKIA[0-9A-Z]{16}", "CRITICAL"),
    "sql_string_concat": (
        r"(?i)(SELECT|INSERT|UPDATE|DELETE).*(\+|%s).*",
        "HIGH",
    ),
    "subprocess_shell_true": (
        r"subprocess\.(run|call|Popen).*shell\s*=\s*True",
        "HIGH",
    ),
    "md5_usage": (r"hashlib\.md5\s*\(", "MEDIUM"),
    "sha1_usage": (r"hashlib\.sha1\s*\(", "MEDIUM"),
    "eval_usage": (r"\beval\s*\(", "HIGH"),
    "innerhtml_assignment": (r"innerHTML\s*=\s*", "MEDIUM"),
}


def scan_file_patterns(content: str, patterns: Dict[str, Tuple[str, str]]) -> List[PatternMatch]:
    matches: List[PatternMatch] = []
    lines = content.splitlines()
    for line_num, line in enumerate(lines, start=1):
        for name, (pattern, severity) in patterns.items():
            if re.search(pattern, line):
                matches.append(
                    PatternMatch(
                        pattern_name=name,
                        line_number=line_num,
                        line_content=line.strip(),
                        severity=severity,
                    )
                )
    return matches
