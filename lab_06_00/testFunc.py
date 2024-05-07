import tkinter as tk
import subprocess
from typing import Tuple, List
# Tесты для функции
from Paint_over_figure_seed import paint_over_figure
from Grid import X_PART, Y_PART
from Point import draw_line


# константы
SIZE_OF_CANVAS = 40
DIRECTORY_PICTURE = "results"
DS = int(SIZE_OF_CANVAS / 2)  # центр рисования

# преобразует имя тестового файла в текстовую расшифровку


def decode_operation(operation: str) -> None:
    name_test, point_seed, color, timeout = (
        operation.split('\\')[-1]).split('_')
    point_seed = [i.replace('m', '-') for i in point_seed.split('-')]
    path, filename = operation.rsplit('\\', 1)
    inf_filename = rf"{path}\info_{filename}.txt"
    file = open(inf_filename, "w", encoding='utf-8')
    file.write(f"Тестируется закраска фигуры '{name_test}'.\n")
    file.write(
        f"Координаты затравки x = {point_seed[X_PART]}, y = {point_seed[Y_PART]}.\n")
    file.write(f"Цвет закраски в 16-ичной системе {color}.\n")
    file.write(f"Задержка закраски = {timeout}.")
    file.close()

# конвертирует *.ps файлик в *.jpg


def converte_ps_jpg(filename: str) -> None:
    cmd = rf"magick {filename}.ps {filename}.jpg"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0]
    print(result.decode('cp866'))

# рисует границы


def draw_borders(cnv: tk.Canvas, edges_mat: List[List[Tuple[int]]]) -> None:
    # проходимся по всем замкнутым фигурам
    for fig in edges_mat:
        # проходимся по всем точкам замкнутой фигуры
        count_points_fig = len(fig)
        if count_points_fig > 1:
            for i in range(count_points_fig + 1):
                fig1 = fig[:i]
                # print(fig[i % count_points_fig], edges_mat, fig)
                x, y = fig[i % count_points_fig]
                draw_line(cnv, x, y, fig1)

# запускает функцию, которая отрисовывает что-то на холсте, который сохраняется в картинку


def cnv_draw_save(filename: str, func, params: Tuple[any], pre_func, pre_params: List[int]) -> None:
    # Создаем окно Tkinter
    root = tk.Tk()
    # Создаем холст Tkinter
    canvas = tk.Canvas(root, width=SIZE_OF_CANVAS, height=SIZE_OF_CANVAS)
    # подготовка (отрисовка линий)
    pre_func(canvas, pre_params)
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

# задаёт координаты квадрата по центру и длине стороны


def make_square(center: Tuple[int], side: int) -> List[Tuple[int]]:
    half_side = round(side / 2)
    point1 = (center[X_PART] - half_side, center[Y_PART] - half_side)
    point2 = (center[X_PART] + half_side, center[Y_PART] - half_side)
    point3 = (center[X_PART] + half_side, center[Y_PART] + half_side)
    point4 = (center[X_PART] - half_side, center[Y_PART] + half_side)
    return [point1, point2, point3, point4]

# преобразование координат точки в строку для имени файла


def transform_point(point: Tuple[int]) -> str:
    point_str = f"{point[X_PART]}-{point[Y_PART]}".replace('--', '-')
    if point_str[0] == '-':
        point_str = "m" + point_str[1:]
    return point_str

# отрисовка отрезка по его координатам конца и начала
# paint_over_figure


def test_paint_over_figure() -> None:
    # тестовые данные: массив координат точек фигур, цвет фигуры, задержка и краткое пояснение результата
    big_square = make_square((DS, DS), DS)
    little_square = make_square((DS, DS), DS / 2)
    triangle = [(DS/2, DS/2), (DS/2, DS*3/2), (DS*3/2, DS*3/2)]
    shorts = [(DS/2, DS/2), (DS/2, DS*3/2), (DS*3/4, DS*3/2), (DS*3/4, DS),
              (DS*5/4, DS), (DS*5/4, DS*3/2), (DS*3/2, DS*3/2), (DS*3/2, DS/2)]
    test_data = [((DS, DS), [big_square], "#ff0000", 0, "square"),  # красный квадрат (затравка внутри)
                 # зелёный треугольник (затравка снаружи)
                 ((DS/2, DS/2), [triangle], "#00ff00", 0, "triangle"),
                 ((DS*5/4, DS*5/4), [big_square, little_square], "#0000ff", 0,
                  "square-with-a-hole"),  # синий квадрат с дыркой (затравка внутри)
                 ((DS/2, DS/2), [shorts], "#ff0000", 0, "shorts")]  # красные шорты (затравка снаружи)
    # проходимся по тестовым данным
    for data in test_data:
        point_seed, edges_mat, color_draw, timeout, name = data
        filename = rf"{DIRECTORY_PICTURE}\{name}_{transform_point(point_seed)}_{color_draw}_{timeout}"
        params = data[:-1]
        cnv_draw_save(filename, paint_over_figure,
                      params, draw_borders, edges_mat)
