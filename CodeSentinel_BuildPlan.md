# 🛡️ CodeSentinel — Complete Build Plan
### Multi-Agent Security & Code Audit System for the Hermes Agent Challenge

---

## 📌 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Project Structure](#3-project-structure)
4. [Tech Stack & Dependencies](#4-tech-stack--dependencies)
5. [Day-by-Day Build Plan](#5-day-by-day-build-plan)
6. [Complete Code Guide](#6-complete-code-guide)
   - [config.py](#61-configpy)
    - [Input: GitHub Fetcher](#62-input-github-fetcher)
    - [Input: Local Loader](#63-input-local-loader)
    - [Tools: File Reader](#64-tools-file-reader)
    - [Tools: Pattern Scanner](#65-tools-pattern-scanner)
    - [Tools: Dependency Checker](#66-tools-dependency-checker)
    - [Agents: Security Agent](#67-agents-security-agent)
    - [Agents: Performance Agent](#68-agents-performance-agent)
    - [Agents: Architecture Agent](#69-agents-architecture-agent)
    - [Agents: Test Agent](#610-agents-test-agent)
    - [Agents: Dependency Agent](#611-agents-dependency-agent)
    - [Agents: Orchestrator](#612-agents-orchestrator)
    - [Agents: Synthesis Agent](#613-agents-synthesis-agent)
    - [Output: Markdown Report](#614-output-markdown-report)
    - [Output: HTML Report](#615-output-html-report)
    - [Output: JSON Report](#616-output-json-report)
    - [main.py CLI](#617-mainpy-cli)
7. [Hermes Agent Integration Guide](#7-hermes-agent-integration-guide)
8. [Sample Output](#8-sample-output)
9. [Testing Strategy](#9-testing-strategy)
10. [Security & Privacy Considerations](#10-security--privacy-considerations)
11. [CI/CD & Automation](#11-cicd--automation)
12. [Packaging & Release](#12-packaging--release)
13. [Operational Limits & Ignore Rules](#13-operational-limits--ignore-rules)
14. [DEV.to Submission Guide](#14-devto-submission-guide)
15. [Judging Criteria Checklist](#15-judging-criteria-checklist)

---

## 1. Project Overview

**CodeSentinel** is an autonomous multi-agent code audit system powered by Hermes Agent. It takes any GitHub repository URL or local codebase as input and deploys a team of specialized AI agents to analyze it from every security and quality angle simultaneously.

### The Problem It Solves

Developers ship code fast. Security is almost always an afterthought. Static linters catch syntax issues but miss logic-level vulnerabilities. Manual code reviews are slow, inconsistent, and expensive. CodeSentinel bridges this gap — an autonomous AI auditor that thinks like a senior security engineer, runs in seconds, and costs nothing.

### What Makes It Stand Out

- **Multi-agent orchestration** — 5 specialized agents running in parallel via `asyncio`
- **Hermes Agent at the core** — each agent uses Hermes Agent for reasoning, not just pattern matching
- **Real security intelligence** — not just regex, but context-aware vulnerability detection
- **Beautiful dual output** — both Markdown and interactive HTML dashboard
- **Zero config for users** — one command, full audit

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     USER INPUT                          │
│         GitHub URL  ──or──  Local Path / ZIP            │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  INPUT LAYER                            │
│   github_fetcher.py        local_loader.py              │
│   (clone repo via GitPython)  (read path/unzip)         │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  TOOLS LAYER                            │
│   file_reader.py   pattern_scanner.py   dep_checker.py  │
│   (chunk files)    (AST + regex scan)   (CVE lookup)    │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              ORCHESTRATOR AGENT (Hermes)                │
│          Spawns all agents in parallel (asyncio)        │
└──┬──────────┬──────────┬──────────┬────────────┬────────┘
   │          │          │          │            │
   ▼          ▼          ▼          ▼            ▼
🔐 Security  ⚡ Perf   🏗️ Arch   🧪 Test    📦 Deps
  Agent      Agent     Agent     Agent       Agent
(Hermes)   (Hermes)  (Hermes)  (Hermes)   (Hermes)
   │          │          │          │            │
   └──────────┴──────────┴──────────┴────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              SYNTHESIS AGENT (Hermes)                   │
│   Merges findings, deduplicates, scores by severity     │
│   Outputs structured JSON                               │
└───────────────────────┬─────────────────────────────────┘
                        │
              ┌─────────┴──────────┐
              ▼                    ▼
     📄 Markdown Report    🌐 HTML Dashboard
     (report_md.py)        (report_html.py)
```

---

## 3. Project Structure

```
codesentinel/
│
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py         # Lead agent, asyncio coordination
│   ├── security_agent.py       # SQLi, XSS, secrets, auth flaws, OWASP Top 10
│   ├── performance_agent.py    # N+1, memory leaks, blocking calls
│   ├── architecture_agent.py   # SOLID violations, coupling, God classes
│   ├── test_agent.py           # Coverage gaps, missing error handling
│   ├── dependency_agent.py     # CVEs, outdated packages, license issues
│   └── synthesis_agent.py      # Merge, deduplicate, prioritize, score
│
├── input/
│   ├── __init__.py
│   ├── github_fetcher.py       # Clone/fetch from GitHub URL
│   └── local_loader.py         # Load from local path or ZIP
│
├── output/
│   ├── __init__.py
│   ├── report_md.py            # Generate Markdown audit report
│   ├── report_html.py          # Generate HTML dashboard
│   ├── report_json.py          # Generate machine-readable JSON
│   └── templates/
│       └── dashboard.html      # Jinja2 HTML template
│
├── tools/
│   ├── __init__.py
│   ├── file_reader.py          # Recursive file reading + chunking
│   ├── pattern_scanner.py      # Regex + AST-based scanning
│   └── dep_checker.py          # pip-audit + OSV API integration
│
├── tests/
│   ├── test_security_agent.py
│   ├── test_performance_agent.py
│   ├── test_orchestrator.py
│   └── sample_repos/           # Small vulnerable repos for testing
│
├── main.py                     # CLI entrypoint (Typer)
├── config.py                   # Settings, Hermes Agent config
├── requirements.txt
├── pyproject.toml              # Build metadata + console entrypoint
├── .codesentinelignore         # Custom ignore rules (like .gitignore)
├── .github/
│   └── workflows/
│       └── ci.yml              # CI run with optional severity gate
├── CHANGELOG.md
├── LICENSE
├── README.md
└── .env.example
```

---

## 4. Tech Stack & Dependencies

### Core
| Library | Purpose | Install |
|---|---|---|
| `hermes-agent` | Nous Research agentic AI | `pip install hermes-agent` |
| `typer` | Beautiful CLI | `pip install typer[all]` |
| `pydantic-settings` | Config management | `pip install pydantic-settings` |
| `asyncio` | Parallel agent execution | stdlib |
| `python-dotenv` | Env var loading | `pip install python-dotenv` |

### Input
| Library | Purpose | Install |
|---|---|---|
| `gitpython` | Clone GitHub repos | `pip install gitpython` |
| `requests` | GitHub API calls | `pip install requests` |

### Analysis
| Library | Purpose | Install |
|---|---|---|
| `ast` | Python AST parsing | stdlib |
| `pip-audit` | CVE checking | `pip install pip-audit` |
| `packaging` | Version comparison | `pip install packaging` |
| `bandit` | Security linting (tool) | `pip install bandit` |
| `pathspec` | .gitignore-style matching | `pip install pathspec` |

### Output
| Library | Purpose | Install |
|---|---|---|
| `jinja2` | HTML templating | `pip install jinja2` |
| `rich` | Terminal UI | `pip install rich` |
| `markdown` | MD rendering | `pip install markdown` |

### requirements.txt
```
hermes-agent>=0.1.0
typer[all]>=0.12.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
gitpython>=3.1.0
requests>=2.31.0
jinja2>=3.1.0
rich>=13.0.0
markdown>=3.5.0
pip-audit>=2.6.0
packaging>=23.0
bandit>=1.7.0
pathspec>=0.11.0
```

---

## 5. Day-by-Day Build Plan

### Day 1 — Foundation & Input Layer
**Goal:** Hermes Agent running locally, both input methods working

**Morning (2–3 hrs):**
- [ ] Install Hermes Agent, follow quickstart: https://hermes-agent.nousresearch.com/docs/
- [ ] Watch quickstart video: https://www.youtube.com/watch?v=R3YOGfTBcQg
- [ ] Set up project structure (create all folders and `__init__.py` files)
- [ ] Create `config.py` with Hermes Agent settings
- [ ] Create `.env` file with API keys

**Afternoon (3–4 hrs):**
- [ ] Build `github_fetcher.py` — clone repo from URL, handle auth, clean up temp dirs
- [ ] Build `local_loader.py` — accept path or ZIP, validate, return file tree
- [ ] Build `file_reader.py` — recursive reading, filter by extension, chunk large files
- [ ] Test: clone a small public GitHub repo and print all Python files

**Evening (1–2 hrs):**
- [ ] Build `pattern_scanner.py` skeleton — regex patterns for common vulnerabilities
- [ ] Write basic tests in `tests/` to confirm input layer works

---

### Day 2 — Security & Dependency Agents
**Goal:** Two fully working specialized agents producing real findings

**Morning (2–3 hrs):**
- [ ] Build `security_agent.py`:
  - Hardcoded secrets (API keys, passwords, tokens)
  - SQL injection patterns
  - XSS vulnerabilities
  - Insecure deserialization
  - Weak cryptography (MD5, SHA1)
  - Path traversal
  - Command injection
  - OWASP Top 10 coverage

**Afternoon (2–3 hrs):**
- [ ] Build `dep_checker.py`:
  - Parse `requirements.txt`, `package.json`, `Gemfile`, `pom.xml`
  - Call OSV API for CVE lookups: `https://api.osv.dev/v1/query`
  - Integrate `pip-audit` for Python deps
  - Flag outdated packages using PyPI API
- [ ] Build `dependency_agent.py` wrapping the tool

**Evening (1–2 hrs):**
- [ ] Test both agents against a sample vulnerable repo (e.g., DVWA or create your own)
- [ ] Fix edge cases, refine prompts

---

### Day 3 — Performance, Architecture & Test Agents
**Goal:** Remaining three specialized agents working

**Morning (2–3 hrs):**
- [ ] Build `performance_agent.py`:
  - N+1 query patterns in ORM usage
  - Synchronous calls inside async functions
  - Large loops with DB calls
  - Memory leaks (unclosed resources, circular references)
  - Inefficient string concatenation in loops

**Afternoon (2–3 hrs):**
- [ ] Build `architecture_agent.py`:
  - God classes (files > 500 lines, classes > 20 methods)
  - Circular imports detection
  - Deep inheritance chains
  - High coupling between modules
  - SOLID principle violations (using AST)

**Evening (2 hrs):**
- [ ] Build `test_agent.py`:
  - Missing try/except around risky operations
  - Untested public functions (no corresponding test file)
  - Missing input validation
  - Bare except clauses
  - Missing type hints on public APIs
- [ ] Integration test: run all 5 agents on same repo, confirm they don't crash

---

### Day 4 — Orchestrator & Synthesis
**Goal:** Full parallel multi-agent pipeline working end to end

**Morning (3–4 hrs):**
- [ ] Build `orchestrator.py`:
  ```python
  # Key pattern: asyncio.gather() for parallel agent execution
  results = await asyncio.gather(
      security_agent.analyze(codebase),
      performance_agent.analyze(codebase),
      architecture_agent.analyze(codebase),
      test_agent.analyze(codebase),
      dependency_agent.analyze(codebase),
  )
  ```
  - Progress tracking with `rich` progress bar
  - Error handling per agent (one failing shouldn't kill the rest)
  - Timeout handling

**Afternoon (3–4 hrs):**
- [ ] Build `synthesis_agent.py`:
  - Merge all findings into unified list
  - Deduplicate overlapping findings (same file + line)
  - Score severity: Critical / High / Medium / Low / Info
  - Group by category and file
  - Generate executive summary
  - Output structured JSON:
    ```json
    {
      "summary": { "critical": 3, "high": 12, "medium": 8, "low": 5 },
      "findings": [...],
      "top_files": [...],
      "recommendations": [...]
    }
    ```

**Evening (1 hr):**
- [ ] End-to-end test: GitHub URL → parallel agents → synthesis → JSON output
- [ ] Time the full pipeline, optimize if needed

---

### Day 5 — Output Layer & CLI Polish
**Goal:** Beautiful reports and smooth CLI experience

**Morning (2–3 hrs):**
- [ ] Build `report_md.py`:
  - Executive summary with emoji severity badges
  - Findings table sortable by severity
  - Per-finding code snippets with line numbers
  - Recommendations section
  - Stats section (files scanned, issues found, time taken)

**Afternoon (3–4 hrs):**
- [ ] Build `report_html.py` + Jinja2 template:
  - Sidebar navigation (by category / by severity / by file)
  - Severity donut chart (Chart.js)
  - Findings by category bar chart
  - Filterable / searchable findings table
  - Code viewer with syntax highlighting (highlight.js)
  - Dark/light mode toggle
  - Print-friendly CSS

**Evening (1–2 hrs):**
- [ ] Build `main.py` CLI:
  ```
  codesentinel --github https://github.com/user/repo
  codesentinel --local ./my-project
  codesentinel --local ./project.zip --output ./reports
  codesentinel --github <url> --agents security,deps  # run subset
    codesentinel --github <url> --json ./reports/report.json
    codesentinel --github <url> --fail-on high  # exit 1 if High+ found
  ```
- [ ] Add `--verbose` flag, `--output` dir flag
- [ ] Add `--json`, `--fail-on`, `--include`, `--exclude`, `--respect-gitignore` flags
- [ ] Add `.codesentinelignore` support (like .gitignore)
- [ ] Beautiful terminal output with `rich` tables and progress bars

---

### Day 6 — Demo, Polish & Submission
**Goal:** Win-worthy submission

**Morning (2–3 hrs):**
- [ ] Run CodeSentinel on 3 real repos:
  1. A well-known intentionally vulnerable repo (e.g., `WebGoat`, `DVWA`)
  2. A popular open source project (find one with some real issues)
  3. Your own test repo
- [ ] Capture screenshots of HTML dashboard
- [ ] Record a 3–5 minute demo video (Loom or OBS):
  - Show CLI command running
  - Show terminal progress output
  - Show final HTML dashboard with findings
  - Click through a Critical finding with code snippet

**Afternoon (2–3 hrs):**
- [ ] Write README.md:
  - Project description + architecture diagram (ASCII)
  - Installation instructions
  - Usage examples
  - Screenshots of output
  - How Hermes Agent powers it
- [ ] Final code cleanup, add docstrings, type hints

**Evening (1–2 hrs):**
- [ ] Write and publish DEV.to submission post (template below in Section 14)
- [ ] Tag: `hermesagentchallenge`, `devchallenge`, `agents`
- [ ] Submit! 🎉

---

## 6. Complete Code Guide

### 6.1 config.py

```python
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Hermes Agent
    hermes_model: str = "hermes-3-llama-3.1-70b"
    hermes_base_url: str = "http://localhost:11434"  # or your endpoint
    
    # GitHub
    github_token: str = Field(default="", env="GITHUB_TOKEN")
    
    # Scanning
    max_file_size_kb: int = 500        # Skip files larger than this
    max_files_per_repo: int = 1000     # Cap for huge repos
    supported_extensions: list = [
        ".py", ".js", ".ts", ".java", ".go",
        ".rb", ".php", ".cs", ".cpp", ".c"
    ]
    
    # Output
    output_dir: str = "./codesentinel-reports"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

### 6.2 Input: GitHub Fetcher

**File:** `input/github_fetcher.py`

```python
import os
import tempfile
import shutil
from git import Repo
from pathlib import Path
from config import settings

def fetch_github_repo(url: str) -> Path:
    """Clone a GitHub repo to a temp directory. Returns path to cloned repo."""
    tmp_dir = tempfile.mkdtemp(prefix="codesentinel_")
    
    try:
        print(f"[*] Cloning {url}...")
        clone_url = url
        
        # Inject token for private repos
        if settings.github_token:
            # Convert https://github.com/user/repo
            # to https://token@github.com/user/repo
            clone_url = url.replace(
                "https://", f"https://{settings.github_token}@"
            )
        
        Repo.clone_from(clone_url, tmp_dir, depth=1)  # depth=1 = faster
        print(f"[✓] Cloned to {tmp_dir}")
        return Path(tmp_dir)
    
    except Exception as e:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise RuntimeError(f"Failed to clone repo: {e}")

def cleanup(path: Path):
    """Remove temp cloned repo after analysis."""
    shutil.rmtree(path, ignore_errors=True)
```

---

### 6.3 Input: Local Loader

**File:** `input/local_loader.py`

```python
import zipfile
import shutil
import tempfile
from pathlib import Path

def load_local(path_str: str) -> Path:
    """Load a local directory or ZIP file. Returns path to codebase."""
    path = Path(path_str).resolve()
    
    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path}")
    
    if path.is_dir():
        return path
    
    if path.suffix == ".zip":
        tmp_dir = tempfile.mkdtemp(prefix="codesentinel_")
        with zipfile.ZipFile(path, 'r') as zf:
            zf.extractall(tmp_dir)
        print(f"[✓] Extracted ZIP to {tmp_dir}")
        return Path(tmp_dir)
    
    raise ValueError(f"Unsupported input: {path}. Use a directory or .zip file.")
```

---

### 6.4 Tools: File Reader

**File:** `tools/file_reader.py`

```python
from pathlib import Path
from typing import Generator
from config import settings
from dataclasses import dataclass

@dataclass
class CodeFile:
    path: str           # relative path from repo root
    content: str        # file content
    language: str       # detected language
    line_count: int

EXTENSION_TO_LANG = {
    ".py": "python", ".js": "javascript", ".ts": "typescript",
    ".java": "java", ".go": "go", ".rb": "ruby",
    ".php": "php", ".cs": "csharp", ".cpp": "cpp", ".c": "c"
}

def read_codebase(root: Path) -> list[CodeFile]:
    """Recursively read all supported code files from a directory."""
    files = []
    root = Path(root)
    
    skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 
                 'venv', 'dist', 'build', '.next', 'vendor'}
    
    for file_path in root.rglob("*"):
        # Skip hidden dirs and common non-code dirs
        if any(part in skip_dirs for part in file_path.parts):
            continue
        
        if not file_path.is_file():
            continue
        
        ext = file_path.suffix.lower()
        if ext not in settings.supported_extensions:
            continue
        
        # Skip huge files
        size_kb = file_path.stat().st_size / 1024
        if size_kb > settings.max_file_size_kb:
            continue
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            relative = str(file_path.relative_to(root))
            files.append(CodeFile(
                path=relative,
                content=content,
                language=EXTENSION_TO_LANG.get(ext, "unknown"),
                line_count=content.count('\n')
            ))
        except Exception:
            continue
        
        if len(files) >= settings.max_files_per_repo:
            break
    
    return files

def chunk_file(file: CodeFile, chunk_size: int = 200) -> list[str]:
    """Split large files into chunks of N lines for agent processing."""
    lines = file.content.split('\n')
    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunk = '\n'.join(lines[i:i + chunk_size])
        chunks.append(chunk)
    return chunks
```

**Missing piece to add:** respect `.gitignore` and `.codesentinelignore` with `pathspec`:

```python
import pathspec

def build_ignore_spec(root: Path) -> pathspec.PathSpec:
    patterns = []
    for name in [".gitignore", ".codesentinelignore"]:
        p = root / name
        if p.exists():
            patterns += p.read_text().splitlines()
    return pathspec.PathSpec.from_lines("gitwildmatch", patterns)
```

---

### 6.5 Tools: Pattern Scanner

**File:** `tools/pattern_scanner.py`

```python
import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class PatternMatch:
    pattern_name: str
    line_number: int
    line_content: str
    severity: str   # CRITICAL, HIGH, MEDIUM, LOW

# Security patterns
SECURITY_PATTERNS = {
    # Hardcoded secrets
    "hardcoded_password": (r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']{4,}["\']', "HIGH"),
    "hardcoded_api_key": (r'(?i)(api_key|apikey|api-key)\s*=\s*["\'][a-zA-Z0-9]{16,}["\']', "CRITICAL"),
    "hardcoded_secret": (r'(?i)(secret|token)\s*=\s*["\'][^"\']{8,}["\']', "HIGH"),
    "aws_key": (r'AKIA[0-9A-Z]{16}', "CRITICAL"),
    
    # SQL Injection
    "sql_string_concat": (r'(?i)(SELECT|INSERT|UPDATE|DELETE).*\+\s*(request|user|input|param)', "HIGH"),
    "sql_format_string": (r'(?i)cursor\.execute\s*\(\s*["\'].*%[s|d].*["\']', "HIGH"),
    
    # Command Injection
    "os_system_user_input": (r'os\.system\s*\(.*\+', "CRITICAL"),
    "subprocess_shell_true": (r'subprocess\.(run|call|Popen).*shell\s*=\s*True', "HIGH"),
    
    # Weak Crypto
    "md5_usage": (r'hashlib\.md5\s*\(', "MEDIUM"),
    "sha1_usage": (r'hashlib\.sha1\s*\(', "MEDIUM"),
    
    # Path Traversal
    "path_traversal": (r'open\s*\(.*\+.*\)', "MEDIUM"),
    
    # XSS (for web frameworks)
    "eval_usage": (r'\beval\s*\(', "HIGH"),
    "innerHTML_assignment": (r'innerHTML\s*=\s*', "MEDIUM"),
}

def scan_file_patterns(content: str, patterns: dict) -> list[PatternMatch]:
    """Scan file content for regex patterns. Returns list of matches."""
    matches = []
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, start=1):
        for name, (pattern, severity) in patterns.items():
            if re.search(pattern, line):
                matches.append(PatternMatch(
                    pattern_name=name,
                    line_number=line_num,
                    line_content=line.strip(),
                    severity=severity
                ))
    return matches
```

---

### 6.6 Tools: Dependency Checker

**File:** `tools/dep_checker.py`

```python
import json
import requests
import subprocess
from pathlib import Path

OSV_API = "https://api.osv.dev/v1/query"
PYPI_API = "https://pypi.org/pypi/{package}/json"

def check_python_deps(repo_path: Path) -> list[dict]:
    """Check Python dependencies for CVEs using pip-audit."""
    req_file = repo_path / "requirements.txt"
    if not req_file.exists():
        return []
    
    try:
        result = subprocess.run(
            ["pip-audit", "-r", str(req_file), "--format", "json"],
            capture_output=True, text=True, timeout=60
        )
        if result.stdout:
            data = json.loads(result.stdout)
            return data.get("dependencies", [])
    except Exception as e:
        print(f"[!] pip-audit failed: {e}")
    
    return []

def query_osv(package: str, version: str, ecosystem: str = "PyPI") -> list[dict]:
    """Query OSV API for known vulnerabilities."""
    payload = {
        "version": version,
        "package": {"name": package, "ecosystem": ecosystem}
    }
    try:
        resp = requests.post(OSV_API, json=payload, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("vulns", [])
    except Exception:
        pass
    return []

def parse_requirements(req_file: Path) -> list[tuple[str, str]]:
    """Parse requirements.txt into (package, version) tuples."""
    packages = []
    for line in req_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '==' in line:
            name, version = line.split('==', 1)
            packages.append((name.strip(), version.strip()))
        elif '>=' in line:
            name = line.split('>=')[0].strip()
            packages.append((name, "unknown"))
    return packages
```

**Missing piece to add:** multi-ecosystem dependency support.

Targets and sources:
- Node: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` (ecosystem `npm`) + optional `npm audit --json`
- Python: `requirements.txt`, `poetry.lock`, `Pipfile.lock` (ecosystem `PyPI`)
- Java: `pom.xml`, `build.gradle` (ecosystem `Maven`)
- Go: `go.sum` (ecosystem `Go`)
- Ruby: `Gemfile.lock` (ecosystem `RubyGems`)

OSV query per package:
```python
def query_osv_generic(name: str, version: str, ecosystem: str) -> list[dict]:
    payload = {"version": version, "package": {"name": name, "ecosystem": ecosystem}}
    resp = requests.post(OSV_API, json=payload, timeout=10)
    return resp.json().get("vulns", []) if resp.status_code == 200 else []
```

---

### 6.7 Agents: Security Agent

**File:** `agents/security_agent.py`

```python
import asyncio
from tools.file_reader import CodeFile
from tools.pattern_scanner import scan_file_patterns, SECURITY_PATTERNS
from hermes_agent import HermesAgent  # adjust import per actual package
from config import settings
from dataclasses import dataclass
from typing import Optional

@dataclass
class SecurityFinding:
    file: str
    line: int
    issue: str
    severity: str   # CRITICAL, HIGH, MEDIUM, LOW
    description: str
    recommendation: str
    category: str = "security"

class SecurityAgent:
    """
    Specialized agent for detecting security vulnerabilities.
    Uses pattern scanning + Hermes Agent for context-aware analysis.
    """
    
    def __init__(self):
        self.agent = HermesAgent(
            model=settings.hermes_model,
            system_prompt="""You are a senior application security engineer.
            Analyze code snippets for security vulnerabilities including:
            - OWASP Top 10 vulnerabilities
            - Hardcoded credentials and secrets
            - Injection flaws (SQL, Command, LDAP)
            - Broken authentication patterns
            - Sensitive data exposure
            - Insecure cryptographic usage
            - Path traversal vulnerabilities
            
            For each finding provide:
            - Issue name
            - Severity (CRITICAL/HIGH/MEDIUM/LOW)
            - Brief description
            - Specific recommendation to fix
            
            Be precise. Only report real vulnerabilities, not false positives.
            Respond in JSON format."""
        )
    
    async def analyze(self, files: list[CodeFile]) -> list[SecurityFinding]:
        findings = []
        
        for file in files:
            # Step 1: Fast pattern scan
            pattern_matches = scan_file_patterns(file.content, SECURITY_PATTERNS)
            
            if not pattern_matches and len(file.content) < 100:
                continue
            
            # Step 2: Send suspicious files to Hermes Agent for deep analysis
            prompt = f"""
File: {file.path}
Language: {file.language}

Code:
```{file.language}
{file.content[:3000]}  # limit context size
```

Pattern scan flagged these lines: {[m.line_number for m in pattern_matches]}

Perform a thorough security review. Return JSON array of findings:
[{{"line": N, "issue": "...", "severity": "...", "description": "...", "recommendation": "..."}}]
If no issues found, return empty array [].
"""
            try:
                response = await self.agent.run_async(prompt)
                agent_findings = self._parse_response(response, file.path)
                findings.extend(agent_findings)
            except Exception as e:
                # Fall back to pattern matches if agent fails
                for match in pattern_matches:
                    findings.append(SecurityFinding(
                        file=file.path,
                        line=match.line_number,
                        issue=match.pattern_name,
                        severity=match.severity,
                        description=f"Detected pattern: {match.line_content}",
                        recommendation="Review this code for security issues."
                    ))
        
        return findings
    
    def _parse_response(self, response: str, file_path: str) -> list[SecurityFinding]:
        """Parse Hermes Agent JSON response into SecurityFinding objects."""
        import json, re
        findings = []
        
        # Extract JSON from response
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if not json_match:
            return []
        
        try:
            data = json.loads(json_match.group())
            for item in data:
                findings.append(SecurityFinding(
                    file=file_path,
                    line=item.get("line", 0),
                    issue=item.get("issue", "Unknown"),
                    severity=item.get("severity", "MEDIUM"),
                    description=item.get("description", ""),
                    recommendation=item.get("recommendation", "")
                ))
        except json.JSONDecodeError:
            pass
        
        return findings
```

> **Note:** Follow the same pattern for `performance_agent.py`, `architecture_agent.py`, and `test_agent.py` — each gets a specialized system prompt and targeted analysis logic.

---

### 6.8 Agents: Performance Agent

**File:** `agents/performance_agent.py`

Key patterns to detect:
```python
PERFORMANCE_PATTERNS = {
    "db_in_loop": (r'for\s+\w+\s+in\s+.*:\s*\n.*\.(filter|get|query|execute)', "HIGH"),
    "sleep_in_async": (r'async\s+def.*:\n.*time\.sleep\(', "MEDIUM"),
    "string_concat_loop": (r'for\s+\w+.*:\s*\n.*\w+\s*\+=\s*["\']', "LOW"),
    "open_without_context": (r'=\s*open\s*\((?!.*with)', "MEDIUM"),
}

# System prompt focus:
"""You are a performance engineering expert. Detect:
- N+1 database query patterns
- Blocking I/O in async contexts
- Memory leaks (unclosed connections, large data in memory)
- Inefficient algorithms (O(n²) where O(n) possible)
- Missing caching for expensive operations"""
```

---

### 6.9 Agents: Architecture Agent

**File:** `agents/architecture_agent.py`

Key analysis:
```python
import ast

def count_methods(source: str) -> int:
    """Count number of methods in a Python file using AST."""
    tree = ast.parse(source)
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            count += 1
    return count

def find_imports(source: str) -> list[str]:
    """Extract all imports using AST."""
    tree = ast.parse(source)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(n.name for n in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports

# System prompt focus:
"""You are a software architect. Identify:
- God classes (>500 lines, >15 methods)
- High coupling between unrelated modules
- Deep inheritance chains (>3 levels)
- Missing abstraction layers
- Violations of Single Responsibility Principle"""
```

---

### 6.10 Agents: Test Agent

**File:** `agents/test_agent.py`

```python
# System prompt focus:
"""You are a QA engineering expert. Analyze code for:
- Public functions/methods with no corresponding tests
- Missing error handling around I/O, network, DB operations
- Bare except clauses that swallow errors
- Missing input validation on public APIs
- Edge cases not covered (empty input, None, large values)
- Missing type hints on public interfaces"""
```

---

### 6.11 Agents: Dependency Agent

**File:** `agents/dependency_agent.py`

```python
from tools.dep_checker import check_python_deps, parse_requirements, query_osv
from pathlib import Path
from dataclasses import dataclass

@dataclass
class DependencyFinding:
    package: str
    version: str
    issue: str
    severity: str
    cve_ids: list[str]
    description: str
    recommendation: str
    category: str = "dependency"

class DependencyAgent:
    async def analyze(self, repo_path: Path) -> list[DependencyFinding]:
        findings = []
        
        # Check Python deps via pip-audit
        vuln_deps = check_python_deps(repo_path)
        for dep in vuln_deps:
            for vuln in dep.get("vulns", []):
                findings.append(DependencyFinding(
                    package=dep["name"],
                    version=dep["version"],
                    issue=vuln.get("id", "Unknown CVE"),
                    severity=self._map_severity(vuln.get("aliases", [])),
                    cve_ids=vuln.get("aliases", []),
                    description=vuln.get("details", ""),
                    recommendation=f"Upgrade {dep['name']} to a patched version."
                ))
        
        return findings
    
    def _map_severity(self, aliases: list) -> str:
        # Map CVE severity from aliases
        for alias in aliases:
            if "CRITICAL" in alias.upper():
                return "CRITICAL"
        return "HIGH"
```

---

### 6.12 Agents: Orchestrator

**File:** `agents/orchestrator.py`

```python
import asyncio
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from tools.file_reader import read_codebase
from agents.security_agent import SecurityAgent
from agents.performance_agent import PerformanceAgent
from agents.architecture_agent import ArchitectureAgent
from agents.test_agent import TestAgent
from agents.dependency_agent import DependencyAgent
from agents.synthesis_agent import SynthesisAgent

console = Console()

class Orchestrator:
    def __init__(self):
        self.security = SecurityAgent()
        self.performance = PerformanceAgent()
        self.architecture = ArchitectureAgent()
        self.test = TestAgent()
        self.dependency = DependencyAgent()
        self.synthesis = SynthesisAgent()
    
    async def audit(self, repo_path: Path) -> dict:
        """Run all agents in parallel, synthesize results."""
        console.print("\n[bold cyan]🛡️  CodeSentinel Starting Audit...[/bold cyan]\n")
        
        # Read all code files
        console.print("[*] Reading codebase...")
        files = read_codebase(repo_path)
        console.print(f"[✓] Found {len(files)} files to analyze\n")
        
        # Run all 5 agents simultaneously
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            tasks = {
                "🔐 Security Analysis": self.security.analyze(files),
                "⚡ Performance Analysis": self.performance.analyze(files),
                "🏗️  Architecture Analysis": self.architecture.analyze(files),
                "🧪 Test Coverage Analysis": self.test.analyze(files),
                "📦 Dependency Analysis": self.dependency.analyze(repo_path),
            }
            
            progress_tasks = {
                name: progress.add_task(name, total=None)
                for name in tasks
            }
            
            # Gather results in parallel
            results = await asyncio.gather(
                *tasks.values(),
                return_exceptions=True  # Don't fail if one agent errors
            )
        
        # Map results back to agent names
        agent_results = {}
        for name, result in zip(tasks.keys(), results):
            if isinstance(result, Exception):
                console.print(f"[yellow]⚠ {name} failed: {result}[/yellow]")
                agent_results[name] = []
            else:
                agent_results[name] = result
        
        # Synthesize all findings
        console.print("\n[*] Synthesizing findings...")
        report = await self.synthesis.synthesize(agent_results)
        
        console.print(f"\n[bold green]✅ Audit Complete![/bold green]")
        console.print(f"   Critical: [red]{report['summary']['critical']}[/red]")
        console.print(f"   High:     [yellow]{report['summary']['high']}[/yellow]")
        console.print(f"   Medium:   [blue]{report['summary']['medium']}[/blue]")
        console.print(f"   Low:      [white]{report['summary']['low']}[/white]\n")
        
        return report
```

---

### 6.13 Agents: Synthesis Agent

**File:** `agents/synthesis_agent.py`

```python
import asyncio
from hermes_agent import HermesAgent
from config import settings
from dataclasses import asdict
import json

class SynthesisAgent:
    """
    Merges findings from all agents, deduplicates, scores, and 
    generates an executive summary.
    """
    
    def __init__(self):
        self.agent = HermesAgent(
            model=settings.hermes_model,
            system_prompt="""You are a principal security engineer writing 
            an executive summary of a code audit. Given findings from multiple 
            specialized agents, produce:
            1. A clear executive summary (3-5 sentences)
            2. Top 3 most critical actions to take
            3. Overall security score (0-100)
            Be direct, actionable, and avoid jargon."""
        )
    
    async def synthesize(self, agent_results: dict) -> dict:
        all_findings = []
        
        for agent_name, findings in agent_results.items():
            for f in findings:
                d = asdict(f) if hasattr(f, '__dataclass_fields__') else f
                all_findings.append(d)
        
        # Deduplicate: same file + same line + same issue
        seen = set()
        unique_findings = []
        for f in all_findings:
            key = (f.get('file', ''), f.get('line', 0), f.get('issue', ''))
            if key not in seen:
                seen.add(key)
                unique_findings.append(f)
        
        # Score by severity
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in unique_findings:
            sev = f.get('severity', 'LOW').upper()
            if sev in severity_counts:
                severity_counts[sev] += 1
        
        # Sort by severity
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
        unique_findings.sort(key=lambda f: severity_order.get(f.get('severity', 'LOW').upper(), 5))
        
        # Get top affected files
        from collections import Counter
        file_counts = Counter(f.get('file', '') for f in unique_findings)
        top_files = [{"file": f, "count": c} for f, c in file_counts.most_common(10)]
        
        # Generate executive summary via Hermes Agent
        summary_prompt = f"""
Code audit findings summary:
- Critical issues: {severity_counts['CRITICAL']}
- High issues: {severity_counts['HIGH']}
- Medium issues: {severity_counts['MEDIUM']}
- Low issues: {severity_counts['LOW']}

Top issues found:
{json.dumps(unique_findings[:10], indent=2)}

Write an executive summary and top 3 recommendations. Return JSON:
{{"executive_summary": "...", "top_recommendations": ["...", "...", "..."], "security_score": N}}
"""
        
        try:
            response = await self.agent.run_async(summary_prompt)
            summary_data = self._parse_json(response)
        except Exception:
            summary_data = {
                "executive_summary": f"Audit found {len(unique_findings)} issues across {severity_counts['CRITICAL']} critical, {severity_counts['HIGH']} high severity categories.",
                "top_recommendations": ["Address all CRITICAL findings immediately", "Review HIGH severity findings this sprint", "Establish security review process"],
                "security_score": max(0, 100 - severity_counts['CRITICAL']*20 - severity_counts['HIGH']*5)
            }
        
        return {
            "summary": severity_counts,
            "findings": unique_findings,
            "top_files": top_files,
            "executive_summary": summary_data.get("executive_summary", ""),
            "top_recommendations": summary_data.get("top_recommendations", []),
            "security_score": summary_data.get("security_score", 50),
            "total_findings": len(unique_findings)
        }
    
    def _parse_json(self, response: str) -> dict:
        import re
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {}
```

---

### 6.14 Output: Markdown Report

**File:** `output/report_md.py`

```python
from pathlib import Path
from datetime import datetime

SEVERITY_EMOJI = {
    "CRITICAL": "🔴",
    "HIGH": "🟠",
    "MEDIUM": "🟡",
    "LOW": "🟢",
    "INFO": "⚪"
}

def generate_markdown(report: dict, repo_name: str, output_path: Path):
    lines = []
    
    # Header
    lines += [
        f"# 🛡️ CodeSentinel Audit Report",
        f"**Repository:** `{repo_name}`  ",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
        f"**Security Score:** {report.get('security_score', 'N/A')}/100",
        "",
        "---",
        "",
        "## 📋 Executive Summary",
        "",
        report.get("executive_summary", "No summary available."),
        "",
        "## 📊 Findings Overview",
        "",
        "| Severity | Count |",
        "|---|---|",
    ]
    
    summary = report.get("summary", {})
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        emoji = SEVERITY_EMOJI[sev]
        count = summary.get(sev, 0)
        lines.append(f"| {emoji} {sev} | {count} |")
    
    lines += [
        "",
        "## 🎯 Top Recommendations",
        "",
    ]
    for i, rec in enumerate(report.get("top_recommendations", []), 1):
        lines.append(f"{i}. {rec}")
    
    lines += ["", "---", "", "## 🔍 Detailed Findings", ""]
    
    current_severity = None
    for finding in report.get("findings", []):
        sev = finding.get("severity", "LOW").upper()
        if sev != current_severity:
            current_severity = sev
            lines += ["", f"### {SEVERITY_EMOJI.get(sev, '')} {sev}", ""]
        
        lines += [
            f"#### {finding.get('issue', 'Unknown Issue')}",
            f"- **File:** `{finding.get('file', 'unknown')}`"
            + (f" (line {finding.get('line')})" if finding.get('line') else ""),
            f"- **Description:** {finding.get('description', '')}",
            f"- **Recommendation:** {finding.get('recommendation', '')}",
            "",
        ]
        
        if finding.get("line_content"):
            lines += [
                "```",
                finding["line_content"],
                "```",
                "",
            ]
    
    output_path.write_text('\n'.join(lines))
    print(f"[✓] Markdown report: {output_path}")
```

---

### 6.15 Output: HTML Report

**File:** `output/report_html.py`

```python
from jinja2 import Template
from pathlib import Path
from datetime import datetime
import json

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CodeSentinel Report — {{ repo_name }}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
  :root {
    --critical: #ff4444; --high: #ff8800;
    --medium: #ffcc00; --low: #44bb44;
    --bg: #0d1117; --surface: #161b22;
    --border: #30363d; --text: #e6edf3;
  }
  body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', sans-serif; margin: 0; }
  .header { background: var(--surface); border-bottom: 1px solid var(--border); padding: 24px 40px; }
  .score { font-size: 48px; font-weight: bold; color: {% if report.security_score > 70 %}var(--low){% elif report.security_score > 40 %}var(--medium){% else %}var(--critical){% endif %}; }
  .container { max-width: 1200px; margin: 0 auto; padding: 24px 40px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 24px; }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
  .CRITICAL { background: var(--critical); color: white; }
  .HIGH { background: var(--high); color: white; }
  .MEDIUM { background: var(--medium); color: black; }
  .LOW { background: var(--low); color: white; }
  .finding { border-left: 3px solid var(--border); padding: 16px; margin: 8px 0; border-radius: 0 8px 8px 0; }
  .finding.CRITICAL { border-color: var(--critical); }
  .finding.HIGH { border-color: var(--high); }
  input[type=search] { width: 100%; padding: 8px 12px; background: var(--bg); border: 1px solid var(--border); color: var(--text); border-radius: 4px; margin-bottom: 16px; }
</style>
</head>
<body>
<div class="header">
  <h1>🛡️ CodeSentinel</h1>
  <p>{{ repo_name }} &middot; {{ date }}</p>
  <div class="score">{{ report.security_score }}/100</div>
</div>
<div class="container">
  <div class="grid">
    <div class="card">
      <h3>Findings by Severity</h3>
      <canvas id="severityChart" height="200"></canvas>
    </div>
    <div class="card">
      <h3>Executive Summary</h3>
      <p>{{ report.executive_summary }}</p>
      <h4>Top Recommendations</h4>
      <ol>{% for rec in report.top_recommendations %}<li>{{ rec }}</li>{% endfor %}</ol>
    </div>
  </div>
  <div class="card" style="margin-top:24px">
    <h3>All Findings ({{ report.total_findings }})</h3>
    <input type="search" id="search" placeholder="Search findings..." oninput="filterFindings(this.value)">
    <div id="findings">
    {% for f in report.findings %}
    <div class="finding {{ f.severity }}" data-text="{{ f.issue }} {{ f.file }} {{ f.description }}">
      <span class="badge {{ f.severity }}">{{ f.severity }}</span>
      <strong style="margin-left:8px">{{ f.issue }}</strong>
      <span style="color:#8b949e; margin-left:8px">{{ f.file }}{% if f.line %} :{{ f.line }}{% endif %}</span>
      <p style="margin:8px 0">{{ f.description }}</p>
      <p style="color:#8b949e">💡 {{ f.recommendation }}</p>
    </div>
    {% endfor %}
    </div>
  </div>
</div>
<script>
hljs.highlightAll();
new Chart(document.getElementById('severityChart'), {
  type: 'doughnut',
  data: {
    labels: ['Critical', 'High', 'Medium', 'Low'],
    datasets: [{
      data: [{{ report.summary.CRITICAL }}, {{ report.summary.HIGH }}, {{ report.summary.MEDIUM }}, {{ report.summary.LOW }}],
      backgroundColor: ['#ff4444','#ff8800','#ffcc00','#44bb44']
    }]
  },
  options: { plugins: { legend: { labels: { color: '#e6edf3' } } } }
});
function filterFindings(q) {
  document.querySelectorAll('.finding').forEach(el => {
    el.style.display = el.dataset.text.toLowerCase().includes(q.toLowerCase()) ? '' : 'none';
  });
}
</script>
</body>
</html>
"""

def generate_html(report: dict, repo_name: str, output_path: Path):
    template = Template(HTML_TEMPLATE)
    html = template.render(
        report=report,
        repo_name=repo_name,
        date=datetime.now().strftime('%Y-%m-%d %H:%M')
    )
    output_path.write_text(html)
    print(f"[✓] HTML report: {output_path}")
```

---

### 6.16 Output: JSON Report

**File:** `output/report_json.py`

```python
from pathlib import Path
import json

def generate_json(report: dict, output_path: Path):
    """Write machine-readable JSON for CI/CD pipelines."""
    output_path.write_text(json.dumps(report, indent=2))
    print(f"[✓] JSON report: {output_path}")
```

**Concrete JSON schema (draft):**

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "CodeSentinel Report",
    "type": "object",
    "required": [
        "summary",
        "findings",
        "top_files",
        "executive_summary",
        "top_recommendations",
        "security_score",
        "total_findings"
    ],
    "properties": {
        "summary": {
            "type": "object",
            "required": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"],
            "properties": {
                "CRITICAL": {"type": "integer", "minimum": 0},
                "HIGH": {"type": "integer", "minimum": 0},
                "MEDIUM": {"type": "integer", "minimum": 0},
                "LOW": {"type": "integer", "minimum": 0},
                "INFO": {"type": "integer", "minimum": 0}
            },
            "additionalProperties": false
        },
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["file", "line", "issue", "severity", "description", "recommendation"],
                "properties": {
                    "file": {"type": "string"},
                    "line": {"type": "integer", "minimum": 0},
                    "issue": {"type": "string"},
                    "severity": {
                        "type": "string",
                        "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
                    },
                    "description": {"type": "string"},
                    "recommendation": {"type": "string"},
                    "category": {"type": "string"},
                    "line_content": {"type": "string"}
                },
                "additionalProperties": true
            }
        },
        "top_files": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["file", "count"],
                "properties": {
                    "file": {"type": "string"},
                    "count": {"type": "integer", "minimum": 0}
                },
                "additionalProperties": false
            }
        },
        "executive_summary": {"type": "string"},
        "top_recommendations": {
            "type": "array",
            "items": {"type": "string"}
        },
        "security_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "total_findings": {"type": "integer", "minimum": 0}
    },
    "additionalProperties": true
}
```

---

### 6.17 main.py CLI

**File:** `main.py`

```python
import typer
import asyncio
from pathlib import Path
from rich.console import Console
from agents.orchestrator import Orchestrator
from input.github_fetcher import fetch_github_repo, cleanup
from input.local_loader import load_local
from output.report_md import generate_markdown
from output.report_html import generate_html
from output.report_json import generate_json
from config import settings
import os

app = typer.Typer(help="🛡️  CodeSentinel — Multi-Agent Code Security Audit")
console = Console()

@app.command()
def audit(
    github: str = typer.Option(None, help="GitHub repository URL"),
    local: str = typer.Option(None, help="Local path or ZIP file"),
    output: str = typer.Option("./reports", help="Output directory"),
    json: str = typer.Option(None, help="Write JSON report to this path"),
    fail_on: str = typer.Option(None, help="Exit non-zero on severity: critical/high/medium/low"),
    verbose: bool = typer.Option(False, help="Verbose output"),
):
    """Run a full security audit on a codebase."""
    
    if not github and not local:
        console.print("[red]Error: Provide --github or --local[/red]")
        raise typer.Exit(1)
    
    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load codebase
    tmp_path = None
    try:
        if github:
            repo_name = github.rstrip('/').split('/')[-1]
            repo_path = fetch_github_repo(github)
            tmp_path = repo_path
        else:
            repo_path = load_local(local)
            repo_name = Path(local).stem
        
        # Run audit
        orchestrator = Orchestrator()
        report = asyncio.run(orchestrator.audit(repo_path))
        
        # Generate reports
        md_path = output_dir / f"{repo_name}_audit.md"
        html_path = output_dir / f"{repo_name}_audit.html"
        
        generate_markdown(report, repo_name, md_path)
        generate_html(report, repo_name, html_path)
        if json:
            generate_json(report, Path(json))
        
        console.print(f"\n[bold]Reports saved to:[/bold]")
        console.print(f"  📄 {md_path}")
        console.print(f"  🌐 {html_path}")
        if json:
            console.print(f"  🧾 {json}")

        if fail_on:
            order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            threshold = order.get(fail_on.lower())
            if threshold is None:
                raise typer.Exit(2)
            summary = report.get("summary", {})
            if any(summary.get(k.upper(), 0) > 0 for k, v in order.items() if v <= threshold):
                raise typer.Exit(1)
    
    finally:
        if tmp_path:
            cleanup(tmp_path)

if __name__ == "__main__":
    app()
```

---

## 7. Hermes Agent Integration Guide

### Installation

```bash
# Install Hermes Agent (check latest docs)
pip install hermes-agent

# Or run locally via Ollama
ollama pull nous-hermes-3

# Set environment
cp .env.example .env
# Edit .env with your Hermes Agent endpoint
```

### Key Integration Points

Hermes Agent is used in **3 critical ways** in CodeSentinel:

1. **Specialized System Prompts** — each agent gets a domain-expert persona (security engineer, performance engineer, etc.) that shapes how Hermes Agent reasons about the code.

2. **Tool Use** — agents use file reading and pattern scanning as tools that Hermes Agent can call and reason about. This is Hermes Agent's strongest capability.

3. **Multi-step Reasoning** — the synthesis agent uses Hermes Agent's planning capability to reason across all findings and produce a coherent executive summary.

### Adapting to Hermes Agent's actual API

Check `https://hermes-agent.nousresearch.com/docs/` for exact API syntax. The core pattern:

```python
from hermes_agent import HermesAgent

agent = HermesAgent(model="hermes-3-llama-3.1-70b")
response = await agent.run_async(
    prompt="Analyze this code for security issues: ...",
    tools=[file_reader_tool, pattern_scanner_tool]
)
```

---

## 8. Sample Output

### Terminal Output
```
🛡️  CodeSentinel Starting Audit...

[*] Reading codebase...
[✓] Found 47 files to analyze

⠿ 🔐 Security Analysis
⠿ ⚡ Performance Analysis
⠿ 🏗️  Architecture Analysis
⠿ 🧪 Test Coverage Analysis
⠿ 📦 Dependency Analysis

[*] Synthesizing findings...

✅ Audit Complete!
   Critical: 3
   High:     12
   Medium:   8
   Low:      5

Reports saved to:
  📄 ./reports/myapp_audit.md
  🌐 ./reports/myapp_audit.html
```

### Markdown Report Preview
```markdown
# 🛡️ CodeSentinel Audit Report
**Repository:** `myapp` | **Score:** 42/100

## Executive Summary
The codebase contains 3 critical vulnerabilities including hardcoded 
AWS credentials and SQL injection risks in the user authentication module...

## Findings Overview
| Severity | Count |
|---|---|
| 🔴 CRITICAL | 3 |
| 🟠 HIGH | 12 |
...

### 🔴 CRITICAL
#### Hardcoded AWS Access Key
- **File:** `config/aws.py` (line 14)
- **Description:** AWS access key found hardcoded in source code
- **Recommendation:** Move to environment variables using os.getenv()
```

---

## 9. Testing Strategy

### Unit Tests

```bash
# Test individual agents
python -m pytest tests/test_security_agent.py -v
python -m pytest tests/test_orchestrator.py -v
```

### Integration Tests with Sample Repos

Use these intentionally vulnerable repos to validate findings:

1. **DVWA** (PHP): `https://github.com/digininja/DVWA`
2. **WebGoat** (Java): `https://github.com/WebGoat/WebGoat`  
3. **Juice Shop** (Node.js): `https://github.com/juice-shop/juice-shop`
4. **pygoat** (Python): `https://github.com/adeyosemanputra/pygoat`

```bash
# Test against a known vulnerable repo
python main.py --github https://github.com/adeyosemanputra/pygoat --output ./test-reports
```

Expected: Security agent should catch SQLi, hardcoded secrets, and broken auth in these repos.

### Validation Checklist
- [ ] GitHub URL input clones and cleans up correctly
- [ ] Local path and ZIP both load correctly
- [ ] All 5 agents return results without crashing
- [ ] Orchestrator handles one agent failure gracefully
- [ ] Synthesis deduplicates correctly
- [ ] Markdown report renders in GitHub
- [ ] HTML dashboard loads in browser with charts working
- [ ] CLI `--help` shows correctly

---

## 10. Security & Privacy Considerations

- **Data disclosure:** clearly document what code is sent to Hermes Agent, and allow `--offline` or `--local-only` mode to skip remote calls.
- **Secret redaction:** mask tokens, API keys, and credentials before sending snippets to the LLM; store redaction events in the report.
- **Least-data mode:** optionally send only small chunks around suspicious lines rather than full files.
- **Temp cleanup:** always delete cloned repos and extracted ZIPs on success or failure.
- **User consent:** add a one-line confirmation in CLI on first run if remote analysis is enabled.

---

## 11. CI/CD & Automation

- **Machine-readable output:** always support `--json` and stable JSON schema for CI parsing.
- **Severity gates:** `--fail-on high` style thresholds for CI pipelines.
- **GitHub Actions example:** run on PRs and upload reports as artifacts.
- **Exit codes:** 0 = pass, 1 = findings at or above threshold, 2 = bad configuration.

Minimal CI workflow example:
```yaml
name: codesentinel
on:
    pull_request:
    push:
        branches: [main]
jobs:
    audit:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4
            - uses: actions/setup-python@v5
                with:
                    python-version: "3.11"
            - run: pip install codesentinel
            - run: codesentinel --local . --json ./reports/audit.json --fail-on high
            - uses: actions/upload-artifact@v4
                with:
                    name: codesentinel-reports
                    path: ./reports
```

---

## 12. Packaging & Release

- **pyproject.toml:** define `codesentinel` console entrypoint and build metadata.
- **Versioning:** Semantic Versioning with CHANGELOG.md updates.
- **Licensing:** add LICENSE and clarify third-party data sources.
- **Dev tooling:** `pytest`, `ruff`, `mypy`, and `pre-commit` for consistent quality.

---

## 13. Operational Limits & Ignore Rules

- **Ignore files:** support `.gitignore` + `.codesentinelignore` with `pathspec`.
- **Include/exclude globs:** CLI flags for narrowing scope.
- **Resource caps:** file count, size limits, per-agent timeouts, and overall time budget.
- **Rate limits:** OSV and API calls should back off and cache results locally.

Minimal ignore file example:
```
# Ignore dependency folders
node_modules/
vendor/

# Build outputs
dist/
build/

# Python virtualenv and cache
.venv/
venv/
__pycache__/

# Minified or generated assets
*.min.js
*.map

# Report outputs
reports/
codesentinel-reports/
```

---

## 14. DEV.to Submission Guide

Use this template for your DEV.to post:

```markdown
*This is a submission for the Hermes Agent Challenge*

## What I Built

**CodeSentinel** — a multi-agent code security audit system powered by Hermes Agent.
Point it at any GitHub repo or local codebase and it deploys 5 specialized AI agents
in parallel to find security vulnerabilities, performance issues, architectural 
problems, test coverage gaps, and dependency CVEs.

## Demo
[Embed Loom video here]
[Add screenshots of HTML dashboard]

## Code
[GitHub repo link]

### Tech Stack
- Python, asyncio
- Hermes Agent (Nous Research)
- GitPython, Jinja2, Typer, Rich
- OSV API, pip-audit
- Chart.js, highlight.js

## How I Used Hermes Agent

CodeSentinel uses Hermes Agent in three distinct ways:

**1. Specialized Expert Agents** — Each of the 5 agents is powered by Hermes Agent
with a domain-specific system prompt (security engineer, performance expert, etc.).
Hermes Agent's instruction-following and reasoning capabilities let each agent think 
like a human expert in that domain.

**2. Tool Use for Code Analysis** — Agents use Hermes Agent's tool-calling to 
invoke file readers and pattern scanners, then reason about the results in context.
This goes beyond simple regex — Hermes Agent understands whether a pattern is 
actually exploitable given the surrounding code.

**3. Multi-step Synthesis** — The final synthesis agent uses Hermes Agent's 
planning capability to reason across hundreds of findings, deduplicate overlapping
issues, and produce a coherent executive summary with prioritized recommendations.
```

---

## 15. Judging Criteria Checklist

| Criteria | How CodeSentinel Nails It |
|---|---|
| ✅ Effective use of Hermes Agent | 6 separate Hermes Agent instances, tool use, multi-step reasoning |
| ✅ Technical implementation | asyncio parallelism, AST analysis, CVE API, clean architecture |
| ✅ Creativity & originality | Multi-agent pattern for security auditing is novel |
| ✅ Usability & UX | One-command CLI, beautiful HTML dashboard, clear findings |

### Bonus Points
- [ ] Add a GitHub Action so people can use it in CI/CD
- [ ] Add support for JavaScript/Node.js CVE checking (via `npm audit`)
- [ ] Record a demo showing it catch a real CVE in a popular open source project
- [ ] Write a companion "Write About" submission explaining the multi-agent architecture

---

*Built for the [Hermes Agent Challenge](https://dev.to/challenges/hermes-agent-2026-05-15) — May 2026*
*Good luck! 🚀*
