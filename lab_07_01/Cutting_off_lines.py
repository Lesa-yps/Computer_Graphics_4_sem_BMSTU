import tkinter as tk
from typing import Tuple, List
from Point_line import Draw_visibl_line, clean_lines, draw_clipper
import Const as c

# вычисление кодов концевых точек и занесение этих кодов в массив 1*4 каждый


def calc_visibl_code(point: Tuple[int], clipper: List[int]) -> List[int]:
    code = [0 for _ in range(c.LEN_CLIPPER)]
    if point[c.X_PART] < clipper[c.X_LEFT]:
        code[c.X_LEFT] = 1
    if point[c.X_PART] > clipper[c.X_RIGHT]:
        code[c.X_RIGHT] = 1
    if point[c.Y_PART] < clipper[c.Y_DOWN]:
        code[c.Y_DOWN] = 1
    if point[c.Y_PART] > clipper[c.Y_UP]:
        code[c.Y_UP] = 1
    return code

# проверка видимости всего отрезка и его точек


def check_visibl(P1: Tuple[int], P2: Tuple[int], clipper: List[int]) -> int:
    # вычисление кодов концевых точек для конца отрезка P1
    T1_code = calc_visibl_code(P1, clipper)
    # вычисление кодов концевых точек для конца отрезка P2
    T2_code = calc_visibl_code(P2, clipper)
    # проверка полной видимости отрезка
    Sum1 = sum(T1_code)
    Sum2 = sum(T2_code)
    if Sum1 == 0 and Sum2 == 0:
        # отрезок полностью видимый можно визуализировать
        return c.LINE_VISIBL
    # отрезок не является полностью видимым
    # проверка случая тривиальной невидимости
    # вычисление логического произведения (Mul) кодов концевых точек отрезка
    Mul = sum([T1_code[i] * T2_code[i] for i in range(len(T1_code))])
    # отрезок невидим
    if Mul != 0:
        return c.LINE_NOT_VISIBL
    # Отрезок может быть частично видимым
    # проверка попадания первой точки внутрь окна
    if Sum1 == 0:
        return c.FIRST_VISIBL
    # проверка попадания второй точки внутрь окна
    if Sum2 == 0:
        return c.SECOND_VISIBL
    # отрезок частично видим или пересекает продолжение диагонали, оставаясь невидимым
    # требуется углублённая проверка на видимость
    return c.DONT_KNOW

# проверка пересечения с левым краем


def check_cross_left(P: Tuple[int], m: float, clipper: List[int]) -> Tuple[any]:
    if clipper[c.X_LEFT] < P[c.X_PART]:
        return False, P
    y = m * (clipper[c.X_LEFT] - P[c.X_PART]) + P[c.Y_PART]
    if (y > clipper[c.Y_UP]) or (y < clipper[c.Y_DOWN]):
        return False, P
    # обнаружено корректное пересечение
    return True, (clipper[c.X_LEFT], y)

# проверка пересечения с правым краем


def check_cross_right(P: Tuple[int], m: float, clipper: List[int]) -> Tuple[any]:
    if clipper[c.X_RIGHT] > P[c.X_PART]:
        return False, P
    y = m * (clipper[c.X_RIGHT] - P[c.X_PART]) + P[c.Y_PART]
    if (y > clipper[c.Y_UP]) or (y < clipper[c.Y_DOWN]):
        return False, P
    # обнаружено корректное пересечение
    return True, (clipper[c.X_RIGHT], y)

# проверка пересечения с верхним краем


def check_cross_up(P: Tuple[int], m: float, clipper: List[int]) -> Tuple[any]:
    if clipper[c.Y_UP] > P[c.Y_PART]:
        return False, P
    x = (1 / m) * (clipper[c.Y_UP] - P[c.Y_PART]) + P[c.X_PART]
    if (x > clipper[c.X_RIGHT]) or (x < clipper[c.X_LEFT]):
        return False, P
    # обнаружено корректное пересечение
    return True, (x, clipper[c.Y_UP])

# проверка пересечения с нижним краем


