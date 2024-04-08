from math import cos, sin, pi, sqrt
from typing import Tuple, List
import tkinter as tk
from time import time

# отрисовывает массив пикселей


def draw_pixels(canvas: tk.Canvas, pixels: List[any]) -> None:
    for i in range(len(pixels)):
        x, y, color = pixels[i]
        canvas.create_rectangle(x, y, x + 1, y + 1, fill=color, outline=color)


# (0) библиотечный алгоритм для окружности
def algo_biblio_circle(cnv: tk.Canvas, xc: int, yc: int, R: int, color: str) -> None:
    cnv.create_oval(xc - R, yc - R, xc + R, yc + R, outline=color, width=1)

# (0) библиотечный алгоритм для эллипса


def algo_biblio_ellipse(cnv: tk.Canvas, xc: int, yc: int, a: int, b: int, color: str) -> None:
    cnv.create_oval(xc - a, yc - b, xc + a, yc + b, outline=color, width=1)

# переводит x и y из одной четверти во все остальные


def calc_all_quarter(x: int, y: int, color: str, xc: int, yc: int) -> List[any]:
    pixels = list()
    pixels.append((xc + x, yc + y, color))  # 1 четверть
    pixels.append((xc - x, yc + y, color))  # 2 четверть
    pixels.append((xc - x, yc - y, color))  # 3 четверть
    pixels.append((xc + x, yc - y, color))  # 4 четверть
    return pixels

# (1) алгоритм по каноническому уравнению для окружности
# (x - x0)^2 + (y - y0)^2 = R^2


def algo_сanon_circle(xc: int, yc: int, R: int, color: str) -> List[any]:
    pixels = list()
    R2 = R**2
    x_fin = round(R / sqrt(2))
    for x in range(x_fin + 1):
        y = sqrt(R2 - x**2)
        pixels += calc_all_quarter(x, y, color, xc, yc)
    for y in range(int(sqrt(R2 - x_fin**2)), 0, -1):
        x = sqrt(R2 - y**2)
        pixels += calc_all_quarter(x, y, color, xc, yc)
    return pixels

# (1) алгоритм по каноническому уравнению для эллипса
# (x - x0)^2 / a^2 + (y - y0)^2 / b^2 = 1


def algo_сanon_ellipse(xc: int, yc: int, a: int, b: int, color: str) -> List[any]:
    pixels = list()
    a2 = a**2
    b2 = b**2
    x_fin = round(a / sqrt(1 + b2 / a2))
    y_fin = round(b / sqrt(1 + a2 / b2))
    for x in range(0, x_fin + 1):
        y = b * sqrt(1 - x**2 / a2)
        pixels += calc_all_quarter(x, y, color, xc, yc)
    for y in range(y_fin, 0 - 1, -1):
        x = a * sqrt(1 - y**2 / b2)
        pixels += calc_all_quarter(x, y, color, xc, yc)
    return pixels

# (2) алгоритм по параметрическому уравнению для окружности
# x = R * cos(t)
# y = R * sin(t)
# где t - угол точки в радианах


def algo_param_circle(xc: int, yc: int, R: int, color: str) -> List[any]:
    pixels = list()
    t = pi / 2
    t_step = 1 / R
    while t > - t_step:
        x = R * cos(t)
        y = R * sin(t)
        pixels += calc_all_quarter(x, y, color, xc, yc)
        t -= t_step
    return pixels

# (2) алгоритм по параметрическому уравнению для эллипса
# x = a * cos(t)
# y = b * sin(t)
# где t - угол точки в радианах


def algo_param_ellipse(xc: int, yc: int, a: int, b: int, color: str) -> List[any]:
    pixels = list()
    t = pi / 2
    t_step = 1 / max(a, b)
    while t > - t_step:
        x = a * cos(t)
        y = b * sin(t)
        pixels += calc_all_quarter(x, y, color, xc, yc)
        t -= t_step
    return pixels

# (3) алгоритм Брезенхема для окружности


def algo_Bres_circle(xc: int, yc: int, R: int, color: str) -> List[any]:
    pixels = list()
    x = 0
    y = R
    pixels += calc_all_quarter(x, y, color, xc, yc)
    pixels += calc_all_quarter(y, x, color, xc, yc)
    delta_i = 2 * (1 - R)
    while x < y:
        side = 2 * (delta_i + y) - 1
        x += 1
        if side >= 0:
            y -= 1
            delta_i += 2 * (x - y + 1)  # диагональный шаг
        else:
            delta_i += x + x + 1  # горизонтальный шаг
        pixels += calc_all_quarter(x, y, color, xc, yc)
        pixels += calc_all_quarter(y, x, color, xc, yc)
    return pixels

# (3) алгоритм Брезенхема для эллипса


