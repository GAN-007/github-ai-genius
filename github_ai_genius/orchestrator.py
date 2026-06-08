from __future__ import annotations

from pathlib import Path

from .analyzer import RepositoryAnalyzer
from .config import Settings
from .generator import ProjectGenerator
from .github_client import GitHubClient
from .llm import OllamaClient
from .models import AgentResult, AgentTask, TaskIntent
from .policy import evaluate_instruction, evaluate_license_for_reuse


class GeniusOrchestrator:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.github = GitHubClient(settings)
        self.analyzer = RepositoryAnalyzer(self.github)
        self.llm = OllamaClient(settings)
        self.generator = ProjectGenerator()

    async def execute(self, task: AgentTask) -> AgentResult:
        decision = evaluate_instruction(task.instruction, self.settings.allow_security_exploit_generation)
        if not decision.allowed:
            return AgentResult(False, 'Task blocked by policy', findings=decision.findings)
        if task.intent == TaskIntent.ANALYZE:
            return await self._analyze(task)
        if task.intent == TaskIntent.BUILD:
            return await self._build(task)
        if task.intent == TaskIntent.TRANSFORM:
            return await self._plan_transform(task)
        return AgentResult(False, 'Unsupported task intent')

    async def _analyze(self, task: AgentTask) -> AgentResult:
        if task.repository is None:
            return AgentResult(False, 'Repository is required')
        report = await self.analyzer.analyze(task.repository)
        return AgentResult(True, 'Repository analysis complete', {'analysis': report}, report.findings)

    async def _build(self, task: AgentTask) -> AgentResult:
        if task.target_stack == 'django-marketplace':
            generated = self.generator.create_django_marketplace(task.output_path or Path('generated'))
            return AgentResult(True, 'Project generated', {'root': str(generated.root), 'files': [str(path) for path in generated.files]})
        response = await self.llm.generate(self._build_prompt(task.instruction))
        return AgentResult(True, 'Build plan generated', {'response': response})

    async def _plan_transform(self, task: AgentTask) -> AgentResult:
        if task.repository is None:
            return AgentResult(False, 'Repository is required')
        report = await self.analyzer.analyze(task.repository)
        license_decision = evaluate_license_for_reuse(report.license_name, self.settings.allow_incompatible_license_copy)
        prompt = self._transform_prompt(task.instruction, report.repository, license_decision.allowed)
        response = await self.llm.generate(prompt)
        return AgentResult(True, 'Transformation plan generated', {'analysis': report, 'response': response}, [*report.findings, *license_decision.findings])

    def _build_prompt(self, instruction: str) -> str:
        return 'Create a complete original production-grade software build plan with file tree, validation commands, and rollout notes. Instruction: ' + instruction

    def _transform_prompt(self, instruction: str, repository: str, direct_reuse_allowed: bool) -> str:
        mode = 'direct improvements allowed where compatible' if direct_reuse_allowed else 'clean-room strategy required'
        return 'Repository: ' + repository + '\nMode: ' + mode + '\nInstruction: ' + instruction + '\nReturn exact steps, changed files, tests, and deployment notes.'
