from github_ai_genius.config import Settings
from github_ai_genius.orchestrator import GeniusOrchestrator


def test_orchestrator_initializes():
    orchestrator = GeniusOrchestrator(Settings())
    assert orchestrator.settings is not None


def test_prompt_helpers_include_context():
    orchestrator = GeniusOrchestrator(Settings())
    assert 'inventory' in orchestrator._build_prompt('inventory')
    assert 'owner/repo' in orchestrator._transform_prompt('improve', 'owner/repo', False)
