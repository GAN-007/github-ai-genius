from github_ai_genius.policy import evaluate_license_for_reuse


def test_permissive_license_allows_reuse():
    assert evaluate_license_for_reuse('MIT').allowed is True


def test_missing_license_blocks_copying():
    decision = evaluate_license_for_reuse(None)
    assert decision.allowed is False
    assert decision.reason == 'missing_license'
