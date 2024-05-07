import pytest
from typing import Tuple
# Tесты для функций
from Cutting_off_lines_any_convex import scal_mul, find_norm, Param_func

# скалярное умножение векторов
# scal_mul


@pytest.mark.parametrize(
    "P1, P2, res",
    [
        pytest.param((1, 0), (0, 1), 0, id="zero"),
        pytest.param((-1, 0), (1, 0), -1, id="neg"),
        pytest.param((0, 1), (0, 1), 1, id="pos")
    ]
)
def test_scal_mul(P1: Tuple[int], P2: Tuple[int], res: int) -> None:
    assert scal_mul(P1, P2) == res

# ищет вектор нормали к отрезку
# find_norm


@pytest.mark.parametrize(
    "P1, P2, P3, P_norm",
    [
        pytest.param((1, 0), (0, 0), (0, 1), (0, 1), id="high"),
        pytest.param((0, 1), (0, 0), (1, 0), (1, 0), id="right"),
        pytest.param((1, 1), (1, 0), (0, 0), (-1, 0), id="left")
    ]
)
def test_find_norm(P1: Tuple[int], P2: Tuple[int], P3: Tuple[int], P_norm: Tuple[float]) -> None:
    assert find_norm(P1, P2, P3) == P_norm

# параметрическое уравнение
# Param_func


@pytest.mark.parametrize(
    "t, P1, P2, res",
    [
        pytest.param(0, (0, 0), (1, 1), (0, 0), id="start"),
        pytest.param(1, (0, 0), (1, 1), (1, 1), id="end"),
        pytest.param(1/2, (0, 0), (1, 1), (1/2, 1/2), id="middle")
    ]
)
def test_Param_func(t: float, P1: Tuple[int], P2: Tuple[int], res: Tuple[float]) -> None:
    assert Param_func(t, P1, P2) == res
