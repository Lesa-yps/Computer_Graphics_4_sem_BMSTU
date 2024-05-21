# Импортируем библиотеки
import tkinter as tk
from typing import Tuple


# константный шаг координатной сетки при ZOOM = 0
STEP_CONST = 50

# высчитывает новые координаты


def new_coord_xy(x: int, y: int, ZOOM: float, SIDE_PLACE: int, HEIGHT_PLACE: int) -> Tuple[int, int]:
    x_res = (int(x) - SIDE_PLACE * STEP_CONST) / ZOOM
    y_res = (int(y) + HEIGHT_PLACE * STEP_CONST) / ZOOM
    return round(x_res), round(y_res)

# вычисляет размеры холста


def calc_size_cnv(canvas: tk.Canvas) -> Tuple[int, int]:
    # Получаем пропорции видимой части холста по x и y
    x_start, x_end = canvas.xview()
    y_start, y_end = canvas.yview()
    # Получаем размеры холста
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    # Вычисляем координаты видимой части холста
    X_SIZE = x_end * canvas_width - x_start * canvas_width
    Y_SIZE = y_end * canvas_height - y_start * canvas_height
    return X_SIZE, Y_SIZE

# перерисовывает координатную сетку (с помощью других функций)


def update_grid(cnv: tk.Canvas, ZOOM: float = 1, SIDE_PLACE: int = 0, HEIGHT_PLACE: int = 0) -> None:
    X_SIZE, Y_SIZE = calc_size_cnv(cnv)
    if X_SIZE == 1 and Y_SIZE == 1:
        X_SIZE = Y_SIZE = 1000
    # Очищаем старую координатную сетку
    clear_grid(cnv)
    # Рисуем новую координатную сетку
    draw_grid(cnv, STEP_CONST, ZOOM, SIDE_PLACE, HEIGHT_PLACE, X_SIZE, Y_SIZE)

# удаляет координатнную сетку


def clear_grid(cnv: tk.Canvas) -> None:
    # Очистка всех объектов с тегом "grid"
    cnv.delete("grid")

# рисует координатную сетку по x


def draw_x_grid(canvas: tk.Canvas, step: int, x_start: int, x_end: int, y_start: int, y_end: int) -> None:
    x = round(step)
    while x <= round(x_end + step):
        canvas.create_line(x, round(
            y_start - step), x, round(y_end + step), fill="gray", dash=(2, 2), tags="grid")
        x += round(step)
    x = round(-step)
    while x >= round(x_start - step):
        canvas.create_line(x, round(
            y_start - step), x, round(y_end + step), fill="gray", dash=(2, 2), tags="grid")
        x -= round(step)

# рисует координатную сетку по y


def draw_y_grid(canvas: tk.Canvas, step: int, x_start: int, x_end: int, y_start: int, y_end: int) -> None:
    y = round(step)
    while y <= round(y_end + step):
        canvas.create_line(round(x_start - step), y, round(x_end + step),
                           y, fill="gray", dash=(2, 2), tags="grid")
        y += round(step)
    y = round(-step)
    while y >= round(y_start - step):
        canvas.create_line(round(x_start - step), y, round(x_end + step),
                           y, fill="gray", dash=(2, 2), tags="grid")
        y -= round(step)

# рисует координатную сетку


def draw_grid(canvas: tk.Canvas, step: int, ZOOM: float, SIDE_PLACE: int, HEIGHT_PLACE: int,
              X_SIZE: int, Y_SIZE: int) -> None:
    x_start = 0 - SIDE_PLACE * step
    y_start = 0 + HEIGHT_PLACE * step
    step *= ZOOM
    if (ZOOM > 1):
        x_end = X_SIZE * 2
        y_end = Y_SIZE * 2
    else:
        x_end, y_end = new_coord_xy(
            X_SIZE, Y_SIZE, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
    canvas.create_line(0, round(y_start - step), 0, round(y_end + step),
                       fill="black", dash=(2, 2), tags="grid", width=3)
    canvas.create_line(round(x_start - step), 0, round(x_end + step),
                       0, fill="black", dash=(2, 2), tags="grid", width=3)
    draw_x_grid(canvas, step, x_start, x_end, y_start, y_end)
    draw_y_grid(canvas, step, x_start, x_end, y_start, y_end)
