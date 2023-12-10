import pytest
from modules.LinearComparison import LinearComparison


@pytest.fixture
def linear_comparison():
    return LinearComparison()


def test_update(linear_comparison):
    m, a, c, x, n = 10, 2, 3, 4, 5
    linear_comparison.update(m, a, c, x, n)
    assert linear_comparison.m == m
    assert linear_comparison.a == a
    assert linear_comparison.c == c
    assert linear_comparison.x == x
    assert linear_comparison.n == n


def test_gen_list(linear_comparison):
    linear_comparison.update(10, 2, 3, 4, 5)
    result = linear_comparison.gen_list()
    assert len(result) == 5


def test_find_period(linear_comparison):
    linear_comparison.update(10, 2, 3, 4, 10)
    linear_comparison.gen_list()
    period = linear_comparison.find_period()
    assert period == 4


def test_find_period_no_result(linear_comparison):
    period = linear_comparison.find_period()
    assert period == 1
