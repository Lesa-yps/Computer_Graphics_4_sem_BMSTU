# Талышева Олеся ИУ7-45Б
# Лабораторная работа №3

# Импортируем библиотеки
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from tkinter import colorchooser
from typing import Optional, List
from Grid import STEP_CONST, update_grid
from Algo_build_line import build_line, build_spectr_line, list_algo
from Measurements import build_step_graph, build_time_bar

# Константы
SIZE_OF_CANVAS = 600  # размер холста
MIN_WIDTH = 870 + 310  # минимальная ширина окна приложения
MIN_HEIGHT = 510 + 130  # минимальная высота окна приложения
# Переменные определяющие расположение/состояние окна
ZOOM = 1  # переменная для определения зума
SIDE_PLACE = 0  # переменная для определения сдвига в сторонв
HEIGHT_PLACE = 0  # переменная для определения сдвига по высоте
num_algo = 0  # по умолчанию выбран нулевой алгоритм
color_line = "#000000"  # цвет отрезка по умолчанию чёрный
EPS = 1e-5


# проверяет заполнены ли поля ввода числами (по умолчанию целыми)

def check_input_field(arr_entry: List[tk.Entry], error: str, is_float: bool = False) -> bool:
    try:
        for i in arr_entry:
            if is_float:
                float(i.get())
            else:
                int(i.get())
    except ValueError:
        mb.showerror('Ошибка!', error)
        return False
    else:
        return True

# проверяет положительность длины отрезка


def check_data_spectr(lenght_line: tk.Entry, angle: tk.Entry) -> bool:
    is_ok = False
    if check_input_field([lenght_line], "Длина отрезка должна быть заполнена.", is_float=True)\
            and check_input_field([angle], "Шаг изменения угла наклона должен быть заполнен.", is_float=True):
        if float(lenght_line.get()) >= 0:
            if (360 >= abs(float(angle.get())) >= EPS):
                is_ok = True
            else:
                mb.showerror(
                    'Ошибка!', "Угол должен быть отличен от нуля и по модулю меньше 360 градусов.")
        else:
            mb.showerror(
                'Ошибка!', "Длина отрезка должна быть неотрицательной.")
    return is_ok

# Возврат к начальному состоянию


def cleaning(cnv: tk.Canvas) -> None:
    global ZOOM, SIDE_PLACE, HEIGHT_PLACE, dict_house, dict_house_old
    # Очистка всего содержимого на холсте
    cnv.delete("all")
    # Масштабирование холста до его стартового размера
    cnv.scale("all", 0, 0, 1, 1)
    # Установка положения прокрутки на начальное значение
    cnv.xview_moveto(0)
    cnv.yview_moveto(0)
    ZOOM, SIDE_PLACE, HEIGHT_PLACE = 1, 0, 0
    # Начальная отрисовка координатной сетки
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
    # сдвиг холста, чтобы (0, 0) был в центре
    for i in range(int(SIZE_OF_CANVAS / (STEP_CONST * 2))):
        move_up()
        move_left()


# Функция вызывается в ответ на действия пользователя и выполняет требуемое или вызывает для этого другую функцию
def fork(text: str, x_start: tk.Entry, y_start: tk.Entry, x_end: tk.Entry, y_end: tk.Entry, lenght_line: tk.Entry,
         angle: tk.Entry, cnv: tk.Canvas) -> None:
    # отрисовка отрезка по его координатам конца и начала
    if text == 'Отрисовать отрезок' and check_input_field([x_start, y_start, x_end, y_end], "Координаты отрезка должны быть заполнены."):
        xs, ys, xe, ye = int(float(x_start.get()) * ZOOM), int(float(y_start.get())
                                                               * ZOOM), int(float(x_end.get()) * ZOOM), int(float(y_end.get()) * ZOOM)
        build_line(cnv, (xs, ys), (xe, ye), num_algo, color_line)
    # отрисовка отрезка по его длине в спектре углов
    elif text == 'Отрисовать отрезки в спектре углов' and check_data_spectr(lenght_line, angle):
        build_spectr_line(cnv, float(lenght_line.get()) * ZOOM,
                          float(angle.get()), num_algo, color_line)
    # Отрисовка гистограммы с временем отрисовки всех алгоритмов
    elif text == 'Временной график' and check_data_spectr(lenght_line, angle):
        build_time_bar(float(lenght_line.get()), float(angle.get()))
    # Отрисовка графика с количеством ступенек в зависимости от угла наклона
    elif text == 'Ступенчатый график' and check_input_field([lenght_line], "Длина отрезка должна быть заполнена.", is_float=True):
        if float(lenght_line.get()) >= 0:
            build_step_graph(float(lenght_line.get()))
        else:
            mb.showerror(
                'Ошибка!', "Длина отрезка должна быть неотрицательной.")
    # Очистка экрана
    elif text == 'Очистить экран':
        cleaning(cnv)


