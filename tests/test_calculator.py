import pytest
from app.agent.tools import calculator

def test_calculator():
    assert calculator("(50 - 45) / 45 * 100") == pytest.approx(11.111111, rel=1e-5)

def test_calculator_rejects_code():
    with pytest.raises(ValueError):
        calculator("__import__('os').system('echo unsafe')")