def check_cross_down(P: Tuple[int], m: float, clipper: List[int]) -> Tuple[any]:
    if clipper[c.Y_DOWN] < P[c.Y_PART]:
        return False, P
    x = (1 / m) * (clipper[c.Y_DOWN] - P[c.Y_PART]) + P[c.X_PART]
    if (x > clipper[c.X_RIGHT]) or (x < clipper[c.X_LEFT]):
        return False, P
    # обнаружено корректное пересечение
    return True, (x, clipper[c.Y_DOWN])

# проверяет пересечение со всеми сторонами отсекателя, последовательно вызывая другие функции


def check_cross_sides(P1: Tuple[int], P2: Tuple[int], P: Tuple[int], clipper: List[int], Fl: int) -> Tuple[any]:
    m = float("inf")
    was_find = False
    # проверка вертикальности отрезка
    if (P2[c.X_PART] - P1[c.X_PART]) != 0:
        # высчитываем наклон прямой
        m = (P2[c.Y_PART] - P1[c.Y_PART]) / (P2[c.X_PART] - P1[c.X_PART])
        # (2) проверка пересечения с левым краем
        was_find, P = check_cross_left(P, m, clipper)
        # (3) проверка пересечения с правым краем
        if not was_find:
            was_find, P = check_cross_right(P, m, clipper)
    # проверка горизонтальности отрезка
    if m != 0 and not was_find:
        # (4) проверка пересечения с верхним краем
        was_find, P = check_cross_up(P, m, clipper)
        # (5) проверка пересечения с нижним краем
        if not was_find:
            was_find, P = check_cross_down(P, m, clipper)
        if not was_find:
            # (6) Отрезок невидим
            Fl = c.LINE_NOT_VISIBL
    return Fl, P

# простой алгоритм двумерного отсечения
# P1, P2 - концевые точки отрезка
# Pr1, Pr2 - концевые точки видимой части отрезка
# Fl - флаг - признак видимости


def cutting_off_line(cnv: tk.Canvas, P1: Tuple[int], P2: Tuple[int], clipper: List[int], color_vis: str, color_unvis: str, ZOOM: float) -> None:
    # инициализация видимых концевых точек
    Pr1 = P1
    Pr2 = P2
    is_all_find = False
    # инициализация признака видимости
    Fl = check_visibl(P1, P2, clipper)
    # отрезок полностью видим
    if Fl == c.LINE_VISIBL:
        is_all_find = True
    if Fl == c.FIRST_VISIBL:
        num = 1
        Pr1 = P1
        P = P2
    elif Fl == c.SECOND_VISIBL:
        num = 2
        Pr1 = P2
        P = P1
    elif Fl == c.DONT_KNOW:
        # внутри окна нет концов отрезка
        # инициализация номера конца отрезка
        num = 0
        P = P1
    # (1)
    while not is_all_find and Fl != c.LINE_NOT_VISIBL:
        # проверяет пересечение со всеми сторонами отсекателя, последовательно вызывая другие функции
        Fl, P = check_cross_sides(P1, P2, P, clipper, Fl)
        if Fl != c.LINE_NOT_VISIBL:
            if num == 0:
                Pr1 = P
                P = P2
                num += 1
            elif num == 1 or num == 2:
                Pr2 = P
                is_all_find = True
    # (7) завершение работы и вызов процедуры черчения
    # флаг показывает: найдена ли видимая часть в результате работы алгоритма
    is_sth_visibl = (Fl != c.LINE_NOT_VISIBL)
    Draw_visibl_line(cnv, (Pr1, Pr2), (P1, P2), is_sth_visibl,
                     color_vis, color_unvis, ZOOM)

# отсечение по всем линиям


def cutting_off_all_lines(cnv: tk.Canvas, line_arr: List[List[Tuple[int]]], clipper: List[int], arr_colors: List[str], ZOOM: float) -> None:
    clean_lines(cnv)
    # рисование отсекателя
    draw_clipper(cnv, clipper, arr_colors[c.COLOR_CLIPPER], ZOOM)
    for i in range(len(line_arr)):
        if len(line_arr[i]) > 0:
            point1 = line_arr[i][0]
            point2 = line_arr[i][1]
            cutting_off_line(cnv, point1, point2, clipper,
                             arr_colors[c.COLOR_VIS_LINE], arr_colors[c.COLOR_UNVIS_LINE], ZOOM)
