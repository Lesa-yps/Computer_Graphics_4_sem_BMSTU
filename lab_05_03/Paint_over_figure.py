import tkinter as tk
from typing import Tuple, List
from time import sleep
from Grid import X_PART, Y_PART
from Point import COLOR_LINE

# цвет фона белый
COLOR_BACK = "#ffffff"

# считываем текущий цвет пикселя


def scan_color(cnv: tk.Canvas, x: int, y: int, color_draw: str) -> Tuple[str, bool]:
    # если пиксель (x, y) - (x + 1, y + 1) содержится среди объектов, имеющих тег "line" color = color_draw
    # если пиксель (x, y) - (x + 1, y + 1) содержится среди объектов, имеющих тег "paint_over" color = color_draw
    # если пиксель (x, y) - (x + 1, y + 1) содержится среди объектов, имеющих тег "back" color = COLOR_BACK
    tag_arr = [("line", COLOR_LINE), ("paint_over",
                                      color_draw), ("back", COLOR_BACK)]
    # находим объекты в области точки
    objects = cnv.find_overlapping(x, y, x + 1, y + 1)
    for object_id in objects:
        tags = cnv.gettags(object_id)
        for tag in tag_arr:
            coords = cnv.coords(object_id)
            if tag[0] in tags and cnv.type(object_id) == "rectangle" and \
                    round(x) == round(coords[X_PART]) and round(y) == round(coords[Y_PART]):
                if tag[0] != "line":
                    cnv.delete(object_id)
                return tag[1], tag[0] == "line"
    return COLOR_BACK, False


# Создаем пиксель заданным цветом
def print_color(cnv: tk.Canvas, x: int, y: int, color: str) -> None:
    tag = "back" if color == COLOR_BACK else "paint_over"
    cnv.create_rectangle(x, y, (x + 1), (y + 1),
                         fill=color, outline=color, tags=tag)

# находит границы цикла по х для закраски


def find_border_draw(x: int, x_bord: int) -> Tuple[int]:
    # если пересечение слева (или на) от перегородки
    if x <= x_bord:
        x_beg_for = x
        x_fin_for = x_bord + 1
    # если пересечение справа от перегородки
    else:
        x_beg_for = x_bord + 1
        x_fin_for = x + 1
    return x_beg_for, x_fin_for

# вычисляем стартовые параметры закраски


def calc_start_param_draw(point1: Tuple[int], point2: Tuple[int], not_ignore_first: bool) -> Tuple[any]:
    xs, ys = point1
    xe, ye = point2
    start_where = 0 if not_ignore_first else 1
    if ye < ys:
        xs, ys, xe, ye = xe, ye, xs, ys
        start_where = 0 if not_ignore_first else -1
    # для горизонтальных прямых
    if ye == ys:
        x_step = 1
        x = min(xs, xe)
        y = ye
    else:
        x_step = (xe - xs) / abs(ye - ys)
        x = xs + x_step if start_where == 1 else xs
        y = ys + 1 if start_where == 1 else ys
    return x, x_step, y, ye - (start_where == -1)

# перекраска


def work_with_color(cnv: tk.Canvas, x_cur: int, x: int, y: int, color_draw: str) -> None:
    # считываем текущий цвет пикселя
    color_cur, is_line = scan_color(cnv, x_cur, y, color_draw)
    # если цвет пикселя - это не цвет границы
    if not is_line:
        # если цвет пикселя - это цвет закраски, меняем его на цвет фона
        if color_cur == color_draw:
            color_cur = COLOR_BACK
        # если цвет пикселя - это цвет фона, меняем его на цвет закраски
        elif color_cur == COLOR_BACK:
            color_cur = color_draw
        # закрашиваем пиксель
        print_color(cnv, x_cur, y, color_cur)
    # print(x_cur, y, color_cur, is_line)

# обработка одного ребра


def paint_over_edge(cnv: tk.Canvas, point1: Tuple[int], point2: Tuple[int], x_bord: int, color_draw: str, timeout: float, not_ignore_first: bool = False) -> None:
    x, x_step, y, ye = calc_start_param_draw(point1, point2, not_ignore_first)
    # проходимся по всем строкам, пересекающим ребро
    # print(x, x_step, y, ye)
    while y <= ye:
        x_cur, x_fin_for = find_border_draw(x, x_bord)
        # print("y = ", y, "x_cur = ", x_cur, "x_fin_for = ", x_fin_for)
        # проходимся по строке от точки пересечения до перегородки, обрабатывая каждый пиксель
        while (x_cur < x_fin_for):
            # перекраска
            work_with_color(cnv, round(x_cur), x, y, color_draw)
            cnv.update()  # Обновление интерфейса для отображения изменений
            x_cur += 1
            sleep(timeout)
        # переходим к следующей строке
        y += 1
        x += x_step

# находит координату x для перегородки (самую правую)


def calc_x_border(edges_mat: List[List[Tuple[int]]]) -> int:
    x_border = 0
    is_found = False
    for fig in edges_mat:
        for point in fig:
            if point[X_PART] > x_border or not is_found:
                x_border = point[X_PART]
                is_found = True
    return x_border

# закрашивает фигуру, проходясь по всем рёбрам


def paint_over_figure(cnv: tk.Canvas, edges_mat: List[List[Tuple[int]]], color_draw: str, timeout: float) -> None:
    # находит координату x для перегородки (срединную)
    x_border = calc_x_border(edges_mat)
    # print("x_border = ", x_border)
    # проходимся по всем замкнутым фигурам
    for fig in edges_mat:
        # проходимся по всем точкам замкнутой фигуры
        count_points_fig = len(fig)
        if count_points_fig > 1:
            for i in range(count_points_fig):
                # обрабатываем текущее ребро
                point1 = fig[i]
                point2 = fig[(i + 1) % count_points_fig]
                # print("\np1 = ", point1, "p2 = ", point2)
                not_ignore_first = (i == 0)
                paint_over_edge(cnv, point1, point2, x_border,
                                color_draw, timeout, not_ignore_first)
