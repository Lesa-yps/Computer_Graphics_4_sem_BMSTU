# Tесты для функций
from Geometric_transforms import same_num, same_tuple, for_each_tuple, brain_turn_house, \
     brain_scale_house, brain_move_house
from House import build_start_house
from typing import Tuple, Dict, Any


# сравнивает вещественные числа (одинаковые -> 1, разные -> 0)  с погрешностью 0.0001
# same_num
def test_same_num() -> None:
    # оба положительные одинаковые
    assert same_num(1.0, 1.0)
    # оба отрицательные одинаковые
    assert same_num(-1.11, -1.11)
    # почти одинаковые с очень маленькой погрешностью
    assert same_num(1.0, 1.00001)
    # по модулю одинаковые, но разных знаков
    assert not same_num(1.0, -1.0)
    # разные
    assert not same_num(1.0, 2.0)


# сравнивает кортежи вещественных чисел (все части кортежа одинаковые -> 1,
# хоть 1 отличается -> 0) с погрешностью 0.0001
# same_tuple
def test_same_tuple() -> None:
    # оба положительные одинаковые
    assert same_tuple((1, 2), (1, 2))
    # оба отрицательные одинаковые
    assert same_tuple((-1, -2), (-1, -2))
    # почти одинаковые с очень маленькой погрешностью
    assert same_tuple((1.0, 2.0), (1.0, 2.00001))
    # x1 == y2 и x2 == y1
    assert not same_tuple((1, 2), (2, 1))
    # разные
    assert not same_tuple((1.0, 2.0), (2.0, 3.0))
    # почти одинаковые с недостаточно маленькой погрешностью
    assert not same_tuple((1, 2), (1, 2.001))

# вспомогательные функции для тестов
def sum_x(elem: Tuple[int, int], param: int) -> int:
    return elem[0] + param
def sum_y(elem: Tuple[int, int], param: int) -> int:
    return elem[1] + param

# применяет функции к каждому x и y в массиве кортежей
# for_each_tuple
def test_for_each_tuple() -> None:
    # в массиве 1 нулевой элемент
    assert for_each_tuple([(0, 0)], sum_x, 0, sum_y, 0) == [(0, 0)]
    # функция воздействует только на x
    assert for_each_tuple([(1, 2), (3, 4)], sum_x, 1, sum_y, 0) == [(2, 2), (4, 4)]
    # функция воздействует только на y
    assert for_each_tuple([(1, 2), (3, 4)], sum_x, 0, sum_y, 1) == [(1, 3), (3, 5)]
    # функция воздействует на оба коэффициента
    assert for_each_tuple([(1, 2), (3, 4)], sum_x, 1, sum_y, 1) == [(2, 3), (4, 5)]
    # есть отрицательные коэффициенты
    assert for_each_tuple([(-1, 2), (-3, 4)], sum_x, 1, sum_y, 1) == [(0, 3), (-2, 5)]
    # функция воздействует на x и y с разными параметрами
    assert for_each_tuple([(1, 2), (3, 4)], sum_x, 10, sum_y, -5) == [(11, -3), (13, -1)]
    # пустой массив
    assert for_each_tuple([], sum_x, 1, sum_y, 1) == []



# сравнивае домики по ключевым параметрам
def cmp_control(house1: Dict[str, Any], house2: Dict[str, Any]) -> bool:
    res = (house1["center"] == house2["center"]) * (house1["roof"] == house2["roof"]) * (house1["grass"] == house2["grass"])
    res *= (house1["door"] == house2["door"]) * (house1["wind_frame"] == house2["wind_frame"])
    return res

# "шапка" для тестов изменения домика (прогоняет функцию с переданными параметрами, а затем сравнивает с переданным "верным" вариантом)
def hat_test_change_house(dict_house1_right: Dict[str, Any], func, param: Tuple[any]) -> bool:
    dict_house = build_start_house()
    dict_house1 = func(param, dict_house)
    return cmp_control(dict_house1_right, dict_house1)

