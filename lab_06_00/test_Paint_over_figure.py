# Tесты для функций
from Paint_over_figure import point_comparison, find_area_located, AREA_PIXELS

# сравнивает текущую точку на максимум/минимум с текущими максимумом/минимумом по х/у координатам
# point_comparison


def test_point_comparison() -> None:
    # точка ни минимальная, ни максимальная
    assert point_comparison((-1, -1), (1, 1), (0, 0)) == ((-1, -1), (1, 1))
    # точка максимальная по у
    assert point_comparison((-1, -1), (1, 1), (0, 2)) == ((-1, -1), (1, 2))
    # точка минимальная по х
    assert point_comparison((-1, -1), (1, 1), (-2, 0)) == ((-2, -1), (1, 1))

# находим в какой области находятся фигуры
# find_area_located


def test_find_area_located() -> None:
    # затравка внутри фигуры
    test_list = [[(0, 0), (1, 1), (2, 2)]]
    assert find_area_located(test_list, (1, 1)) == (
        (0 - AREA_PIXELS, 0 - AREA_PIXELS), (2 + AREA_PIXELS, 2 + AREA_PIXELS))
    # затравка левее фигуры
    test_list = [[(1, 1)]]
    assert find_area_located(test_list, (0, 1)) == (
        (0 - AREA_PIXELS, 1 - AREA_PIXELS), (1 + AREA_PIXELS, 1 + AREA_PIXELS))
    # затравка выше фигуры
    test_list = [[(0, 0)], [(1, 1)], [(2, 2)]]
    assert find_area_located(test_list, (2, 4)) == (
        (0 - AREA_PIXELS, 0 - AREA_PIXELS), (2 + AREA_PIXELS, 4 + AREA_PIXELS))
