import pytest

from appsvc_profiler.helpers import is_like_false, is_like_true

@pytest.mark.parametrize(
    "input,expected_result",
    [
        pytest.param(None, False),
        pytest.param(0, False),
        pytest.param(1, True),
        pytest.param("true", True),
        pytest.param("True", True),
        pytest.param("anytext", False),
    ]
    )
def test_is_like_true(input, expected_result):
    assert is_like_true(input) == expected_result
    
@pytest.mark.parametrize(
    "input,expected_result",
    [
        pytest.param(None, False),
        pytest.param(0, True),
        pytest.param(1, False),
        pytest.param("false", True),
        pytest.param("False", True),
        pytest.param("anytext", False),
    ]
    )
def test_is_like_false(input, expected_result):
    assert is_like_false(input) == expected_result