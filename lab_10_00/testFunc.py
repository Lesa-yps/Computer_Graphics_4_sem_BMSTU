import pytest
import tkinter as tk
import subprocess
from typing import Tuple
# Tесты для функции
from Floating_horizon import floating_horizon
from Formula import list_of_func

# константы
SIZE_OF_CANVAS = 800
DIRECTORY_PICTURE = "results"

# преобразует имя тестового файла в текстовую расшифровку


def decode_operation(operation: str) -> None:
    path, filename = operation.rsplit('\\', 1)
    name, func_num, scale_coef = filename.split('_')
    inf_filename = rf"{path}\info_{filename}.txt"
    file = open(inf_filename, "w", encoding='utf-8')
    file.write("Тестируется алгоритм плавающего горизонта.\n")
    file.write(f"Имя теста: '{name}'.\n")
    file.write(f"Функция: {list_of_func[int(func_num)][-1]}.\n",)
    file.write(f"Масштабирование = {scale_coef}.\n",)
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
    canvas.pack()
    # Обновляем окно для правильного отображения размеров холста
    root.update()
    # отрисовка (работа функции)
    func(canvas, *params)
    root.update()
    # после создания PS-файла
    canvas.postscript(file=rf"{filename}.ps", colormode="color")
    # Закрываем окно Tkinter после завершения конвертации
    root.destroy()
    converte_ps_jpg(filename)
    decode_operation(filename)


# алгоритм плавающего горизонта
# floating_horizon
@pytest.mark.parametrize(
    "func_num, x_params, z_params, transform_matrix, color_plane, scale_coef, name",
    # тестовые данные (номер функции, интервалы по x и z, матрица поворотов, цвет плоскости, коэффициент масштабирования)
    [
        pytest.param(0, (-10, 100, 10), (-10, 100, 10), [[0.75, 0.433, -0.5, 0], [-0.22, 0.875, 0.433, 0], [0.63, -0.22, 0.75, 0], [0, 0, 0, 1]], \
                     "#ff0000", 30, "rotate-all-30", id="rotate-all-30")  # y = sin(x) * cos(z) повернут по 30 градусов по всем 3 осям, масштабирование 30
    ]
)
def test_cutting_off_polygon(func_num, x_params, z_params, transform_matrix, color_plane, scale_coef, name) -> None:
    filename = rf"{DIRECTORY_PICTURE}\{name}_{func_num}_{scale_coef}"
    func = list_of_func[func_num][0]
    print("test")
    params = (func, x_params, z_params,
              transform_matrix, color_plane, scale_coef)
    cnv_draw_save(filename, floating_horizon, params)
