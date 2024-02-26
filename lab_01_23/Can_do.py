# Импортируем библиотеки
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from typing import List, Tuple
from Mozg import brain, iterate_points, same_turple, new_coord_xy, STEP_CONST

# вычисляет размеры холста
def calc_size_cnv(canvas: tk.Canvas) -> Tuple[int, int]:
    # Получаем пропорции видимой части холста по x и y
    x_start, x_end = canvas.xview()
    y_start, y_end = canvas.yview()
    # Получаем размеры холста
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    #print(x_start, x_end, y_start, y_end, canvas_width, canvas_height)
    # Вычисляем координаты видимой части холста
    X_SIZE = x_end * canvas_width - x_start * canvas_width
    Y_SIZE = y_end * canvas_height - y_start * canvas_height
    return X_SIZE, Y_SIZE

# проверка что точка есть в массиве
def point_in_table(arr: List[Tuple[int, int]], point: Tuple[int, int]) -> int:
    for i in arr:
        if same_turple(i, point):
            return 1
    return 0

# перерисовывает координатную сетку (с помощью других функций)
def update_grid(cnv: tk.Canvas, ZOOM: int = 1, SIDE_PLACE: int = 0, HEIGHT_PLACE: int = 0) -> None:
    X_SIZE, Y_SIZE = calc_size_cnv(cnv)
    if X_SIZE == 1 and Y_SIZE == 1:
        X_SIZE = Y_SIZE = 1000
    #print(X_SIZE, Y_SIZE)
    # Очищаем старую координатную сетку
    clear_grid(cnv)
    # Рисуем новую координатную сетку
    draw_grid(cnv, STEP_CONST, ZOOM, SIDE_PLACE, HEIGHT_PLACE, X_SIZE, Y_SIZE)  # Подставьте вашу функцию рисования сетки и нужные параметры

# удаляет координатнную сетку
def clear_grid(cnv: tk.Canvas) -> None:
    # Очистка всех объектов с тегом "grid" (предполагается, что сетка нарисована с этим тегом)
    cnv.delete("grid")

# рисует координатную сетку
def draw_grid(canvas: tk.Canvas, step: int, ZOOM: int, SIDE_PLACE: int, HEIGHT_PLACE: int,\
              X_SIZE: int, Y_SIZE: int) -> None:
    x_start = 0 - SIDE_PLACE * step
    y_start = 0 + HEIGHT_PLACE * step
    step *= ZOOM
    if (ZOOM > 1):
        x_end = X_SIZE * 2
        y_end = Y_SIZE * 2
    else:
        x_end, y_end = new_coord_xy(X_SIZE, Y_SIZE, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
    #print(step, ZOOM, SIDE_PLACE, HEIGHT_PLACE, X_SIZE, Y_SIZE, x_start, x_end, "x_s =", int(x_start - step),\
          #"x_e =", int(x_end + step), "step =", int(step))
    canvas.create_line(0, round(y_start - step), 0, round(y_end + step), fill="black", dash=(2, 2), tags="grid", width = 3)
    canvas.create_line(round(x_start - step), 0, round(x_end + step), 0, fill="black", dash=(2, 2), tags="grid", width = 3)
    x = round(step)
    while x <= round(x_end + step):
        canvas.create_line(x, round(y_start - step), x, round(y_end + step), fill="gray", dash=(2, 2), tags="grid")
        x += round(step)
    x = round(-step)
    while x >= round(x_start - step):
        canvas.create_line(x, round(y_start - step), x, round(y_end + step), fill="gray", dash=(2, 2), tags="grid")
        x -= round(step)
    y = round(step)
    while y <= round(y_end + step):
        canvas.create_line(round(x_start - step), y, round(x_end + step), y, fill="gray", dash=(2, 2), tags="grid")
        y += round(step)
    y = round(-step)
    while y >= round(y_start - step):
        canvas.create_line(round(x_start - step), y, round(x_end + step), y, fill="gray", dash=(2, 2), tags="grid")
        y -= round(step)


# удаляет все линии и подписи точек от результата
def clean_res(cnv: tk.Canvas) -> None:
    text_objects = cnv.find_withtag("coordinates")
    #print(text_objects)
    for text_object in text_objects:
        cnv.delete(text_object)
    cnv.delete("line")


# В ответ на нажатие левой кнопкой мышки отрисовывается точка
def touch(x_input: int, y_input: int, cnv: tk.Canvas, tree: ttk.Treeview, ZOOM: int, SIDE_PLACE: int, HEIGHT_PLACE: int,\
          change_coord: bool = True, check_in_table: bool = True) -> None:
    if change_coord:
        x_table, y_table = new_coord_xy(x_input, y_input, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
        x_input, y_input = x_table * ZOOM, y_table * ZOOM
    else:
        x_table, y_table = x_input, y_input
        #x_input, y_input = new_coord_xy(x_input, y_input, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
        x_input, y_input = x_input * ZOOM, y_input * ZOOM
    #print(x_input, y_input, x_table, y_table, ZOOM)
    clean_res(cnv)
    # проверяем есть ли уже добавляемая точка
    arr = iterate_points(tree)
    if point_in_table(arr, (x_table, y_table)) and check_in_table:
        mb.showerror('Ошибка!', "Такая точка уже существует.")
    else:
        if check_in_table:
            tree.insert("", "end", values=(x_table, y_table))
        weight = 4 * ZOOM
        cnv.create_oval(x_input - weight, y_input - weight, x_input + weight, y_input + weight, fill = "red", outline = "red", tags="point")
        cnv.create_oval(x_input - ZOOM, y_input - ZOOM, x_input + ZOOM, y_input + ZOOM, fill = "black", outline = "black", tags="point")
