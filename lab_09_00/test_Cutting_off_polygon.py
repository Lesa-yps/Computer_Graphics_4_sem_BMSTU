import pytest
from typing import Tuple, List
# Tесты для функций
from Cutting_off_polygon import fact_cross, visible, find_cross, is_convex, sign

# подпрограмма определения факта пересечения ребра многоугольника состороной окна
# fact_cross


@pytest.mark.parametrize(
    "start, end, W1, W2, res",
    [
        pytest.param((0, 1), (1, 0), (0, 0), (1, 1), True, id="first_test"),
    ]
)
def test_fact_cross(start: Tuple[int], end: Tuple[int], W1: Tuple[int], W2: Tuple[int], res: bool) -> None:
    assert fact_cross(start, end, W1, W2) == res

# подпрограмма определения видимости точки
# видимость point следует определить относительно стороны P1P2
# вернёт значение меньшее нуля, если point невидима, равное нулю, если лежит на стороне P1P2, больше нуля - видима
# в этой подпрограмме используется вычисление векторного произведения
# visible


@pytest.mark.parametrize(
    "point, P1, P2, res",
    [
        pytest.param((1, 1), (0, 0), (0, 1), 1, id="visible"),
        pytest.param((-1, 1), (0, 0), (0, 1), -1, id="invisible"),
    ]
)
def test_visible(point: Tuple[int], P1: Tuple[int], P2: Tuple[int], res: int) -> None:
    assert visible(point, P1, P2) == res


# подпрограмма вычисления точки пересечения двух отрезков
# find_cross


@pytest.mark.parametrize(
    "P1, P2, W1, W2, res",
    [
        pytest.param((0, 1), (1, 0), (0, 0), (1, 1),
                     (0.5, 0.5), id="center_cross"),
    ]
)
def test_find_cross(P1: Tuple[int], P2: Tuple[int], W1: Tuple[int], W2: Tuple[int], res: Tuple[float]) -> None:
    assert find_cross(P1, P2, W1, W2) == res


# проверка отсекателя на выпуклость + второй возвращаемый параметр показывает в какую сторону шёл обход
# (по часовой - меньше нуля, против часовой - больше нуля)
# is_convex

@pytest.mark.parametrize(
    "figure, res",
    [
        pytest.param([(0, 0), (1, 0), (1, 1), (0, 1)],
                     (True, 1), id="convex_clockwise"),
    ]
)
def test_is_convex(figure: List[Tuple[int]], res: Tuple[bool, int]) -> None:
    assert is_convex(figure) == res

# определяет знак числа
# sign


@pytest.mark.parametrize(
    "x, res",
    [
        pytest.param(1, 1, id="positive"),
    ]
)
def test_sign(x: float, res: int) -> None:
    assert sign(x) == res