# обработка события изменения размера окна
def resize_checker(event: tk.Event) -> None:
    # Получаем текущие размеры окна
    current_width = window.winfo_width()
    current_height = window.winfo_height()
    # Проверяем, если текущий размер меньше минимального, то устанавливаем его минимальным
    if current_width < MIN_WIDTH or current_height < MIN_HEIGHT:
        window.geometry(f'{MIN_WIDTH}x{MIN_HEIGHT}')
    # Начальная отрисовка координатной сетки
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)


# Создаём окошко и обозначаем его параметры
window = tk.Tk()
window["bg"] = 'light pink'
window.title("Лабораторная работа по компьютерной графике №3")
window.geometry(f'{MIN_WIDTH}x{MIN_HEIGHT}')
# Устанавливается минимальный размер окна
window.minsize(MIN_WIDTH, MIN_HEIGHT)
# Привязываем обработчик события изменения размера окна
window.bind("<Configure>", resize_checker)


# Создаётся холст с установленными размерами
cnv = tk.Canvas(window, width=SIZE_OF_CANVAS, height=SIZE_OF_CANVAS, bg="white",
                cursor="plus", xscrollincrement=STEP_CONST, yscrollincrement=STEP_CONST)
cnv.grid(row=0, column=1, rowspan=8, sticky='nsew')
window.grid_columnconfigure(1, weight=1)

# Функция создаёт кнопку


def make_button(doing: str, button_frame: tk.Frame, width1: int) -> tk.Button:
    return tk.Button(button_frame, text=doing, bd=7, font=("Calibry", 12), command=lambda: fork(doing, x_start,
                                                                                                y_start, x_end, y_end, lenght_line, angle, cnv), activebackground="salmon", bg="khaki", height=1, width=width1)


# Функция для обработки события выбора алгоритма в выпадающем списке
def what_choose_algo(event: tk.Event):
    global num_algo
    num_algo = chooser_algo.current()


# Создаем выпадающий список алгоритмов
chooser_algo = ttk.Combobox(
    window, width=50, height=35, font=("Calibry", 12), state="readonly")
chooser_algo["values"] = [i[1]
                          for i in list_algo]  # Устанавливаем список вариантов
chooser_algo.current(0)  # Устанавливаем начальное значение
# Привязываем обработчик события выбора элемента
chooser_algo.bind("<<ComboboxSelected>>", what_choose_algo)
chooser_algo.grid(row=0, column=0, padx=10, pady=10)

# выбор цвета отрезка


def choose_color() -> None:
    global color_line
    color = colorchooser.askcolor(title="Выберите цвет")
    # Используется второй элемент кортежа для получения выбранного цвета
    color_line = color[1]


button_color = tk.Button(window, text="Выбрать цвет отрезка", command=choose_color, activebackground="salmon", bg="khaki", width=50,
                         bd=7, font=("Calibry", 12))
button_color.grid(row=1, column=0, padx=10, pady=10)

# Создаем поля для ввода координат начала отрезка
start_input_frame = tk.Frame(window, bg="light pink")
start_input_frame.grid(row=2, column=0, padx=10, pady=10)
tk.Label(start_input_frame, text="Координаты отрезка:", font=(
    "Calibry", 12), bg="light pink").grid(row=0, column=0)
tk.Label(start_input_frame, text="Начало отрезка:", font=(
    "Calibry", 12), bg="light pink").grid(row=1, column=0)
tk.Label(start_input_frame, text="x:", font=("Calibry", 12),
         bg="light pink").grid(row=2, column=0)
