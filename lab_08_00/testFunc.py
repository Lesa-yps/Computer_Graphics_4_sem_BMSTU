import pytest
import tkinter as tk
import subprocess
from typing import Tuple, List
# Tесты для функции
from Cutting_off_lines_any_convex import cutting_off_all_lines
from Const import X_PART, Y_PART

# константы
SIZE_OF_CANVAS = 500
DIRECTORY_PICTURE = "results"
DS = int(SIZE_OF_CANVAS / 2)  # центр рисования

# преобразует имя тестового файла в текстовую расшифровку


def decode_operation(operation: str) -> None:
    name_test = operation.split('\\')[-1]
    path, filename = operation.rsplit('\\', 1)
    inf_filename = rf"{path}\info_{filename}.txt"
    file = open(inf_filename, "w", encoding='utf-8')
    file.write(
        f"Тестируется отсечение линий произвольным выпуклым отсекателем '{name_test}'.\n")
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

# отсечение по всем линиям
# cutting_off_all_lines


@pytest.mark.parametrize(
    "line_arr, clipper, name",
    # тестовые данные (массив линий - координаты отсекателя - название теста)
    [
        pytest.param([[(DS/2, DS/2), (DS, DS)]], [(0, 0), (0, DS*3/2), (DS*3/2, DS*3/2), (DS*3/2, 0)], \
                     "line-is-visible", id="line-is-visible"),  # линия видимая
        pytest.param([[(DS/2, 0), (DS/2, DS*3/2)]], [(DS, 0), (DS, DS*3/2), (DS*3/2, DS*3/2), (DS*3/2, 0)], \
                     "line-is-invisible", id="line-is-invisible"),  # линия невидимая
        pytest.param([[(0, 0), (DS, DS)]], [(DS/2, DS/2), (DS/2, DS*3/2), (DS*3/2, DS*3/2), (DS*3/2, DS/2)], \
                     "line-is-partially-visable", id="line-is-partially-visable")  # линия частично видимая
    ]
)
def test_cutting_off_all_lines(line_arr: List[List[Tuple[int]]], clipper: List[Tuple[int]], name: str) -> None:
    arr_colors = ["#0000ff", "#808080", "#ff0000"]
    def_zoom = 1
    filename = rf"{DIRECTORY_PICTURE}\{name}"
    params = (line_arr, clipper, arr_colors, def_zoom)
    cnv_draw_save(filename, cutting_off_all_lines, params)