# поворот
# brain_turn_house
def test_brain_turn_house() -> None:
    # угол = 90, x_center = 0, y_center = 0
    dict_house1_right = {"center": (0.0, 0.0), "roof": [(-20, 120), (-80, 100), (-80, -100), (-20, -120)], "grass": [(80, 150), (80, -150)],\
                         "door": [(80, 80), (0, 80), (0, 20), (80, 20)], "wind_frame": [(20, -30), (0, -50), (20, -70), (40, -50)]}
    assert hat_test_change_house(dict_house1_right, brain_turn_house, (90, 0, 0))
    # угол = 180, x_center = 0, y_center = 0
    dict_house1_right = {'center': (0.0, 0.0), 'roof': [(120, 20), (100, 80), (-100, 80), (-120, 20)], 'grass': [(150, -80), (-150, -80)],
'door': [(80, -80), (80, 0), (20, 0), (20, -80)], 'wind_frame': [(-30, -20), (-50, 0), (-70, -20), (-50, -40)]}
    assert hat_test_change_house(dict_house1_right, brain_turn_house, (180, 0, 0))
    # угол = 360, x_center = 0, y_center = 0
    dict_house1_right = {'center': (0.0, 0.0), 'roof': [(-120, -20), (-100, -80), (100, -80), (120, -20)], 'grass': [(-150, 80), (150, 80)],
'door': [(-80, 80), (-80, 0), (-20, 0), (-20, 80)], 'wind_frame': [(30, 20), (50, 0), (70, 20), (50, 40)]}
    assert hat_test_change_house(dict_house1_right, brain_turn_house, (360, 0, 0))
    # угол = 0, x_center = 0, y_center = 0
    dict_house1_right = build_start_house()
    assert hat_test_change_house(dict_house1_right, brain_turn_house, (0, 0, 0))
    # угол = 90, x_center = 100, y_center = 100
    dict_house1_right = {'center': (0.0, 200.0), 'roof': [(-20, 320), (-80, 300), (-80, 100), (-20, 80)], 'grass': [(80, 350), (80, 50)],
'door': [(80, 280), (0, 280), (0, 220), (80, 220)], 'wind_frame': [(20, 170), (0, 150), (20, 130), (40, 150)]}
    assert hat_test_change_house(dict_house1_right, brain_turn_house, (90, 100, 100))
    # угол = -90, x_center = -100, y_center = 50
    dict_house1_right = {'center': (-50.0, 150.0), 'roof': [(-30, 30), (30, 50), (30, 250), (-30, 270)], 'grass': [(-130, 0), (-130, 300)],
'door': [(-130, 70), (-50, 70), (-50, 130), (-130, 130)], 'wind_frame': [(-70, 180), (-50, 200), (-70, 220), (-90, 200)]}
    assert hat_test_change_house(dict_house1_right, brain_turn_house, (-90, -100, 50))


# масштабирование
# brain_scale_house
def test_brain_scale_house() -> None:
    # kx = 0, ky = 0, x_m = 0, y_m = 0
    dict_house1_right = {'center': (0, 0), 'roof': [(0, 0), (0, 0), (0, 0), (0, 0)], 'grass': [(0, 0), (0, 0)],\
          'door': [(0, 0), (0, 0), (0, 0), (0, 0)],'wind_frame': [(0, 0), (0, 0), (0, 0), (0, 0)]}
    assert hat_test_change_house(dict_house1_right, brain_scale_house, (0, 0, 0, 0))
    # kx = 1, ky = 1, x_m = 0, y_m = 0
    dict_house1_right = {'center': (0, 0), 'roof': [(-120, -20), (-100, -80), (100, -80), (120, -20)], 'grass': [(-150, 80), (150, 80)],\
          'door': [(-80, 80), (-80, 0), (-20, 0), (-20, 80)],'wind_frame': [(30, 20), (50, 0), (70, 20), (50, 40)]}
    assert hat_test_change_house(dict_house1_right, brain_scale_house, (1, 1, 0, 0))
    # kx = 1, ky = 2, x_m = 0, y_m = 0
    dict_house1_right = {'center': (0, 0), 'roof': [(-120, -40), (-100, -160), (100, -160), (120, -40)], 'grass': [(-150, 160), (150, 160)],\
          'door': [(-80, 160), (-80, 0), (-20, 0), (-20, 160)],'wind_frame': [(30, 40), (50, 0), (70, 40), (50, 80)]}
    assert hat_test_change_house(dict_house1_right, brain_scale_house, (1, 2, 0, 0))
    # kx = 2, ky = 1, x_m = 0, y_m = 0
    dict_house1_right = {'center': (0, 0), 'roof': [(-240, -20), (-200, -80), (200, -80), (240, -20)], 'grass': [(-300, 80), (300, 80)],\
          'door': [(-160, 80), (-160, 0), (-40, 0), (-40, 80)],'wind_frame': [(60, 20), (100, 0), (140, 20), (100, 40)]}
    assert hat_test_change_house(dict_house1_right, brain_scale_house, (2, 1, 0, 0))
    # kx = 2, ky = 2, x_m = 0, y_m = 0
    dict_house1_right = {'center': (0, 0), 'roof': [(-240, -40), (-200, -160), (200, -160), (240, -40)], 'grass': [(-300, 160), (300, 160)],\
          'door': [(-160, 160), (-160, 0), (-40, 0), (-40, 160)],'wind_frame': [(60, 40), (100, 0), (140, 40), (100, 80)]}
    assert hat_test_change_house(dict_house1_right, brain_scale_house, (2, 2, 0, 0))
    # kx = -1, ky = 2, x_m = 0, y_m = 0
    dict_house1_right = {'center': (0, 0), 'roof': [(120, -40), (100, -160), (-100, -160), (-120, -40)], 'grass': [(150, 160), (-150, 160)],\
          'door': [(80, 160), (80, 0), (20, 0), (20, 160)],'wind_frame': [(-30, 40), (-50, 0), (-70, 40), (-50, 80)]}
    assert hat_test_change_house(dict_house1_right, brain_scale_house, (-1, 2, 0, 0))
    # kx = 2, ky = -1, x_m = 0, y_m = 0
    dict_house1_right = {'center': (0, 0), 'roof': [(-240, 20), (-200, 80), (200, 80), (240, 20)], 'grass': [(-300, -80), (300, -80)],\
          'door': [(-160, -80), (-160, 0), (-40, 0), (-40, -80)],'wind_frame': [(60, -20), (100, 0), (140, -20), (100, -40)]}
    assert hat_test_change_house(dict_house1_right, brain_scale_house, (2, -1, 0, 0))
    # kx = -1, ky = -1, x_m = 0, y_m = 0
    dict_house1_right = {'center': (0, 0), 'roof': [(120, 20), (100, 80), (-100, 80), (-120, 20)], 'grass': [(150, -80), (-150, -80)],\
          'door': [(80, -80), (80, 0), (20, 0), (20, -80)],'wind_frame': [(-30, -20), (-50, 0), (-70, -20), (-50, -40)]}
    assert hat_test_change_house(dict_house1_right, brain_scale_house, (-1, -1, 0, 0))
    # kx = 2, ky = 2, x_m = 100, y_m = 100
    dict_house1_right = {'center': (-100, -100), 'roof': [(-340, -140), (-300, -260), (100, -260), (140, -140)], 'grass': [(-400, 60), (200, 60)],\
          'door': [(-260, 60), (-260, -100), (-140, -100), (-140, 60)],'wind_frame': [(-40, -60), (0, -100), (40, -60), (0, -20)]}
    assert hat_test_change_house(dict_house1_right, brain_scale_house, (2, 2, 100, 100))


