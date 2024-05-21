# Талышева Олеся ИУ7-45Б
# Лабораторная работа №8

# Импортируем библиотеки
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from tkinter import colorchooser
from typing import Optional, List, Tuple
from Grid import STEP_CONST, update_grid
from Cutting_off_lines_any_convex import cutting_off_all_lines
from Point_lines import clever_draw_line, clever_draw_clipper, check_input_field, clean_clipper, redraw_clipper, redraw_lines
from Table import cleaning_table, make_clipper, make_line_arr
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
arr_colors = ["#0000ff", "#00ff00", "#ff0000"]  # цвета по умолчанию
# эта переменная блокирует изменение положения и зума холста, пока фигура закрашивается
is_painting = False


# сброс всего наработанного


def cleaning() -> None:
    global ZOOM, SIDE_PLACE, HEIGHT_PLACE
    # Очистка всего содержимого на холсте
    cnv.delete("all")
    # очистка таблиц
    cleaning_table(tree_line)
    cleaning_table(tree_clipper)
    # Масштабирование холста до его стартового размера
    cnv.scale("all", 0, 0, 1, 1)
    # Установка положения прокрутки на начальное значение
    cnv.xview_moveto(0)
    cnv.yview_moveto(0)
    ZOOM, SIDE_PLACE, HEIGHT_PLACE = 1, 0, 0
    # Начальная отрисовка координатной сетки
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)


def sign(x: float) -> int:
    return (x > 0) - (x < 0)

# проверка отсекателя на выпуклость


def is_convex(figure: List[Tuple[int]]) -> bool:
    rc = (len(figure) >= 3)
    if rc:
        sign_now = 0
        i = 0
        while i < len(figure) and rc:
            (x1, y1) = figure[i]
            (x2, y2) = figure[(i + 1) % len(figure)]
            (x3, y3) = figure[(i + 2) % len(figure)]
            ab = (x2 - x1, y2 - y1)
            bc = (x3 - x2, y3 - y2)
            res = sign(ab[c.X_PART] * bc[c.Y_PART] -
                       bc[c.X_PART] * ab[c.Y_PART])
            if sign_now == 0:
                sign_now = res
            elif res != sign_now and res != 0:
                rc = False
            i += 1
    return rc

# Функция вызывается в ответ на действия пользователя и выполняет требуемое или вызывает для этого другую функцию


def fork(text: str) -> None:
    global is_painting
    if is_painting:
        mb.showerror('Ошибка!', "Дождитесь конца отсечения!")
        return
    redraw_lines(cnv, tree_line, ZOOM)
    if text == 'Добавить отрезок' and check_input_field([xs_entry, ys_entry, xe_entry, ye_entry], "добавляемый отрезок"):
        xs, ys, xe, ye = int(xs_entry.get()), int(
            ys_entry.get()), int(xe_entry.get()), int(ye_entry.get())
        clever_draw_line(cnv, tree_line, (xs, ys), (xe, ye), ZOOM)
    elif text == 'Добавить точку отсекателя' and check_input_field([x_clipper_entry, y_clipper_entry], "добавляемая точка отсекателя"):
        x, y = int(x_clipper_entry.get()), int(y_clipper_entry.get())
        clever_draw_clipper(cnv, tree_clipper, (x, y), ZOOM)
    # Вызывается функция для отсечения
    elif text == 'Отсечь':
        is_painting = True
        # формирование отсекателя
        clipper = make_clipper(tree_clipper)
        if not is_convex(clipper):
            mb.showerror('Ошибка!', "Ошибка в введённом отсекателе.")
        else:
            # формирование массива линий из таблицы
            line_arr = make_line_arr(tree_line)
            # отсечение по всем линиям
            cutting_off_all_lines(cnv, line_arr, clipper, arr_colors, ZOOM)
        is_painting = False
    # Удаление отсекателя
    elif text == 'Удалить отсекатель':
        cleaning_table(tree_clipper)
        clean_clipper(cnv)
    # Очистка всего
    elif text == 'Очистить холст':
        cleaning()


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
window.title("Лабораторная работа по компьютерной графике №8")
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

