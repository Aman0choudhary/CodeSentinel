from pathlib import Path
from typing import List, Tuple, Dict
import requests

OSV_API = "https://api.osv.dev/v1/query"


def parse_requirements(req_file: Path) -> List[Tuple[str, str]]:
    packages: List[Tuple[str, str]] = []
    for line in req_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" in line:
            name, version = line.split("==", 1)
            packages.append((name.strip(), version.strip()))
        elif ">=" in line:
            name = line.split(">=", 1)[0].strip()
            packages.append((name, "unknown"))
    return packages


def query_osv(name: str, version: str, ecosystem: str) -> List[Dict]:
    payload = {"version": version, "package": {"name": name, "ecosystem": ecosystem}}
    resp = requests.post(OSV_API, json=payload, timeout=10)
    if resp.status_code == 200:
        return resp.json().get("vulns", [])
    return []


def _severity_from_cvss(score: float) -> str:
    if score >= 9.0:
        return "CRITICAL"
    if score >= 7.0:
        return "HIGH"
    if score >= 4.0:
        return "MEDIUM"
    return "LOW"


def _map_vuln_severity(vuln: Dict) -> str:
    for sev in vuln.get("severity", []):
        if sev.get("type") == "CVSS_V3":
            try:
                score = float(sev.get("score", 0))
                return _severity_from_cvss(score)
            except ValueError:
                continue
    return "HIGH"


def check_python_deps(repo_path: Path) -> List[Dict]:
    req_file = repo_path / "requirements.txt"
    if not req_file.exists():
        return []

    findings: List[Dict] = []
    for name, version in parse_requirements(req_file):
        if version == "unknown":
            continue
        try:
            vulns = query_osv(name, version, "PyPI")
        except Exception:
            continue
        for vuln in vulns:
            findings.append(
                {
                    "package": name,
                    "version": version,
                    "id": vuln.get("id", ""),
                    "summary": vuln.get("summary", ""),
                    "details": vuln.get("details", ""),
                    "severity": _map_vuln_severity(vuln),
                }
            )
    return findings
