import pytest
import tkinter as tk
import subprocess
from typing import Tuple, List
# Tесты для функции
from Cutting_off_polygon import cutting_off_polygon

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
        f"Тестируется отсечение многоугольника произвольным выпуклым отсекателем '{name_test}'.\n")
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
    # отрисовка (работа функции)
    func(canvas, *params)
    canvas.pack()
    root.update()
    # после создания PS-файла
    canvas.postscript(file=rf"{filename}.ps", colormode="color")
    # Закрываем окно Tkinter после завершения конвертации
    root.destroy()
    converte_ps_jpg(filename)
    decode_operation(filename)

# отсечение многоугольника по всем сторонам отсекателя
# cutting_off_polygon


@pytest.mark.parametrize(
    "polygon, clipper, name",
    # тестовые данные (массив линий - координаты отсекателя - название теста)
    [
        pytest.param([(DS/2, DS/2), (DS*5/4, DS/2), (DS*5/4, DS*5/4), (DS/2, DS*5/4)], \
                     [(DS*3/4, DS*3/4), (DS*3/4, DS*3/2), (DS*3/2, DS*3/2), (DS*3/2, DS*3/4)], \
                     "partially_visible", id="partially_visible"),  # частично видимый многоугольник
        pytest.param([(DS/2, DS/2), (DS*3/4, DS/2), (DS*3/4, DS*3/4), (DS/2, DS*3/4)], \
                     [(DS*5/4, DS*5/4), (DS*5/4, DS*3/2), (DS*3/2, DS*3/2), (DS*3/2, DS*5/4)], \
                     "invisible", id="invisible"),  # невидимый многоугольник
        pytest.param([(DS*3/4, DS*3/4), (DS*3/4, DS*5/4), (DS*5/4, DS*5/4), (DS*5/4, DS*3/4)], \
                     [(DS/2, DS/2), (DS/2, DS*3/2), (DS*3/2, DS*3/2), (DS*3/2, DS/2)], \
                     "visible", id="visible"),  # видимый многоугольник
    ]
)
def test_cutting_off_polygon(polygon: List[Tuple[int]], clipper: List[Tuple[int]], name: str) -> None:
    arr_colors = ["#0000ff", "#808080", "#ff0000"]
    def_zoom = 1
    filename = rf"{DIRECTORY_PICTURE}\{name}"
    params = (polygon, clipper, arr_colors, def_zoom)
    cnv_draw_save(filename, cutting_off_polygon, params)
