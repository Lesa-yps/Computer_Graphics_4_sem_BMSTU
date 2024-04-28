# Талышева Олеся ИУ7-45Б
# Лабораторная работа №6

# Импортируем библиотеки
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from tkinter import colorchooser
from typing import Optional
from Grid import STEP_CONST, update_grid, new_coord_xy
from Paint_over_figure import paint_over_figure, AREA_PIXELS
from Point import touch, check_input_field, draw_line

# Константы
SIZE_OF_CANVAS = 500  # размер холста
MIN_WIDTH = 870 + 257  # минимальная ширина окна приложения
MIN_HEIGHT = 550 + 140  # минимальная высота окна приложения
# Переменные определяющие расположение/состояние окна
ZOOM = 1  # переменная для определения зума
SIDE_PLACE = 0  # переменная для определения сдвига в сторонв
HEIGHT_PLACE = 0  # переменная для определения сдвига по высоте
color_fig = "#000000"  # цвет фигуры по умолчанию чёрный
# эта переменная блокирует изменение положения и зума холста, пока фигура закрашивается
is_painting = False
# список замкнутых фигур, состоящий из списка рёбер
edges_mat = [list()]

# сброс всего наработанного


def cleaning(cnv: tk.Canvas, tree: ttk.Treeview) -> None:
    global ZOOM, SIDE_PLACE, HEIGHT_PLACE, edges_mat
    # Очистка всего содержимого на холсте
    cnv.delete("all")
    # Получаем все элементы таблицы
    items = tree.get_children()
    # Удаляем каждый элемент из таблицы
    for item in items:
        tree.delete(item)
    # удалили все старые фигуры (ребра)
    edges_mat = [list()]
    # Масштабирование холста до его стартового размера
    cnv.scale("all", 0, 0, 1, 1)
    # Установка положения прокрутки на начальное значение
    cnv.xview_moveto(0)
    cnv.yview_moveto(0)
    ZOOM, SIDE_PLACE, HEIGHT_PLACE = 1, 0, 0
    # Начальная отрисовка координатной сетки
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)

# проверка поля ввода таймаута (задержки)


def check_timeout(time_entry: tk.Entry) -> bool:
    rc = True
    time_str = time_entry.get()
    if time_str != "":
        try:
            float(time_str)
        except ValueError:
            mb.showerror(
                'Ошибка!', "Поле ввода задержки выполнения должно быть веществе")
            rc = False
    return rc

# Функция вызывается в ответ на действия пользователя и выполняет требуемое или вызывает для этого другую функцию


def fork(text: str) -> None:
    global edges_mat, is_painting
    if is_painting:
        mb.showerror('Ошибка!', "Дождитесь конца закраски фигуры!")
    # Отрисовка точку
    elif text == 'Добавить точку' and check_input_field(x_add_entry, y_add_entry, "добавляемая точка"):
        x, y = int(x_add_entry.get()), int(y_add_entry.get())
        touch(x, y, cnv, tree, ZOOM, SIDE_PLACE,
              HEIGHT_PLACE, edges_mat[-1], is_painting, False)
    # для замыкания фигуры в edges_mat создаётся новый список
    elif text == 'Замкнуть фигуру' and len(edges_mat[-1]) > 0:
        if (len(edges_mat[-1]) > 1):
            x, y = edges_mat[-1][0]
            draw_line(cnv, x, y, edges_mat[-1])
        edges_mat.append(list())
    # Вызывается функция paint_over_figure для закраски фигуры
    elif text == 'Закрасить фигуру' and check_timeout(time_entry) and check_input_field(x_seed_entry, y_seed_entry, "затравка"):
        is_painting = True
        # если поле времени задержки пусто, то оно нуль
        timeout = 0 if time_entry.get() == "" else float(time_entry.get())
        # координаты затравки
        point_seed = (round(int(x_seed_entry.get()) * ZOOM),
                      round(int(y_seed_entry.get()) * ZOOM))
        paint_over_figure(cnv, point_seed, edges_mat, color_fig, timeout)
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
window.title("Лабораторная работа по компьютерной графике №5")
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
table_frame.grid(row=0, rowspan=5, columnspan=2, column=0, padx=10, pady=10)
# стиль
style = ttk.Style().configure('Treeview', font=("Calibry", 12))
# Создаем Treeview для отображения таблицы
tree = ttk.Treeview(table_frame, columns=(
    "x", "y"), show="headings", height=20)
