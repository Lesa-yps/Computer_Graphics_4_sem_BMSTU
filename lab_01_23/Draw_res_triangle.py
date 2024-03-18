import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
import math
from typing import List, Tuple

# функция находит точку посредине между двумя точками


def middle_point(point1: Tuple[int, int], point2: Tuple[int, int]) -> Tuple[int, int]:
    return ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)

# функция вычисляет угловой коэффициент прямой проходящей через обе эти точки


def slope(point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
    if point2[0] - point1[0] != 0:
        return (point2[1] - point1[1]) / (point2[0] - point1[0])
    else:
        # Возвращаем бесконечность, чтобы обозначить вертикальную прямую
        return float('inf')

# Функция находит по 3 точкам угол с вершиной в первой точке


def cosine_rule_angle(point1: Tuple[int, int], point2: Tuple[int, int], point3: Tuple[int, int]) -> float:
    # находим длины сторон
    a = math.dist(point2, point3)
    b = math.dist(point1, point3)
    c = math.dist(point1, point2)
    return math.degrees(math.acos((b**2 + c**2 - a**2) / (2 * b * c)))

# функция находит максимальный угол между медианой и биссектрисой в треугольнике (по трём кортежам - точкам)


def angle_bisector_median(point1: Tuple[int, int], point2: Tuple[int, int], point3: Tuple[int, int]) -> Tuple[float, Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    # находит координаты пересечения медиан с противоположной стороной
    mid_c = middle_point(point1, point2)
    mid_a = middle_point(point2, point3)
    mid_b = middle_point(point3, point1)
    # находит координаты пересечения биссектрис с противоположной стороной
    bis_a = find_bisector_intersection(point1, point2, point3)
    bis_b = find_bisector_intersection(point2, point1, point3)
    bis_c = find_bisector_intersection(point3, point1, point2)
    # по теореме косинусов находим углы между биссектрисами и медианами
    angle_res_a = cosine_rule_angle(point1, bis_a, mid_a)
    angle_res_b = cosine_rule_angle(point2, bis_b, mid_b)
    angle_res_c = cosine_rule_angle(point3, bis_c, mid_c)
    # и выбирается наибольший
    angle_res_max = max(angle_res_a, angle_res_b, angle_res_c)
    if (angle_res_a == angle_res_max):
        return angle_res_max, point1, point2, point3
    elif (angle_res_b == angle_res_max):
        return angle_res_max, point2, point1, point3
    return angle_res_max, point3, point1, point2

# возвращает список кортежей - точек из таблицы


def iterate_points(tree: ttk.Treeview) -> List[Tuple[int, int]]:
    arr = []
    for child in tree.get_children():
        item = tree.item(child)
        x = item['values'][0]  # Получаем значение X
        y = item['values'][1]  # Получаем значение Y
        arr.append((x, y))
    return arr

# сравнивает вещественные числа (одинаковые -> 1, разные -> 0) с погрешностью 0.0001


def same_num(a: float, b: float) -> int:
    EPS = 0.0001
    if abs(a - b) < EPS:
        return 1
    return 0

# проверка что треугольник не линия (не линия -> 1, на одной прямой все 3 точки -> 0)


def check_points(point1: Tuple[int, int], point2: Tuple[int, int], point3: Tuple[int, int]) -> int:
    if same_num(slope(point1, point2), slope(point1, point3)):
        return 0
    return 1

# сравнивает кортежи вещественных чисел (все части кортежа одинаковые -> 1,
# хоть 1 отличается -> 0) с погрешностью 0.0001


def same_turple(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    if same_num(a[0], b[0]) and same_num(a[1], b[1]):
        return 1
    return 0

# Функция определяет 3 точки, поведённый через которые треугольник будет имет между бисс и медианой наибольший угол
# треугольник и бисс с медианой рисуются


def draw_res_triangle(cnv: tk.Canvas, tree: tk.ttk.Treeview, ZOOM: int, SIDE_PLACE: int, HEIGHT_PLACE: int) -> None:
    max_angle = -1
    res_angle = list()
    arr = iterate_points(tree)
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            for k in range(j + 1, len(arr)):
                if check_points(arr[i], arr[j], arr[k]):
                    res, main_point, point1, point2 = angle_bisector_median(
                        arr[i], arr[j], arr[k])
                    # функция находит максимальный угол между медианой и биссектрисой в треугольнике (по трём кортежам - точкам)
                    if max_angle < res:
                        res_angle = [main_point, point1, point2]
                        max_angle = res
    if len(arr) < 3:
        mb.showerror(
            'Ошибка!', "Задача не может быть решена: введено недостаточное количество точек (минимум 3).")
    elif max_angle < 0:
        mb.showerror(
            'Ошибка!', "Задача не может быть решена за неимением треугольников.")
    else:
        draw_triangle(cnv, res_angle, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
        mb.showinfo('Максимальный угол',
                    "Максимальный угол междуу биссектрисой и медианой в треугольнике равен {:.2f} градус(а/ов).".format(max_angle))
        # print(res_angle, max_angle)
    return res_angle, max_angle


# находит координаты пересечения биссектрисы с противоположной стороной
def find_bisector_intersection(B: Tuple[int, int], A: Tuple[int, int], C: Tuple[int, int]) -> Tuple[float, float]:
    # Вычисляем длины сторон треугольника
    a_side = math.sqrt((C[0] - B[0]) ** 2 + (C[1] - B[1]) ** 2)
    b_side = math.sqrt((C[0] - A[0]) ** 2 + (C[1] - A[1]) ** 2)
    c_side = math.sqrt((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2)
    # Вычисляем длины частей на которые биссектриса делит противолежащую сторону (формулы выведены вручную)
    AD = c_side * b_side / (a_side + c_side)
    # Вычисляем координаты точки пересечения биссектрисы с стороной BC (формулы выведены вручную)
    x = (C[0] - A[0]) * AD / b_side + A[0]
    y = (C[1] - A[1]) * AD / b_side + A[1]
    return x, y

# рисует линию и подписывает её концы


def draw_line(cnv: tk.Canvas, point1: Tuple[int, int], point2: Tuple[int, int], ZOOM: int, color: str) -> None:
    # отрисовка линии
    width_line = 2
    cnv.create_line(point1[0] * ZOOM, point1[1] * ZOOM, point2[0] *
                    ZOOM, point2[1] * ZOOM, fill=color, tags="line", width=width_line)
    # Добавление подписи координат точек с тегом
    label1 = f"({round(point1[0])}, {round(point1[1])})"
    cnv.create_text(point1[0] * ZOOM, point1[1] * ZOOM,
                    text=label1, anchor="sw", tags="coordinates")
    label2 = f"({round(point2[0])}, {round(point2[1])})"
    cnv.create_text(point2[0] * ZOOM, point2[1] * ZOOM,
                    text=label2, anchor="sw", tags="coordinates")

# рисует результат (треугольник, биссектрису и медиану)


def draw_triangle(cnv: tk.Canvas, res_angle: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]], ZOOM: int, SIDE_PLACE: int, HEIGHT_PLACE: int) -> None:
    # Нарисуем сам треугольник
    draw_line(cnv, res_angle[0], res_angle[1], ZOOM, "green")
    draw_line(cnv, res_angle[0], res_angle[2], ZOOM, "green")
    draw_line(cnv, res_angle[1], res_angle[2], ZOOM, "green")
    # находим точку - середину противоположной стороны и рисуем медиану
    mid_point = middle_point(res_angle[1], res_angle[2])
    draw_line(cnv, res_angle[0], mid_point, ZOOM, "brown")
    # рисует биссектрису
    bis_point = find_bisector_intersection(
        res_angle[0], res_angle[1], res_angle[2])
    # Нарисуем биссектрису
    draw_line(cnv, bis_point, res_angle[0], ZOOM, "blue")
