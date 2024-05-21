import tkinter as tk
from typing import Tuple, List
from Draw import draw_polygon, clean_all
from Matrix import inverse_mat, multy_mat
import Const as c

# определяет знак числа


def sign(x: float) -> int:
    return (x > 0) - (x < 0)

# проверка отсекателя на выпуклость + второй возвращаемый параметр показывает в какую сторону шёл обход
# (по часовой - меньше нуля, против часовой - больше нуля)


def is_convex(figure: List[Tuple[int]]) -> Tuple[bool, int]:
    rc = (len(figure) >= 3)
    sign_now = 0
    if rc:
        i = 0
        while i < len(figure) and rc:
            (x1, y1) = figure[i]
            (x2, y2) = figure[(i + 1) % len(figure)]
            (x3, y3) = figure[(i + 2) % len(figure)]
            ab = (x2 - x1, y2 - y1)
            bc = (x3 - x2, y3 - y2)
            res = sign(ab[c.X_PART] * bc[c.Y_PART] -
                       bc[c.X_PART] * ab[c.Y_PART])
            if sign_now == 0:
                sign_now = res
            elif res != sign_now and res != 0:
                rc = False
            i += 1
    return rc, sign_now

# подпрограмма вычисления точки пересечения двух отрезков
# подпрограмма использует параметрическое описание отрезков


def find_cross(P1: Tuple[int], P2: Tuple[int], W1: Tuple[int], W2: Tuple[int]) -> Tuple[float]:
    # сформировать матрицу коэффициентов
    coef_mat = [[P2[c.X_PART] - P1[c.X_PART], W2[c.X_PART] - W1[c.X_PART]],
                [P2[c.Y_PART] - P1[c.Y_PART], W2[c.Y_PART] - W1[c.Y_PART]]]
    # сформировать матрицу правых частей
    right_mat = [[W1[c.X_PART] - P1[c.X_PART]], [W1[c.Y_PART] - P1[c.Y_PART]]]
    # обратить матрицу коэффициентов
    rcoef_mat = inverse_mat(coef_mat)
    # вычислить значения параметров в точке пересечения
    param_mat = multy_mat(rcoef_mat, right_mat)
    # вычислить координаты точки пересечения
    point_cross = (P1[c.X_PART] + (P2[c.X_PART] - P1[c.X_PART]) * param_mat[0]
                   [0], P1[c.Y_PART] + (P2[c.Y_PART] - P1[c.Y_PART]) * param_mat[0][0])
    return point_cross

# подпрограмма определения видимости точки
# видимость point следует определить относительно стороны P1P2
# вернёт значение меньшее нуля, если point невидима, равное нулю, если лежит на стороне P1P2, больше нуля - видима
# в этой подпрограмме используется вычисление векторного произведения


def visible(point: Tuple[int], P1: Tuple[int], P2: Tuple[int]) -> int:
    R1 = (point[c.X_PART] - P1[c.X_PART]) * (P2[c.Y_PART] - P1[c.Y_PART])
    R2 = (point[c.Y_PART] - P1[c.Y_PART]) * (P2[c.X_PART] - P1[c.X_PART])
    R3 = R1 - R2
    return sign(R3)


# подпрограмма определения факта пересечения ребра многоугольника состороной окна
def fact_cross(start: Tuple[int], end: Tuple[int], W1: Tuple[int], W2: Tuple[int]) -> bool:
    # определить видимость начальной точки ребра многоугольника
    start_vis = visible(start, W1, W2)
    # определить видимость конечной точки ребра многоугольника
    end_vis = visible(end, W1, W2)
    # считается, что ребро многоугольника, которое начинается или заканчивается на стороне окна, не пересекается с ней
    # эта точка должна быть занесена в результат ранее
    if (start_vis < 0 and end_vis > 0) or (start_vis > 0 and end_vis < 0):
        is_cross = True
    else:
        is_cross = False
    return is_cross

# алгоритм Созерленда-Ходжмена для отсечения многоугольника


def cutting_off_polygon_edge(Wi: Tuple[int], Wi1: Tuple[int], P: List[Tuple[int]]) -> List[Tuple[int]]:
    Np = len(P)
    # установить счётчик вершин результата и обнулить результат
    Nq = 0
    Q = list()
    S = P[0]
    # отсечь каждое ребро многоугольника по данной стороне окна
    for j in range(Np):
        # запомнить первую вершину
        if j == 0:
            F = P[j]
        # проверить факт пересечения ребром многоугольника стороны окна
        else:
            is_cross = fact_cross(S, P[j], Wi, Wi1)
            # если ребро пересекает сторону окна, вычислить точку пересечения
            if is_cross:
                point = find_cross(S, P[j], Wi, Wi1)
                # занести точку пересечения в результат
                Nq += 1
                Q.append(point)
        # изменить начальную точку ребра многоугольника
        S = P[j]
        # проверить видимость конечной точи (теперь это S) ребра многоугольника
        S_vis = visible(S, Wi, Wi1)
        if S_vis >= 0:
            # Если точка видима, то занести её в результат
            Nq += 1
            Q.append(S)
    # обработать замыкающее ребро мнооугольника
    # если результат пуст, то перейти к следующей стороне окна
    if Nq != 0:
        # проверить факт пересечения последним ребром многоугольника стороны окна
        is_cross = fact_cross(S, F, Wi, Wi1)
        if is_cross:
            # факт пересечения установлен, вычислить точку пересечения
            point = find_cross(S, F, Wi, Wi1)
            # занести точку пересечения в результат
            Nq += 1
            Q.append(point)
    # теперь многоугольник отсечен стороной Wi, Wi1 окна
    # работа алгоритма возобновляется с результатом отсечения
    return Q


# отсечение многоугольника по всем сторонам отсекателя

def cutting_off_polygon(cnv: tk.Canvas, polygon: List[Tuple[int]], clipper: List[Tuple[int]], arr_colors: List[str], ZOOM: float) -> None:
    clean_all(cnv)
    # рисование отсекателя
    draw_polygon(
        cnv, clipper, arr_colors[c.COLOR_CLIPPER], ZOOM, "clipper_line")
    # рисование стартового полигона
    draw_polygon(
        cnv, polygon, arr_colors[c.COLOR_UNVIS_LINE], ZOOM, "unvis_line")
    i = 0
    while i < len(clipper) and len(polygon) != 0:
        point1 = clipper[i]
        point2 = clipper[(i + 1) % len(clipper)]
        polygon = cutting_off_polygon_edge(point1, point2, polygon)
        i += 1
    # рисуем результат
    draw_polygon(cnv, polygon, arr_colors[c.COLOR_VIS_LINE], ZOOM, "vis_line")
