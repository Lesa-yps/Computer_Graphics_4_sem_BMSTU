import tkinter as tk
from typing import Tuple, List
import Const as c

# скалярное умножение векторов
def scal_mul(vec1, vec2):
    return vec1[c.X_PART] * vec2[c.X_PART] + vec1[c.Y_PART] * vec2[c.Y_PART]

# ищет вектор нормали к отрезку
def find_norm(point1, point2, point3):
    xs, ys = point1
    xe, ye = point2
    new_point = (ye - ys, -(xe - xs))
    vec13 = (point3[c.X_PART] - point1[c.X_PART], point3[c.Y_PART] - point1[c.Y_PART])
    if scal_mul(new_point, vec13) < 0:
        new_point = (new_point[c.X_PART] * (-1), new_point[c.Y_PART] * (-1))
    #print(point1, point2, point3, new_point)
    return new_point

# параметрическое уравнение
def Param_func(t, P1, P2):
    x = P1[c.X_PART] + (P2[c.X_PART] - P1[c.X_PART]) * t
    y = P1[c.Y_PART] + (P2[c.Y_PART] - P1[c.Y_PART]) * t
    return (x, y)

def Draw_visibl_line(cnv, P_res, P, Fl, color_vis, color_unvis, ZOOM):
    print(P, P_res, Fl)

# алгоритм двумерного отсечения Кируса-Бека
# P1, P2 - концевые точки отрезка
# k - число сторон отсекающего окна
# ni - вектор нормали к i-той стороне окна
# fi - точка, лежащая на i-той стороне окна
# D = (P2 - P1) - директриса отрезка
# Wi = (P1 - fi) - весовая функция
# td, tu - нижний и верхний пределы значений параметра t
# Fl - флаг видимости отрезка
# P_res - координаты видимого отрезка, который отрисуется
def cutting_off_line(cnv: tk.Canvas, P1: Tuple[int], P2: Tuple[int], clipper: List[int], color_vis: str, color_unvis: str, ZOOM: int) -> None:
    # инициализировать пределы значений параметра, предполагая полную видимость отрезка
    td = 0
    tu = 1
    # вычислить директрису D
    D = (P2[c.X_PART] - P1[c.X_PART], P2[c.Y_PART] - P1[c.Y_PART])
    # число сторон отсекающего окна
    k = len(clipper)
    # флаг видимости отрезка
    Fl = True
    # координаты видимого отрезка, который отрисуется
    P_res = None
    # начать главный цикл
    i = 1
    while (i <= k) and Fl and not P_res:
        # вычислить Wi, ni, D * ni и Wi * ni
        Wi = (P1[c.X_PART] - clipper[i - 1][c.X_PART], P1[c.Y_PART] - clipper[i - 1][c.Y_PART])
        ni = find_norm(clipper[i - 1], clipper[i % k], clipper[(i + 1) % k])
        D_scal = scal_mul(D, ni)
        W_scal = scal_mul(Wi, ni)
        # отрезок вырождается в точку?
        if D_scal == 0:
            if W_scal < 0:
                # точка невидима относительно текущей вершины
                Fl = False
            # отрезок выродился в точку
            if P1 == P2:
                P_res = (P1, P2)
        else:
            # отрезок невырожден, вычислить t
            t = - W_scal / D_scal
            # поиск верхнего и нижнего пределов t
            if D_scal > 0:
                # поиск нижнего предела
                # верно ли, что t <= 1?
                if t > 1:
                    Fl = False
                else:
                    td = max(t, td)
            else:
                # поиск верхнего предела
                # верно ли, что 0 <= t <= 1?
                if t < 0:
                    Fl = False
                else:
                    tu = min(t, tu)
        i += 1
    # проверка на невидимость отрезка
    print(td, tu, P_res)
    if td > tu:
        Fl = False
    if Fl and not P_res:
        P_res = (Param_func(td, P1, P2), Param_func(tu, P1, P2))
    Draw_visibl_line(cnv, P_res, (P1, P2), Fl, color_vis, color_unvis, ZOOM)

# отсечение по всем линиям


def cutting_off_all_lines(cnv: tk.Canvas, line_arr: List[List[Tuple[int]]], clipper: List[int], arr_colors: List[str], ZOOM: int) -> None:
    for i in range(len(line_arr)):
        if len(line_arr[i]) > 0:
            point1 = line_arr[i][0]
            point2 = line_arr[i][1]
            cutting_off_line(cnv, point1, point2, clipper,
                             arr_colors[c.COLOR_VIS_LINE], arr_colors[c.COLOR_UNVIS_LINE], ZOOM)

clipper = [(0, 0), (0, 0), (10, 0), (10, 10), (0, 10)]
line_arr = [[(0, 0), (20, 20)]]
arr_colors = ["#000000" for _ in range(3)]
cutting_off_all_lines(None, line_arr, clipper, arr_colors, 1)
