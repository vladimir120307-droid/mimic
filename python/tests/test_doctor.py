from mimic.doctor import run_all


def test_doctor_returns_checks():
    results = run_all()
    assert len(results) > 0
    names = {r.name for r in results}
    assert "Python version" in names
    assert "Python packages" in names


def test_each_check_has_valid_status():
    for r in run_all():
        assert r.status in {"ok", "warn", "fail"}
        assert r.name
        assert r.detail
