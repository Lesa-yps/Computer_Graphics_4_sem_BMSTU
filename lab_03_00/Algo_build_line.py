from math import floor, fabs, radians, cos, sin, pi
from typing import Tuple
import tkinter as tk

# константы
X_PART = 0
Y_PART = 1
Intens = 255  # максимальная интенсивность

# отрисовывает массив пикселей


def draw_pixels(canvas: tk.Canvas, pixels: Tuple[any]) -> None:
    for i in range(len(pixels)):
        x, y, color = pixels[i]
        canvas.create_rectangle(x, y, x + 1, y + 1, fill=color, outline=color)


# (0) библиотечный алгоритм
def algo_biblio(cnv: tk.Canvas, point1: Tuple[int], point2: Tuple[int], color: str) -> None:
    cnv.create_line(point1, point2, fill=color, width=1)

# (1) Алгоритм цифрового дифференциального анализатора


def algo_DDA(point1: Tuple[int], point2: Tuple[int], color: str, calc_step: bool = False) -> Tuple[any]:
    pixels = list()
    count_step = 0
    # насколько за длину отрезка изменились х и у
    dx = point2[X_PART] - point1[X_PART]
    dy = point2[Y_PART] - point1[Y_PART]
    dmax = max(abs(dx), abs(dy))
    if (dmax == 0):
        pixels.append([round(point1[X_PART]), round(point1[Y_PART]), color])
    else:
        # шаг изменения по коодинатам
        dx /= dmax
        dy /= dmax
        xi, yi = point1
        pixels.append([round(xi), round(yi), color])
        i = 0
        while (i < dmax):
            if calc_step:
                x_old, y_old = xi, yi
            xi += dx
            yi += dy
            if calc_step and round(x_old) != round(xi) and round(y_old) != round(yi):
                count_step += 1
            else:
                pixels.append([round(xi), round(yi), color])
            i += 1
    if calc_step:
        return count_step
    else:
        return pixels

# x > 0 -> 1; x < 0 -> -1; x == 0 -> 0


def sign(x: int) -> int:
    return (x > 0) - (x < 0)

# (2) Алгоритм Брезенхема с действительными данными


def algo_Bres_real(point1: Tuple[int], point2: Tuple[int], color: str, calc_step: bool = False) -> Tuple[any]:
    pixels = list()
    count_step = 0
    # насколько за длину отрезка изменились х и у
    dx = point2[X_PART] - point1[X_PART]
    dy = point2[Y_PART] - point1[Y_PART]
    if dx == 0 and dy == 0:
        pixels.append([round(point1[X_PART]), round(point1[Y_PART]), color])
    else:
        # знак изменения х и у
        x_sign, y_sign = sign(dx), sign(dy)
        dx, dy = abs(dx), abs(dy)
        # делаем dx > dy, запоминаем, если поменяли
        is_change_xy = False
        if (dy > dx):
            dx, dy = dy, dx
            is_change_xy = True
        e = dy / dx - 0.5
        xi, yi = point1
        i = 0
        while (i <= dx):
            if calc_step:
                x_old, y_old = xi, yi
            else:
                pixels.append([round(xi), round(yi), color])
            if (e >= 0):
                if is_change_xy:
                    xi += x_sign
                else:
                    yi += y_sign
                e -= 1
            if is_change_xy:
                yi += y_sign
            else:
                xi += x_sign
            e += dy / dx
            if calc_step and round(x_old) != round(xi) and round(y_old) != round(yi):
                count_step += 1
            i += 1
    if calc_step:
        return count_step
    else:
        return pixels

# (3) Алгоритм Брезенхема с целочисленными данными


def algo_Bres_int(point1: Tuple[int], point2: Tuple[int], color: str, calc_step: bool = False) -> Tuple[any]:
    pixels = list()
    count_step = 0
    # насколько за длину отрезка изменились х и у
    dx = point2[X_PART] - point1[X_PART]
    dy = point2[Y_PART] - point1[Y_PART]
    if dx == 0 and dy == 0:
        pixels.append([round(point1[X_PART]), round(point1[Y_PART]), color])
    else:
        # знак изменения х и у
        x_sign, y_sign = sign(dx), sign(dy)
        dx, dy = abs(dx), abs(dy)
        # делаем dx > dy, запоминаем, если поменяли
        is_change_xy = False
        if (dy > dx):
            dx, dy = dy, dx
            is_change_xy = True
        dx_double, dy_double = 2 * dx, 2 * dy
        e = dy_double - dx
        xi, yi = point1
        i = 0
        while (i <= dx):
            if calc_step:
                x_old, y_old = xi, yi
            else:
                pixels.append([round(xi), round(yi), color])
            if (e >= 0):
                if is_change_xy:
                    xi += x_sign
                else:
                    yi += y_sign
                e -= dx_double
            if is_change_xy:
                yi += y_sign
            else:
                xi += x_sign
            e += dy_double
            if calc_step and round(x_old) != round(xi) and round(y_old) != round(yi):
                count_step += 1
            i += 1
    if calc_step:
        return count_step
    else:
        return pixels

# переводит RGB представление цвета в 16-ичное


def rgb_to_hex(rgb_color: Tuple[int]) -> str:
    return '#{0:02x}{1:02x}{2:02x}'.format(*rgb_color)
# переводит 16-ичное представление цвета в RGB


def hex_to_rgb(hex_color: str) -> Tuple[int]:
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)
# Добавляет к цвету овещённость