x_start = tk.Entry(start_input_frame, font=("Calibry", 12))
x_start.grid(row=2, column=1)
tk.Label(start_input_frame, text="y:", font=("Calibry", 12),
         bg="light pink").grid(row=3, column=0)
y_start = tk.Entry(start_input_frame, font=("Calibry", 12))
y_start.grid(row=3, column=1)

# Создаем поля для ввода координат конца отрезка
end_input_frame = tk.Frame(window, bg="light pink")
end_input_frame.grid(row=3, column=0, padx=10, pady=10)
tk.Label(end_input_frame, text="Конец отрезка:", font=(
    "Calibry", 12), bg="light pink").grid(row=0, column=0)
tk.Label(end_input_frame, text="x:", font=("Calibry", 12),
         bg="light pink").grid(row=1, column=0)
x_end = tk.Entry(end_input_frame, font=("Calibry", 12))
x_end.grid(row=1, column=1)
tk.Label(end_input_frame, text="y:", font=("Calibry", 12),
         bg="light pink").grid(row=2, column=0)
y_end = tk.Entry(end_input_frame, font=("Calibry", 12))
y_end.grid(row=2, column=1)

# Создаем кнопку дляя отрисовки отрезка
make_button('Отрисовать отрезок', window, 50).grid(
    row=4, column=0, padx=10, pady=10)

# Создаем поля для ввода параметров исследования визуальных характеристик
visual_input_frame = tk.Frame(window, bg="light pink")
visual_input_frame.grid(row=5, column=0, padx=10, pady=10)
tk.Label(visual_input_frame, text="Исследование визуальных характеристик:",
         font=("Calibry", 12), bg="light pink").grid(row=0, column=0)
tk.Label(visual_input_frame, text="Угол:", font=(
    "Calibry", 12), bg="light pink").grid(row=1, column=0)
angle = tk.Entry(visual_input_frame, font=("Calibry", 12))
angle.grid(row=1, column=1)
tk.Label(visual_input_frame, text="Длина отрезка:", font=(
    "Calibry", 12), bg="light pink").grid(row=2, column=0)
lenght_line = tk.Entry(visual_input_frame, font=("Calibry", 12))
lenght_line.grid(row=2, column=1)


# Создаем кнопку дляя отрисовки отрезков в спектре углов
make_button('Отрисовать отрезки в спектре углов', window,
            50).grid(row=6, column=0, padx=10, pady=10)

# Создаем кнопок для построения временного и ступенчатого графика, очистки экрана
button_frame1 = tk.Frame(window)
button_frame1.grid(row=7, column=0, padx=10, pady=10)
make_button('Временной график', button_frame1,
            16).grid(row=0, column=0, stick='we')
make_button('Ступенчатый график', button_frame1, 18).grid(
    row=0, column=1, stick='we')
make_button('Очистить экран', button_frame1, 13).grid(
    row=0, column=2, stick='we')


tk.Label(window, text="Талышева Олеся ИУ7-45Б", bg='light pink',
         fg='grey', font=("Arial", 12, 'italic')).grid(row=8, column=0)

# Функции для приближения и удаления


def zoom_in(event: Optional[tk.Event] = None) -> None:
    global ZOOM
    ZOOM *= 1.1
    cnv.scale("all", 0, 0, 1.1, 1.1)
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)


def zoom_out(event: Optional[tk.Event] = None) -> None:
    global ZOOM
    ZOOM *= 0.9
    cnv.scale("all", 0, 0, 0.9, 0.9)
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
# Функции для перемещения
# Функция для перемещения влево


def move_left(event: Optional[tk.Event] = None) -> None:
    global SIDE_PLACE
    SIDE_PLACE += 1
    cnv.xview_scroll(round(-1 * ZOOM), "units")
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
# Функция для перемещения вправо


def move_right(event: Optional[tk.Event] = None) -> None:
    global SIDE_PLACE
    SIDE_PLACE -= 1
    cnv.xview_scroll(round(1 * ZOOM), "units")
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)


def move_up(event: Optional[tk.Event] = None) -> None:
    global HEIGHT_PLACE
    HEIGHT_PLACE -= 1
    cnv.yview_scroll(round(-1 * ZOOM), "units")
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)


