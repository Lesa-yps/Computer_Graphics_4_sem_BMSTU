# Tесты для функций
from Algo_build_line import sign, rgb_to_hex, hex_to_rgb, add_light_color


# x > 0 -> 1; x < 0 -> -1; x == 0 -> 0
# sign
def test_sign() -> None:
    # положительное, по модулю единица
    assert sign(1) == 1
    # положительное, больше единицы
    assert sign(3) == 1
    # отрицательное, меньше единицы
    assert sign(-5) == -1
    # отрицательное, по модулю единица
    assert sign(-1) == -1
    # нуль
    assert sign(0) == 0

# переводит RGB представление цвета в 16-ичное
# rgb_to_hex


def test_rgb_to_hex() -> None:
    # красный
    assert rgb_to_hex((255, 0, 0)) == '#ff0000'
    # зелёный
    assert rgb_to_hex((0, 255, 0)) == '#00ff00'
    # синий
    assert rgb_to_hex((0, 0, 255)) == '#0000ff'
    # чёрный
    assert rgb_to_hex((0, 0, 0)) == '#000000'
    # белый
    assert rgb_to_hex((255, 255, 255)) == '#ffffff'
    # (R == G == B) != 0 != 255
    assert rgb_to_hex((100, 100, 100)) == '#646464'

# переводит 16-ичное представление цвета в RGB
# hex_to_rgb


def test_hex_to_rgb() -> None:
    # красный
    assert hex_to_rgb('#ff0000') == (255, 0, 0)
    # зелёный
    assert hex_to_rgb('#00ff00') == (0, 255, 0)
    # синий
    assert hex_to_rgb('#0000ff') == (0, 0, 255)
    # чёрный
    assert hex_to_rgb('#000000') == (0, 0, 0)
    # белый
    assert hex_to_rgb('#ffffff') == (255, 255, 255)
    # (R == G == B) != 0 != 255
    assert hex_to_rgb('#646464') == (100, 100, 100)

# Добавляет к цвету овещённость
# add_light_color


def test_add_light_color() -> None:
    # черный, добавляем освещённость 0
    assert add_light_color('#000000', 0) == '#000000'
    # черный, добавляем освещённость 100
    assert add_light_color('#000000', 100) == '#646464'
    # черный, добавляем освещённость 255
    assert add_light_color('#000000', 255) == '#ffffff'
    # белый, добавляем освещённость 100
    assert add_light_color('#ffffff', 100) == '#ffffff'
    # (R == G == B) != 0 != 255 освещенность = 50
    assert add_light_color("646464", 50) == '#969696'
    # (R == G == B) != 0 != 255 освещенность = - (R == G == B)
    assert add_light_color('#646464', -100) == '#000000'
    # (R == G == B) != 0 != 255 освещенность = 255 - (R == G == B)
    assert add_light_color("646464", 155) == '#ffffff'
