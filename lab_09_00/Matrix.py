import numpy as np
from typing import List

# нахождение обратной матрицы


def inverse_mat(matrix: List[List[float]]) -> List[List[float]]:
    # Преобразуем обычный список в numpy-массив
    np_matrix = np.array(matrix)
    # Вычисляем обратную матрицу
    try:
        inv_np_matrix = np.linalg.inv(np_matrix)
    except np.linalg.LinAlgError:
        raise ValueError("Матрица является вырожденной и не имеет обратной")
    # Преобразуем numpy-массив обратно в обычный список
    inv_matrix = inv_np_matrix.tolist()
    return inv_matrix

# нахождение произведения матриц


def multy_mat(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    # Проверяем, могут ли матрицы быть перемножены
    if len(A[0]) != len(B):
        raise ValueError(
            "Число столбцов первой матрицы должно быть равно числу строк второй матрицы")
    # Инициализируем результирующую матрицу нулями
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    # Выполняем умножение матриц
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result
