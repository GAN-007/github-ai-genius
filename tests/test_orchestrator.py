from github_ai_genius.config import Settings
from github_ai_genius.orchestrator import GeniusOrchestrator


def test_orchestrator_initializes(tmp_path):
    orchestrator = GeniusOrchestrator(Settings(GENIUS_WORKSPACE_DIR=tmp_path))
    assert orchestrator.settings is not None
    assert orchestrator.state is not None


def test_prompt_helpers_include_context(tmp_path):
    orchestrator = GeniusOrchestrator(Settings(GENIUS_WORKSPACE_DIR=tmp_path))
    assert 'inventory' in orchestrator._build_prompt('inventory')
    assert 'owner/repo' in orchestrator._transform_prompt('improve', 'owner/repo', False)
