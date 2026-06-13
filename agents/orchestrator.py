import asyncio
from pathlib import Path
from typing import List

from agents.architecture_agent import ArchitectureAgent
from agents.dependency_agent import DependencyAgent
from agents.performance_agent import PerformanceAgent
from agents.security_agent import SecurityAgent
from agents.synthesis_agent import SynthesisAgent
from agents.test_agent import TestAgent
from tools.file_reader import read_codebase
from tools.hermes_client import HermesClient


class Orchestrator:
    def __init__(self, hermes_client: HermesClient) -> None:
        self.security = SecurityAgent(hermes_client)
        self.performance = PerformanceAgent()
        self.architecture = ArchitectureAgent()
        self.test = TestAgent()
        self.dependency = DependencyAgent()
        self.synthesis = SynthesisAgent()

    async def audit(
        self,
        repo_path: Path,
        include_globs: List[str],
        exclude_globs: List[str],
        respect_gitignore: bool,
    ) -> dict:
        files = read_codebase(
            repo_path,
            include_globs=include_globs,
            exclude_globs=exclude_globs,
            respect_gitignore=respect_gitignore,
        )

        tasks = [
            self.security.analyze(files),
            self.performance.analyze(files),
            self.architecture.analyze(files),
            self.test.analyze(files),
            self.dependency.analyze(repo_path),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        agent_results = {}
        names = ["security", "performance", "architecture", "test", "dependency"]

        for name, result in zip(names, results):
            if isinstance(result, Exception):
                agent_results[name] = []
            else:
                agent_results[name] = result

        return await self.synthesis.synthesize(agent_results)
