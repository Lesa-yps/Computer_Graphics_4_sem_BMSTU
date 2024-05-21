import pytest
from typing import List
# Tесты для функций
from Matrix import inverse_mat, multy_mat

# нахождение обратной матрицы
# inverse_mat


@pytest.mark.parametrize(
    "matrix, res",
    [
        pytest.param([[2, 5, 7], [6, 3, 4], [5, -2, -3]], [[1, -1, 1],
                     [-38, 41, -34], [27, -29, 24]], id="first_test"),
    ]
)
def test_inverse_mat(matrix: List[List[float]], res: List[List[float]]) -> None:
    computed = inverse_mat(matrix)
    assert len(computed) == len(res)  # Проверка размера матриц
    for row_computed, row_res in zip(computed, res):
        assert len(row_computed) == len(row_res)  # Проверка размера строк
        for val_computed, val_res in zip(row_computed, row_res):
            # Сравнение элемента с погрешностью
            assert val_computed == pytest.approx(val_res, abs=1e-9)

# нахождение произведения матриц
# multy_mat


@pytest.mark.parametrize(
    "A, B, res",
    [
        pytest.param([[2, -3, 1], [5, 4, -2]], [[-7, 5], [2, -1],
                     [4, 3]], [[-16, 16], [-35, 15]], id="first_test"),
    ]
)
def test_multy_mat(A: List[List[float]], B: List[List[float]], res: List[List[float]]) -> None:
    assert multy_mat(A, B) == res
