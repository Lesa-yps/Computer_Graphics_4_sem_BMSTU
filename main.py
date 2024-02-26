# Талышева Олеся ИУ7-45Б
# Лабораторная работа №1

# Импортируем библиотеки
import tkinter as tk
import tkinter.messagebox as mb
from typing import Optional
from Grid import *
from House import *
from Mozg import *

# Константы
SIZE_OF_CANVAS = 500 # размер холста
MIN_WIDTH = 870 + 290 # минимальная ширина окна приложения
MIN_HEIGHT = 510 + 130 # минимальная высота окна приложения
# Переменные определяющие расположение/состояние окна
ZOOM = 1 # переменная для определения зума
SIDE_PLACE = 0 # переменная для определения сдвига в сторонв
HEIGHT_PLACE = 0 # переменная для определения сдвига по высоте

# словарь - дом
dict_house = dict()
# словарь сохраненный дом с прошлого шага
dict_house_old = dict()

    
# Функция вызывается в ответ на действия пользователя и выполняет требуемое или вызывает для этого другую функцию
def fork(text: str, dx: tk.Entry, dy: tk.Entry, kx: tk.Entry, ky: tk.Entry, x_m: tk.Entry, y_m: tk.Entry, \
         angle_turn: tk.Entry, x_t: tk.Entry, y_t: tk.Entry,cnv: tk.Canvas) -> None:
    global ZOOM, SIDE_PLACE, HEIGHT_PLACE
    global ZOOM, dict_house, dict_house_old
    # перенос
    if text == 'Перенести':
        x_d = dx.get()
        y_d = dy.get()
        if x_d and y_d:
            dict_house_old = copy_house(dict_house)
            dict_house = brain_move_house(float(x_d), float(y_d), dict_house)
            draw_house(cnv, dict_house)
            dx.delete(0, "end")
            dy.delete(0, "end")
        else:
            mb.showerror('Ошибка!', "Оба параметра переноса должны быть заполнены.")
    # масштабирование
    elif text == 'Масштабировать':
        x_k = kx.get()
        y_k = ky.get()
        m_x = x_m.get()
        m_y = y_m.get()
        if x_k == "" or y_k == "":
            mb.showerror('Ошибка!', "Оба коэффициента масштафирования должны быть заполнены.")
        elif m_x == "" or m_y == "":
            mb.showerror('Ошибка!', "Обе координаты центра масштафирования должны быть заполнены.")
        else:
            dict_house_old = copy_house(dict_house)
            dict_house = brain_scale_house(float(x_k), float(y_k), round(float(m_x)), round(float(m_y)), dict_house)
            draw_house(cnv, dict_house)
            kx.delete(0, "end")
            ky.delete(0, "end")
            x_m.delete(0, "end")
            y_m.delete(0, "end")
    # поворот
    elif text == 'Повернуть':
        angle = angle_turn.get()
        t_x = x_t.get()
        t_y = y_t.get()
        if angle == "":
            mb.showerror('Ошибка!', "Угол поворота должен быть заполнен.")
        elif t_x == "" or t_y == "":
            mb.showerror('Ошибка!', "Обе координаты центра поворота должны быть заполнены.")
        else:
            dict_house_old = copy_house(dict_house)
            dict_house = brain_turn_house(float(angle), round(float(t_x)), round(float(t_y)), dict_house)
            draw_house(cnv, dict_house)
            angle_turn.delete(0, "end")
            x_t.delete(0, "end")
            y_t.delete(0, "end")
    # Возврат домика к состоянию "на шаг назад"
    elif text == 'Шаг назад':
        #print(dict_house_old["rect"], dict_house["rect"])
        dict_house = copy_house(dict_house_old)
        #print(dict_house_old["rect"], dict_house["rect"])
        draw_house(cnv, dict_house)
    # Очистка всего
    elif text == 'Сброс':
        # Очистка всего содержимого на холсте
        cnv.delete("all")
        # Масштабирование холста до его стартового размера
        cnv.scale("all", 0, 0, 1, 1)
        # Установка положения прокрутки на начальное значение
        cnv.xview_moveto(0)
        cnv.yview_moveto(0)
        center_x = center_y = SIZE_OF_CANVAS // 2
        cnv.configure(scrollregion=(-center_x, -center_y, center_x, center_y))
        ZOOM, SIDE_PLACE, HEIGHT_PLACE = 1, center_x / STEP_CONST, - center_y / STEP_CONST
        # Начальная отрисовка координатной сетки
        update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
        #print(ZOOM, SIDE_PLACE, HEIGHT_PLACE)
        dict_house = build_start_house()
        dict_house_old = copy_house(dict_house)
        draw_house(cnv, dict_house)

            

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
window.title("Лабораторная работа по компьютерной графике №1")
window.geometry(f'{MIN_WIDTH}x{MIN_HEIGHT}')
# Устанавливается минимальный размер окна
window.minsize(MIN_WIDTH, MIN_HEIGHT)
# Привязываем обработчик события изменения размера окна
window.bind("<Configure>", resize_checker)


