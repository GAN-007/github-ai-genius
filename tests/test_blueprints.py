from pathlib import Path

from github_ai_genius.blueprints import StackBlueprints
from github_ai_genius.quality import QualityGate


def test_fastapi_blueprint_generates_quality_project(tmp_path: Path):
    result = StackBlueprints().create_fastapi_service(tmp_path, 'service')
    assert (result.root / 'app' / 'main.py').exists()
    assert QualityGate().inspect_project(result.root).passed is True


def test_react_blueprint_generates_expected_files(tmp_path: Path):
    result = StackBlueprints().create_react_vite_app(tmp_path, 'web')
    assert (result.root / 'package.json').exists()
    assert (result.root / 'src' / 'App.tsx').exists()
