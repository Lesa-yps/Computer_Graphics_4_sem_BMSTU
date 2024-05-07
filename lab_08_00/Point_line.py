# Импортируем библиотеки
import tkinter as tk
import tkinter.messagebox as mb
from typing import Tuple, List, Optional
from tkinter import ttk
from math import sqrt
from Table import get_ind_point
import Const as c

# линии чёрным рисуем, а отсекатель красным
COLOR_LINE = "#000000"
COLOR_CLIPPER = "#ff0000"

# отрисовывает массив пикселей


def draw_pixels(canvas: tk.Canvas, pixels: Tuple[any], tag: str, color: str) -> None:
    for i in range(len(pixels)):
        x, y = pixels[i]
        canvas.create_rectangle(
            x, y, x + 1, y + 1, fill=color, outline=color, tags=tag)

# Алгоритм цифрового дифференциального анализатора


def algo_DDA(point1: Tuple[int], point2: Tuple[int]) -> Tuple[any]:
    pixels = list()
    # насколько за длину отрезка изменились х и у
    dx = point2[c.X_PART] - point1[c.X_PART]
    dy = point2[c.Y_PART] - point1[c.Y_PART]
    dmax = max(abs(dx), abs(dy))
    if (dmax == 0):
        pixels.append([round(point1[c.X_PART]), round(point1[c.Y_PART])])
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
def draw_line(cnv: tk.Canvas, point1: Tuple[int], point2: Tuple[int], tag: str, color: str = COLOR_LINE) -> None:
    pixels = algo_DDA(point1, point2)
    draw_pixels(cnv, pixels, tag, color)


# надстройка над рисованием отрезка


def clever_draw_line(cnv: tk.Canvas, tree: ttk.Treeview, point1: Tuple[int], point2: Tuple[int], ZOOM: int) -> None:
    x1_table, y1_table = point1
    x2_table, y2_table = point2
    x1_input, y1_input, x2_input, y2_input = x1_table * \
        ZOOM, y1_table * ZOOM, x2_table * ZOOM, y2_table * ZOOM
    tree.insert("", "end", values=(x1_table, y1_table, x2_table, y2_table))
    draw_line(cnv, (x1_input, y1_input),
              (x2_input, y2_input), "start_line", COLOR_LINE)

# перерисовка всей таблицы линий
def redraw_lines(cnv: tk.Canvas, tree_line: ttk.Treeview, ZOOM: int):
    clean_lines(cnv)
    for item in tree_line.get_children():
        points = list()
        for i in range(4):
            points.append(int(tree_line.item(item, "values")[i]) * ZOOM)
        draw_line(cnv, (points[0], points[1]), (points[2], points[3]), "start_line", COLOR_LINE)

# надстройка над рисованием отсекателя


def clever_draw_clipper(cnv: tk.Canvas, tree: ttk.Treeview, point1: Tuple[int], ZOOM: int) -> None:
    x1_table, y1_table = point1
    tree.insert("", "end", values=(x1_table, y1_table))
    redraw_clipper(cnv, tree, ZOOM)


# перерисовка всей таблицы отсекателя
def redraw_clipper(cnv: tk.Canvas, tree_clipper: ttk.Treeview, ZOOM: int) -> None:
    clean_clipper(cnv)
    points = list()
    for item in tree_clipper.get_children():
        x = int(tree_clipper.item(item, "values")[0]) * ZOOM
        y = int(tree_clipper.item(item, "values")[1]) * ZOOM
        points.append((x, y))
    for i in range(len(points)):
        point1 = points[i]
        point2 = points[(i + 1) % len(points)]
        draw_line(cnv, point1, point2, "clipper_line", COLOR_CLIPPER)

# проверяет заполнены ли поля ввода координат числами


def check_input_field(arr_entry: List[tk.Entry], help_str: str, echo_err: bool = True) -> bool:
    try:
        for i in arr_entry:
            int(i.get())
    except ValueError:
        if echo_err:
            mb.showerror(
                'Ошибка!', f"Все поля координат должны быть заполнены ({help_str}).")
        return False
    else:
        return True

# очищает холст от линий

def clean_all(cnv: tk.Canvas) -> None:
    cnv.delete("unvis_line")
    cnv.delete("vis_line")
    clean_clipper(cnv)
    cnv.delete("start_line")

def clean_lines(cnv: tk.Canvas) -> None:
    cnv.delete("unvis_line")
    cnv.delete("vis_line")
    cnv.delete("start_line")

def clean_clipper(cnv: tk.Canvas) -> None:
    cnv.delete("clipper_line")

# расстояние между двумя точками


def dist(point1: Tuple[int], point2: Tuple[int]) -> float:
    return sqrt((point2[c.X_PART] - point1[c.X_PART])**2 + (point2[c.Y_PART] - point1[c.Y_PART])**2)

# рисует отрезок (видимую и невидимую его часть)


def Draw_visibl_line(cnv: tk.Canvas, res_points: Tuple[Tuple[int]], points: Tuple[Tuple[int]], is_sth_visibl: bool, color_vis: str, color_unvis: str, ZOOM: int) -> None:
    P1, P2 = points
    P1_z, P2_z = (P1[c.X_PART] * ZOOM, P1[c.Y_PART] *
                  ZOOM), (P2[c.X_PART] * ZOOM, P2[c.Y_PART] * ZOOM)
    if is_sth_visibl:
        Pr1, Pr2 = res_points
        if dist(Pr1, P1) > dist(Pr1, P2):
            P1, P2 = P2, P1
        Pr1_z, Pr2_z = (Pr1[c.X_PART] * ZOOM, Pr1[c.Y_PART]
                        * ZOOM), (Pr2[c.X_PART] * ZOOM, Pr2[c.Y_PART] * ZOOM)
        draw_line(cnv, P1_z, Pr1_z, tag="unvis_line", color=color_unvis)
        draw_line(cnv, P2_z, Pr2_z, tag="unvis_line", color=color_unvis)
        draw_line(cnv, Pr1_z, Pr2_z, tag="vis_line", color=color_vis)
    else:
        draw_line(cnv, P1_z, P2_z, tag="unvis_line", color=color_unvis)

# рисование отсекателя


def draw_clipper(cnv: tk.Canvas, clipper: List[int], color_clipper: str, ZOOM: int) -> None:
    for i in range(len(clipper)):
        point1 = (clipper[i][c.X_PART] * ZOOM, clipper[i][c.Y_PART] * ZOOM)
        point2 = (clipper[(i + 1) % len(clipper)][c.X_PART] * ZOOM, clipper[(i + 1) % len(clipper)][c.Y_PART] * ZOOM)
        draw_line(cnv, point1, point2, tag="clipper_line", color=color_clipper)
