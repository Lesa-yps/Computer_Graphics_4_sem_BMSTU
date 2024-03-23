import tkinter as tk
import subprocess
# Tесты для функций
from Geometric_transforms import brain_turn_house, brain_scale_house, brain_move_house, same_tuple
from House import constructor_house, draw_house
from typing import Tuple, Dict, Any

SIZE_OF_CANVAS = 500
ZOOM = 1
DIRECTORY_PICTURE = "results"
ds = SIZE_OF_CANVAS / 2.0  # центр фигуры

# преобразует имя тестового файла в текстовую расшифровку


def decode_operation(operation: str) -> None:
    parts = operation.split('_')
    action = parts[0]
    params = [i.replace('m', ' - ').replace('p', ' + ')
              for i in parts[1].split('-')]
    filename = rf"{DIRECTORY_PICTURE}\info_{operation}.txt"
    file = open(filename, "w", encoding='utf-8')
    if action == 'scale':
        file.write("Тестируется масштабирование фигуры.\n")
        file.write(
            f"Коэффициенты масштабирования фигуры kx = {params[0]}, ky = {params[1]}.\n")
        coords_center = parts[2].replace(
            '-', ', ').replace('m', ' - ').replace('p', ' + ').replace('c', 'центр_фигуры')
        file.write(f"Центр масштабирования фигуры = ({coords_center}).\n")
    elif action == 'turn':
        file.write("Тестируется поворот фигуры.\n")
        file.write(f"Угол поворота фигуры = {params[0]} градусов.\n")
        coords_center = parts[2].replace(
            '-', ', ').replace('m', ' - ').replace('p', ' + ').replace('c', 'центр_фигуры')
        file.write(f"Центр поворота фигуры = ({coords_center}).\n")
    elif action == 'move':
        file.write("Тестируется перемещение фигуры.\n")
        file.write(
            f"Коэффициенты перемещения фигуры dx = {params[0]}, dy = {params[1]}.\n")
    else:
        raise ValueError(f"Unknown action: {action}")
    file.close()

# конвертирует *.ps файлик в *.png


def converte_ps_png(filename: str) -> None:
    cmd = rf"magick {filename}.ps {filename}.jpg"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0]
    print(result.decode('cp866'))

# отрисовывает домик и сохраняет его


def draw_house_save(house: Dict[str, Any], filename: str) -> None:
    # Создаем окно Tkinter
    root = tk.Tk()
    # Создаем холст Tkinter
    canvas = tk.Canvas(root, width=SIZE_OF_CANVAS, height=SIZE_OF_CANVAS)
    draw_house(canvas, house, ZOOM)
    canvas.pack()
    root.update()
    # после создания нашего PS
    canvas.postscript(file=rf"{filename}.ps", colormode="color")
    # Закрываем окно Tkinter после завершения конвертации
    root.destroy()
    converte_ps_png(filename)

# запускает отрисовку стартового домика, прогоняет его через переданную функцию, затем запускает отрисовку итогового домика


def save_draw_test_house(dict_house: Dict[str, Any], func, param: Tuple[any], filename: str) -> Dict[str, Any]:
    draw_house_save(dict_house, rf"{DIRECTORY_PICTURE}\in_{filename}")
    dict_house_res = func(param, dict_house)
    draw_house_save(dict_house_res, rf"{DIRECTORY_PICTURE}\out_{filename}")
    decode_operation(filename)
    return dict_house_res

# сравнивае домики по ключевым параметрам


def cmp_control(house1: Dict[str, Any], house2: Dict[str, Any]) -> bool:
    res = same_tuple(house1["center"], house2["center"]) * same_tuple(house1["rect"][0], house2["rect"][0])\
        * same_tuple(house1["rect"][-1], house2["rect"][-1])
    return res

# поворот
# brain_turn_house


