from github_ai_genius.models import RepositoryAnalysis
from github_ai_genius.readiness_score import ScoreEngine


def complete_analysis() -> RepositoryAnalysis:
    return RepositoryAnalysis(
        repository='owner/repo',
        default_branch='main',
        files_scanned=20,
        total_bytes=1000,
        languages={'Python': 1000},
        frameworks=['FastAPI', 'Docker', 'GitHub Actions'],
        package_managers=['python-build-system'],
        entrypoints=['main.py'],
        test_commands=['pytest'],
        license_name='MIT',
    )


def test_score_engine_requires_release_evidence_for_production():
    report = ScoreEngine().evaluate(complete_analysis())
    assert report.foundation >= 90
    assert report.production < 90


def test_score_engine_reports_complete_repository_with_green_release_evidence():
    report = ScoreEngine().evaluate(complete_analysis(), release_passed=True, release_seen=True)
    assert report.foundation >= 90
    assert report.production >= 90
