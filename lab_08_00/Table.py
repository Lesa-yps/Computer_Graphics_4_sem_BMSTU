from tkinter import ttk
from typing import Optional, List, Tuple

# Очистка таблицы
def cleaning_table(tree: ttk.Treeview) -> None:
    # Получаем все элементы таблицы
    items = tree.get_children()
    # Удаляем каждый элемент из таблицы
    for item in items:
        tree.delete(item)

# достаёт точку по индексу из таблицы
def get_ind_point(tree: ttk.Treeview, ind: int) -> Optional[Tuple[int, int]]:
    children = tree.get_children("")  # Получаем всех дочерних элементов корня
    if children:  # Проверяем, есть ли дочерние элементы
        id = children[ind]  # Получаем идентификатор элемента по индексу
        values = tree.item(id)["values"]  # Получаем значения элемента
        if values:  # Проверяем, есть ли значения
            return tuple(map(int, values))  # Преобразуем значения в кортеж целых чисел
    return None  # Возвращаем None, если таблица пуста или нет значений в элементе


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