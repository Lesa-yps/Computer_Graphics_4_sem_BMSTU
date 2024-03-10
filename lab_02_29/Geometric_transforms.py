import math
from typing import List, Tuple, Dict, Any

# сравнивает вещественные числа (одинаковые -> True, разные -> False) с погрешностью 0.0001
def same_num(a: float, b: float) -> bool:
    EPS = 0.0001
    return abs(a - b) < EPS

# сравнивает кортежи вещественных чисел (все части кортежа одинаковые -> True,
# хоть 1 отличается -> False) с погрешностью 0.0001
def same_tuple(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
    return same_num(a[0], b[0]) and same_num(a[1], b[1])

# применяет функции к каждому элементу словаря
def for_each_elem_house(dict_house: Dict[str, Any], func_x, param_x, func_y, param_y) -> Dict[str, Any]:
    dict_house["center"] = (func_x(dict_house["center"], param_x), func_y(dict_house["center"], param_y))
    dict_house["grass"] = for_each_tuple(dict_house["grass"], func_x, param_x, func_y, param_y)
    dict_house["rect"] = for_each_tuple(dict_house["rect"], func_x, param_x, func_y, param_y)
    dict_house["roof"] = for_each_tuple(dict_house["roof"], func_x, param_x, func_y, param_y)
    dict_house["wind"]["center"] = (func_x(dict_house["wind"]["center"], param_x), func_y(dict_house["wind"]["center"], param_y))
    dict_house["wind"]["points"] = for_each_tuple(dict_house["wind"]["points"], func_x, param_x, func_y, param_y)
    dict_house["wind_frame"] = for_each_tuple(dict_house["wind_frame"], func_x, param_x, func_y, param_y)
    dict_house["door"] = for_each_tuple(dict_house["door"], func_x, param_x, func_y, param_y)
    dict_house["door_handle"] = for_each_tuple(dict_house["door_handle"], func_x, param_x, func_y, param_y)
    return dict_house

# применяет функции к каждому x и y
def for_each_tuple(arr_tuple: List[Tuple[int, int]], func_x, param_x, func_y, param_y) -> List[Tuple[int, int]]:
    for i in range(len(arr_tuple)):
        arr_tuple[i] = (round(func_x(arr_tuple[i], param_x)), round(func_y(arr_tuple[i], param_y)))
    return arr_tuple

# функции двигают координаты на параметр
def func_move_x(elem: Tuple[int, int], ds: int) -> int:
    return elem[0] + ds
def func_move_y(elem: Tuple[int, int], ds: int) -> int:
    return elem[1] + ds
# перенос
def brain_move_house(param: Tuple[int, int], dict_house: Dict[str, Any]) -> Dict[str, Any]:
    dx, dy = param
    #print(dict_house["rect"], dx, dy)
    dict_house = for_each_elem_house(dict_house, func_move_x, dx, func_move_y, dy)
    #print(dict_house["rect"])
    return dict_house

# функции масштабирует координаты
def func_scale_x(elem: Tuple[int, int], param: Tuple[float, float]) -> float:
    x1 = elem[0]
    kx, x_m = param
    x1 = kx * x1 + x_m * (1 - kx)
    return x1
def func_scale_y(elem: Tuple[int, int], param: Tuple[float, float]) -> float:
    y1 = elem[1]
    ky, y_m = param
    y1 = ky * y1 + y_m * (1 - ky)
    return y1
# масштабирование
def brain_scale_house(param: Tuple[float, float, int, int], dict_house: Dict[str, Any]) -> Dict[str, Any]:
    kx, ky, x_m, y_m = param
    dx, dy = dict_house["center"]
    dict_house = brain_move_house((-dx, -dy), dict_house)
    dict_house = for_each_elem_house(dict_house, func_scale_x, (kx, x_m - dx), func_scale_y, (ky, y_m - dy))
    dict_house = brain_move_house((dx, dy), dict_house)
    return dict_house

# функции поворачивает координаты
def func_turn_x(elem: Tuple[int, int], param: Tuple[float, float, float]) -> float:
    x1, y1 = elem
    x_c, y_c, angle = param
    x1 = x_c + (x1 - x_c) * math.cos(math.radians(angle)) + (y1 - y_c) * math.sin(math.radians(angle))
    return x1
def func_turn_y(elem: Tuple[int, int], param: Tuple[float, float, float]) -> float:
    x1, y1 = elem
    x_c, y_c, angle = param
    y1 = y_c - (x1 - x_c) * math.sin(math.radians(angle)) + (y1 - y_c) * math.cos(math.radians(angle))
    return y1
# поворот
def brain_turn_house(param: Tuple[float, int, int], dict_house: Dict[str, Any]) -> Dict[str, Any]:
    angle, x_t, y_t = param
    dx, dy = dict_house["center"]
    dict_house = brain_move_house((-dx, -dy), dict_house)
    param_func = (x_t - dx, y_t - dy, angle)
    dict_house = for_each_elem_house(dict_house, func_turn_x, param_func, func_turn_y, param_func)
    dict_house = brain_move_house((dx, dy), dict_house)
    return dict_house