# перенос
# brain_move_house
def test_brain_move_house() -> None:
    # dx = 0, dy = 0
    dict_house1_right = {'center': (0, 0), 'roof': [(-120, -20), (-100, -80), (100, -80), (120, -20)], 'grass': [(-150, 80), (150, 80)],\
          'door': [(-80, 80), (-80, 0), (-20, 0), (-20, 80)],'wind_frame': [(30, 20), (50, 0), (70, 20), (50, 40)]}
    assert hat_test_change_house(dict_house1_right, brain_move_house, (0, 0))
    # dx = 100, dy = 0
    dict_house1_right = {'center': (100, 0), 'roof': [(-20, -20), (0, -80), (200, -80), (220, -20)], 'grass': [(-50, 80), (250, 80)],\
          'door': [(20, 80), (20, 0), (80, 0), (80, 80)],'wind_frame': [(130, 20), (150, 0), (170, 20), (150, 40)]}
    assert hat_test_change_house(dict_house1_right, brain_move_house, (100, 0))
    # dx = 0, dy = 100
    dict_house1_right = {'center': (0, 100), 'roof': [(-120, 80), (-100, 20), (100, 20), (120, 80)], 'grass': [(-150, 180), (150, 180)],\
                         'door': [(-80, 180), (-80, 100), (-20, 100), (-20, 180)],'wind_frame': [(30, 120), (50, 100), (70, 120), (50, 140)]}
    assert hat_test_change_house(dict_house1_right, brain_move_house, (0, 100))
    # dx = 100, dy = 100
    dict_house1_right = {'center': (100, 100), 'roof': [(-20, 80), (0, 20), (200, 20), (220, 80)], 'grass': [(-50, 180), (250, 180)],\
                         'door': [(20, 180), (20, 100), (80, 100), (80, 180)],'wind_frame': [(130, 120), (150, 100), (170, 120), (150, 140)]}
    assert hat_test_change_house(dict_house1_right, brain_move_house, (100, 100))
    # dx = -100, dy = -50
    dict_house1_right = {'center': (-100, -50), 'roof': [(-220, -70), (-200, -130), (0, -130), (20, -70)], 'grass': [(-250, 30), (50, 30)],\
                         'door': [(-180, 30), (-180, -50), (-120, -50), (-120, 30)],'wind_frame': [(-70, -30), (-50, -50), (-30, -30), (-50, -10)]}
    assert hat_test_change_house(dict_house1_right, brain_move_house, (-100, -50))
    # dx = 10, dy = -300
    dict_house1_right = {'center': (10, -300), 'roof': [(-110, -320), (-90, -380), (110, -380), (130, -320)], 'grass': [(-140, -220), (160, -220)],\
                         'door': [(-70, -220), (-70, -300), (-10, -300), (-10, -220)],'wind_frame': [(40, -280), (60, -300), (80, -280), (60, -260)]}
    assert hat_test_change_house(dict_house1_right, brain_move_house, (10, -300))

