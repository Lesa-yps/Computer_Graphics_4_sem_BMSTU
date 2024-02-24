# Импортируем библиотеки
import tkinter as tk
import tkinter.messagebox as mb
import math

STEP_CONST = 50

def new_coord_xy(x, y, ZOOM, SIDE_PLACE, HEIGHT_PLACE):
    x_res = (int(x) - SIDE_PLACE * STEP_CONST) / ZOOM
    y_res = (int(y) + HEIGHT_PLACE * STEP_CONST) / ZOOM
    return round(x_res), round(y_res)

# функция находит точку посредине между дввумя точками
def middle_point(point1, point2):
    return ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)

# функция вычисляет угловой коэффициент прямой проходящей через обе эти точки
def slope(point1, point2):
    if point2[0] - point1[0] != 0:
        return (point2[1] - point1[1]) / (point2[0] - point1[0])
    else:
        return float('inf')  # Возвращаем бесконечность, чтобы обозначить вертикальную прямую

# Функция находит по 3 точкам угол с вершиной в первой точке
def cosine_rule_angle(point1, point2, point3):
    # находим длины сторон
    a = math.dist(point2, point3)
    b = math.dist(point1, point3)
    c = math.dist(point1, point2)
    return math.degrees(math.acos((b**2 + c**2 - a**2) / (2 * b * c)))

# функция находит максимальный угол между медианой и биссектрисой в треугольнике (по трём кортежам - точкам)
def angle_bisector_median(point1, point2, point3):
    # находит координаты пересечения медиан с противоположной стороной
    mid_c = middle_point(point1, point2)
    mid_a = middle_point(point2, point3)
    mid_b = middle_point(point3, point1)
    # находит координаты пересечения биссектрис с противоположной стороной
    bis_a = find_bisector_intersection(point1, point2, point3)
    bis_b = find_bisector_intersection(point2, point1, point3)
    bis_c = find_bisector_intersection(point3, point1, point2)
    # по теореме косинусов находим углы между биссектрисами и медианами
    angle_res_a = cosine_rule_angle(point1, bis_a, mid_a)
    angle_res_b = cosine_rule_angle(point2, bis_b, mid_b)
    angle_res_c = cosine_rule_angle(point3, bis_c, mid_c)
    # и выбирается наибольший
    angle_res_max = max(angle_res_a, angle_res_b, angle_res_c)
    if (angle_res_a == angle_res_max):
        return angle_res_max, point1, point2, point3
    elif (angle_res_b == angle_res_max):
        return angle_res_max, point2, point1, point3
    return angle_res_max, point3, point1, point2

# возвращает список кортежей - точек из таблицы
def iterate_points(tree):
    arr = []
    for child in tree.get_children():
        item = tree.item(child)
        x = item['values'][0]  # Получаем значение X
        y = item['values'][1]  # Получаем значение Y
        arr.append((x, y))
    #print(arr)
    return arr

# сравнивает вещественные числа (одинаковые -> 1, разные -> 0) с погрешностью 0.0001
def same_num(a, b):
    EPS = 0.0001
    if abs(a - b) < EPS:
        return 1
    return 0

# проверка что треугольник не линия (не линия -> 1, на одной прямой все 3 точки -> 0)
def check_points(point1, point2, point3):
    if same_num(slope(point1, point2), slope(point1, point3)):
        return 0
    return 1

# сравнивает кортежи вещественных чисел (все части кортежа одинаковые -> 1,
# хоть 1 отличается -> 0) с погрешностью 0.0001
def same_turple(a, b):
    if same_num(a[0], b[0]) and same_num(a[1], b[1]):
        return 1
    return 0