# Создаётся холст с установленными размерами
cnv = tk.Canvas(window, width=SIZE_OF_CANVAS, height=SIZE_OF_CANVAS, bg="white",\
                cursor = "plus", xscrollincrement = STEP_CONST, yscrollincrement = STEP_CONST)
cnv.grid(row=0, column=1, rowspan=6, sticky='nsew')
window.grid_columnconfigure(1, weight=1)


# Создаем поля для ввода параметров переноса
input_frame = tk.Frame(window, bg="light pink")
input_frame.grid(row=0, column=0, padx=10, pady=10)
tk.Label(input_frame, text="Параметры переноса:", font=("Calibry", 12), bg="light pink").grid(row=0, column=0)
tk.Label(input_frame, text="dx:", font=("Calibry", 12), bg="light pink").grid(row=1, column=0)
dx = tk.Entry(input_frame, font=("Calibry", 12))
dx.grid(row=1, column=1)
tk.Label(input_frame, text="dy:", font=("Calibry", 12), bg="light pink").grid(row=2, column=0)
dy = tk.Entry(input_frame, font=("Calibry", 12))
dy.grid(row=2, column=1)

# Создаем поля для ввода параметров масштабирования
input_frame = tk.Frame(window, bg="light pink")
input_frame.grid(row=1, column=0, padx=10, pady=10)
tk.Label(input_frame, text="Коэффициенты масштабирования:", font=("Calibry", 12), bg="light pink").grid(row=0, column=0)
tk.Label(input_frame, text="dx:", font=("Calibry", 12), bg="light pink").grid(row=1, column=0)
kx = tk.Entry(input_frame, font=("Calibry", 12))
kx.grid(row=1, column=1)
tk.Label(input_frame, text="dy:", font=("Calibry", 12), bg="light pink").grid(row=2, column=0)
ky = tk.Entry(input_frame, font=("Calibry", 12))
ky.grid(row=2, column=1)
tk.Label(input_frame, text="Координаты центра масштабирования:", font=("Calibry", 12), bg="light pink").grid(row=3, column=0)
tk.Label(input_frame, text="X:", font=("Calibry", 12), bg="light pink").grid(row=4, column=0)
x_m = tk.Entry(input_frame, font=("Calibry", 12))
x_m.grid(row=4, column=1)
tk.Label(input_frame, text="Y:", font=("Calibry", 12), bg="light pink").grid(row=5, column=0)
y_m = tk.Entry(input_frame, font=("Calibry", 12))
y_m.grid(row=5, column=1)

# Создаем поля для ввода параметров поворота
input_frame = tk.Frame(window, bg="light pink")
input_frame.grid(row=2, column=0, padx=10, pady=10)
tk.Label(input_frame, text="Угол поворота:", font=("Calibry", 12), bg="light pink").grid(row=0, column=0)
angle_turn = tk.Entry(input_frame, font=("Calibry", 12))
angle_turn.grid(row=0, column=1)
tk.Label(input_frame, text="Координаты центра поворота:", font=("Calibry", 12), bg="light pink").grid(row=1, column=0)
tk.Label(input_frame, text="X:", font=("Calibry", 12), bg="light pink").grid(row=2, column=0)
x_t = tk.Entry(input_frame, font=("Calibry", 12))
x_t.grid(row=2, column=1)
tk.Label(input_frame, text="Y:", font=("Calibry", 12), bg="light pink").grid(row=3, column=0)
y_t = tk.Entry(input_frame, font=("Calibry", 12))
y_t.grid(row=3, column=1)


# Функция создаёт кнопку
def make_button(doing, button_frame, width1):
    return tk.Button(button_frame, text=doing, bd=7, font=("Calibry", 12),
                     command=lambda: fork(doing, dx, dy, kx, ky, x_m, y_m, angle_turn, x_t, y_t, cnv),
                     activebackground="salmon", bg="khaki", height=1, width=width1)

# Создаем кнопок для переноса, масштабирования и поворота
button_frame1 = tk.Frame(window)
button_frame1.grid(row=3, column=0, padx=10, pady=10)
make_button('Перенести', button_frame1, 13).grid(row = 0, column = 0, stick = 'we')
make_button('Масштабировать', button_frame1, 14).grid(row = 0, column = 1, stick = 'we')
make_button('Повернуть', button_frame1, 13).grid(row = 0, column = 2, stick = 'we')

# Создаем кнопки для сброса изменений и шага назад
make_button('Шаг назад', window, 45).grid(row=4, column=0, padx=10, pady=10)
make_button('Сброс', window, 45).grid(row=5, column=0, padx=10, pady=10)

tk.Label(window, text="Талышева Олеся ИУ7-45Б", bg='light pink', fg = 'grey', font=("Arial", 12, 'italic')).grid(row=6, column=0)

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
def make_cnv_button(doing, button_frame, width1, func):
    return tk.Button(button_frame, text = doing, bd = 7, font = ("Calibry", 12),\
                     command = lambda: func(), activebackground = "salmon", bg = "khaki", height = 1, width = width1)