# Создаем фреймы для размещения таблиц
table_frame = tk.Frame(window)
table_frame.grid(row=0, rowspan=2, column=0, padx=5, pady=2, sticky="nsew")
# стиль
style = ttk.Style().configure('Treeview', font=("Calibry", 12))
# Создаем Treeview для отображения таблицы отрезков
tk.Label(table_frame, text="Введённые линии:",
         font=("Calibry", 12)).grid(row=0, column=0)
tree_line = ttk.Treeview(table_frame, columns=(
    "xs", "ys", "xe", "ye"), show="headings", height=15)
tree_line.heading("xs", text="Xн")
tree_line.heading("ys", text="Yн")
tree_line.heading("xe", text="Xк")
tree_line.heading("ye", text="Yк")
tree_line.column("xs", width=50)
tree_line.column("ys", width=50)
tree_line.column("xe", width=50)
tree_line.column("ye", width=50)
tree_line.grid(row=1, column=0, padx=5, pady=2)
# Создаем Treeview для отображения таблицы точек отсекателя
tk.Label(table_frame, text="Точки отсекателя:",
         font=("Calibry", 12)).grid(row=0, column=1)
tree_clipper = ttk.Treeview(table_frame, columns=(
    "x", "y"), show="headings", height=15)
tree_clipper.heading("x", text="X")
tree_clipper.heading("y", text="Y")
tree_clipper.column("x", width=100)
tree_clipper.column("y", width=100)
tree_clipper.grid(row=1, column=1, padx=5, pady=2)


# Функция создаёт кнопку


def make_button(doing: str, button_frame: tk.Frame, width1: int) -> tk.Button:
    return tk.Button(button_frame, text=doing, bd=7, font=("Calibry", 12),
                     command=lambda: fork(doing),
                     activebackground="salmon", bg="khaki", height=1, width=width1, cursor="hand1")


# Создаем поля для ввода отрезка
input_line_frame = tk.Frame(window)
input_line_frame.grid(row=2, column=0, padx=5, pady=2)
tk.Label(input_line_frame, text="Отрезок:", font=("Calibry", 12)).grid(
    row=0, column=0, columnspan=2, sticky="w")
tk.Label(input_line_frame, text="Xн:", font=(
    "Calibry", 12)).grid(row=1, column=0)
xs_entry = tk.Entry(input_line_frame, font=("Calibry", 12))
xs_entry.grid(row=1, column=1)
tk.Label(input_line_frame, text="Yн:", font=(
    "Calibry", 12)).grid(row=2, column=0)
ys_entry = tk.Entry(input_line_frame, font=("Calibry", 12))
ys_entry.grid(row=2, column=1)
tk.Label(input_line_frame, text="Xк:", font=(
    "Calibry", 12)).grid(row=1, column=2)
xe_entry = tk.Entry(input_line_frame, font=("Calibry", 12))
xe_entry.grid(row=1, column=3)
tk.Label(input_line_frame, text="Yк:", font=(
    "Calibry", 12)).grid(row=2, column=2)
ye_entry = tk.Entry(input_line_frame, font=("Calibry", 12))
ye_entry.grid(row=2, column=3)
# Создаем кнопку для добавления отрезка
make_button('Добавить отрезок', input_line_frame, 10).grid(
    row=3, column=0, columnspan=8, stick='we')

# Создаем поля для ввода точек отсекателя
input_clipper_frame = tk.Frame(window)
input_clipper_frame.grid(row=3, column=0, padx=5, pady=2)
tk.Label(input_clipper_frame, text="Отсекатель:", font=(
    "Calibry", 12)).grid(row=0, column=0, columnspan=2, sticky="w")
tk.Label(input_clipper_frame, text="X:", font=(
    "Calibry", 12)).grid(row=1, column=0)
x_clipper_entry = tk.Entry(input_clipper_frame, font=("Calibry", 12))
x_clipper_entry.grid(row=1, column=1)
tk.Label(input_clipper_frame, text="Y:", font=(
    "Calibry", 12)).grid(row=1, column=2)
y_clipper_entry = tk.Entry(input_clipper_frame, font=("Calibry", 12))
y_clipper_entry.grid(row=1, column=3)
# Создаем кнопку для добавления точки отсекателя
make_button('Добавить точку отсекателя', input_clipper_frame, 23).grid(
    row=2, column=0, columnspan=2, stick='we')
