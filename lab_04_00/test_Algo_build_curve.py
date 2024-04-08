# Tесты для функций
from Algo_build_curve import calc_all_quarter

# цвет по умолчанию чёрный
color_def = "#000000"

# переводит x и y из одной четверти во все остальные
# calc_all_quarter


def test_calc_all_quarter() -> None:
    # x = y = 0 (координаты точки нулевые), xc = yc = 0 (координаты центра нулевые)
    right_res = [(0, 0, color_def), (0, 0, color_def),
                 (0, 0, color_def), (0, 0, color_def)]
    assert calc_all_quarter(0, 0, color_def, 0, 0) == right_res
    # x = y = 0 (координаты точки нулевые), xc = yc = 100 (координаты центра равные ненулевые)
    right_res = [(100, 100, color_def), (100, 100, color_def),
                 (100, 100, color_def), (100, 100, color_def)]
    assert calc_all_quarter(0, 0, color_def, 100, 100) == right_res
    # x = y = 0 (координаты точки нулевые), xc = 50 yc = 10 (координаты центра неравные положительные)
    right_res = [(50, 10, color_def), (50, 10, color_def),
                 (50, 10, color_def), (50, 10, color_def)]
    assert calc_all_quarter(0, 0, color_def, 50, 10) == right_res
    # x = y = 0 (координаты точки нулевые), xc = -50 yc = -10 (координаты центра неравные отрицательные)
    right_res = [(-50, -10, color_def), (-50, -10, color_def),
                 (-50, -10, color_def), (-50, -10, color_def)]
    assert calc_all_quarter(0, 0, color_def, -50, -10) == right_res
    # x = 10 y = -20 (координаты точки неравные), xc = yc = 0 (координаты центра нулевые)
    right_res = [(10, -20, color_def), (-10, -20, color_def),
                 (-10, 20, color_def), (10, 20, color_def)]
    assert calc_all_quarter(10, -20, color_def, 0, 0) == right_res
    # x = 10 y = -20 (координаты точки неравные), xc = 100 yc = 50 (координаты центра ненулевые)
    right_res = [(110, 30, color_def), (90, 30, color_def),
                 (90, 70, color_def), (110, 70, color_def)]
    assert calc_all_quarter(10, -20, color_def, 100, 50) == right_res
