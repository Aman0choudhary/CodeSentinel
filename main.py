import asyncio
from pathlib import Path
from typing import List

import typer
from rich.console import Console

from agents.orchestrator import Orchestrator
from config import settings
from input.github_fetcher import fetch_github_repo, cleanup
from input.local_loader import load_local
from output.report_md import generate_markdown
from output.report_json import generate_json
from tools.hermes_client import HermesClient

app = typer.Typer(help="CodeSentinel - Multi-Agent Code Security Audit")
console = Console()


@app.command()
def audit(
    github: str = typer.Option(None, help="GitHub repository URL"),
    local: str = typer.Option(None, help="Local path or ZIP file"),
    output: str = typer.Option(None, help="Output directory"),
    json_out: str = typer.Option(None, "--json", help="Write JSON report to this path"),
    fail_on: str = typer.Option(None, help="Exit non-zero on severity: critical/high/medium/low"),
    include: List[str] = typer.Option(None, "--include", "-i", help="Include glob (repeatable)"),
    exclude: List[str] = typer.Option(None, "--exclude", "-x", help="Exclude glob (repeatable)"),
    respect_gitignore: bool = typer.Option(True, help="Honor .gitignore and .codesentinelignore"),
    offline: bool = typer.Option(False, help="Disable remote LLM calls"),
    verbose: bool = typer.Option(False, help="Verbose output"),
) -> None:
    if bool(github) == bool(local):
        console.print("Error: Provide either --github or --local")
        raise typer.Exit(1)

    output_dir = Path(output or settings.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    hermes_client = HermesClient(
        base_url=settings.hermes_base_url,
        api_key=settings.hermes_api_key,
        model=settings.hermes_model,
        api_path=settings.hermes_api_path,
        timeout_seconds=settings.hermes_timeout_seconds,
        enabled=settings.hermes_enabled and not offline,
        verbose=verbose,
    )

    tmp_path = None
    try:
        if github:
            repo_name = github.rstrip("/").split("/")[-1]
            repo_path = fetch_github_repo(github)
            tmp_path = repo_path
        else:
            repo_path = load_local(local)
            repo_name = Path(local).stem

        orchestrator = Orchestrator(hermes_client=hermes_client)
        report = asyncio.run(
            orchestrator.audit(
                repo_path,
                include_globs=include or [],
                exclude_globs=exclude or [],
                respect_gitignore=respect_gitignore,
            )
        )

        md_path = output_dir / f"{repo_name}_audit.md"
        generate_markdown(report, repo_name, md_path)

        if json_out:
            generate_json(report, Path(json_out))

        console.print("Reports saved to:")
        console.print(f"  {md_path}")
        if json_out:
            console.print(f"  {json_out}")

        if fail_on:
            order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            threshold = order.get(fail_on.lower())
            if threshold is None:
                raise typer.Exit(2)
            summary = report.get("summary", {})
            if any(
                summary.get(k.upper(), 0) > 0
                for k, v in order.items()
                if v <= threshold
            ):
                raise typer.Exit(1)

    finally:
        if tmp_path:
            cleanup(tmp_path)


if __name__ == "__main__":
    app()
