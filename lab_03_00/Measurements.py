from math import radians, cos, sin, pi
import numpy as np
import matplotlib.pyplot as plt
import time
from typing import List
from Algo_build_line import list_algo

# количество замеров времени
COUNT_RUNS = 25

# построение гистограммы с временем работы всех алгоритмов


def draw_step_bar(list_y: List[float]) -> None:
    plt.figure(figsize=(10, 7))
    plt.rcParams['font.size'] = '12'
    # Добавление подписей и заголовка
    plt.ylabel('Время')
    plt.title('Замеры времени построения спектров алгоритмами')
    x_bars = np.arange(5)
    algo_names = ["ЦДА", "Брезенхем\n(real)", "Брезенхем\n(int)",
                  "Брезенхем\n(с устранением\n ступенчатости)", "Ву"]
    plt.xticks(x_bars, algo_names, rotation=5)
    plt.bar(x_bars, list_y, align="center", alpha=1)
    # Показать график
    plt.show()

# Сбор данных и отрисовка гистограммы с временем работы всех алгоритмов


def build_time_bar(lenght_line: float, angle_step: float) -> None:
    # сбор данных для гистограммы
    angle_step = radians(angle_step)
    color_def = "#000000"
    point_start = (0, 0)
    # список с временами работы всех алгоритмов
    list_algo_times = [0 for _ in range(1, len(list_algo))]
    for i in range(1, len(list_algo)):
        time_algo = 0.0
        algo = list_algo[i][0]
        for _ in range(COUNT_RUNS):
            angle_now = 0
            while angle_now < (2 * pi):
                point_end = (cos(angle_now) * lenght_line,
                             sin(angle_now) * lenght_line)
                time_start = time.time()
                algo(point_start, point_end, color_def)
                time_algo += time.time() - time_start
                angle_now += angle_step
        list_algo_times[i - 1] = time_algo / COUNT_RUNS
    # построение гистограммы с временем работы всех алгоритмов
    draw_step_bar(list_algo_times)


# построение графиков ступенчатости
def draw_step_graph(list_x: List[float], matrix_y: List[List[int]]) -> None:
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.size'] = '12'
    # Генерация цветов и маркеров
    colors = ["red", "blue", "green", "gray", "pink"]
    markers = ['o', 's', '^', 'D', 'P', "X"]
    # Построение кривых
    for i in range(len(matrix_y)):
        plt.plot(list_x, matrix_y[i], label=list_algo[i + 1][1],
                 color=colors[i % len(colors)], marker=markers[i % len(markers)])
    # Добавление подписей и заголовка
    plt.xlabel('Угол (градусы)')
    plt.ylabel('Количество ступенек')
    plt.title('Исследование ступенчатости алгоритмов')
    plt.legend()
    plt.xticks(list(range(0, 91, 5)))
    # Включение сетки
    plt.grid(True)
    # Показать график
    plt.show()

# Сбор данных и отрисовка графиков ступенчатости


def build_step_graph(lenght_line: float) -> None:
    # сбор данных для графиков
    angle_step = radians(2)
    color_def = "#000000"
    point_start = (0, 0)
    list_angle = list()
    # список со списками с количеством шагов у каждого алгоритма
    list_algo_steps = [list() for _ in range(1, len(list_algo))]
    angle_now = 0
    while angle_now < (pi / 2.0 + 0.01):
        list_angle.append(angle_now * 180 / pi)
        point_end = (cos(angle_now) * lenght_line,
                     sin(angle_now) * lenght_line)
        for i in range(1, len(list_algo)):
            algo = list_algo[i][0]
            count_steps = algo(point_start, point_end,
                               color_def, calc_step=True)
            list_algo_steps[i - 1].append(count_steps)
        angle_now += angle_step
    # построение графиков
    draw_step_graph(list_angle, list_algo_steps)
