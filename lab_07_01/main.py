# Талышева Олеся ИУ7-45Б
# Лабораторная работа №7

# Импортируем библиотеки
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from tkinter import colorchooser
from typing import Optional, List, Tuple
from Grid import STEP_CONST, update_grid
from Cutting_off_lines import cutting_off_all_lines
from Point_line import clever_draw_line, check_input_field
import Const as c

# Константы
SIZE_OF_CANVAS = 500  # размер холста
MIN_WIDTH = 870 + 257  # минимальная ширина окна приложения
MIN_HEIGHT = 550 + 140  # минимальная высота окна приложения
# Переменные определяющие расположение/состояние окна
ZOOM = 1  # переменная для определения зума
SIDE_PLACE = 0  # переменная для определения сдвига в сторонв
HEIGHT_PLACE = 0  # переменная для определения сдвига по высоте
# массив цветов
arr_colors = ["#000000" for _ in range(3)]  # цвет по умолчанию чёрный
# эта переменная блокирует изменение положения и зума холста, пока фигура закрашивается
is_painting = False

# сброс всего наработанного


def cleaning(cnv: tk.Canvas, tree: ttk.Treeview) -> None:
    global ZOOM, SIDE_PLACE, HEIGHT_PLACE
    # Очистка всего содержимого на холсте
    cnv.delete("all")
    # Получаем все элементы таблицы
    items = tree.get_children()
    # Удаляем каждый элемент из таблицы
    for item in items:
        tree.delete(item)
    # Масштабирование холста до его стартового размера
    cnv.scale("all", 0, 0, 1, 1)
    # Установка положения прокрутки на начальное значение
    cnv.xview_moveto(0)
    cnv.yview_moveto(0)
    ZOOM, SIDE_PLACE, HEIGHT_PLACE = 1, 0, 0
    # Начальная отрисовка координатной сетки
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)

# формирование отсекателя


def make_clipper() -> List[int]:
    clipper = [0 for _ in range(c.LEN_CLIPPER)]
    clipper[c.X_LEFT] = int(xl_clipper_entry.get())
    clipper[c.X_RIGHT] = int(xr_clipper_entry.get())
    if clipper[c.X_LEFT] > clipper[c.X_RIGHT]:
        clipper[c.X_LEFT], clipper[c.X_RIGHT] = clipper[c.X_RIGHT], clipper[c.X_LEFT]
    clipper[c.Y_UP] = int(yu_clipper_entry.get())
    clipper[c.Y_DOWN] = int(yd_clipper_entry.get())
    if clipper[c.Y_DOWN] > clipper[c.Y_UP]:
        clipper[c.Y_UP], clipper[c.Y_DOWN] = clipper[c.Y_DOWN], clipper[c.Y_UP]
    return clipper

# формирование массива линий из таблицы


def make_line_arr() -> List[List[Tuple[int]]]:
    line_arr = list()
    for item in tree.get_children():
        xs = int(tree.item(item, "values")[0])
        ys = int(tree.item(item, "values")[1])
        xe = int(tree.item(item, "values")[2])
        ye = int(tree.item(item, "values")[3])
        line_arr.append([(xs, ys), (xe, ye)])
    return line_arr


# Функция вызывается в ответ на действия пользователя и выполняет требуемое или вызывает для этого другую функцию


def fork(text: str) -> None:
    global is_painting
    if is_painting:
        mb.showerror('Ошибка!', "Дождитесь конца отсечения!")
    elif text == 'Добавить отрезок' and check_input_field([xs_entry, ys_entry, xe_entry, ye_entry], "добавляемый отрезок"):
        xs, ys, xe, ye = int(xs_entry.get()), int(
            ys_entry.get()), int(xe_entry.get()), int(ye_entry.get())
        clever_draw_line(cnv, tree, (xs, ys), (xe, ye), ZOOM)
    # Вызывается функция для отсечения
    elif text == 'Отсечь' and check_input_field([xl_clipper_entry, xr_clipper_entry, yu_clipper_entry, yd_clipper_entry], "отсекатель"):
        is_painting = True
        # формирование отсекателя
        clipper = make_clipper()
        # формирование массива линий из таблицы
        line_arr = make_line_arr()
        # отсечение по всем линиям
        cutting_off_all_lines(cnv, line_arr, clipper, arr_colors, ZOOM)
        is_painting = False
    # Очистка всего
    elif text == 'Очистить холст':
        cleaning(cnv, tree)


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
window.title("Лабораторная работа по компьютерной графике №7")
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

