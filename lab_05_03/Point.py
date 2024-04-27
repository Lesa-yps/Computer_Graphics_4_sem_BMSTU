# Импортируем библиотеки
import tkinter as tk
import tkinter.messagebox as mb
from typing import Tuple, List
from tkinter import ttk
from Grid import new_coord_xy, X_PART, Y_PART

# линии черным рисуем
COLOR_LINE = "#000000"

# отрисовывает массив пикселей


def draw_pixels(canvas: tk.Canvas, pixels: Tuple[any], color: str) -> None:
    for i in range(len(pixels)):
        x, y = pixels[i]
        canvas.create_rectangle(
            x, y, x + 1, y + 1, fill=color, outline=color, tags="line")

# Алгоритм цифрового дифференциального анализатора


def algo_DDA(point1: Tuple[int], point2: Tuple[int]) -> Tuple[any]:
    pixels = list()
    # насколько за длину отрезка изменились х и у
    dx = point2[X_PART] - point1[X_PART]
    dy = point2[Y_PART] - point1[Y_PART]
    dmax = max(abs(dx), abs(dy))
    if (dmax == 0):
        pixels.append([round(point1[X_PART]), round(point1[Y_PART])])
    else:
        # шаг изменения по коодинатам
        dx /= dmax
        dy /= dmax
        xi, yi = point1
        pixels.append([round(xi), round(yi)])
        i = 0
        while (i < dmax):
            xi += dx
            yi += dy
            pixels.append([round(xi), round(yi)])
            i += 1
    return pixels


# рисует линию попиксельно
def draw_line(cnv: tk.Canvas, xs: int, ys: int, edges_arr: List[Tuple[int]], color: str = COLOR_LINE) -> None:
    if len(edges_arr) == 0:
        cnv.create_rectangle(xs, ys, xs + 1, ys + 1,
                             fill=color, outline=color, tags="line")
    else:
        point1 = (xs, ys)
        point2 = (edges_arr[-1][X_PART], edges_arr[-1][Y_PART])
        pixels = algo_DDA(point1, point2)
        draw_pixels(cnv, pixels, color)


# В ответ на нажатие левой кнопкой мышки отрисовывается точка


def touch(x_input: int, y_input: int, cnv: tk.Canvas, tree: ttk.Treeview, ZOOM: int, SIDE_PLACE: int, HEIGHT_PLACE: int,
          edges_arr: List[Tuple[int]], is_painting: bool, change_coord: bool = True, check_in_table: bool = True) -> None:
    if is_painting:
        mb.showerror('Ошибка!', "Дождитесь конца закраски фигуры!")
        return
    if change_coord:
        x_table, y_table = new_coord_xy(
            x_input, y_input, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
        x_input, y_input = x_table * ZOOM, y_table * ZOOM
    else:
        x_table, y_table = x_input, y_input
        x_input, y_input = x_input * ZOOM, y_input * ZOOM
    clean_res(cnv)
    if check_in_table:
        tree.insert("", "end", values=(x_table, y_table))
    draw_line(cnv, x_input, y_input, edges_arr, COLOR_LINE)
    edges_arr.append((x_input, y_input))

# очищает закраску


def clean_res(cnv: tk.Canvas) -> None:
    cnv.delete("paint_over")
    cnv.delete("back")

# проверяет заполнены ли поля ввода координат числами


def check_input_field(x_entry: tk.Entry, y_entry: tk.Entry) -> bool:
    try:
        int(x_entry.get())
        int(y_entry.get())
    except ValueError:
        mb.showerror('Ошибка!', "Оба поля координат должны быть заполнены.")
        return False
    else:
        return True
