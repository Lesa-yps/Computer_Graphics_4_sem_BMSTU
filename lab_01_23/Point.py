# Импортируем библиотеки
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from typing import List, Tuple
from Draw_res_triangle import same_turple, iterate_points
from Grid import new_coord_xy

# проверка что точка есть в массиве
def point_in_table(arr: List[Tuple[int, int]], point: Tuple[int, int]) -> int:
    for i in arr:
        if same_turple(i, point):
            return 1
    return 0

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

# удаляет все линии и подписи точек от результата
def clean_res(cnv: tk.Canvas) -> None:
    text_objects = cnv.find_withtag("coordinates")
    #print(text_objects)
    for text_object in text_objects:
        cnv.delete(text_object)
    cnv.delete("line")

# удаляет выделенную в таблице точку
def del_point(cnv: tk.Canvas, tree: ttk.Treeview, ZOOM: int, SIDE_PLACE: int, HEIGHT_PLACE: int) -> None:
    # достаём выделенное значение из таблицы
    selected_item = tree.selection()
    if selected_item:
        for item_id in selected_item:
            item = tree.item(item_id)
            x_table = item['values'][0]  # Получаем значение x_table
            y_table = item['values'][1]  # Получаем значение y_table
            tree.delete(item_id)  # Удаляем элемент из Treeview
        # Получаем все объекты с тегом "point"
        point_objects = cnv.find_withtag("point")
        # Проходимся по найденным объектам и удаляем их
        for obj in point_objects:
            cnv.delete(obj)
            # Получаем все элементы из таблицы
        items = tree.get_children()
        # Проходимся по каждому элементу и отрисовываем его на холсте
        for item in items:
            # Получаем координаты точки из таблицы
            x_table = int(tree.item(item, "values")[0])
            y_table = int(tree.item(item, "values")[1])
            # Отрисовываем точку на холсте
            touch(x_table, y_table, cnv, tree, ZOOM, SIDE_PLACE, HEIGHT_PLACE, change_coord=False, check_in_table=False)
    else:
        mb.showerror('Ошибка!', "Точка для удаления не выбрана.")

# проверяет заполнены ли поля ввода координат числами
def check_input_field(x_entry: tk.Entry, y_entry: tk.Entry) -> bool:
    try:
        int_x, int_y = int(x_entry.get()), int(y_entry.get())
    except ValueError:
        mb.showerror('Ошибка!', "Оба поля координат должны быть заполнены.")
        return False
    else:
        return True

# проверяет данные для редактирования точки
def check_edited_point(x_entry: tk.Entry, y_entry: tk.Entry, tree: ttk.Treeview) -> bool:
    # достаём выделенное значение из таблицы
    selected_item = tree.selection()
    if not selected_item:
        mb.showerror('Ошибка!', "Точка для редактирования не выбрана.")
    else:
        if check_input_field(x_entry, y_entry):
            # проверяем есть ли уже добавляемая точка
            arr = iterate_points(tree)
            if point_in_table(arr, (int(x_entry.get()), int(y_entry.get()))):
                mb.showerror('Ошибка!', "Такая точка уже существует.")
            else:
                return True
    return False
