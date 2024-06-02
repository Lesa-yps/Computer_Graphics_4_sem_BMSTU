# Талышева Олеся ИУ7-45Б
# Лабораторная работа №10

# Импортируем библиотеки
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from tkinter import colorchooser
from typing import Optional
from math import pi, cos, sin
from Floating_horizon import floating_horizon
from Draw import check_input_field, check_matrix_exist
from Formula import list_of_func
import Const as c

# Константы
MIN_WIDTH = 870 + 257  # минимальная ширина окна приложения
MIN_HEIGHT = 550 + 140  # минимальная высота окна приложения
SIZE_OF_CANVAS = 500  # размер холста
STEP_CONST = 50  # шаг перемещения
# Переменные определяющие расположение/состояние окна
ZOOM = 1  # масштаб
SIDE_PLACE = 0  # переменная для определения сдвига в стороне
HEIGHT_PLACE = 0  # переменная для определения сдвига по высоте
# цвет плоскости по-умолчанию синий
color_plane = "#0000ff"
# коэффициент масштабирования рисовки (по-умолчанию 30)
DEF_SCALE_COEF = 30
# эта переменная блокирует изменение положения и зума холста, пока рисуется плоскость
is_painting = False
# эти переменные показывают происходит ли изменение графика
is_rotate = False
is_scale = False
# номер выбранной функции
num_func = 0
# матрица поворотов
transform_matrix = list()


# сброс всего наработанного


def cleaning() -> None:
    global ZOOM, SIDE_PLACE, HEIGHT_PLACE
    # Очистка всего содержимого на холсте
    cnv.delete("all")
    # Масштабирование холста до его стартового размера
    cnv.scale("all", 0, 0, 1, 1)
    # Установка положения прокрутки на начальное значение
    ds = 0
    cnv.xview_moveto(ds)
    cnv.yview_moveto(ds)
    ZOOM, SIDE_PLACE, HEIGHT_PLACE = 1, ds, ds

# умножение матриц


