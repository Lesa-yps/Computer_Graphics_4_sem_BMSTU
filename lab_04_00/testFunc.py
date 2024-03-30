import tkinter as tk
import subprocess
from typing import Tuple
from Grid import update_grid
# Tесты для функции
from Algo_build_curve import build_curve, list_algo

# константы
X_PART = 0
Y_PART = 1
SIZE_OF_CANVAS = 600
DIRECTORY_PICTURE = "results"
DS = int(SIZE_OF_CANVAS / 2)  # центр рисования

# преобразует имя тестового файла в текстовую расшифровку


def decode_operation(operation: str) -> None:
    parts = (operation.split('\\')[-1]).split('_')
    num_algo = int(parts[0])
    cir_or_ell = int(parts[1])
    center = [i.replace('m', '-') for i in parts[2].split('-')]
    if cir_or_ell == 0:
        R = parts[3].replace('m', '-')
    else:
        a, b = [i.replace('m', '-') for i in parts[3].split('-')]
    color = parts[4]
    path, name = operation.rsplit('\\', 1)
    filename = rf"{path}\info_{name}.txt"
    file = open(filename, "w", encoding='utf-8')
    file.write("Тестируется " + list_algo[num_algo][2] + '\n')
    if cir_or_ell == 0:
        file.write("Строится окружность.\n")
    else:
        file.write("Строится эллипс.\n")
    file.write(
        f"Центральная точка x = {center[X_PART]}, y = {center[Y_PART]}.\n")
    if cir_or_ell == 0:
        file.write(f"Радиус = {R}.\n")
    else:
        file.write(f"Полуоси по абсциссе (a) = {a}, по ординате (b) = {b}.\n")
    file.write(f"Цвет фигуры в 16-ичной системе {color}.")
    file.close()

# конвертирует *.ps файлик в *.jpg


def converte_ps_jpg(filename: str) -> None:
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
    converte_ps_jpg(filename)
    decode_operation(filename)

# преобразование координат точки в строку для имени файла


def transform_point(point: Tuple[int]) -> str:
    point_str = f"{point[X_PART]}-{point[Y_PART]}".replace('--', '-')
    if point_str[0] == '-':
        point_str = "m" + point_str[1:]
    return point_str


# отрисовка отрезка по его координатам конца и начала
# build_curve
def test_build_curve() -> None:
    # тестовые точки: массив кортежей (центральная_точка, окружность_или_эллипс (0 - окружность / 1 - эллипс), \
    # радиус или (полуось_по_х, полуось_по_y), цвет)
    test_points = [((DS, DS), 0, 100, "#ff0000"),  # красная окружность R = 100
                   # зелёный эллипс a = 100 b = 50
                   ((DS, DS), 1, (100, 50), "#00ff00"),
                   # синий эллипс a = 50 b = 100
                   ((DS, DS), 1, (50, 100), "#0000ff")]
    # проходимся по тестовым точкам
    for point_two in test_points:
        if point_two[1] == 0:
            center, cir_or_ell, R, color = point_two
        else:
            center, cir_or_ell, axes, color = point_two
        # проходимся по всем алгоритмам
        for num_algo in range(len(list_algo)):
            # print(center, R, axes, num_algo, cir_or_ell, color)
            if cir_or_ell == 0:
                params = ((*center, R), num_algo, cir_or_ell, color)
            else:
                params = ((*center, *axes), num_algo, cir_or_ell, color)
            filename = rf"{DIRECTORY_PICTURE}\{num_algo}_{cir_or_ell}_{transform_point(center)}"
            if cir_or_ell == 0:
                filename += f"_{str(R).replace('-', 'm')}_{color}"
            else:
                filename += f"_{transform_point(axes)}_{color}"
            cnv_draw_save(filename, build_curve, params)
