import math
import tkinter as tk
from typing import Dict, List, Tuple


# генерирует 720 точек по окружности
def generate_circle_points(center_x: int, center_y: int, radius: int) -> List[Tuple[int, int]]:
    circle_points = []
    angle_degrees = 0
    while angle_degrees < 360:
        # Преобразование угла из градусов в радианы
        angle_radians = math.radians(angle_degrees)
        # Вычисление координат точки на окружности
        x = center_x + radius * math.cos(angle_radians)
        y = center_y + radius * math.sin(angle_radians)
        circle_points.append((x, y))
        angle_degrees += 0.5
    return circle_points

# стартовое создание домика
def build_start_house() -> Dict[str, any]:
    house = dict()
    house["center"] = (0, 0)
    house["grass"] = [(-150, 80), (150, 80)]
    house["rect"] = [(-100, 80), (-100, -20), (100, -20), (100, 80)]
    house["roof"] = [(-120, -20), (-100, -80), (100, -80), (120, -20)]
    house["wind"] = {"center": (50, 20), "radius": 20, "points": generate_circle_points(50, 20, 20)}
    house["wind_frame"] = [(30, 20), (50, 0), (70, 20), (50, 40)]
    house["door"] = [(-80, 80), (-80, 0), (-20, 0), (-20, 80)]
    house["door_handle"] = [(-35, 50), (-35, 30), (-25, 30), (-25, 50)]
    return house

# рисует ломаную прямую по массиву кортежей-точек
def draw_polyline(cnv: tk.Canvas, arr_tuple: List[Tuple[int, int]], color: str, width_line: int, ZOOM: int, is_closed: bool = True) -> None:
    coords = [coord * ZOOM for point in arr_tuple for coord in point] + [arr_tuple[0][0] * ZOOM, arr_tuple[0][1] * ZOOM]
    cnv.create_line(coords, fill=color, tags="line", width=width_line)

# рисует овал
def draw_oval(cnv: tk.Canvas, wind: Dict[str, any], width_line: int, color: str, ZOOM: float) -> None:
    for i in range(len(wind["points"])):
        x1, y1 = wind["points"][i]
        x2, y2 = wind["points"][(i + 1) % len(wind["points"])]
        cnv.create_line(x1 * ZOOM, y1 * ZOOM, x2 * ZOOM, y2 * ZOOM, fill=color, tags="line", width=width_line)

# удаляет старую отрисовку домика
def delete_house(cnv: tk.Canvas) -> None:
    cnv.delete("line")
    cnv.delete("coordinates")
    cnv.delete("point")

# отрисовка домика
def draw_house(cnv: tk.Canvas, house: Dict[str, any], ZOOM: float) -> None:
    delete_house(cnv)
    width_line = 2
    label = "({:}, {:})".format(int(house["center"][0]), int(house["center"][1]))
    cnv.create_text(house["center"][0] * ZOOM, house["center"][1] * ZOOM, text=label, anchor="sw", tags="coordinates")
    cnv.create_oval(house["center"][0] * ZOOM - width_line, house["center"][1] * ZOOM - width_line, house["center"][0] * ZOOM + width_line,\
                    house["center"][1] * ZOOM + width_line, fill = "red", outline = "black", tags="point")
    draw_polyline(cnv, house["grass"], "green", width_line, ZOOM)
    draw_polyline(cnv, house["rect"], "blue", width_line, ZOOM)
    draw_polyline(cnv, house["roof"], "blue", width_line, ZOOM)
    draw_oval(cnv, house["wind"], width_line, "red", ZOOM)
    cnv.create_line(house["wind_frame"][0][0] * ZOOM, house["wind_frame"][0][1] * ZOOM, house["wind_frame"][2][0] * ZOOM,\
                    house["wind_frame"][2][1] * ZOOM, fill="red", tags="line", width=width_line)
    cnv.create_line(house["wind_frame"][1][0] * ZOOM, house["wind_frame"][1][1] * ZOOM, house["wind_frame"][3][0] * ZOOM,\
                    house["wind_frame"][3][1] * ZOOM, fill="red", tags="line", width=width_line)
    draw_polyline(cnv, house["door"], "brown", width_line, ZOOM)
    cnv.create_line(house["door"][0][0] * ZOOM, house["door"][0][1] * ZOOM, house["door"][2][0] * ZOOM, house["door"][2][1] * ZOOM,\
                    fill="brown", tags="line", width=width_line)
    cnv.create_line(house["door"][1][0] * ZOOM, house["door"][1][1] * ZOOM, house["door"][3][0] * ZOOM, house["door"][3][1] * ZOOM,\
                    fill="brown", tags="line", width=width_line)
    draw_polyline(cnv, house["door_handle"], "brown", width_line, ZOOM)

# глубоко копирует домик
def copy_house(house: Dict[str, any]) -> Dict[str, any]:
    copy_house = dict()
    copy_house["center"] = house["center"]
    copy_house["grass"] = [i for i in house["grass"]]
    copy_house["rect"] = [i for i in house["rect"]]
    copy_house["roof"] = [i for i in house["roof"]]
    copy_house["wind"] = {"center": house["wind"]["center"], "radius": house["wind"]["radius"], "points": [i for i in house["wind"]["points"]]}
    copy_house["wind_frame"] = [i for i in house["wind_frame"]]
    copy_house["door"] = [i for i in house["door"]]
    copy_house["door_handle"] = [i for i in house["door_handle"]]
    return copy_house
