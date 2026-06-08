from github_ai_genius.analyzer import detect_package_managers, infer_entrypoints
from github_ai_genius.models import RepoFile, RepositoryRef


def test_repository_ref_parses_url():
    ref = RepositoryRef.parse('https://github.com/GAN-007/github-ai-genius.git')
    assert ref.full_name == 'GAN-007/github-ai-genius'


def test_package_manager_detection():
    files = [RepoFile(path='pyproject.toml', sha='a', size=10), RepoFile(path='go.mod', sha='b', size=10)]
    assert detect_package_managers(files) == ['python-build-system', 'go']


def test_entrypoint_inference():
    files = [RepoFile(path='manage.py', sha='a', size=10), RepoFile(path='src/App.tsx', sha='b', size=10)]
    assert infer_entrypoints(files) == ['manage.py', 'src/App.tsx']