def multy_matrix(matrix1, matrix2):
    res_matrix = [[0 for _ in range(c.MATRIX_SIZE)]
                  for _ in range(c.MATRIX_SIZE)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                res_matrix[i][j] += matrix1[i][k] * matrix2[k][j]
    return res_matrix


# функция поворачивает график и вызывает функцию отрисовки
def rotate_axis(axis, coef_rotate_entry):
    global transform_matrix
    angle = float(coef_rotate_entry.get()) * pi / 180
    if axis == c.X_PART:
        rotating_matrix = [[1,           0,          0, 0],
                           [0,  cos(angle), sin(angle), 0],
                           [0, -sin(angle), cos(angle), 0],
                           [0,           0,          0, 1]]
    elif axis == c.Y_PART:
        rotating_matrix = [[cos(angle), 0, -sin(angle), 0],
                           [0, 1,           0, 0],
                           [sin(angle), 0,  cos(angle), 0],
                           [0, 0,           0, 1]]
    else:
        rotating_matrix = [[cos(angle),  sin(angle), 0, 0],
                           [-sin(angle), cos(angle), 0, 0],
                           [0,          0, 1, 0],
                           [0,          0, 0, 1]]
    transform_matrix = multy_matrix(transform_matrix, rotating_matrix)
    fork('Построить')


# подготовка параметров и вызов функции с алгоритмом плавающего горизонта


def prepare_floating_horizon():
    global transform_matrix
    func = list_of_func[num_func][0]
    x_params = (int(x_start_entry.get()), int(
        x_count_entry.get()), int(x_end_entry.get()))
    z_params = (int(z_start_entry.get()), int(
        z_count_entry.get()), int(z_end_entry.get()))
    if not is_scale and not is_rotate:
        transform_matrix = [[(i == j) for i in range(c.MATRIX_SIZE)]
                            for j in range(c.MATRIX_SIZE)]
    coef_scale = DEF_SCALE_COEF if not is_scale else float(
        coef_scale_entry.get())
    # вызов функции, реализующей алгоритм плавающего горизонта
    floating_horizon(cnv, func, x_params, z_params,
                     transform_matrix, color_plane, coef_scale)

# Функция вызывается в ответ на действия пользователя и выполняет требуемое или вызывает для этого другую функцию


def fork(text: str) -> None:
    global is_painting
    if is_painting:
        mb.showerror('Ошибка!', "Дождитесь конца построения плоскости!")
        return
    if text == 'Построить':
        handle_draw()
    elif text == 'Масштабировать':
        handle_scale()
    elif text == 'Повернуть по x':
        handle_rotate(c.X_PART, coef_rotate_x_entry)
    elif text == 'Повернуть по y':
        handle_rotate(c.Y_PART, coef_rotate_y_entry)
    elif text == 'Повернуть по z':
        handle_rotate(c.Z_PART, coef_rotate_z_entry)
    elif text == 'Очистить холст':
        cleaning()


def handle_draw():
    global is_painting
    if not (check_input_field([x_start_entry, x_count_entry, x_end_entry], int, "x") and
            check_input_field([z_start_entry, z_count_entry, z_end_entry], int, "z")):
        return
    is_painting = True
    prepare_floating_horizon()
    is_painting = False


def handle_scale():
    global is_scale, transform_matrix
    if check_input_field([coef_scale_entry], float, "коэффициент масштабирования") and \
       check_matrix_exist(transform_matrix):
        is_scale = True
        fork('Построить')
        is_scale = False


def handle_rotate(axis, coef_rotate_entry):
    global is_rotate, transform_matrix
    if check_input_field([coef_rotate_entry], float, f"угол поворота вокруг оси {axis}") and \
       check_matrix_exist(transform_matrix):
        is_rotate = True
        rotate_axis(axis, coef_rotate_entry)
        is_rotate = False


# обработка события изменения размера окна
def resize_checker(event: tk.Event) -> None:
    # Получаем текущие размеры окна
    current_width = window.winfo_width()
    current_height = window.winfo_height()
    # Проверяем, если текущий размер меньше минимального, то устанавливаем его минимальным
    if current_width < MIN_WIDTH or current_height < MIN_HEIGHT:
        window.geometry(f'{MIN_WIDTH}x{MIN_HEIGHT}')


# Создаём окошко и обозначаем его параметры
window = tk.Tk()
window["bg"] = 'light pink'
window.title("Лабораторная работа по компьютерной графике №10")
window.geometry(f'{MIN_WIDTH}x{MIN_HEIGHT}')
# Устанавливается минимальный размер окна
window.minsize(MIN_WIDTH, MIN_HEIGHT)
# Привязываем обработчик события изменения размера окна
window.bind("<Configure>", resize_checker)


# Создаётся холст с установленными размерами
cnv = tk.Canvas(window, width=SIZE_OF_CANVAS, height=SIZE_OF_CANVAS, bg="white",
                cursor="plus", xscrollincrement=STEP_CONST, yscrollincrement=STEP_CONST)
cnv.grid(row=0, column=2, rowspan=8, sticky='nsew')
window.grid_columnconfigure(2, weight=1)

# Функция создаёт кнопку


def make_button(doing: str, button_frame: tk.Frame, width1: int) -> tk.Button:
    return tk.Button(button_frame, text=doing, bd=7, font=("Calibry", 12),
                     command=lambda: fork(doing),
                     activebackground="salmon", bg="khaki", height=1, width=width1, cursor="hand1")


# Функция для обработки события выбора функции в выпадающем списке
def what_choose_func(event: tk.Event):
    global num_algo
    num_algo = chooser_func.current()


# Создаем поле для выбора формулы
formula_frame = tk.Frame(window)
formula_frame.grid(row=0, column=0, padx=5, pady=2)
tk.Label(formula_frame, text="Формула (от x, y, z):", font=("Calibry", 12)).grid(
    row=0, column=0, columnspan=2, sticky="w")
# Создаем выпадающий список формул
chooser_func = ttk.Combobox(formula_frame, width=32,
                            height=35, font=("Calibry", 12), state="readonly")
chooser_func["values"] = [i[-1]
                          for i in list_of_func]  # Устанавливаем список вариантов
chooser_func.current(0)  # Устанавливаем начальное значение (0)
# Привязываем обработчик события выбора элемента
chooser_func.bind("<<ComboboxSelected>>", what_choose_func)
chooser_func.grid(row=1, column=0, padx=10, pady=10, sticky="we", columnspan=2)


# Создаем поля для ввода интервала по х
input_x_frame = tk.Frame(window)
input_x_frame.grid(row=1, column=0, padx=5, pady=2)
tk.Label(input_x_frame, text="Интервал изменения по х:", font=("Calibry", 12)).grid(
    row=0, column=0, columnspan=2, sticky="w")
tk.Label(input_x_frame, text="от:", font=(
    "Calibry", 12)).grid(row=1, column=0)
x_start_entry = tk.Entry(input_x_frame, font=("Calibry", 12))
x_start_entry.grid(row=1, column=1)
x_start_entry.insert(0, "-10")
tk.Label(input_x_frame, text="до:", font=(
    "Calibry", 12)).grid(row=2, column=0)
x_end_entry = tk.Entry(input_x_frame, font=("Calibry", 12))
x_end_entry.grid(row=2, column=1)
x_end_entry.insert(0, "10")
tk.Label(input_x_frame, text="количество шагов:", font=(
    "Calibry", 12)).grid(row=3, column=0)
x_count_entry = tk.Entry(input_x_frame, font=("Calibry", 12))
x_count_entry.grid(row=3, column=1)
x_count_entry.insert(0, "100")


# Создаем поля для ввода интервала по z
input_z_frame = tk.Frame(window)
input_z_frame.grid(row=2, column=0, padx=5, pady=2)
tk.Label(input_z_frame, text="Интервал изменения по z:", font=("Calibry", 12)).grid(
    row=0, column=0, columnspan=2, sticky="w")
tk.Label(input_z_frame, text="от:", font=(
    "Calibry", 12)).grid(row=1, column=0)
z_start_entry = tk.Entry(input_z_frame, font=("Calibry", 12))
z_start_entry.grid(row=1, column=1)
z_start_entry.insert(0, "-10")
tk.Label(input_z_frame, text="до:", font=(
    "Calibry", 12)).grid(row=2, column=0)
z_end_entry = tk.Entry(input_z_frame, font=("Calibry", 12))
z_end_entry.grid(row=2, column=1)
z_end_entry.insert(0, "10")
tk.Label(input_z_frame, text="количество шагов:", font=(
    "Calibry", 12)).grid(row=3, column=0)
z_count_entry = tk.Entry(input_z_frame, font=("Calibry", 12))
z_count_entry.grid(row=3, column=1)
z_count_entry.insert(0, "100")


# выбор цвета плоскости


def choose_color() -> None:
    global color_plane
    color = colorchooser.askcolor(title="Выберите цвет")
    # Используется второй элемент кортежа для получения выбранного цвета
    color_plane = color[1]


# кнопка выбора цветов
button_color = tk.Button(window, text="Выбрать цвет плоскости", command=lambda: choose_color(), activebackground="salmon", bg="khaki",
                         width=10, height=1, bd=7, font=("Calibry", 12))
button_color.grid(row=3, column=0, stick='we')


# масштабирование
scale_frame = tk.Frame(window)
scale_frame.grid(row=4, column=0, padx=5, pady=2)
tk.Label(scale_frame, text="Коэфф. масштаб.:", font=(
    "Calibry", 12)).grid(row=0, column=0, sticky="w")
coef_scale_entry = tk.Entry(scale_frame, font=("Calibry", 12))
coef_scale_entry.grid(row=0, column=1)
coef_scale_entry.insert(0, "30")
make_button('Масштабировать', scale_frame, 35).grid(
    row=1, column=0, columnspan=2, stick='we')


# поворот
rotate_frame = tk.Frame(window)
rotate_frame.grid(row=5, column=0, padx=5, pady=2)
tk.Label(rotate_frame, text="Поворот:", font=(
    "Calibry", 12)).grid(row=0, column=0, sticky="w")
tk.Label(rotate_frame, text="Коэффициент по х:", font=(
    "Calibry", 12)).grid(row=1, column=0, sticky="w")
coef_rotate_x_entry = tk.Entry(rotate_frame, font=("Calibry", 12))
coef_rotate_x_entry.grid(row=1, column=1)
coef_rotate_x_entry.insert(0, "30")
make_button('Повернуть по x', rotate_frame, 35).grid(
    row=2, column=0, columnspan=2, stick='we')
tk.Label(rotate_frame, text="Коэффициент по y:", font=(
    "Calibry", 12)).grid(row=3, column=0, sticky="w")
coef_rotate_y_entry = tk.Entry(rotate_frame, font=("Calibry", 12))
coef_rotate_y_entry.grid(row=3, column=1)
coef_rotate_y_entry.insert(0, "30")
make_button('Повернуть по y', rotate_frame, 35).grid(
    row=4, column=0, columnspan=2, stick='we')
tk.Label(rotate_frame, text="Коэффициент по z:", font=(
    "Calibry", 12)).grid(row=5, column=0, sticky="w")
coef_rotate_z_entry = tk.Entry(rotate_frame, font=("Calibry", 12))
coef_rotate_z_entry.grid(row=5, column=1)
coef_rotate_z_entry.insert(0, "30")
make_button('Повернуть по z', rotate_frame, 35).grid(
    row=6, column=0, columnspan=2, stick='we')


# Создаем поле для кнопок
res_frame = tk.Frame(window)
res_frame.grid(row=6, column=0, padx=5, pady=2)
# Создаем кнопку для построения
make_button('Построить', res_frame, 15).grid(row=0, column=0, stick='we')
# Создаем кнопку для очиски холста
make_button('Очистить холст', res_frame, 18).grid(
    row=0, column=1, stick='we')


tk.Label(window, text="Талышева Олеся ИУ7-45Б", bg='light pink',
         fg='grey', font=("Arial", 12, 'italic')).grid(row=8, column=0)

# Функции для приближения и удаления


def zoom_in(event: Optional[tk.Event] = None) -> None:
    if not is_painting:
        global ZOOM
        ZOOM *= 1.1
        cnv.scale("all", 0, 0, 1.1, 1.1)


def zoom_out(event: Optional[tk.Event] = None) -> None:
    if not is_painting:
        global ZOOM
        ZOOM *= 0.9
        cnv.scale("all", 0, 0, 0.9, 0.9)

# Функции для перемещения
# Функция для перемещения влево


def move_left(event: Optional[tk.Event] = None) -> None:
    if not is_painting:
        global SIDE_PLACE
        SIDE_PLACE += 1
        cnv.xview_scroll(round(-1 * ZOOM), "units")

# Функция для перемещения вправо


def move_right(event: Optional[tk.Event] = None) -> None:
    if not is_painting:
        global SIDE_PLACE
        SIDE_PLACE -= 1
        cnv.xview_scroll(round(1 * ZOOM), "units")


def move_up(event: Optional[tk.Event] = None) -> None:
    if not is_painting:
        global HEIGHT_PLACE
        HEIGHT_PLACE -= 1
        cnv.yview_scroll(round(-1 * ZOOM), "units")


def move_down(event: Optional[tk.Event] = None) -> None:
    if not is_painting:
        global HEIGHT_PLACE
        HEIGHT_PLACE += 1
        cnv.yview_scroll(round(1 * ZOOM), "units")


# Функция создаёт кнопку (только ей передаётся функция которая вызывается при нажатии)


def make_cnv_button(doing: str, button_frame: tk.Frame, width1: int, func) -> None:
    return tk.Button(button_frame, text=doing, bd=7, font=("Calibry", 12),
                     command=lambda: func(), activebackground="salmon", bg="khaki", height=1, width=width1)


# Создаем кнопок для изменения конфигурации холста
button_frame3 = tk.Frame(window)
button_frame3.grid(row=8, column=2, padx=0, pady=0)
make_cnv_button('вверх', button_frame3, 10, move_up).grid(
    row=0, column=0, stick='we')
make_cnv_button('вниз', button_frame3, 10, move_down).grid(
    row=0, column=1, stick='we')
make_cnv_button('вправо', button_frame3, 10, move_right).grid(
    row=0, column=2, stick='we')
make_cnv_button('влево', button_frame3, 10, move_left).grid(
    row=0, column=3, stick='we')
make_cnv_button('увеличить', button_frame3, 10, zoom_in).grid(
    row=0, column=5, stick='we')
make_cnv_button('уменьшить', button_frame3, 10, zoom_out).grid(
    row=0, column=6, stick='we')

for i in range(9):
    window.grid_rowconfigure(i, weight=1)

# Создаём меню
menu = tk.Menu(window)
window.config(menu=menu)

# Создаёт вкладку меню "Действия" с выпадающим меню с действиями
menu_in = tk.Menu(menu, tearoff=0)

menu_in.add_command(label='Выбрать цвет плоскости',
                    command=choose_color)
menu_in.add_command(label='Построить',
                    command=lambda: fork('Построить'))
menu_in.add_command(label='Очистить холст',
                    command=lambda: fork('Очистить холст'))

menu.add_cascade(label="Действия", menu=menu_in)


# Создаёт вкладку меню "Информация" с выпадающим меню с информацией об авторе и программе
menu_inf = tk.Menu(menu, tearoff=0)

menu_inf.add_command(label='Информация об авторе', command=lambda: mb.showinfo(
    'Информация об авторе', "Программу разработала студентка МГТУ им.Н.Э.Баумана группы ИУ7-45Б Талышева Олеся Николаевна."))
menu_inf.add_command(label='Информация о программе', command=lambda: mb.showinfo('Информация о программе',
                                                                                 "Реализация алгоритма плавающего горизонта."))
menu_inf.add_command(label='Руководство пользователя', command=lambda: mb.showinfo('Руководство пользователя',
                                                                                   "Программа реализовывает алгоритм алгоритм плавающего горизонта.\n"
                                                                                   "Можно выбрать формулу для построения, цвет плоскости, коэффициент масштабирования и поворот уже построенного графика "
                                                                                   "по любой из 3-ёх осей. Коэффициент масштабирования по-умолчанию равен 30-и."
                                                                                   "Алгоритм плавающего горизонта запускается по нижитию на кнопку 'Построить'. "
                                                                                   "Можно перемещать и зумить холст, а также вернуть его в стартовое состояние (кнопка 'Очистить холст')."))
menu.add_cascade(label="Информация", menu=menu_inf)


# Функция даёт вставить только +,- и цифры
def checker(key: str) -> None:
    # Создаётся список с названиями окошек ввода
    butt = [(x_start_entry, "целые"), (x_count_entry, "целые"), (x_end_entry, "целые"),
            (z_start_entry, "целые"), (z_count_entry,
                                       "целые"), (z_end_entry, "целые"),
            (coef_scale_entry, "вещественные"), (coef_rotate_x_entry, "вещественные"),
            (coef_rotate_y_entry, "вещественные"), (coef_rotate_z_entry, "вещественные")]
    # Проходимся по всем 6-и окошкам
    for j in range(len(butt)):
        try:
            butt_str = butt[j][0].get()
            if butt_str != "" and butt_str[-1] not in "-+" and butt[j][0].index(tk.INSERT) != 0:
                if butt[j][1] == "вещественные":
                    float(butt_str)
                elif butt[j][1] == "целые":
                    int(butt_str)
        except ValueError:
            # Считывае позицию курсора в этом окошке
            ind = butt[j][0].index(tk.INSERT)
            # Удаляем невалидный символ из поля ввода
            new_str = butt_str
            new_str = new_str[:ind - 1] + new_str[ind:]
            butt[j][0].delete(0, tk.END)
            butt[j][0].insert(0, new_str)
            mb.showerror(
                'Ошибка!', f"В это поле ввода можно вводить только {butt[j][1]} числа.")


# Реагирует на ввод и вызывает функцию checker
window.bind('<KeyRelease>', checker)

# реакция на закрытие окна


def on_closing() -> None:
    if mb.askokcancel("Выход", "Вы уверены что хотите выйти из приложения?"):
        window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)

# Функция для обработки события прокрутки колеса мыши


def scroll(event: tk.Event) -> None:
    if event.delta > 0:
        zoom_in()
    else:
        zoom_out()
# Функция для обработки события нажатия клавиш клавиатуры


def key_press(event: tk.Event) -> None:
    if event.keysym == "Up":
        move_up()
    elif event.keysym == "Down":
        move_down()
    elif event.keysym == "Left":
        move_left()
    elif event.keysym == "Right":
        move_right()


# Привязка обработчиков событий к холсту
cnv.bind("<MouseWheel>", scroll)
window.bind("<KeyPress>", key_press)

# Начальная конфигурация
fork("Очистить холст")

# Включается обработчик событий
window.mainloop()
