from pathlib import Path

from github_ai_genius.generator import ProjectGenerator
from github_ai_genius.quality import QualityGate


def test_django_marketplace_generator_writes_expected_files(tmp_path: Path):
    generated = ProjectGenerator().create_django_marketplace(tmp_path, 'marketplace')
    paths = {path.relative_to(generated.root).as_posix() for path in generated.files}
    assert 'README.md' in paths
    assert 'manage.py' in paths
    assert 'marketplace/settings.py' in paths
    assert 'accounts/models.py' in paths
    assert 'listings/models.py' in paths
    assert 'bookings/models.py' in paths
    assert 'payments/models.py' in paths
    assert 'accounts/admin.py' in paths
    assert 'listings/serializers.py' in paths
    assert 'bookings/views.py' in paths
    assert 'payments/views.py' in paths
    assert (generated.root / 'payments' / 'services.py').exists()


def test_django_marketplace_generator_passes_quality_gate(tmp_path: Path):
    generated = ProjectGenerator().create_django_marketplace(tmp_path, 'marketplace')
    assert QualityGate().inspect_project(generated.root).passed is True
