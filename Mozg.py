from typing import List, Tuple

# сравнивает вещественные числа (одинаковые -> 1, разные -> 0) с погрешностью 0.0001
def same_num(a: float, b: float) -> int:
    EPS = 0.0001
    if abs(a - b) < EPS:
        return 1
    return 0

# сравнивает кортежи вещественных чисел (все части кортежа одинаковые -> 1,
# хоть 1 отличается -> 0) с погрешностью 0.0001
def same_turple(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    if same_num(a[0], b[0]) and same_num(a[1], b[1]):
        return 1
    return 0

def brain_move_house(dx, dy, dict_house):
    return dict_house

def brain_scale_house(kx, ky, x_m, y_m, dict_house):
    return dict_house

def brain_turn_house(angle, x_t, y_t, dict_house):
    return dict_house
