from tkinter import ttk
from typing import List, Tuple

# Очистка таблицы


def cleaning_table(tree: ttk.Treeview) -> None:
    # Получаем все элементы таблицы
    items = tree.get_children()
    # Удаляем каждый элемент из таблицы
    for item in items:
        tree.delete(item)

# формирование многоугольника из таблицы


def make_polygon(tree_polygon: ttk.Treeview) -> List[Tuple[int]]:
    polygon = list()
    for item in tree_polygon.get_children():
        x = int(tree_polygon.item(item, "values")[0])
        y = int(tree_polygon.item(item, "values")[1])
        if len(polygon) == 0 or polygon[-1] != (x, y):
            polygon.append((x, y))
    if len(polygon) > 1 and polygon[-1] == polygon[0]:
        polygon.pop()
    return polygon
