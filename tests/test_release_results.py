from pathlib import Path

from github_ai_genius.release_results import ReleaseReport, ReleaseResult, load_release_report, write_release_report


def test_release_report_pass_rate():
    report = ReleaseReport((ReleaseResult('unit', True, 'ok'), ReleaseResult('lint', False, 'no'),))
    assert report.passed is False
    assert report.pass_rate == 50


def test_release_report_roundtrip(tmp_path: Path):
    path = tmp_path / 'release.json'
    report = ReleaseReport((ReleaseResult('unit', True, 'ok'),))
    write_release_report(path, report)
    loaded = load_release_report(path)
    assert loaded.passed is True
    assert loaded.results[0].name == 'unit'