# Создаем фрейм для размещения таблицы
table_frame = tk.Frame(window)
table_frame.grid(row=0, rowspan=5, columnspan=2, column=0, padx=5, pady=2)
# стиль
style = ttk.Style().configure('Treeview', font=("Calibry", 12))
# Создаем Treeview для отображения таблицы
tree = ttk.Treeview(table_frame, columns=(
    "xs", "ys", "xe", "ye"), show="headings", height=20)
tree.heading("xs", text="Xн")
tree.heading("ys", text="Yн")
tree.heading("xe", text="Xк")
tree.heading("ye", text="Yк")
tree.column("xs", width=100)
tree.column("ys", width=100)
tree.column("xe", width=100)
tree.column("ye", width=100)
tree.pack()

# Функция создаёт кнопку


def make_button(doing: str, button_frame: tk.Frame, width1: int) -> tk.Button:
    return tk.Button(button_frame, text=doing, bd=7, font=("Calibry", 12),
                     command=lambda: fork(doing),
                     activebackground="salmon", bg="khaki", height=1, width=width1, cursor="hand1")


# Создаем поля для ввода отрезка
input_frame = tk.Frame(window)
input_frame.grid(row=5, column=0, padx=5, pady=2)
tk.Label(input_frame, text="Xн:", font=("Calibry", 12)).grid(row=0, column=0)
xs_entry = tk.Entry(input_frame, font=("Calibry", 12))
xs_entry.grid(row=0, column=1)
tk.Label(input_frame, text="Yн:", font=("Calibry", 12)).grid(row=0, column=2)
ys_entry = tk.Entry(input_frame, font=("Calibry", 12))
ys_entry.grid(row=0, column=3)
tk.Label(input_frame, text="Xк:", font=("Calibry", 12)).grid(row=1, column=0)
xe_entry = tk.Entry(input_frame, font=("Calibry", 12))
xe_entry.grid(row=1, column=1)
tk.Label(input_frame, text="Yк:", font=("Calibry", 12)).grid(row=1, column=2)
ye_entry = tk.Entry(input_frame, font=("Calibry", 12))
ye_entry.grid(row=1, column=3)
# Создаем кнопку для добавления отрезка
make_button('Добавить отрезок', input_frame, 10).grid(
    row=2, column=0, columnspan=8, stick='we')


# выбор цвета отрезка
def choose_color(num) -> None:
    color = colorchooser.askcolor(title="Выберите цвет")
    # Используется второй элемент кортежа для получения выбранного цвета
    arr_colors[num] = color[1]


# Создаем фрейм для кнопок выбора цветов
color_frame = tk.Frame(window)
color_frame.grid(row=6, column=0, padx=5, pady=2)
tk.Label(color_frame, text="Выбор цветов:",
         font=("Calibry", 12)).grid(row=0, column=0)
button1_color = tk.Button(color_frame, text="Отсекателя", command=lambda: choose_color(c.COLOR_CLIPPER), activebackground="salmon", bg="khaki",
                          width=23, height=1, bd=7, font=("Calibry", 12))
button1_color.grid(row=0, column=1, stick='we')
button2_color = tk.Button(color_frame, text="Видимых линий", command=lambda: choose_color(c.COLOR_VIS_LINE), activebackground="salmon", bg="khaki",
                          width=20, height=1, bd=7, font=("Calibry", 12))
button2_color.grid(row=1, column=0, stick='we')
button3_color = tk.Button(color_frame, text="Невидимых линий", command=lambda: choose_color(c.COLOR_UNVIS_LINE), activebackground="salmon", bg="khaki",
                          width=23, height=1, bd=7, font=("Calibry", 12))
button3_color.grid(row=1, column=1, stick='we')


# Создаем поле для ввода отсекателя
res_frame = tk.Frame(window)
res_frame.grid(row=7, column=0, padx=5, pady=2)
tk.Label(res_frame, text="Координаты отсекателя:", font=(
    "Calibry", 12)).grid(row=0, column=0, columnspan=2, stick='we')
tk.Label(res_frame, text="Xп:", font=("Calibry", 12)).grid(row=1, column=0)
xr_clipper_entry = tk.Entry(res_frame, font=("Calibry", 12))
xr_clipper_entry.grid(row=1, column=1)
tk.Label(res_frame, text="Yв:", font=("Calibry", 12)).grid(row=1, column=2)
yu_clipper_entry = tk.Entry(res_frame, font=("Calibry", 12))
yu_clipper_entry.grid(row=1, column=3)
tk.Label(res_frame, text="Xл:", font=("Calibry", 12)).grid(row=2, column=0)
xl_clipper_entry = tk.Entry(res_frame, font=("Calibry", 12))
xl_clipper_entry.grid(row=2, column=1)
tk.Label(res_frame, text="Yн:", font=("Calibry", 12)).grid(row=2, column=2)
yd_clipper_entry = tk.Entry(res_frame, font=("Calibry", 12))
yd_clipper_entry.grid(row=2, column=3)
# Создаем кнопку для отсечения
make_button('Отсечь', res_frame,
            15).grid(row=3, column=0, columnspan=2, stick='we')