def test_brain_turn_house() -> None:
    # угол = 90, x_center = ds, y_center = ds
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_turn_house, (90, ds, ds), "turn_90_c-c")
    dict_house_right = constructor_house(
        (ds, ds), (80 + ds, 100 + ds), (80 + ds, -100 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # угол = 180, x_center = ds, y_center = ds
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_turn_house, (180, ds, ds), "turn_180_c-c")
    dict_house_right = constructor_house(
        (ds, ds), (100 + ds, -80 + ds), (-100 + ds, -80 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # угол = 360, x_center = ds, y_center = ds
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_turn_house, (360, ds, ds), "turn_360_c-c")
    dict_house_right = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # угол = 0, x_center = ds, y_center = ds
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_turn_house, (0, ds, ds), "turn_0_c-c")
    dict_house_right = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # угол = 90, x_center = ds+50, y_center = ds+50
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_turn_house, (90, ds+50, ds+50), "turn_90_cp50-cp50")
    dict_house_right = constructor_house(
        (ds, 100 + ds), (80 + ds, 200 + ds), (80 + ds, ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # угол = -90, x_center = ds-50, y_center = ds+50
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_turn_house, (-90, ds-50, ds+50), "turn_m90_cm50-cp50")
    dict_house_right = constructor_house(
        (ds, 100 + ds), (-80 + ds, ds), (-80 + ds, 200 + ds))
    assert cmp_control(dict_house_right, dict_house_res)

# масштабирование
# brain_scale_house


def test_brain_scale_house() -> None:
    # kx = 0, ky = 0, x_m = ds, y_m = ds
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_scale_house, (0, 0, ds, ds), "scale_0-0_c-c")
    dict_house_right = constructor_house((ds, ds), (ds, ds), (ds, ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # kx = 1, ky = 1, x_m = ds, y_m = ds
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_scale_house, (1, 1, ds, ds), "scale_1-1_c-c")
    dict_house_right = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # kx = 1, ky = 2, x_m = ds, y_m = ds
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_scale_house, (1, 2, ds, ds), "scale_1-2_c-c")
    dict_house_right = constructor_house(
        (ds, ds), (-100 + ds, 160 + ds), (100 + ds, 160 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # kx = 2, ky = 1, x_m = ds, y_m = ds
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_scale_house, (2, 1, ds, ds), "scale_2-1_c-c")
    dict_house_right = constructor_house(
        (ds, ds), (-200 + ds, 80 + ds), (200 + ds, 80 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # kx = 2, ky = 2, x_m = ds, y_m = ds
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_scale_house, (2, 2, ds, ds), "scale_2-2_c-c")
    dict_house_right = constructor_house(
        (ds, ds), (-200 + ds, 160 + ds), (200 + ds, 160 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # kx = -1, ky = 2, x_m = ds, y_m = ds
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_scale_house, (-1, 2, ds, ds), "scale_m1-2_c-c")
    dict_house_right = constructor_house(
        (ds, ds), (100 + ds, 160 + ds), (-100 + ds, 160 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # kx = 2, ky = -1, x_m = ds, y_m = ds
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_scale_house, (2, -1, ds, ds), "scale_2-m1_c-c")
    dict_house_right = constructor_house(
        (ds, ds), (-200 + ds, -80 + ds), (200 + ds, -80 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # kx = -1, ky = -1, x_m = ds, y_m = ds
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_scale_house, (-1, -1, ds, ds), "scale_m1-m1_c-c")
    dict_house_right = constructor_house(
        (ds, ds), (100 + ds, -80 + ds), (-100 + ds, -80 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # kx = 2, ky = 2, x_m = ds + 50, y_m = ds + 50
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_scale_house, (2, 2, ds + 50, ds + 50), "scale_2-2_cp50-cp50")
    dict_house_right = constructor_house(
        (ds - 50, ds - 50), (-250 + ds, 110 + ds), (150 + ds, 110 + ds))
    assert cmp_control(dict_house_right, dict_house_res)


# перенос
# brain_move_house
def test_brain_move_house() -> None:
    # dx = 0, dy = 0
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_move_house, (0, 0), "move_0-0")
    dict_house_right = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # dx = 100, dy = 0
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_move_house, (100, 0), "move_100-0")
    dict_house_right = constructor_house(
        (100 + ds, ds), (ds, 80 + ds), (200 + ds, 80 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # dx = 0, dy = 100
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_move_house, (0, 100), "move_0-100")
    dict_house_right = constructor_house(
        (ds, 100 + ds), (-100 + ds, 180 + ds), (100 + ds, 180 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # dx = 100, dy = 100
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_move_house, (100, 100), "move_100-100")
    dict_house_right = constructor_house(
        (100 + ds, 100 + ds), (ds, 180 + ds), (200 + ds, 180 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # dx = -100, dy = -50
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_move_house, (-100, -50), "move_m100-m50")
    dict_house_right = constructor_house(
        (-100 + ds, -50 + ds), (-200 + ds, 30 + ds), (ds, 30 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
    # dx = 10, dy = -150
    dict_house = constructor_house(
        (ds, ds), (-100 + ds, 80 + ds), (100 + ds, 80 + ds))
    dict_house_res = save_draw_test_house(
        dict_house, brain_move_house, (10, -150), "move_10-m150")
    dict_house_right = constructor_house(
        (10 + ds, -150 + ds), (-90 + ds, -70 + ds), (110 + ds, -70 + ds))
    assert cmp_control(dict_house_right, dict_house_res)