# Функция определяет 3 точки, поведённый через которые треугольник будет имет между бисс и медианой наибольший угол
# треугольник и бисс с медианой рисуются
def brain(cnv, tree, ZOOM, SIDE_PLACE, HEIGHT_PLACE):
    max_angle = -1
    res_angle = list()
    arr = iterate_points(tree)
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            for k in range(j + 1, len(arr)):
                if check_points(arr[i], arr[j], arr[k]):
                    res, main_point, point1, point2 = angle_bisector_median(arr[i], arr[j], arr[k])
                    # функция находит максимальный угол между медианой и биссектрисой в треугольнике (по трём кортежам - точкам)
                    if max_angle < res:
                        res_angle = [main_point, point1, point2]
                        max_angle = res
    if len(arr) < 3:
        mb.showerror('Ошибка!', "Задача не может быть решена: введено недостаточное количество треугольников.")
    elif max_angle < 0:
        mb.showerror('Ошибка!', "Задача не может быть решена за неимением треугольников.")
    else:
        draw_triangle(cnv, res_angle, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
        mb.showinfo('Максимальный угол', "Максимальный угол междуу биссектрисой и медианой в треугольнике равен {:.2f} градус(а/ов).".format(max_angle))
        #print(res_angle, max_angle)
    return res_angle, max_angle




# находит координаты пересечения биссектрисы с противоположной стороной
def find_bisector_intersection(B, A, C):
    # Вычисляем длины сторон треугольника
    a_side = math.sqrt((C[0] - B[0]) ** 2 + (C[1] - B[1]) ** 2)
    b_side = math.sqrt((C[0] - A[0]) ** 2 + (C[1] - A[1]) ** 2)
    c_side = math.sqrt((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2)
    # Вычисляем длины частей на которые биссектриса делит противолежащую сторону (формулы выведены вручную)
    AD = c_side * b_side / (a_side + c_side)
    #DC = b - AD
    # Вычисляем координаты точки пересечения биссектрисы с стороной BC (формулы выведены вручную)
    x = (C[0] - A[0]) * AD / b_side + A[0]
    y = (C[1] - A[1]) * AD / b_side + A[1]
    return x, y

# Функция для построения биссектрисы по трем точкам
##def draw_bisector(cnv, point1, point2, point3):
##    x, y = find_bisector_intersection(point1, point2, point3)
##    # Нарисуем биссектрису
##    cnv.create_line(x, y, point1[0], point1[1], fill="blue", tags="line", width = 2)

# рисует линию и подписывает её концы
def draw_line(cnv, x1, y1, x2, y2, color):
    x1, y1, x2, y2 = round(x1), round(y1), round(x2), round(y2)
    # отрисовка линии
    width_line = 2
    cnv.create_line(x1, y1, x2, y2, fill=color, tags="line", width = width_line)
    # Добавление подписи координат точек с тегом
    label1 = f"({x1}, {y1})"
    cnv.create_text(x1, y1, text=label1, anchor="sw", tags="coordinates")
    label2 = f"({x2}, {y2})"
    cnv.create_text(x2, y2, text=label2, anchor="sw", tags="coordinates")

# рисует результат (треугольник, биссектрису и медиану)
def draw_triangle(cnv, res_angle, ZOOM, SIDE_PLACE, HEIGHT_PLACE):
    # Нарисуем сам треугольник
    x_a, y_a = res_angle[0][0] * ZOOM, res_angle[0][1] * ZOOM
    x_b, y_b = res_angle[1][0] * ZOOM, res_angle[1][1] * ZOOM
    x_c, y_c = res_angle[2][0] * ZOOM, res_angle[2][1] * ZOOM
    #print(x_a, y_a, x_b, y_b, x_c, y_c, ZOOM)
    draw_line(cnv, x_a, y_a, x_b, y_b, "green")
    #cnv.create_line(x_a, y_a, x_b, y_b, fill="green", tags="line", width = width_line)
    draw_line(cnv, x_a, y_a, x_c, y_c, "green")
    #cnv.create_line(x_a, y_a, x_c, y_c, fill="green", tags="line", width = width_line)
    draw_line(cnv, x_b, y_b, x_c, y_c, "green")
    #cnv.create_line(x_b, y_b, x_c, y_c, fill="green", tags="line", width = width_line)
    # находим точку - середину противоположной стороны и рисуем медиану
    mid_point = middle_point((x_b, y_b), (x_c, y_c))
    draw_line(cnv, x_a, y_a, mid_point[0], mid_point[1], "brown")
    #cnv.create_line(x_a, y_a, mid_point[0], mid_point[1], fill="brown", tags="line", width = width_line)
    # рисует биссектрису
    #draw_bisector(cnv, (x_a, y_a), (x_b, y_b), (x_c, y_c))
    x_bis, y_bis = find_bisector_intersection((x_a, y_a), (x_b, y_b), (x_c, y_c))
    # Нарисуем биссектрису
    draw_line(cnv, x_bis, y_bis, x_a, y_a, "blue")
    #cnv.create_line(x_bis, y_bis, x_a, y_a, fill="blue", tags="line", width = width_line)
    


    