tree.heading("x", text="X")
tree.heading("y", text="Y")
tree.column("x", width=200)
tree.column("y", width=200)
tree.pack()

# Функция создаёт кнопку


def make_button(doing: str, button_frame: tk.Frame, width1: int) -> tk.Button:
    return tk.Button(button_frame, text=doing, bd=7, font=("Calibry", 12),
                     command=lambda: fork(doing),
                     activebackground="salmon", bg="khaki", height=1, width=width1)


# Создаем поля для ввода координат
input_frame = tk.Frame(window)
input_frame.grid(row=5, column=0, padx=10, pady=10)
tk.Label(input_frame, text="X:", font=("Calibry", 12)).grid(row=0, column=0)
x_add_entry = tk.Entry(input_frame, font=("Calibry", 12))
x_add_entry.grid(row=0, column=1)
tk.Label(input_frame, text="Y:", font=("Calibry", 12)).grid(row=0, column=2)
y_add_entry = tk.Entry(input_frame, font=("Calibry", 12))
y_add_entry.grid(row=0, column=3)
# Создаем кнопку для добавления точки
make_button('Добавить точку', input_frame, 13).grid(
    row=1, column=0, columnspan=4, stick='we')


# выбор цвета отрезка
def choose_color() -> None:
    global color_fig
    color = colorchooser.askcolor(title="Выберите цвет")
    # Используется второй элемент кортежа для получения выбранного цвета
    color_fig = color[1]


# Создаем фрейм для кнопок (1)
butt_frame = tk.Frame(window)
butt_frame.grid(row=6, column=0, padx=10, pady=10)
# Создаем кнопку для замыкания фигуры
make_button('Замкнуть фигуру', butt_frame, 16).grid(
    row=0, column=0, stick='we')
button_color = tk.Button(butt_frame, text="Выбрать цвет закраски", command=choose_color, activebackground="salmon", bg="khaki",
                         width=25, height=1, bd=7, font=("Calibry", 12))
button_color.grid(row=0, column=1, stick='we')


# Создаем поле для ввода задержки
res_frame = tk.Frame(window)
res_frame.grid(row=7, column=0, padx=10, pady=10)
tk.Label(res_frame, text="Время задержки:", font=(
    "Calibry", 12)).grid(row=0, column=0, columnspan=2, stick='we')
time_entry = tk.Entry(res_frame, font=("Calibry", 12))
time_entry.grid(row=0, column=2, columnspan=2, stick='we')
# координаты затравочного пикселя
tk.Label(res_frame, text="Затравочный пиксель:", font=(
    "Calibry", 12)).grid(row=1, column=0, columnspan=2)
tk.Label(res_frame, text="X:", font=("Calibry", 12)).grid(row=2, column=0)
x_seed_entry = tk.Entry(res_frame, font=("Calibry", 12))
x_seed_entry.grid(row=2, column=1)
tk.Label(res_frame, text="Y:", font=("Calibry", 12)).grid(row=2, column=2)
y_seed_entry = tk.Entry(res_frame, font=("Calibry", 12))
y_seed_entry.grid(row=2, column=3)
# Создаем кнопку для закраски фигуры
make_button('Закрасить фигуру', res_frame,
            20).grid(row=3, column=0, columnspan=2, stick='we')
