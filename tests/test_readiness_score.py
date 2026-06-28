from github_ai_genius.models import RepositoryAnalysis
from github_ai_genius.readiness_score import ScoreEngine


def test_score_engine_reports_complete_repository():
    analysis = RepositoryAnalysis(
        repository='owner/repo',
        default_branch='main',
        files_scanned=20,
        total_bytes=1000,
        languages={'Python': 1000},
        frameworks=['FastAPI', 'Docker'],
        package_managers=['python-build-system'],
        entrypoints=['main.py'],
        test_commands=['pytest'],
        license_name='MIT',
    )
    report = ScoreEngine().evaluate(analysis)
    assert report.foundation >= 90
    assert report.production >= 90