make_button('Удалить отсекатель', input_clipper_frame, 20).grid(
    row=2, column=2, columnspan=2, stick='we')

# выбор цвета отрезка


def choose_color(num: int) -> None:
    color = colorchooser.askcolor(title="Выберите цвет")
    # Используется второй элемент кортежа для получения выбранного цвета
    arr_colors[num] = color[1]


# Создаем фрейм для кнопок выбора цветов
color_frame = tk.Frame(window)
color_frame.grid(row=4, column=0, padx=5, pady=2)
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
res_frame.grid(row=5, column=0, padx=5, pady=2)
# Создаем кнопку для отсечения
make_button('Отсечь', res_frame,
            20).grid(row=0, column=0, stick='we')
# Создаем кнопку для очиски холста
make_button('Очистить холст', res_frame, 23).grid(
    row=0, column=1, stick='we')


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
menu_in.add_command(label='Добавить точку отсекателя',
                    command=lambda: fork('Добавить точку отсекателя'))
menu_in.add_command(label='Отсечь',
                    command=lambda: fork('Отсечь'))
menu_in.add_command(label='Удалить отсекатель',
                    command=lambda: fork('Удалить отсекатель'))
menu_in.add_command(label='Очистить холст',
                    command=lambda: fork('Очистить холст'))

menu.add_cascade(label="Действия", menu=menu_in)


# Создаёт вкладку меню "Информация" с выпадающим меню с информацией об авторе и программе
menu_inf = tk.Menu(menu, tearoff=0)

menu_inf.add_command(label='Информация об авторе', command=lambda: mb.showinfo(
    'Информация об авторе', "Программу разработала студентка МГТУ им.Н.Э.Баумана группы ИУ7-45Б Талышева Олеся Николаевна."))
menu_inf.add_command(label='Информация о программе', command=lambda: mb.showinfo('Информация о программе',
                                                                                 "Реализация простого алгоритма отсечения отрезка произвольным выпуклым отсекателем."))
menu_inf.add_command(label='Руководство пользователя', command=lambda: mb.showinfo('Руководство пользователя',
                                                                                   "Программа реализовывает простой алгоритм отсечения отрезка произвольным выпуклым отсекателем.\n"
                                                                                   "Отрезки строятся вводом с клавиатуры в специальные поля. Координаты отсекателя по точкам "
                                                                                   "также вводятся с клавиатуры в специальные поля (после запуска алгоритма ломаная замыкается). "
                                                                                   "Координаты введённых отрезков и точек отсекателя отображаются слева от холста в таблице. "
                                                                                   "По двойному клику на строку она удаляется с холста и из таблицы. "
                                                                                   "Программа также позволяет выбрать цвета отсекателя, видимых и невидимых отрезков. "
                                                                                   "Алгоритм отсечения запускается по нижитию на кнопку 'Отсечь'. "
                                                                                   "Можно перемещать и зумить холст, а также вернуть его в стартовое состояние. "
                                                                                   "Координаты можно ввести только целые."))
menu.add_cascade(label="Информация", menu=menu_inf)


# Функция даёт вставить только +,- и цифры
def checker(key: str) -> None:
    # Создаётся список с названиями окошек ввода
    butt = [(x_clipper_entry, "целые"), (y_clipper_entry, "целые"),
            (xs_entry, "целые"), (xe_entry, "целые"), (ys_entry, "целые"), (ye_entry, "целые")]
    # Проходимся по всем 6-и окошкам
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


def delete_selected_row(event, table):
    # Получаем выделенную строку из таблицы
    selected_item = table.selection()
    # Убеждаемся, что строка выделена и удаляем её
    if selected_item:
        table.delete(selected_item)
        redraw_lines(cnv, tree_line, ZOOM)
        redraw_clipper(cnv, tree_clipper, ZOOM)


# Привязываем функцию delete_selected_row к событию двойного клика на строке каждой из таблиц
tree_line.bind(
    "<Double-1>", lambda event: delete_selected_row(event, tree_line))
tree_clipper.bind(
    "<Double-1>", lambda event: delete_selected_row(event, tree_clipper))

# Начальная конфигурация
fork("Очистить холст")

# Включается обработчик событий
window.mainloop()