# Создаем кнопок для изменения конфигурации холста
button_frame3 = tk.Frame(window)
button_frame3.grid(row=6, column=1, padx=0, pady=0)
make_cnv_button('вверх', button_frame3, 10, move_up).grid(row = 0, column = 0, stick = 'we')
make_cnv_button('вниз', button_frame3, 10, move_down).grid(row = 0, column = 1, stick = 'we')
make_cnv_button('вправо', button_frame3, 10, move_right).grid(row = 0, column = 2, stick = 'we')
make_cnv_button('влево', button_frame3, 10, move_left).grid(row = 0, column = 3, stick = 'we')
make_cnv_button('увеличить', button_frame3, 10, zoom_in).grid(row = 0, column = 5, stick = 'we')
make_cnv_button('уменьшить', button_frame3, 10, zoom_out).grid(row = 0, column = 6, stick = 'we')

for i in range(9):
    window.grid_rowconfigure(i, weight=1)

# Обработчик нажания кнопками мыши на холст
cnv.bind('<Button-3>', lambda event: fork('Шаг назад', dx, dy, kx, ky, x_m, y_m, angle_turn, x_t, y_t, cnv))

# Создаём меню
menu = tk.Menu(window) 
window.config(menu = menu)

# Создаёт вкладку меню "Действия" с выпадающим меню с действиями
menu_in = tk.Menu(menu, tearoff = 0)

menu_in.add_command(label = 'Перенести', command = lambda: fork('Перенести', dx, dy, kx, ky, x_m, y_m, angle_turn, x_t, y_t, cnv))
menu_in.add_command(label = 'Масштабировать', command = lambda: fork('Масштабировать', dx, dy, kx, ky, x_m, y_m, angle_turn, x_t, y_t, cnv))
menu_in.add_command(label = 'Повернуть', command = lambda: fork('Повернуть', dx, dy, kx, ky, x_m, y_m, angle_turn, x_t, y_t, cnv))
menu_in.add_command(label = 'Шаг назад', command = lambda: fork('Шаг назад', dx, dy, kx, ky, x_m, y_m, angle_turn, x_t, y_t, cnv))
menu_in.add_command(label = 'Сброс', command = lambda: fork('Сброс', dx, dy, kx, ky, x_m, y_m, angle_turn, x_t, y_t, cnv))

menu.add_cascade(label = "Действия", menu = menu_in)


# Создаёт вкладку меню "Информация" с выпадающим меню с информацией об авторе и программе
menu_inf = tk.Menu(menu, tearoff = 0)

menu_inf.add_command(label = 'Информация об авторе', command = lambda: mb.showinfo('Информация об авторе', "автор - Талышева ИУ7-45Б"))
menu_inf.add_command(label = 'Информация о программе', command = lambda: mb.showinfo('Информация о программе',\
"На плоскости заданы множество точек. Найти треугольник \
с наибольшим углом между медианой и биссектрисой и отрисовать графически."))
menu_inf.add_command(label = 'Руководство пользователя', command = lambda: mb.showinfo('Руководство пользователя',\
"- Нажатие левой кнопкой мыши по холсту построит точку в месте нажатия.\n\
- Также точку можно добавить на холст"))

menu.add_cascade(label = "Информация", menu = menu_inf)

# стартовое создание и отрисовка домика
fork('Сброс', dx, dy, kx, ky, x_m, y_m, angle_turn, x_t, y_t, cnv)


# Функция даёт вставить только +,- и цифры
def checker(key: str) -> None:
    # Создаётся список с названиями окошек ввода
    butt = [kx, ky]
    # Проходимся по всем 5-и окошкам
    for j in range(len(butt)):
        try:
            #print(f"!{butt[j].get()}! kx=!{kx.get()}! ky=!{ky.get()}! {key.keysym}")
            float(butt[j].get())
        except:
            # Считывае позицию курсора в этом окошке
            ind = butt[j].index(tk.INSERT)
            # Если позиция изменилась по сравнению с предыдущей и она не равна 0
            if ind != 0:
                # Если символ не +,- или цифра
                if not (ind == 1 and butt[j].get()[0] in "+-"):
                    # Удаляем невалидный символ из поля ввода
                    a = butt[j].get()
                    a = a[:ind - 1] + a[ind:]
                    butt[j].delete(0, tk.END)
                    butt[j].insert(0, a)
                    mb.showerror('Ошибка!', "Можно вводить только целые числа.")


# Реагирует на ввод и вызывает функцию checker
x_m.bind('<KeyRelease>', checker)
y_m.bind('<KeyRelease>', checker)
x_t.bind('<KeyRelease>', checker)
y_t.bind('<KeyRelease>', checker)
kx.bind('<KeyRelease>', checker)
ky.bind('<KeyRelease>', checker)
dx.bind('<KeyRelease>', checker)
dy.bind('<KeyRelease>', checker)
angle_turn.bind('<KeyRelease>', checker)

# реакция на закрытие окна
def on_closing() -> None:
    if mb.askokcancel("Выход", "Вы уверены что хотите выйти из приложения?"):
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)

# Функция для обработки события прокрутки колеса мыши
def scroll(event: 'event') -> None:
    if event.delta > 0:
        zoom_in()
    else:
        zoom_out()
# Функция для обработки события нажатия клавиш клавиатуры
def key_press(event: 'event') -> None:
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


