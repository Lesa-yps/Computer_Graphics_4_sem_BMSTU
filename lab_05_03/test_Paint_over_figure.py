# Tесты для функций
from Paint_over_figure import calc_x_border, calc_start_param_draw, find_border_draw

# находит границы цикла по х для закраски
# find_border_draw


def test_find_border_draw() -> None:
    # x слева от перегородки
    assert find_border_draw(-1, 0) == (-1, 1)
    # x справа от перегородки
    assert find_border_draw(1, 0) == (1, 2)
    # x на перегородке
    assert find_border_draw(0, 0) == (0, 1)


# вычисляем стартовые параметры закраски
# calc_start_param_draw
def test_calc_start_param_draw() -> None:
    # точка1 выше точки2
    assert calc_start_param_draw((0, 0), (1, 1), False) == (1, 1, 1, 1)
    # точка2 выше точки1
    assert calc_start_param_draw((1, 1), (0, 0), False) == (0, 1, 0, 0)
    # точки совпадают
    assert calc_start_param_draw((0, 0), (0, 0), False) == (0, 1, 0, 0)
    # начнёт с первой
    assert calc_start_param_draw((0, 0), (3, 3), True) == (0, 1, 0, 3)

# находит координату x для перегородки (самую правую)
# calc_x_border


def test_calc_x_border() -> None:
    # одна фигура несколько точек
    test_list = [[(0, 0), (1, 1), (2, 2)]]
    assert calc_x_border(test_list) == 2
    # одна фигура одна точка
    test_list = [[(1, 1)]]
    assert calc_x_border(test_list) == 1
    # несколько фигур по одной точке
    test_list = [[(0, 0)], [(1, 1)], [(2, 2)]]
    assert calc_x_border(test_list) == 2
    # несколько фигур по несколько точек
    test_list = [[(0, 0), (1, 1)], [(2, 2)]]
    assert calc_x_border(test_list) == 2
