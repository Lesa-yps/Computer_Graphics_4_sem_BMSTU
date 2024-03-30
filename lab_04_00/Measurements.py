import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from Algo_build_curve import list_algo, build_spectr_curve

# количество замеров времени
COUNT_RUNS = 25

# Сбор данных и отрисовка графика с временами работы всех алгоритмов


def draw_step_graph(list_x: List[float], matrix_y: List[List[float]], cir_or_ell: int) -> None:
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.size'] = '12'
    # Генерация цветов и маркеров
    colors = ["red", "blue", "green", "gray", "pink"]
    markers = ['o', 's', '^', 'D', 'P', "X"]
    # Построение кривых
    for i in range(len(matrix_y)):
        plt.plot(list_x, matrix_y[i], label=list_algo[i + 1][2],
                 color=colors[i % len(colors)], marker=markers[i % len(markers)])
    # Добавление подписей и заголовка
    plt.xlabel('Радиус (по x)')
    plt.ylabel('Время')
    if cir_or_ell == 0:
        plt.title(
            'Исследование времени работы алгоритмов вычисления точек для постороения окружностей')
    else:
        plt.title(
            'Исследование времени работы алгоритмов вычисления точек для построения эллипсов')
    plt.legend()
    plt.xticks(list_x)
    # Включение сетки
    plt.grid(True)
    # Показать график
    plt.show()


def build_time_graph(params: Tuple[any], step_R: int, count: int, cir_or_ell: int) -> None:
    # сбор данных для графика
    # цвет по-умолчанию чёрный
    color_def = "#000000"
    # список с временами работы всех алгоритмов
    list_algo_times = [[0 for _ in range(count)]
                       for i in range(1, len(list_algo))]
    list_R = np.arange(params[2], count * step_R + params[2], step_R)
    for num_algo in range(1, len(list_algo)):
        for _ in range(COUNT_RUNS):
            list_time_now = build_spectr_curve(
                None, params, step_R, count, num_algo, cir_or_ell, color_def, calc_time=True)
            list_algo_times[num_algo - 1] = [list_algo_times[num_algo - 1]
                                             [i] + list_time_now[i] for i in range(count)]
        list_algo_times[num_algo - 1] = [list_algo_times[num_algo - 1]
                                         [i] / COUNT_RUNS for i in range(count)]
    # построение графиков с временем работы всех алгоритмов
    draw_step_graph(list_R, list_algo_times, cir_or_ell)
