import pytest
# Tесты для функций
from Mozg_01 import same_num, same_turple, check_points, find_bisector_intersection, angle_bisector_median


# сравнивает вещественные числа (одинаковые -> 1, разные -> 0)  с погрешностью 0.0001
# same_num
def test_same_num() -> None:
    # оба положительные одинаковые
    assert same_num(1.0, 1.0) == 1
    # оба отрицательные одинаковые
    assert same_num(-1.11, -1.11) == 1
    # почти одинаковые с очень маленькой погрешностью
    assert same_num(1.0, 1.00001) == 1
    # по модулю одинаковые, но разных знаков
    assert same_num(1.0, -1.0) == 0
    # разные
    assert same_num(1.0, 2.0) == 0


# сравнивает кортежи вещественных чисел (все части кортежа одинаковые -> 1,
# хоть 1 отличается -> 0) с погрешностью 0.0001
# same_turple
def test_same_turple() -> None:
    # оба положительные одинаковые
    assert same_turple((1, 2), (1, 2)) == 1
    # оба отрицательные одинаковые
    assert same_turple((-1, -2), (-1, -2)) == 1
    # почти одинаковые с очень маленькой погрешностью
    assert same_turple((1.0, 2.0), (1.0, 2.00001)) == 1
    # x1 == y2 и x2 == y1
    assert same_turple((1, 2), (2, 1)) == 0
    # разные
    assert same_turple((1.0, 2.0), (2.0, 3.0)) == 0
    # почти одинаковые с недостаточно маленькой погрешностью
    assert same_turple((1, 2), (1, 2.001)) == 0


# проверка что треугольник не линия (не линия -> 1, на одной прямой все 3 точки -> 0)
# check_points
def test_check_points() -> None:
    # на 1 прямой
    assert check_points((0, 0), (1, 1), (2, 2)) == 0
    # почти на 1 прямой
    assert check_points((0, 0), (1, 1), (2, 3)) == 1
    # не на 1 прямой
    assert check_points((-1, -1), (1, -1), (0, 1)) == 1


# находит координаты пересечения биссектрисы с противоположной стороной
# find_bisector_intersection
def test_find_bisector_intersection() -> None:
    # Тест с обычными координатами точек треугольника
    assert find_bisector_intersection((0, 0), (2, 0), (0, 2)) == pytest.approx((1.0, 1.0), abs=0.01)
    # Тест с точками, где одна из координат равна 0
    assert find_bisector_intersection((0, 0), (3, 0), (0, 4)) == pytest.approx((1.714, 1.714), abs=0.01)
    # Тест с отрицательными координатами точек треугольника
    assert find_bisector_intersection((-1, -1), (-3, -1), (-1, -3)) == pytest.approx((-2.0, -2.0), abs=0.01)
    # Тест с большими координатами
    assert find_bisector_intersection((100, 100), (200, 100), (100, 200)) == pytest.approx((150.0, 150.0), abs=0.01)
    # Тест с точками, расположенными в других квадрантах
    assert find_bisector_intersection((-5, 5), (-5, -5), (5, -5)) == pytest.approx((-0.857, -5.0), abs=0.01)
    # Тест с точками на оси координат
    assert find_bisector_intersection((0, 0), (0, 5), (5, 0)) == pytest.approx((2.5, 2.5), abs=0.01)
    # Тест с точками на одной линии
    assert find_bisector_intersection((0, 0), (0, 2), (0, 5)) == pytest.approx((0.0, 2.857), abs=0.01)
    # Тест с точками, где одна из координат равна 0
    assert find_bisector_intersection((0, 0), (2, 0), (0, 4)) == pytest.approx((1.333, 1.333), abs=0.01)


# функция находит максимальный угол между медианой и биссектрисой в треугольнике (по трём кортежам - точкам)
# angle_bisector_median
@pytest.mark.parametrize("point1, point2, point3, expected_angle, expected_order", [ # в результатах пока какая-то фигня
    ((0, 0), (3, 0), (0, 4), 8.130, ((0, 0), (3, 0), (0, 4))), # прямоугольные треугольники
    ((0, 0), (1, 0), (1, 1), 4.065, ((0, 0), (1, 0), (1, 1))),
    ((0, 0), (0, 2), (3, 0), 11.309, ((0, 0), (0, 2), (3, 0))),
    ((-1, -1), (1, -1), (0, 1), 1.973, ((-1, -1), (1, -1), (0, 1))), # отрицательные координаты
    ((0, 100), (-1, 0), (1, 0), 43.568, ((-1, 0), (0, 100), (1, 0))), # один угол очень острый равносторонний остроугольный треугольник
    ((0, 100), (0, 0), (1, 50), 0.191, ((0, 100), (0, 0), (1, 50))), # равносторонний тупоугольный треугольник
    ((0, 100), (0, 0), (1, 99), 66.620, ((1, 99), (0, 100), (0, 0))) # очень кривой тупоугольный треугольник
])
def test_angle_bisector_median(point1: tuple[int, int], point2: tuple[int, int], point3: tuple[int, int], expected_angle: float,\
                               expected_order: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]):
    """
    Функция тестирования для функции angle_bisector_median.
    
    Принимает:
    - point1: tuple[int, int] - кортеж координат первой точки (x, y).
    - point2: tuple[int, int] - кортеж координат второй точки (x, y).
    - point3: tuple[int, int] - кортеж координат третьей точки (x, y).
    - expected_angle: float - ожидаемый угол между медианой и биссектрисой.
    - expected_order: tuple[tuple[int, int], tuple[int, int], tuple[int, int]] - ожидаемый порядок точек через
    которые проходит максимальный угол.
    """
    result = angle_bisector_median(point1, point2, point3)
    assert result[0] == pytest.approx(expected_angle, abs=0.01)
    assert result[1:] == expected_order
