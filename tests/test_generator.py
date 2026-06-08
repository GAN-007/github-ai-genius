from pathlib import Path

from github_ai_genius.generator import ProjectGenerator


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
    assert (generated.root / 'payments' / 'services.py').exists()
