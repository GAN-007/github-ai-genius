from github_ai_genius.gap_detector import GapDetector
from github_ai_genius.models import RepositoryAnalysis


def test_gap_detector_flags_missing_basics():
    analysis = RepositoryAnalysis(repository='owner/repo', default_branch='main', files_scanned=1, total_bytes=10, languages={}, frameworks=[], package_managers=[], entrypoints=[], test_commands=[])
    gaps = GapDetector().detect(analysis)
    codes = {gap.code for gap in gaps}
    assert 'tests.missing' in codes
    assert 'entrypoint.missing' in codes
    assert 'license.missing' in codes