def algo_Bres_ellipse(xc: int, yc: int, a: int, b: int, color: str) -> List[any]:
    pixels = list()
    x = 0
    y = b
    pixels += calc_all_quarter(x, y, color, xc, yc)
    a2 = a**2
    b2 = b**2
    delta_i = b2 - a2 * (1 + 2 * b)  # Пробная функция
    while y >= 0:
        if delta_i > 0:  # второй интервал (больше меняется y)
            side = 2 * delta_i + b2 * 2 * (-x + 1)
            y -= 1
            delta_i += a2 * (-y - y + 1)
            if (side <= 0):
                x += 1
                delta_i += b2 * (x + x + 1)
        else:  # первый интервал (больше меняется x)
            side = 2 * delta_i + a2 * 2 * (y + 1)
            x += 1
            delta_i += b2 * (x + x + 1)
            if (side >= 0):
                y -= 1
                delta_i += a2 * (-y - y + 1)
        pixels += calc_all_quarter(x, y, color, xc, yc)
    return pixels

# (4) алгоритм средней точки для окружности


def algo_midpoint_circle(xc: int, yc: int, R: int, color: str) -> List[any]:
    pixels = list()
    x = R
    y = 0
    pixels += calc_all_quarter(x, y, color, xc, yc)
    pixels += calc_all_quarter(y, x, color, xc, yc)
    delta_i = 1 - R
    while x >= y:
        y += 1
        delta_i += y + y + 1
        if delta_i >= 0:
            x -= 1
            delta_i -= (x + x)
        pixels += calc_all_quarter(x, y, color, xc, yc)
        pixels += calc_all_quarter(y, x, color, xc, yc)
    return pixels

# (3) алгоритм средней точки для эллипса


def algo_midpoint_ellipse(xc: int, yc: int, a: int, b: int, color: str) -> List[any]:
    pixels = list()
    pixels += calc_all_quarter(0, b, color, xc, yc)
    pixels += calc_all_quarter(a, 0, color, xc, yc)
    a2 = a**2
    b2 = b**2
    a2_2 = a2 * 2
    b2_2 = b2 * 2
    # координаты граничной точки
    fin_x = round(a / sqrt(b2 / a2 + 1))
    fin_y = round(b / sqrt(a2 / b2 + 1))
    # рассчитываем точки на интервале от x = 0 до граничного x
    y = b
    delta_x = b2 - round(a2 * (b - 0.25))
    for x in range(0, fin_x + 1):
        if (delta_x > 0):
            y -= 1
            delta_x -= a2_2 * y
        delta_x += (x + x + 3) * b2
        pixels += calc_all_quarter(x, y, color, xc, yc)
    # рассчитываем точки на интервале от y = 0 до граничного y
    x = a
    delta_y = a2 - round(b2 * (a - 0.25))
    for y in range(0, fin_y + 1):
        if (delta_y > 0):
            x -= 1
            delta_y -= b2_2 * x
        delta_y += (y + y + 3) * a2
        pixels += calc_all_quarter(x, y, color, xc, yc)
    return pixels

# отрисовка кривой по переданным параметрам


def build_curve(cnv: tk.Canvas, params: Tuple[int], num_algo: int, cir_or_ell: int, color_curve: str, calc_time: bool = False) -> float:
    func = list_algo[num_algo][cir_or_ell]
    if (num_algo != 0):
        if calc_time:
            time_start = time()
            pixels = func(*params, color_curve)
            time_diff = time() - time_start
            return time_diff
        else:
            pixels = func(*params, color_curve)
        draw_pixels(cnv, pixels)
    else:
        # библиотечный алгоритм список пикселей не возвращает, а сразу рисует
        func(cnv, *params, color_curve)
    return -1.0

# отрисовка кривой в спектре


def build_spectr_curve(cnv: tk.Canvas, params: Tuple[int], step: int, count: int, num_algo: int, cir_or_ell: int,
                       color_curve: str, calc_time: bool = False) -> List[float]:
    time_res = list()
    count_now = 0
    if cir_or_ell:
        ratio = params[3] / params[2]
    while (count_now < count):
        time_i = build_curve(cnv, params, num_algo,
                             cir_or_ell, color_curve, calc_time)
        if calc_time:
            time_res += [time_i]
        count_now += 1
        Ra = params[2] + step
        if cir_or_ell:
            params = (params[0], params[1], Ra, Ra * ratio)
        else:
            params = (params[0], params[1], Ra)
    return time_res


# список алгоритмов
list_algo = [(algo_biblio_circle, algo_biblio_ellipse, "Библиотечный алгоритм"), (algo_сanon_circle, algo_сanon_ellipse, "Каноническое уравнение"),
             (algo_param_circle, algo_param_ellipse, "Параметрическое уравнение"), (
                 algo_Bres_circle, algo_Bres_ellipse, "Алгоритм Брезенхема"),
             (algo_midpoint_circle, algo_midpoint_ellipse, "Алгоритм средней точки")]
