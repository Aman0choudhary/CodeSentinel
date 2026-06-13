from datetime import datetime
from pathlib import Path

SEVERITY_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]


def generate_markdown(report: dict, repo_name: str, output_path: Path) -> None:
    lines = []
    lines.append("# CodeSentinel Audit Report")
    lines.append("")
    lines.append(f"Repository: {repo_name}")
    lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Security Score: {report.get('security_score', 'N/A')}/100")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(report.get("executive_summary", "No summary available."))
    lines.append("")
    lines.append("## Findings Overview")
    lines.append("")
    lines.append("| Severity | Count |")
    lines.append("|---|---|")

    summary = report.get("summary", {})
    for sev in SEVERITY_ORDER:
        lines.append(f"| {sev} | {summary.get(sev, 0)} |")

    lines.append("")
    lines.append("## Top Recommendations")
    lines.append("")
    for i, rec in enumerate(report.get("top_recommendations", []), 1):
        lines.append(f"{i}. {rec}")

    lines.append("")
    lines.append("## Detailed Findings")
    lines.append("")

    current_severity = None
    for finding in report.get("findings", []):
        sev = finding.get("severity", "LOW").upper()
        if sev != current_severity:
            current_severity = sev
            lines.append("")
            lines.append(f"### {sev}")
            lines.append("")

        lines.append(f"#### {finding.get('issue', 'Unknown Issue')}")
        file_line = finding.get("file", "unknown")
        if finding.get("line"):
            file_line += f" (line {finding.get('line')})"
        lines.append(f"- File: {file_line}")
        lines.append(f"- Description: {finding.get('description', '')}")
        lines.append(f"- Recommendation: {finding.get('recommendation', '')}")
        lines.append("")

        if finding.get("line_content"):
            lines.append("```")
            lines.append(finding["line_content"])
            lines.append("```")
            lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
