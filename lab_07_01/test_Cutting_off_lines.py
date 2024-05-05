from typing import Tuple, List
import Const as c
# Tесты для функций
from Cutting_off_lines import calc_visibl_code, check_visibl


# создаёт тестовый отсекатель (точки передавать: слева_сверху, справа_снизу)
def make_test_clipper(point1: Tuple[int], point2: Tuple[int]) -> List[int]:
    test_clipper = [0 for _ in range(c.LEN_CLIPPER)]
    test_clipper[c.X_LEFT] = point1[c.X_PART]
    test_clipper[c.X_RIGHT] = point2[c.X_PART]
    test_clipper[c.Y_UP] = point2[c.Y_PART]
    test_clipper[c.Y_DOWN] = point1[c.Y_PART]
    return test_clipper

# вычисление кодов концевых точек и занесение этих кодов в массив 1*4 каждый
# calc_visibl_code


def test_calc_visibl_code() -> None:
    clipper = make_test_clipper((0, 0), (100, 100))
    # точка видима
    right_res = [0 for _ in range(c.LEN_CLIPPER)]
    assert calc_visibl_code((50, 50), clipper) == right_res
    # точка слева от отсекателя
    right_res = [0 for _ in range(c.LEN_CLIPPER)]
    right_res[c.X_LEFT] = 1
    assert calc_visibl_code((-50, 50), clipper) == right_res
    # точка справа сверху от отсекателя
    right_res = [0 for _ in range(c.LEN_CLIPPER)]
    right_res[c.X_RIGHT] = 1
    right_res[c.Y_UP] = 1
    assert calc_visibl_code((150, 200), clipper) == right_res

# проверка видимости всего отрезка и его точек
# check_visibl


def test_check_visibl() -> None:
    clipper = make_test_clipper((0, 0), (100, 100))
    # линия видима
    assert check_visibl((0, 0), (50, 50), clipper) == c.LINE_VISIBL
    # линия тривиально невидима
    assert check_visibl((200, 200), (250, 250), clipper) == c.LINE_NOT_VISIBL
    # первая точка видима, вторая нет
    assert check_visibl((0, 0), (250, 250), clipper) == c.FIRST_VISIBL
    # вторая точка видима, первая нет
    assert check_visibl((-10, -10), (50, 50), clipper) == c.SECOND_VISIBL
    # видимость определить не удалось базовыми проверками
    assert check_visibl((50, -50), (-50, 50), clipper) == c.DONT_KNOW
