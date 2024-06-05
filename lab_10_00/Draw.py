# Импортируем библиотеки
import tkinter as tk
import tkinter.messagebox as mb
from typing import Tuple, List
import Const as c

# отрисовка точки (если она в пределах холста) и обновление горизонтов


def draw_point(cnv: tk.Canvas, Y_up_horizon: List[float], Y_down_horizon: List[float], x: float, y: float, color_point: str,
               tag: str) -> bool:
    if (0 <= x <= cnv.winfo_width()) and (0 <= y <= cnv.winfo_height()):
        x, y = round(x), round(y)
        if Y_up_horizon[x] < y:
            Y_up_horizon[x] = y
            cnv.create_rectangle(
                x, y, x + 1, y + 1, fill=color_point, outline=color_point, tags=tag)
        elif Y_down_horizon[x] > y:
            Y_down_horizon[x] = y
            cnv.create_rectangle(
                x, y, x + 1, y + 1, fill=color_point, outline=color_point, tags=tag)
        return True
    return False

# рисует линию попиксельно
# Алгоритм цифрового дифференциального анализатора


def draw_line_algo_DDA(cnv: tk.Canvas, Y_up_horizon: List[float], Y_down_horizon: List[float], point1: Tuple[int],
                       point2: Tuple[int], color_point: str, tag: str) -> None:
    if point2[c.X_PART] < point2[c.X_PART]:
        point1, point2 = point2, point1
    # насколько за длину отрезка изменились х и у
    dx = point2[c.X_PART] - point1[c.X_PART]
    dy = point2[c.Y_PART] - point1[c.Y_PART]
    xi, yi, _ = point1
    is_vis = draw_point(cnv, Y_up_horizon, Y_down_horizon,
                        xi, yi, color_point, tag)
    dmax = max(dx, dy)
    if (dmax != 0):
        # шаг изменения по коодинатам
        dx /= dmax
        dy /= dmax
        i = 0
        while (i < dmax) and is_vis:
            xi += dx
            yi += dy
            is_vis = draw_point(cnv, Y_up_horizon,
                                Y_down_horizon, xi, yi, color_point, tag)
            i += 1

# проверяет заполнены ли поля ввода координат числами


def check_input_field(arr_entry: List[tk.Entry], func, help_str: str, echo_err: bool = True) -> bool:
    try:
        for i in arr_entry:
            func(i.get())
    except ValueError:
        if echo_err:
            mb.showerror(
                'Ошибка!', f"Поля для {help_str} некорректно заполнены.")
        return False
    else:
        return True

# очищает холст от линий


def clean_all(cnv: tk.Canvas) -> None:
    cnv.delete("plane")


# проверка того, что матрица существует (была инициализирована)
def check_matrix_exist(matrix: List[List[float]]) -> bool:
    if (len(matrix) == 0):
        mb.showerror("Ошибка", "Перед изменением графика его нужно построить.")
        return False
    return True
