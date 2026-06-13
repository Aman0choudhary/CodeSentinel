import re
from typing import List, Tuple, Dict

REDACTION_PATTERNS = {
    "aws_access_key": r"AKIA[0-9A-Z]{16}",
    "generic_api_key": r"(?i)api[_-]?key\s*=\s*['\"][^'\"]+['\"]",
    "generic_secret": r"(?i)(secret|token)\s*=\s*['\"][^'\"]+['\"]",
    "password_assignment": r"(?i)(password|passwd|pwd)\s*=\s*['\"][^'\"]+['\"]",
}


def redact_secrets(text: str) -> Tuple[str, List[Dict]]:
    redactions: List[Dict] = []
    redacted = text

    for name, pattern in REDACTION_PATTERNS.items():
        def _replace(match: re.Match) -> str:
            redactions.append({"pattern": name, "snippet": match.group(0)[:8]})
            return f"<redacted:{name}>"

        redacted = re.sub(pattern, _replace, redacted)

    return redacted, redactions
