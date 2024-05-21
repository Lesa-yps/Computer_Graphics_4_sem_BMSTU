# Импортируем библиотеки
import tkinter as tk
import tkinter.messagebox as mb
from typing import Tuple, List
from tkinter import ttk
from math import sqrt
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


# добавляет координаты точки из полей ввода в таблицу


def add_point_tree(tree: ttk.Treeview, point: Tuple[int]) -> None:
    x, y = int(point[c.X_PART].get()), int(point[c.Y_PART].get())
    tree.insert("", "end", values=(x, y))


# перерисовка полигона из таблицы
def redraw_polygon(cnv: tk.Canvas, tree_polygon: ttk.Treeview, ZOOM: float, tag: str, color: str) -> None:
    points = list()
    for item in tree_polygon.get_children():
        x = int(tree_polygon.item(item, "values")[0]) * ZOOM
        y = int(tree_polygon.item(item, "values")[1]) * ZOOM
        points.append((x, y))
    for i in range(len(points)):
        point1 = points[i]
        point2 = points[(i + 1) % len(points)]
        draw_line(cnv, point1, point2, tag, color)

# перерисовка всеx таблиц


def redraw_canvas(cnv: tk.Canvas, tree_polygon: ttk.Treeview, tree_clipper: ttk.Treeview, ZOOM: float) -> None:
    clean_all(cnv)
    # перерисовка отсекателя
    redraw_polygon(cnv, tree_clipper, ZOOM, "clipper_line", COLOR_CLIPPER)
    # перерисовка многоугольника
    redraw_polygon(cnv, tree_polygon, ZOOM, "start_line", COLOR_LINE)

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
    clean_polygon(cnv)
    clean_clipper(cnv)


def clean_polygon(cnv: tk.Canvas) -> None:
    cnv.delete("unvis_line")
    cnv.delete("vis_line")
    cnv.delete("start_line")


def clean_clipper(cnv: tk.Canvas) -> None:
    cnv.delete("clipper_line")

# расстояние между двумя точками


def dist(point1: Tuple[int], point2: Tuple[int]) -> float:
    return sqrt((point2[c.X_PART] - point1[c.X_PART])**2 + (point2[c.Y_PART] - point1[c.Y_PART])**2)

# Рисует полигон


def draw_polygon(cnv: tk.Canvas, polygon: List[Tuple[int]], color_polygon: str, ZOOM: float, tag_polygon: str) -> None:
    for i in range(len(polygon)):
        point1 = (polygon[i][c.X_PART] * ZOOM, polygon[i][c.Y_PART] * ZOOM)
        point2 = (polygon[(i + 1) % len(polygon)][c.X_PART] *
                  ZOOM, polygon[(i + 1) % len(polygon)][c.Y_PART] * ZOOM)
        draw_line(cnv, point1, point2, tag=tag_polygon, color=color_polygon)