def add_light_color(color: str, light: float) -> str:
    rgb_color = hex_to_rgb(color)
    new_rgb_color = tuple(min(255, max(0, int(i + light))) for i in rgb_color)
    return rgb_to_hex(new_rgb_color)
# (4) Алгоритм Брезенхема с устранением ступенчатости


def algo_Bres_del_step(point1: Tuple[int], point2: Tuple[int], color: str, calc_step: bool = False) -> Tuple[any]:
    pixels = list()
    count_step = 0
    # насколько за длину отрезка изменились х и у
    dx = point2[X_PART] - point1[X_PART]
    dy = point2[Y_PART] - point1[Y_PART]
    if dx == 0 and dy == 0:
        pixels.append([round(point1[X_PART]), round(point1[Y_PART]), color])
    else:
        # знак изменения х и у
        x_sign, y_sign = sign(dx), sign(dy)
        dx, dy = abs(dx), abs(dy)
        # делаем dx > dy, запоминаем, если поменяли
        is_change_xy = False
        if (dy > dx):
            dx, dy = dy, dx
            is_change_xy = True
        m = dy / dx
        w = 1 - m
        e = 0.5
        xi, yi = point1
        i = 0
        while (i <= dx):
            if calc_step:
                x_old, y_old = xi, yi
            else:
                pixels.append(
                    [round(xi), round(yi), add_light_color(color, Intens * e)])
            if (e < w):
                if is_change_xy:
                    yi += y_sign
                else:
                    xi += x_sign
                e += m
            else:
                xi += x_sign
                yi += y_sign
                e -= w
            if calc_step and round(x_old) != round(xi) and round(y_old) != round(yi):
                count_step += 1
            i += 1
    if calc_step:
        return count_step
    else:
        return pixels


# вспомогательная функция алгоритму Ву, вычисляющая m и параметры для for
def calc_m_param_for(dx: int, dy: int, y1: int, y2: int) -> Tuple[int]:
    m = 1
    step_for = 1
    if (dy != 0):
        m = dx / dy
    m1 = m
    if (y1 > y2):
        m1 *= -1
        step_for *= -1
    if (dy < dx):
        end_for = round(y2) - 1
    else:
        end_for = round(y2) + 1
    return m, m1, step_for, end_for
# (5) Алгоритм Ву


def algo_Wu(point1: Tuple[int], point2: Tuple[int], color: str, calc_step: bool = False) -> Tuple[any]:
    pixels = list()
    count_step = 0
    x1, y1 = point1
    x2, y2 = point2
    # насколько за длину отрезка изменились х и у
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        pixels.append([round(point1[X_PART]), round(point1[Y_PART]), color])
    else:
        if (abs(dy) >= abs(dx)):
            m, m1, step_for, end_for = calc_m_param_for(dx, dy, y1, y2)
            for yi in range(round(y1), end_for, step_for):
                d1 = x1 - floor(x1)
                d2 = 1 - d1
                if calc_step and int(x1) != int(x1 + m) and yi < round(y2):
                    count_step += 1
                else:
                    pixels.append(
                        [int(x1), yi, add_light_color(color, Intens * fabs(d1))])
                    pixels.append(
                        [int(x1) + 1, yi, add_light_color(color, Intens * fabs(d2))])
                x1 += m1
        else:
            m, m1, step_for, end_for = calc_m_param_for(dy, dx, x1, x2)
            for xi in range(round(x1), end_for, step_for):
                d1 = y1 - floor(y1)
                d2 = 1 - d1
                if calc_step and int(y1) != int(y1 + m) and xi < round(x2):
                    count_step += 1
                else:
                    pixels.append(
                        [xi, int(y1), add_light_color(color, Intens * fabs(d1))])
                    pixels.append(
                        [xi, int(y1) + 1, add_light_color(color, Intens * fabs(d2))])
                y1 += m1
    if calc_step:
        return count_step
    else:
        return pixels


# отрисовка отрезка по его координатам конца и начала
def build_line(cnv: tk.Canvas, point1: Tuple[int], point2: Tuple[int], num_algo: int, color_line: str) -> None:
    if (num_algo != 0):
        func = list_algo[num_algo][0]
        pixels = func(point1, point2, color_line)
        draw_pixels(cnv, pixels)
    else:
        # библиотечный алгоритм список пикселей не возвращает, а сразу рисует
        algo_biblio(cnv, point1, point2, color_line)

# отрисовка отрезка по его длине в спектре углов


def build_spectr_line(cnv: tk.Canvas, lenght_line: float, angle_step: float, num_algo: int, color_line: str) -> None:
    angle_step = radians(angle_step)
    angle_now = 0
    point_start = (0, 0)
    while (angle_now < 2 * pi):
        point_end = (int(cos(angle_now) * lenght_line),
                     int(sin(angle_now) * lenght_line))
        # print(point_start, point_end)
        build_line(cnv, point_start, point_end, num_algo, color_line)
        angle_now += angle_step


# список алгоритмов
list_algo = [(algo_biblio, "Библиотечный алгоритм"), (algo_DDA, "Алгоритм цифрового дифференциального анализатора"),
             (algo_Bres_real, "Алгоритм Брезенхема с действительными данными"), (
                 algo_Bres_int, "Алгоритм Брезенхема с целочисленными данными"),
             (algo_Bres_del_step, "Алгоритм Брезенхема с устранением ступенчатости"), (algo_Wu, "Алгоритм Ву")]