# Создаем кнопку для очиски холста
make_button('Очистить холст', res_frame, 18).grid(
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

# при нажатии на левую кнопку мыши координаты заносятся в поле ввода коордиат затравки и вызывается функция для закраски


def put_coords_seed(event: Optional[tk.Event]) -> None:
    if is_painting:
        mb.showerror('Ошибка!', "Дождитесь конца закраски фигуры!")
    else:
        x_table, y_table = new_coord_xy(
            event.x, event.y, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
        x_seed_entry.delete(0, tk.END)
        x_seed_entry.insert(0, str(round(x_table * ZOOM)))
        y_seed_entry.delete(0, tk.END)
        y_seed_entry.insert(0, str(round(y_table * ZOOM)))
        # print(ZOOM, event.x, event.y, round(x_table * ZOOM), round(y_table * ZOOM))
        fork('Закрасить фигуру')


# Обработчик нажания кнопками мыши на холст
cnv.bind('<Button-1>', lambda event: touch(event.x, event.y,
         cnv, tree, ZOOM, SIDE_PLACE, HEIGHT_PLACE, edges_mat[-1], is_painting))
cnv.bind('<Button-3>', lambda event: put_coords_seed(event))

# Создаём меню
menu = tk.Menu(window)
window.config(menu=menu)

# Создаёт вкладку меню "Действия" с выпадающим меню с действиями
menu_in = tk.Menu(menu, tearoff=0)

menu_in.add_command(label='Добавить точку',
                    command=lambda: fork('Добавить точку'))
menu_in.add_command(label='Замкнуть фигуру',
                    command=lambda: fork('Замкнуть фигуру'))
menu_in.add_command(label='Закрасить фигуру',
                    command=lambda: fork('Закрасить фигуру'))
menu_in.add_command(label='Очистить холст',
                    command=lambda: fork('Очистить холст'))

menu.add_cascade(label="Действия", menu=menu_in)


# Создаёт вкладку меню "Информация" с выпадающим меню с информацией об авторе и программе
menu_inf = tk.Menu(menu, tearoff=0)

menu_inf.add_command(label='Информация об авторе', command=lambda: mb.showinfo(
    'Информация об авторе', "Программу разработала студентка МГТУ им.Н.Э.Баумана группы ИУ7-45Б Талышева Олеся Николаевна."))
menu_inf.add_command(label='Информация о программе', command=lambda: mb.showinfo('Информация о программе',
                                                                                 "Реализация алгоритма построчного затравочного заполнения."))
menu_inf.add_command(label='Руководство пользователя', command=lambda: mb.showinfo('Руководство пользователя',
                                                                                   "Программа реализовывает алгоритм построчного затравочного заполнения.\n"
                                                                                   "Точки строятся посредством левой кнопки мышки или вводом с клавиатуры. Последовательно "
                                                                                   "введённые точки соединяются линией. Соединить начало и конец ломаной (тем самым завершив "
                                                                                   "построение фигуры) можно кнопкой 'Замкнуть'. Введённые точки отображаются слева от холста в таблице. "
                                                                                   "Затравку можно выбрать, нажав правой кнопкой мышки на холст в нужном месте или ввести с клавиатуры. "
                                                                                   f"Если затравка окажется вне фигур, закрасится область вокруг фигур в {AREA_PIXELS} пикселей(я). "
                                                                                   "Программа также позволяет выбрать цвет закраски фигуры, задержку во время закраски, "
                                                                                   "перемещать и зумить холст (что используется только для просмотра результата), а также вернуть его в стартовое состояние."))
menu.add_cascade(label="Информация", menu=menu_inf)


# Функция даёт вставить только +,- и цифры
def checker(key: str) -> None:
    # Создаётся список с названиями окошек ввода
    butt = [(x_add_entry, "целые"), (y_add_entry, "целые"),
            (x_seed_entry, "целые"), (y_seed_entry, "целые"),
            (time_entry, "вещественные")]
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