def move_down(event: Optional[tk.Event] = None) -> None:
    global HEIGHT_PLACE
    HEIGHT_PLACE += 1
    cnv.yview_scroll(round(1 * ZOOM), "units")
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)

# Функция создаёт кнопку (только ей передаётся функция которая вызывается при нажатии)


def make_cnv_button(doing: str, button_frame: tk.Frame, width1: int, func) -> tk.Button:
    return tk.Button(button_frame, text=doing, bd=7, font=("Calibry", 12),
                     command=lambda: func(), activebackground="salmon", bg="khaki", height=1, width=width1)


# Создаем кнопок для изменения конфигурации холста
button_frame3 = tk.Frame(window)
button_frame3.grid(row=8, column=1, padx=0, pady=0)
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
menu_act = tk.Menu(menu, tearoff=0)
action_list = ['Отрисовать отрезок', 'Отрисовать отрезки в спектре углов',
               'Временной график', 'Ступенчатый график', 'Очистить экран']
for action in action_list:
    menu_act.add_command(label=action, command=lambda action=action: fork(
        action, x_start, y_start, x_end, y_end, lenght_line, angle, cnv))
menu.add_cascade(label="Действия", menu=menu_act)


# Создаёт вкладку меню "Информация" с выпадающим меню с информацией об авторе и программе
menu_inf = tk.Menu(menu, tearoff=0)
menu_inf.add_command(label='Информация об авторе', command=lambda: mb.showinfo(
    'Информация об авторе', "Програму разработала студентка МГТУ им. Баумана Талышева Олеся Николаевна учебная группа ИУ7-45Б."))
menu_inf.add_command(label='Информация о программе', command=lambda: mb.showinfo('Информация о программе',
                                                                                 "Реализация и исследование алгоритмов построения отрезка."))
menu_inf.add_command(label='Руководство пользователя', command=lambda: mb.showinfo('Руководство пользователя',
                                                                                   "В верхнем окошке пользователю предоставляется выбор алгоритма для построения отрезка.\n\
     Кнопка 'Выбрать цвет отрезка' позволяет пользователю выбрать цвет, которым будет нарисован отрезок.\n\
     Ниже вводятся координаты начала и конца отрезка (целочисленные) и затем кнопка 'Отрисовать отрезок' строит отрезок по введенным координатам.\n\
     Для отрисовки отрезка в спектре углов по соответствующей кнопке нужно ввести угол (от 1 до 360 по модулю) и\
     длину отрезка (неотрицательную), оба значения вещественные.\n\
     Также программа позволяет построить гистограмму замеров времени сбора данных для построения отрезков в спектрах углов и\n\
     график ступенчатости алгоритмов по углу (с шагом 2 градуса) по соответствующим кнопкам.\n\
     Кнопка 'Очистить экран' позволяет привести холст в стартовое положение.\n\
     Также под холстом представлены кнопки, позволяющие зумить и двигать изображение (что могут и стрелочки на клавиатуре и скролл мышки)."))

menu.add_cascade(label="Информация", menu=menu_inf)

# приведение холста в стартовое состояние
fork('Очистить экран', x_start, y_start, x_end, y_end, lenght_line, angle, cnv)


# Функция даёт вставить только +,- и цифры
def checker(key: str) -> None:
    # Создаётся список с названиями окошек ввода
    butt = [(x_start, "целые"), (y_start, "целые"), (x_end, "целые"),
            (y_end, "целые"), (lenght_line, "вещественные"), (angle, "вещественные")]
    # Проходимся по всем 5-и окошкам
    for j in range(len(butt)):
        try:
            if (butt[j][0].get()) != "" and (butt[j][0].get())[-1] not in "-+" and butt[j][0].index(tk.INSERT) != 0:
                if butt[j][1] == "вещественные":
                    float(butt[j][0].get())
                elif butt[j][1] == "целые":
                    int(butt[j][0].get())
        except ValueError:
            # Считывае позицию курсора в этом окошке
            ind = butt[j][0].index(tk.INSERT)
            # Удаляем невалидный символ из поля ввода
            new_str = butt[j][0].get()
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

# Включается обработчик событий
window.mainloop()
