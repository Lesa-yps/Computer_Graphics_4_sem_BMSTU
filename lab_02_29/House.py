import math
import tkinter as tk
from typing import Dict, List, Tuple

X_PART, Y_PART = 0, 1
EPS = 0.0001

# функция вычисляет угловой коэффициент прямой перпендикулярный проходящей через обе эти точки


def slope(point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
    if point2[0] - point1[0] != 0:
        return (point2[1] - point1[1]) / (point2[0] - point1[0])
    else:
        # Возвращаем бесконечность, чтобы обозначить вертикальную прямую
        return float('inf')
# поиск х2 и у2 по расстоянию от (х1, у1), самим (х1, у1), и уравнению прямой (k и b)
# возвращаются точки слева и справа от (х1, у1) на заданном расстоянии


def find_xy_by_len(point1, k, lena):
    x1, y1 = point1
    if (k == float('inf')):
        y2_l, x2_l = y1 - lena, x1
        y2_h, x2_h = y1 + lena, x1
    elif (abs(k) < EPS):
        y2_l, x2_l = y1, x1 - lena
        y2_h, x2_h = y1, x1 + lena
    else:
        b = y1 - k * x1
        a2 = 1 + k**2
        b2 = - x1 + k * b - k * y1
        c2 = - lena ** 2 + x1 ** 2 + b ** 2 - 2 * b * y1 + y1 ** 2
        sqrt_D = math.sqrt(b2 ** 2 - a2 * c2)
        x2_h = (- b2 + sqrt_D) / a2
        x2_l = (- b2 - sqrt_D) / a2
        y2_h = k * x2_h + b
        y2_l = k * x2_l + b
    return (x2_l, y2_l), (x2_h, y2_h)

# какую посчитанную точку на расстоянии len выберем


def choose_point_side(left_less_rect: Tuple[int, int], right_less_rect: Tuple[int, int]) -> Tuple[int, int]:
    if (left_less_rect[X_PART] < right_less_rect[X_PART]):
        right_choose = 1
        left_choose = 0
    else:
        right_choose = 0
        left_choose = 1
    return right_choose, left_choose


def choose_point_hight(center_point: Tuple[int, int], left_less_rect: Tuple[int, int], k_norm: float) -> Tuple[int, int]:
    if (k_norm >= 0):
        hight_choose = 1 if (
            left_less_rect[Y_PART] < center_point[Y_PART]) else 0
        less_choose = 0 if (
            left_less_rect[Y_PART] < center_point[Y_PART]) else 1
    else:
        hight_choose = 0 if (
            left_less_rect[Y_PART] < center_point[Y_PART]) else 1
        less_choose = 1 if (
            left_less_rect[Y_PART] < center_point[Y_PART]) else 0
    return less_choose, hight_choose

# конструктор домика


def constructor_house(center_point: Tuple[int, int], left_less_rect: Tuple[int, int], right_less_rect: Tuple[int, int]) -> Dict[str, any]:
    # точка посреди низа домика
    middle_less_rect = (
        (right_less_rect[0] + left_less_rect[0]) / 2, (right_less_rect[1] + left_less_rect[1]) / 2)
    # высота и ширина домика
    hight_house = math.dist(middle_less_rect, center_point) * 2
    width_house = math.dist(right_less_rect, left_less_rect)
    # находим коэффициенты параллельных и перпендикулярных прямых
    k_norm = slope(middle_less_rect, center_point)
    k_parall = slope(right_less_rect, left_less_rect)
    # какую посчитанную точку на расстоянии len выберем
    right_choose, left_choose = choose_point_side(
        left_less_rect, right_less_rect)
    less_choose, hight_choose = choose_point_hight(
        center_point, left_less_rect, k_norm)
    # донаходим координаты прямоугольника
    left_hight_rect = find_xy_by_len(
        left_less_rect, k_norm, hight_house * 5/8)[hight_choose]
    right_hight_rect = find_xy_by_len(
        right_less_rect, k_norm, hight_house * 5/8)[hight_choose]
    # находим координаты крыши
    left_hight_roof = find_xy_by_len(
        left_less_rect, k_norm, hight_house)[hight_choose]
    right_hight_roof = find_xy_by_len(
        right_less_rect, k_norm, hight_house)[hight_choose]
    left_less_roof = find_xy_by_len(
        left_hight_rect, k_parall, width_house * 1/10)[left_choose]
    right_less_roof = find_xy_by_len(
        right_hight_rect, k_parall, width_house * 1/10)[right_choose]
    # находим координаты травы
    left_grass = find_xy_by_len(
        left_less_rect, k_parall, width_house * 1/4)[left_choose]
    right_grass = find_xy_by_len(
        right_less_rect, k_parall, width_house * 1/4)[right_choose]
    # находим координаты фрейма и центра окна
    frame_hight = find_xy_by_len(
        center_point, k_parall, width_house * 1/4)[right_choose]
    frame_less = find_xy_by_len(
        frame_hight, k_norm, hight_house * 1/4)[less_choose]
    center_circle = find_xy_by_len(
        frame_hight, k_norm, hight_house * 1/8)[less_choose]
    frame_right = find_xy_by_len(
        center_circle, k_parall, width_house * 1/10)[right_choose]
    frame_left = find_xy_by_len(
        center_circle, k_parall, width_house * 1/10)[left_choose]
    # находим координаты двери
    door_hight_right = find_xy_by_len(
        center_point, k_parall, width_house * 1/10)[left_choose]
    door_hight_left = find_xy_by_len(
        center_point, k_parall, width_house * 2/5)[left_choose]
    door_less_right = find_xy_by_len(
        middle_less_rect, k_parall, width_house * 1/10)[left_choose]
    door_less_left = find_xy_by_len(
        middle_less_rect, k_parall, width_house * 2/5)[left_choose]
    # находим координаты ручки двери
    help_handle_point = find_xy_by_len(
        center_point, k_parall, width_house * 1/8)[left_choose]
    right_hight_handle = find_xy_by_len(
        help_handle_point, k_norm, hight_house * 3/16)[less_choose]
    left_hight_handle = find_xy_by_len(
        right_hight_handle, k_parall, width_house * 1/20)[left_choose]
    right_less_handle = find_xy_by_len(
        right_hight_handle, k_norm, hight_house * 1/8)[less_choose]
    left_less_handle = find_xy_by_len(
        left_hight_handle, k_norm, hight_house * 1/8)[less_choose]
    # Заполняем домик
    house = dict()
    house["center"] = center_point
    house["grass"] = [left_grass, right_grass]
    house["rect"] = [left_less_rect, left_hight_rect,
                     right_hight_rect, right_less_rect]
    house["roof"] = [left_less_roof, left_hight_roof,
                     right_hight_roof, right_less_roof]
    house["wind"] = {"center": center_circle,
                     "a": frame_right, "b": frame_hight, "angle": math.degrees(math.atan(k_parall))}
    house["wind_frame"] = [frame_left, frame_hight, frame_right, frame_less]
    house["door"] = [door_less_left, door_hight_left,
                     door_hight_right, door_less_right]
    house["door_handle"] = [left_less_handle, left_hight_handle,
                            right_hight_handle, right_less_handle]
    return house

# рисует ломаную прямую по массиву кортежей-точек


def draw_polyline(cnv: tk.Canvas, arr_tuple: List[Tuple[int, int]], color: str, width_line: int, ZOOM: int, is_closed: bool = True) -> None:
    coords = [coord * ZOOM for point in arr_tuple for coord in point] + \
        [arr_tuple[0][0] * ZOOM, arr_tuple[0][1] * ZOOM]
    cnv.create_line(coords, fill=color, tags="line", width=width_line)

# рисует эллипс


def DrawEllipse(cnv: tk.Canvas, wind: Dict[str, any], width_line: int, color: str, ZOOM: float) -> None:
    pa, pb, pc = wind["center"], wind["a"], wind["b"]
    n = 100
    pellipse = list()
    for i in range(n):
        x = round(pa[X_PART] + (pb[X_PART] - pa[X_PART]) * math.cos(i * 2 * math.pi / n) + (pc[X_PART] - pa[X_PART])
                  * math.sin(i * 2 * math.pi / n))
        y = round(pa[Y_PART] + (pb[Y_PART] - pa[Y_PART]) * math.cos(i * 2 * math.pi / n) + (pc[Y_PART] - pa[Y_PART])
                  * math.sin(i * 2 * math.pi / n))
        pellipse.append((x, y))
    draw_polyline(cnv, pellipse, color, width_line, ZOOM)


# удаляет старую отрисовку домика
def delete_house(cnv: tk.Canvas) -> None:
    cnv.delete("line")
    cnv.delete("coordinates")
    cnv.delete("point")

# отрисовка домика


def draw_house(cnv: tk.Canvas, house: Dict[str, any], ZOOM: float) -> None:
    delete_house(cnv)
    width_line = 2
    label = "({:}, {:})".format(
        int(house["center"][0]), int(house["center"][1]))
    cnv.create_text(house["center"][0] * ZOOM, house["center"]
                    [1] * ZOOM, text=label, anchor="sw", tags="coordinates")
    cnv.create_oval(house["center"][0] * ZOOM - width_line, house["center"][1] * ZOOM - width_line, house["center"][0] * ZOOM + width_line,
                    house["center"][1] * ZOOM + width_line, fill="red", outline="black", tags="point")
    draw_polyline(cnv, house["grass"], "green", width_line, ZOOM)
    draw_polyline(cnv, house["rect"], "blue", width_line, ZOOM)
    draw_polyline(cnv, house["roof"], "blue", width_line, ZOOM)
    DrawEllipse(cnv, house["wind"], width_line, "red", ZOOM)
    cnv.create_line(house["wind_frame"][0][0] * ZOOM, house["wind_frame"][0][1] * ZOOM, house["wind_frame"][2][0] * ZOOM,
                    house["wind_frame"][2][1] * ZOOM, fill="red", tags="line", width=width_line)
    cnv.create_line(house["wind_frame"][1][0] * ZOOM, house["wind_frame"][1][1] * ZOOM, house["wind_frame"][3][0] * ZOOM,
                    house["wind_frame"][3][1] * ZOOM, fill="red", tags="line", width=width_line)
    draw_polyline(cnv, house["door"], "brown", width_line, ZOOM)
    cnv.create_line(house["door"][0][0] * ZOOM, house["door"][0][1] * ZOOM, house["door"][2][0] * ZOOM, house["door"][2][1] * ZOOM,
                    fill="brown", tags="line", width=width_line)
    cnv.create_line(house["door"][1][0] * ZOOM, house["door"][1][1] * ZOOM, house["door"][3][0] * ZOOM, house["door"][3][1] * ZOOM,
                    fill="brown", tags="line", width=width_line)
    draw_polyline(cnv, house["door_handle"], "brown", width_line, ZOOM)

# глубоко копирует домик


def copy_house(house: Dict[str, any]) -> Dict[str, any]:
    copy_house = dict()
    copy_house["center"] = house["center"]
    copy_house["grass"] = [i for i in house["grass"]]
    copy_house["rect"] = [i for i in house["rect"]]
    copy_house["roof"] = [i for i in house["roof"]]
    copy_house["wind"] = {"center": house["wind"]["center"],
                          "a": house["wind"]["a"], "b": house["wind"]["b"]}
    copy_house["wind_frame"] = [i for i in house["wind_frame"]]
    copy_house["door"] = [i for i in house["door"]]
    copy_house["door_handle"] = [i for i in house["door_handle"]]
    return copy_house
