import tkinter as tk
from typing import Tuple, List
from time import sleep
from Stack import Stack
from Grid import X_PART, Y_PART
from Point import COLOR_LINE

# цвет фона белый
COLOR_BACK = "#ffffff"
# сколько пискелей закрашивается вокруг фигуры, если затравка будет вне её
AREA_PIXELS = 10

# считываем текущий цвет пикселя


def scan_color(cnv: tk.Canvas, x: int, y: int, color_draw: str) -> str:
    # если пиксель (x, y) - (x + 1, y + 1) содержится среди объектов, имеющих тег "line" color = color_draw
    # если пиксель (x, y) - (x + 1, y + 1) содержится среди объектов, имеющих тег "paint_over" color = color_draw
    tag_arr = [("line", COLOR_LINE), (color_draw, color_draw)]
    # находим объекты в области точки
    objects = cnv.find_overlapping(x, y, x + 1, y + 1)
    for object_id in objects:
        tags = cnv.gettags(object_id)
        for tag in tag_arr:
            coords = cnv.coords(object_id)
            if tag[0] in tags and cnv.type(object_id) == "rectangle" and \
                    round(x) == round(coords[X_PART]) and round(y) == round(coords[Y_PART]):
                return tag[1]
    return COLOR_BACK


# Создаем пиксель заданным цветом (+ задержка)
def print_color(cnv: tk.Canvas, x: int, y: int, color: str, timeout: float) -> None:
    # print(x, y)
    cnv.create_rectangle(x, y, (x + 1), (y + 1),
                         fill=color, outline=color, tags=color)
    cnv.update()
    sleep(timeout)

# сравнивает текущую точку на максимум/минимум с текущими максимумом/минимумом по х/у координатам


def point_comparison(min_point: Tuple[int], max_point: Tuple[int], point: Tuple[int]) -> Tuple[Tuple[int]]:
    if (min_point[X_PART] is None or min_point[X_PART] > point[X_PART]):
        min_point = (point[X_PART], min_point[Y_PART])
    if (min_point[Y_PART] is None or min_point[Y_PART] > point[Y_PART]):
        min_point = (min_point[X_PART], point[Y_PART])
    if (max_point[X_PART] is None or max_point[X_PART] < point[X_PART]):
        max_point = (point[X_PART], max_point[Y_PART])
    if (max_point[Y_PART] is None or max_point[Y_PART] < point[Y_PART]):
        max_point = (max_point[X_PART], point[Y_PART])
    return min_point, max_point

# находим в какой области находятся фигуры


def find_area_located(edges_mat: List[List[Tuple[int]]], point_seed: Tuple[int]) -> Tuple[Tuple[int]]:
    min_point, max_point = (None, None), (None, None)
    for fig in edges_mat:
        for point in fig:
            min_point, max_point = point_comparison(
                min_point, max_point, point)
    min_point, max_point = point_comparison(min_point, max_point, point_seed)
    # увеличиваем область на AREA_PIXELS пикселей вокруг фигуры
    min_point = (min_point[X_PART] - AREA_PIXELS,
                 min_point[Y_PART] - AREA_PIXELS)
    max_point = (max_point[X_PART] + AREA_PIXELS,
                 max_point[Y_PART] + AREA_PIXELS)
    return min_point, max_point

# проверим, что строка выше/ниже не является ни границей многоугольника,
# ни уже полностью заполненной; если это не так, то найти затравку,
# начиная с левого края подынтервала сканирующей строки


def check_near_str(cnv: tk.Canvas, x_left: int, x_right: int, y: int, my_stack: Stack, color_draw: str) -> None:
    x = x_left
    while x <= x_right:
        # ищем затравку на строке выше/ниже
        is_seed_find = False
        color_cur = scan_color(cnv, x, y, color_draw)
        while color_cur != COLOR_LINE and color_cur != color_draw and x < x_right:
            if not is_seed_find:
                is_seed_find = True
            x += 1
            color_cur = scan_color(cnv, x, y, color_draw)
        # помещаем в стек крайний справа пиксель
        if is_seed_find:
            color_cur = scan_color(cnv, x, y, color_draw)
            if color_cur != COLOR_LINE and color_cur != color_draw and x == x_right:
                new_seed = (x, y)
            else:
                new_seed = (x - 1, y)
            my_stack.push(new_seed)
            # print("push", new_seed)
        # продолжим проверку, если интервал был прерван
        x_input = x
        color_cur = scan_color(cnv, x, y, color_draw)
        while (color_cur == COLOR_LINE or color_cur == color_draw) and x < x_right:
            x += 1
            color_cur = scan_color(cnv, x, y, color_draw)
        # удостоверимся, что координата пикселя увеличена
        if x == x_input:
            x += 1

# закрашиваем интервал справа и слева от затравки


def fill_str_near_seed(cnv: tk.Canvas, x: int, y: int, color_draw: str, timeout: float, area: Tuple[Tuple[int]]) -> Tuple[int]:
    # print("\nnew_line")
    print_color(cnv, x, y, color_draw, timeout)
    # сохраняем х-координату затравочного пикселя
    x_tmp = x
    # заполняем интервал справа от затравки
    x += 1
    color_cur = scan_color(cnv, x, y, color_draw)
    while color_cur != COLOR_LINE and x <= area[1][X_PART]:
        print_color(cnv, x, y, color_draw, timeout)
        x += 1
        color_cur = scan_color(cnv, x, y, color_draw)
    # сохраняем крайний справа пиксель
    x_right = x - 1
    # восстанавливаем х-координату затравки
    x = x_tmp
    # заполняем интервал слева от затравки
    x -= 1
    color_cur = scan_color(cnv, x, y, color_draw)
    while color_cur != COLOR_LINE and x >= area[0][X_PART]:
        print_color(cnv, x, y, color_draw, timeout)
        x -= 1
        color_cur = scan_color(cnv, x, y, color_draw)
        # print(x, y, color_cur)
    # сохраняем крайний слева пиксель
    x_left = x + 1
    return x_left, x_right

# алгоритм построчного затравочного заполнения


def paint_over_figure(cnv: tk.Canvas, point_seed: Tuple[int], edges_mat: List[List[Tuple[int]]], color_draw: str, timeout: float) -> None:
    # находим в какой области находятся фигуры
    area = find_area_located(edges_mat, point_seed)
    # инициализируем стек
    my_stack = Stack()
    # засовываем затравку в стек
    my_stack.push(point_seed)
    # цикл продолжается пока есть затравки в стеке
    while not my_stack.is_empty():
        # извлекаем пиксель из стека и присваиваем ему новое значение
        (x, y) = my_stack.pop()
        # закрашиваем интервал справа и слева от затравки
        x_left, x_right = fill_str_near_seed(
            cnv, x, y, color_draw, timeout, area)
        # проверим, что строка выше не является ни границей многоугольника,
        # ни уже полностью заполненной; если это не так, то найти затравку,
        # начиная с левого края подынтервала сканирующей строки
        if (area[1][Y_PART] >= (y + 1)):
            check_near_str(cnv, x_left, x_right, y + 1, my_stack, color_draw)
        # проверим, что строка ниже не является ни границей многоугольника,
        # ни полностью заполненной (эта часть алгоритма совершенно аналогична проверке
        # для строки выше, только вместо y += 1 подставляется y -= 1)
        if (area[0][Y_PART] <= (y - 1)):
            check_near_str(cnv, x_left, x_right, y - 1, my_stack, color_draw)
