from github_ai_genius.models import RepositoryAnalysis
from github_ai_genius.multirepo import MultiRepoSynthesizer
from github_ai_genius.rebuilder import RebuildPlanner


def analysis(repository, frameworks):
    return RepositoryAnalysis(repository=repository, default_branch='main', files_scanned=10, total_bytes=100, languages={'Python': 100}, frameworks=frameworks, package_managers=['python-build-system'], entrypoints=['main.py'], test_commands=['python -m pytest'], license_name='MIT')


def test_multirepo_synthesis_combines_frameworks():
    result = MultiRepoSynthesizer().synthesize([analysis('a/api', ['FastAPI']), analysis('b/web', ['React'])])
    assert 'FastAPI' in result.combined_frameworks
    assert 'React' in result.combined_frameworks
    assert result.integration_strategy


def test_rebuild_planner_creates_steps():
    plan = RebuildPlanner().plan_single(analysis('a/api', ['FastAPI']), 'improve reliability')
    assert plan.steps
    assert 'a/api' in plan.title
