from github_ai_genius.request_controls import SlidingWindow, request_id


def test_request_id_reuses_existing_value():
    assert request_id('abc') == 'abc'


def test_request_id_generates_value():
    assert len(request_id()) >= 16


def test_sliding_window_blocks_after_limit():
    window = SlidingWindow(limit=1, seconds=60)
    assert window.check('client').allowed is True
    decision = window.check('client')
    assert decision.allowed is False
    assert decision.retry_after_seconds >= 1
