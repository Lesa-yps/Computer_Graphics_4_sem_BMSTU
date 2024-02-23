import pytest
# Tесты для функций
from Mozg import same_num, same_turple, check_points, find_bisector_intersection, angle_bisector_median


# сравнивает вещественные числа
# same_num
def test_same_num():
    assert same_num(1.0, 1.0) == 1
    assert same_num(-1.11, -1.11) == 1
    assert same_num(1.0, 1.00001) == 1
    assert same_num(1.0, -1.0) == 0
    assert same_num(1.0, 2.0) == 0


# сравнивает кортежи вещественных чисел
# same_turple
def test_same_turple():
    assert same_turple((1, 2), (1, 2)) == 1
    assert same_turple((1.0, 2.0), (1.0, 2.00001)) == 1
    assert same_turple((1, 2), (2, 1)) == 0
    assert same_turple((1.0, 2.0), (2.0, 3.0)) == 0
    assert same_turple((1, 2), (1, 2.001)) == 1


# проверка что треугольник не линия
# check_points
def test_check_points():
    assert check_points((0, 0), (1, 1), (2, 2)) == 0
    assert check_points((0, 0), (1, 1), (2, 3)) == 1


# находит координаты пересечения биссектрисы с противоположной стороной
# find_bisector_intersection
def test_find_bisector_intersection():
    # Тест с обычными координатами точек треугольника
    assert find_bisector_intersection((0, 0), (2, 0), (0, 2)) == (1.0, 1.0)
    # Тест с точками, где одна из координат равна 0
    assert find_bisector_intersection((0, 0), (3, 0), (0, 4)) == (1.5, 1.5)
    # Тест с отрицательными координатами точек треугольника
    assert find_bisector_intersection((-1, -1), (-3, -1), (-1, -3)) == (-2.0, -2.0)
    # Тест с большими координатами
    assert find_bisector_intersection((100, 100), (200, 100), (100, 200)) == (150.0, 150.0)
    # Тест с точками, расположенными в других квадрантах
    assert find_bisector_intersection((-5, 5), (-5, -5), (5, -5)) == (-5.0, -5.0)
    # Тест с точками на оси координат
    assert find_bisector_intersection((0, 0), (0, 5), (5, 0)) == (2.5, 2.5)
    # Тест с точками на одной линии
    assert find_bisector_intersection((0, 0), (0, 2), (0, 5)) == (0.0, 0.0) #!!!
    # Тест с точками, где одна из координат равна 0
    assert find_bisector_intersection((0, 0), (2, 0), (0, 4)) == (1.0, 1.0)
    # Тест с точками, где все координаты отрицательны
    assert find_bisector_intersection((-1, -1), (-3, -1), (-1, -3)) == (-2.0, -2.0)


# функция находит максимальный угол между медианой и биссектрисой в треугольнике (по трём кортежам - точкам)
# angle_bisector_median
@pytest.mark.parametrize("point1, point2, point3, expected_angle, expected_order", [ # в результатах пока какая-то фигня
    ((0, 0), (3, 0), (0, 4), 90.0, ((0, 4), (0, 0), (3, 0))),
    ((1, 1), (5, 5), (2, 2), 90.0, ((5, 5), (1, 1), (2, 2))),
    ((0, 0), (1, 1), (2, 2), 60.0, ((2, 2), (0, 0), (1, 1))),
    ((0, 0), (1, 0), (1, 1), 90.0, ((1, 1), (0, 0), (1, 0))),
    ((0, 0), (0, 2), (3, 0), 90.0, ((0, 2), (0, 0), (3, 0))),
    ((0, 0), (0, 3), (4, 0), 90.0, ((0, 3), (0, 0), (4, 0)))
])
def test_angle_bisector_median(point1, point2, point3, expected_angle, expected_order):
    result = angle_bisector_median(point1, point2, point3)
    assert result[0] == pytest.approx(expected_angle, abs=0.01)
    assert result[1:] == expected_order
