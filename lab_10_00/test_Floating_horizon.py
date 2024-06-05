import pytest
from typing import Tuple, List
from unittest.mock import Mock
# Tесты для функций
from Floating_horizon import unpack_params, transform_point


# распаковка интервала
# unpack_params

@pytest.mark.parametrize(
    "interval, res",
    [
        pytest.param((0, 20, 100), (0, 100, 5), id="start_before_end"),
        pytest.param((100, 20, 0), (0, 100, 5), id="end_before_start"),
    ]
)
def test_unpack_params(interval: Tuple[float], res: Tuple[float]) -> None:
    assert unpack_params(interval) == res


# умножаем точку-массив на матрицу для трансформации и зум, тем самым применяя масштабирование и поворот (+ смещение к центру холста)
# transform_point

@pytest.mark.parametrize(
    "canvas_size, point, transform_matrix, scale_coef, res",
    [
        pytest.param((800, 600), [1, 1, 1], [[1, 0, 0, 0], [0, 1, 0, 0], [
                     0, 0, 1, 0], [0, 0, 0, 1]], 1, [401, 301, 1], id="basic_transform"),
        pytest.param((800, 600), [2, 2, 2], [[1, 0, 0, 0], [0, 1, 0, 0], [
                     0, 0, 1, 0], [0, 0, 0, 1]], 2, [404, 304, 4], id="scale_transform"),
        pytest.param((800, 600), [1, 1, 1], [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [
                     0, 0, 0, 1]], 0.5, [400.5, 300.5, 0.5], id="half_scale_transform"),
    ]
)
def test_transform_point(canvas_size: Tuple[int], point: List[float], transform_matrix: List[List[float]],
                         scale_coef: float, res: List[float]) -> None:
    cnv = Mock()
    cnv.winfo_width.return_value = canvas_size[0]
    cnv.winfo_height.return_value = canvas_size[1]
    assert transform_point(cnv, point, transform_matrix, scale_coef) == res
