from tkinter import ttk
from typing import List, Tuple

# Очистка таблицы


def cleaning_table(tree: ttk.Treeview) -> None:
    # Получаем все элементы таблицы
    items = tree.get_children()
    # Удаляем каждый элемент из таблицы
    for item in items:
        tree.delete(item)

# формирование отсекателя


def make_clipper(tree_clipper: ttk.Treeview) -> List[Tuple[int]]:
    clipper = list()
    for item in tree_clipper.get_children():
        x = int(tree_clipper.item(item, "values")[0])
        y = int(tree_clipper.item(item, "values")[1])
        if len(clipper) == 0 or clipper[-1] != (x, y):
            clipper.append((x, y))
    if len(clipper) != 0 and clipper[-1] == clipper[0]:
        clipper.pop()
    return clipper

# формирование массива линий из таблицы


def make_line_arr(tree_line: ttk.Treeview) -> List[List[Tuple[int]]]:
    line_arr = list()
    for item in tree_line.get_children():
        points = list()
        for i in range(4):
            points.append(int(tree_line.item(item, "values")[i]))
        line_arr.append([(points[0], points[1]), (points[2], points[3])])
    return line_arr
