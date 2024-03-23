# Tесты для функций
from Geometric_transforms import same_num, same_tuple, for_each_tuple
from typing import Tuple


# сравнивает вещественные числа (одинаковые -> 1, разные -> 0)  с погрешностью 0.0001
# same_num
def test_same_num() -> None:
    # оба положительные одинаковые
    assert same_num(1.0, 1.0)
    # оба отрицательные одинаковые
    assert same_num(-1.11, -1.11)
    # почти одинаковые с очень маленькой погрешностью
    assert same_num(1.0, 1.00001)
    # по модулю одинаковые, но разных знаков
    assert not same_num(1.0, -1.0)
    # разные
    assert not same_num(1.0, 2.0)


# сравнивает кортежи вещественных чисел (все части кортежа одинаковые -> 1,
# хоть 1 отличается -> 0) с погрешностью 0.0001
# same_tuple
def test_same_tuple() -> None:
    # оба положительные одинаковые
    assert same_tuple((1, 2), (1, 2))
    # оба отрицательные одинаковые
    assert same_tuple((-1, -2), (-1, -2))
    # почти одинаковые с очень маленькой погрешностью
    assert same_tuple((1.0, 2.0), (1.0, 2.00001))
    # x1 == y2 и x2 == y1
    assert not same_tuple((1, 2), (2, 1))
    # разные
    assert not same_tuple((1.0, 2.0), (2.0, 3.0))
    # почти одинаковые с недостаточно маленькой погрешностью
    assert not same_tuple((1, 2), (1, 2.001))

# вспомогательные функции для тестов


def sum_x(elem: Tuple[int, int], param: int) -> int:
    return elem[0] + param


def sum_y(elem: Tuple[int, int], param: int) -> int:
    return elem[1] + param

# применяет функции к каждому x и y в массиве кортежей
# for_each_tuple


def test_for_each_tuple() -> None:
    # в массиве 1 нулевой элемент
    assert for_each_tuple([(0, 0)], sum_x, 0, sum_y, 0) == [(0, 0)]
    # функция воздействует только на x
    assert for_each_tuple([(1, 2), (3, 4)], sum_x, 1,
                          sum_y, 0) == [(2, 2), (4, 4)]
    # функция воздействует только на y
    assert for_each_tuple([(1, 2), (3, 4)], sum_x, 0,
                          sum_y, 1) == [(1, 3), (3, 5)]
    # функция воздействует на оба коэффициента
    assert for_each_tuple([(1, 2), (3, 4)], sum_x, 1,
                          sum_y, 1) == [(2, 3), (4, 5)]
    # есть отрицательные коэффициенты
    assert for_each_tuple([(-1, 2), (-3, 4)], sum_x, 1,
                          sum_y, 1) == [(0, 3), (-2, 5)]
    # функция воздействует на x и y с разными параметрами
    assert for_each_tuple([(1, 2), (3, 4)], sum_x, 10,
                          sum_y, -5) == [(11, -3), (13, -1)]
    # пустой массив
    assert for_each_tuple([], sum_x, 1, sum_y, 1) == []
