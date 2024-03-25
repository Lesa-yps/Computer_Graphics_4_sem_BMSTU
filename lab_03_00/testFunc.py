import tkinter as tk
import subprocess
from typing import Tuple
from Grid import update_grid
# Tесты для функции
from Algo_build_line import build_line, list_algo, X_PART, Y_PART

SIZE_OF_CANVAS = 600
ZOOM = 1
DIRECTORY_PICTURE = "results"
ds = int(SIZE_OF_CANVAS / 2)  # центр рисования

# преобразует имя тестового файла в текстовую расшифровку


def decode_operation(operation: str) -> None:
    parts = (operation.split('\\')[-1]).split('_')
    num_algo = int(parts[0])
    point1 = [i.replace('m', '-') for i in parts[1].split('-')]
    point2 = [i.replace('m', '-') for i in parts[2].split('-')]
    color = parts[3]
    path, name = operation.rsplit('\\', 1)
    filename = rf"{path}\info_{name}.txt"
    file = open(filename, "w", encoding='utf-8')
    file.write("Тестируется " + list_algo[num_algo][1] + '\n')
    file.write("Координаты отрезка:\n")
    file.write(
        f"Начальная точка x = {point1[X_PART]}, y = {point1[Y_PART]}.\n")
    file.write(f"Конечная точка x = {point2[X_PART]}, y = {point2[Y_PART]}.\n")
    file.write(f"Цвет отрезка в 16-ичной системе {color}.")
    file.close()

# конвертирует *.ps файлик в *.jpg


def converte_ps_png(filename: str) -> None:
    cmd = rf"magick {filename}.ps {filename}.jpg"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0]
    print(result.decode('cp866'))

# запускает функцию, которая отрисовывает что-то на холсте, который сохраняется в картинку


def cnv_draw_save(filename: str, func, params: Tuple[any]) -> None:
    # Создаем окно Tkinter
    root = tk.Tk()
    # Создаем холст Tkinter
    canvas = tk.Canvas(root, width=SIZE_OF_CANVAS, height=SIZE_OF_CANVAS)
    # сетка
    update_grid(canvas)
    # сама отрисовка
    func(canvas, *params)
    canvas.pack()
    root.update()
    # после создания нашего PS
    canvas.postscript(file=rf"{filename}.ps", colormode="color")
    # Закрываем окно Tkinter после завершения конвертации
    root.destroy()
    converte_ps_png(filename)
    decode_operation(filename)

# преобразование координат точки в строку для имени файла


def transform_point(point: Tuple[int]) -> str:
    point_str = f"{point[X_PART]}-{point[Y_PART]}".replace('--', '-')
    if point_str[0] == '-':
        point_str = "m" + point_str[1:]
    return point_str


# отрисовка отрезка по его координатам конца и начала
# build_line
def test_build_line() -> None:
    # тестовые точки (массив кортежей (стартовая_точка, конечная_точка, цвет)
    test_points = [((ds, ds), (ds + 100, ds + 100), "#ff0000"),  # отрезок под углом 45 градусов
                   # отрезок параллелен оси y
                   ((ds, ds), (ds, ds + 100), "#ff0000"),
                   # отрезок параллелен оси x
                   ((ds, ds), (ds, ds + 100), "#ff0000"),
                   ((ds - 50, ds - 50), (ds + 50, ds), "#ff0000")]  # отрезок под углом 30 градусов к оси x
    # проходимся по тестовым точкам
    for point_two in test_points:
        point1, point2, color = point_two
        # проходимся по всем алгоритмам
        for num_algo in range(len(list_algo)):
            params = (point1, point2, num_algo, color)
            filename = rf"{DIRECTORY_PICTURE}\{num_algo}_{transform_point(point1)}_{transform_point(point2)}_{color}"
            cnv_draw_save(filename, build_line, params)
