from collections import Counter
from typing import Dict, List


SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}


class SynthesisAgent:
    async def synthesize(self, agent_results: Dict[str, List[dict]]) -> dict:
        all_findings: List[dict] = []
        for findings in agent_results.values():
            all_findings.extend(findings)

        seen = set()
        unique_findings: List[dict] = []
        for f in all_findings:
            key = (f.get("file", ""), f.get("line", 0), f.get("issue", ""))
            if key not in seen:
                seen.add(key)
                unique_findings.append(f)

        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in unique_findings:
            sev = f.get("severity", "LOW").upper()
            if sev in severity_counts:
                severity_counts[sev] += 1

        unique_findings.sort(key=lambda f: SEVERITY_ORDER.get(f.get("severity", "LOW").upper(), 5))

        file_counts = Counter(f.get("file", "") for f in unique_findings)
        top_files = [{"file": f, "count": c} for f, c in file_counts.most_common(10)]

        security_score = max(
            0,
            100
            - severity_counts["CRITICAL"] * 20
            - severity_counts["HIGH"] * 5
            - severity_counts["MEDIUM"] * 2
            - severity_counts["LOW"] * 1,
        )

        executive_summary = (
            f"Audit found {len(unique_findings)} issues across "
            f"{severity_counts['CRITICAL']} critical, {severity_counts['HIGH']} high, "
            f"{severity_counts['MEDIUM']} medium, and {severity_counts['LOW']} low findings."
        )

        recommendations = _recommendations(severity_counts)

        return {
            "summary": severity_counts,
            "findings": unique_findings,
            "top_files": top_files,
            "executive_summary": executive_summary,
            "top_recommendations": recommendations,
            "security_score": security_score,
            "total_findings": len(unique_findings),
        }


def _recommendations(summary: Dict[str, int]) -> List[str]:
    recs: List[str] = []
    if summary.get("CRITICAL", 0) > 0:
        recs.append("Address critical findings immediately.")
    if summary.get("HIGH", 0) > 0:
        recs.append("Triage high severity issues this sprint.")
    if summary.get("MEDIUM", 0) > 0:
        recs.append("Schedule fixes for medium issues in upcoming work.")
    if summary.get("LOW", 0) > 0 and len(recs) < 3:
        recs.append("Document and backlog low severity improvements.")
    return recs[:3]