# Создаем кнопку для очиски холста
make_button('Очистить холст', res_frame, 15).grid(
    row=3, column=2, columnspan=2, stick='we')


tk.Label(window, text="Талышева Олеся ИУ7-45Б", bg='light pink',
         fg='grey', font=("Arial", 12, 'italic')).grid(row=8, column=0)

# Функции для приближения и удаления


def zoom_in(event: Optional[tk.Event] = None) -> None:
    if not is_painting:
        global ZOOM
        ZOOM *= 1.1
        cnv.scale("all", 0, 0, 1.1, 1.1)
        update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)


def zoom_out(event: Optional[tk.Event] = None) -> None:
    if not is_painting:
        global ZOOM
        ZOOM *= 0.9
        cnv.scale("all", 0, 0, 0.9, 0.9)
        update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
# Функции для перемещения
# Функция для перемещения влево


def move_left(event: Optional[tk.Event] = None) -> None:
    if not is_painting:
        global SIDE_PLACE
        SIDE_PLACE += 1
        cnv.xview_scroll(round(-1 * ZOOM), "units")
        update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
# Функция для перемещения вправо


def move_right(event: Optional[tk.Event] = None) -> None:
    if not is_painting:
        global SIDE_PLACE
        SIDE_PLACE -= 1
        cnv.xview_scroll(round(1 * ZOOM), "units")
        update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)


def move_up(event: Optional[tk.Event] = None) -> None:
    if not is_painting:
        global HEIGHT_PLACE
        HEIGHT_PLACE -= 1
        cnv.yview_scroll(round(-1 * ZOOM), "units")
        update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)


def move_down(event: Optional[tk.Event] = None) -> None:
    if not is_painting:
        global HEIGHT_PLACE
        HEIGHT_PLACE += 1
        cnv.yview_scroll(round(1 * ZOOM), "units")
        update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)

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

menu_in.add_command(label='Добавить отрезок',
                    command=lambda: fork('Добавить отрезок'))
menu_in.add_command(label='Отсечь',
                    command=lambda: fork('Отсечь'))
menu_in.add_command(label='Очистить холст',
                    command=lambda: fork('Очистить холст'))

menu.add_cascade(label="Действия", menu=menu_in)


# Создаёт вкладку меню "Информация" с выпадающим меню с информацией об авторе и программе
menu_inf = tk.Menu(menu, tearoff=0)

menu_inf.add_command(label='Информация об авторе', command=lambda: mb.showinfo(
    'Информация об авторе', "Программу разработала студентка МГТУ им.Н.Э.Баумана группы ИУ7-45Б Талышева Олеся Николаевна."))
menu_inf.add_command(label='Информация о программе', command=lambda: mb.showinfo('Информация о программе',
                                                                                 "Реализация простого алгоритма отсечения отрезка регулярным отсекателем."))
menu_inf.add_command(label='Руководство пользователя', command=lambda: mb.showinfo('Руководство пользователя',
                                                                                   "Программа реализовывает простой алгоритм отсечения отрезка регулярным отсекателем.\n"
                                                                                   "Отрезки строятся вводом с клавиатуры в специальные поля. Координаты отсекателя "
                                                                                   "(х_левое, х_правое, у_верхнее, у_нижнее) также вводятся с клавиатуры в специальные поля. "
                                                                                   "Координаты введённых отрезков отображаются слева от холста в таблице. "
                                                                                   "Программа также позволяет выбрать цвета отсекателя, видимых и невидимых отрезков. "
                                                                                   "Алгоритм отсечения запускается по нижитию на кнопку 'Отсечь'. "
                                                                                   "Можно перемещать и зумить холст, а также вернуть его в стартовое состояние. "
                                                                                   "Координаты можно ввести только целые."))
menu.add_cascade(label="Информация", menu=menu_inf)


# Функция даёт вставить только +,- и цифры
def checker(key: str) -> None:
    # Создаётся список с названиями окошек ввода
    butt = [(xl_clipper_entry, "целые"), (xr_clipper_entry, "целые"), (yu_clipper_entry, "целые"), (yd_clipper_entry, "целые"),
            (xs_entry, "целые"), (xe_entry, "целые"), (ys_entry, "целые"), (ys_entry, "целые")]
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

# Начальная конфигурация
fork("Очистить холст")

# Включается обработчик событий
window.mainloop()
