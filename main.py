# Талышева Олеся ИУ7-45Б
# Лабораторная работа №1

# Импортируем библиотеки
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from Can_do import *

# Константы
SIZE_OF_CANVAS = 500
MIN_WIDTH = 870 + 257
MIN_HEIGHT = 510 + 140
ZOOM = 1
SIDE_PLACE = 0
HEIGHT_PLACE = 0



# Функция вызывается в ответ на действия пользователя и выполняет требуемое или вызывает для этого другую функцию
def fork(text, x1, y1, cnv, tree):
    global ZOOM, SIDE_PLACE, HEIGHT_PLACE
    #print("ZOOM =", ZOOM)
    cnv.delete("line")
    # Из окошек берутся координаты точек
    x = x1.get()
    y = y1.get()
    point_x1 = 0 if x == "" else int(x)
    point_y1 = 0 if y == "" else int(y)
    # Отрисовка точку
    if text == 'Добавить':
        if x and y:
            touch(point_x1, point_y1, cnv, tree, ZOOM, SIDE_PLACE, HEIGHT_PLACE, False)
            x1.delete(0, "end")
            y1.delete(0, "end")
        else:
            mb.showerror('Ошибка!', "Оба поля координат должны быть заполнены.")
    # Удалить точку
    elif text == 'Удалить':
        # достаём выделенное значение из таблицы
        selected_item = tree.selection()
        if selected_item:
            for item_id in selected_item:
                item = tree.item(item_id)
                x_table = item['values'][0]  # Получаем значение x_table
                y_table = item['values'][1]  # Получаем значение y_table
                tree.delete(item_id)  # Удаляем элемент из Treeview
                x, y = new_coord_xy(x_table, y_table, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
                # Получаем все объекты, перекрывающие указанные координаты x и y
                overlapping_objects = cnv.find_overlapping(x - 1, y - 1, x + 1, y + 1)
                # Проходимся по найденным объектам и удаляем их
                for obj in overlapping_objects:
                    cnv.delete(obj)
        else:
            mb.showerror('Ошибка!', "Точка для удаления не выбрана.")
    # Редактирование точки
    elif text == 'Редактировать':
        # достаём выделенное значение из таблицы
        selected_item = tree.selection()
        if not selected_item:
            mb.showerror('Ошибка!', "Точка для редактирования не выбрана.")
        else:
            if x and y:
                #print(len(x), len(y))
                # проверяем есть ли уже добавляемая точка
                arr = iterate_points(tree)
                if point_in_table(arr, (int(x), int(y))):
                    mb.showerror('Ошибка!', "Такая точка уже существует.")
                else:
                    fork("Удалить", x1, y1, cnv, tree)
                    fork("Добавить", x1, y1, cnv, tree)
            else:
                mb.showerror('Ошибка!', "Оба поля координат должны быть заполнены.")
    # Вызывается функция brain для построения результата
    elif text == 'Построить результат':
        brain(cnv, tree, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
    # Очищаются окошки ввода координат дополнительной точки
    elif text == 'Очистить холст':
        cnv.delete("all")
        # Получаем все элементы таблицы
        items = tree.get_children()
        # Удаляем каждый элемент из таблицы
        for item in items:
            tree.delete(item)
        cnv.scale("all", 0, 0, 1/ZOOM, 1/ZOOM)
        cnv.xview_scroll(round(SIDE_PLACE), "units")
        cnv.yview_scroll(- round(HEIGHT_PLACE), "units")
        ZOOM, SIDE_PLACE, HEIGHT_PLACE = 1, 0, 0
        # Начальная отрисовка координатной сетки
        update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
        #print(ZOOM, SIDE_PLACE, HEIGHT_PLACE)

            

# обработка события изменения размера окна
def resize_checker(event):
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
cnv.grid(row=0, column=2, rowspan=8, sticky='nsew')
window.grid_columnconfigure(2, weight=1)



### Создание горизонтального скроллбара
##xbar = tk.Scrollbar(window, orient="horizontal", command=cnv.xview)
##xbar.grid(row=8, column=2, sticky='ew')  # Прижимаем к низу и распространяем по ширине
### Привязка скроллбара к canvas
##cnv.config(xscrollcommand=xbar.set)
### Создание вертикального скроллбара
##ybar = tk.Scrollbar(window, orient="vertical", command=cnv.yview)
##ybar.grid(row=0, column=3, sticky='ns')  # Прижимаем к правому краю и распространяем по высоте
### Привязка скроллбара к canvas
##cnv.config(yscrollcommand=ybar.set)



X_SIZE, Y_SIZE = calc_size_cnv(cnv)

# Начальная отрисовка координатной сетки
update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)

# Создаем фрейм для размещения таблицы
table_frame = tk.Frame(window)
table_frame.grid(row=0, rowspan=5, columnspan=2, column=0, padx=10, pady=10)
# стиль
style = ttk.Style().configure('Treeview', font=("Calibry", 12))
# Создаем Treeview для отображения таблицы
tree = ttk.Treeview(table_frame, columns=("x", "y"), show="headings", height = 20)
tree.heading("x", text="X")
tree.heading("y", text="Y")
tree.column("x", width=200)
tree.column("y", width=200)
tree.pack()

# Создаем поля для ввода координат
input_frame = tk.Frame(window)
input_frame.grid(row=5, column=0, padx=10, pady=10)
tk.Label(input_frame, text="X:", font=("Calibry", 12)).grid(row=0, column=0)
x1 = tk.Entry(input_frame, font=("Calibry", 12))
x1.grid(row=0, column=1)
tk.Label(input_frame, text="Y:", font=("Calibry", 12)).grid(row=0, column=2)
y1 = tk.Entry(input_frame, font=("Calibry", 12))
y1.grid(row=0, column=3)


# Функция создаёт кнопку
def make_button(doing, button_frame, width1):
    return tk.Button(button_frame, text=doing, bd=7, font=("Calibry", 12),
                     command=lambda: fork(doing, x1, y1, cnv, tree),
                     activebackground="salmon", bg="khaki", height=1, width=width1)

# Создаем кнопок для добавления, удаления и редактирования точек
button_frame1 = tk.Frame(window)
button_frame1.grid(row=6, column=0, padx=10, pady=10)
make_button('Добавить', button_frame1, 13).grid(row = 0, column = 0, stick = 'we')
make_button('Удалить', button_frame1, 13).grid(row = 0, column = 1, stick = 'we')
make_button('Редактировать', button_frame1, 13).grid(row = 0, column = 2, stick = 'we')

# Создаем кнопок для построения результата и очистки холста
button_frame2 = tk.Frame(window)
button_frame2.grid(row=7, column=0, padx=10, pady=10)
make_button('Построить результат', button_frame2, 20).grid(row = 0, column = 0, stick = 'we')
make_button('Очистить холст', button_frame2, 25).grid(row = 0, column = 1, stick = 'we')

tk.Label(window, text="Талышева Олеся ИУ7-45Б", bg='light pink', fg = 'grey', font=("Arial", 12, 'italic')).grid(row=8, column=0)

# Функции для приближения и удаления
def zoom_in(event = None):
    global ZOOM
    ZOOM *= 1.1
    cnv.scale("all", 0, 0, 1.1, 1.1)
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
def zoom_out(event = None):
    global ZOOM
    ZOOM *= 0.9
    cnv.scale("all", 0, 0, 0.9, 0.9)
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
# Функции для перемещения
# Функция для перемещения влево
def move_left(event=None):
    global SIDE_PLACE
    SIDE_PLACE += 1
    cnv.xview_scroll(round(-1 * ZOOM), "units")
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
# Функция для перемещения вправо
def move_right(event=None):
    global SIDE_PLACE
    SIDE_PLACE -= 1
    cnv.xview_scroll(round(1 * ZOOM), "units")
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
def move_up(event = None):
    global HEIGHT_PLACE
    HEIGHT_PLACE -= 1
    cnv.yview_scroll(round(-1 * ZOOM), "units")
    update_grid(cnv, ZOOM, SIDE_PLACE, HEIGHT_PLACE)
def move_down(event = None):
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
button_frame3.grid(row=8, column=2, padx=0, pady=0)
make_cnv_button('вверх', button_frame3, 10, move_up).grid(row = 0, column = 0, stick = 'we')
make_cnv_button('вниз', button_frame3, 10, move_down).grid(row = 0, column = 1, stick = 'we')
make_cnv_button('вправо', button_frame3, 10, move_right).grid(row = 0, column = 2, stick = 'we')
make_cnv_button('влево', button_frame3, 10, move_left).grid(row = 0, column = 3, stick = 'we')
make_cnv_button('увеличить', button_frame3, 10, zoom_in).grid(row = 0, column = 5, stick = 'we')
make_cnv_button('уменьшить', button_frame3, 10, zoom_out).grid(row = 0, column = 6, stick = 'we')

for i in range(9):
    window.grid_rowconfigure(i, weight=1)

# Обработчик нажания кнопками мыши на холст
cnv.bind('<Button-1>', lambda event: touch(event.x, event.y, cnv, tree, ZOOM, SIDE_PLACE, HEIGHT_PLACE))
cnv.bind('<Button-3>', lambda event: fork('Построить результат', x1, y1, cnv, tree))

# Создаём меню
menu = tk.Menu(window) 
window.config(menu = menu)

# Создаёт вкладку меню "Действия" с выпадающим меню с действиями
menu_in = tk.Menu(menu, tearoff = 0)

menu_in.add_command(label = 'Добавить точку', command = lambda: fork('Добавить', x1, y1, cnv, tree))
menu_in.add_command(label = 'Удалить точку', command = lambda: fork('Удалить', x1, y1, cnv, tree))
menu_in.add_command(label = 'Редактировать точку', command = lambda: fork('Редактировать', x1, y1, cnv, tree))
menu_in.add_command(label = 'Построить результат', command = lambda: fork('Построить результат', x1, y1, cnv, tree))
menu_in.add_command(label = 'Очистить холст', command = lambda: fork('Очистить холст', x1, y1, cnv, tree))

menu.add_cascade(label = "Действия", menu = menu_in)


# Создаёт вкладку меню "Информация" с выпадающим меню с информацией об авторе и программе
menu_inf = tk.Menu(menu, tearoff = 0)

menu_inf.add_command(label = 'Информация об авторе', command = lambda: mb.showinfo('Информация об авторе', "автор - Талышева ИУ7-45Б"))
menu_inf.add_command(label = 'Информация о программе', command = lambda: mb.showinfo('Информация о программе',\
"На плоскости заданы множество точек. Найти треугольник \
с наибольшим углом между медианой и биссектрисой и отрисовать графически."))
menu_inf.add_command(label = 'Руководство пользователя', command = lambda: mb.showinfo('Руководство пользователя',\
"- Нажатие левой кнопкой мыши по холсту построит точку в месте нажатия.\n\
- Также точку можно добавить на холст, заполнив поля координат и нажав кнопку 'добавить' (или аналогично в меню во вкладке 'действия').\n\
- Точку можно удалить, выбрав её в таблице и нажав кнопку 'удалить' (или аналогично в меню во вкладке 'действия').\n\
- Точку можно редактировать, выбрав её в таблице, заполнив поля координат знавениями новой точки и нажав кнопку 'редактировать')\n\
(или аналогично в меню во вкладке 'действия').\n\
- Найти результирующие угол и треугольник можно с помощью кнопки 'построить результат' (или аналогично в меню во вкладке 'действия').\n\
- Нажатие правой кнопкой мыши по холсту также построит результирующий треугольник.\n\
- Удалить всё с холста можно с помощью кнопки 'очистить холст' (или аналогично в меню во вкладке 'действия').\n\
- Кнопки 'вверх', 'вниз', 'влево', 'вправо', 'увеличить', 'уменьшить' омогают перемещаться и изменять размер изображения на холсте.\n\
После построения результирующего треугольника его стороны будут отрисованы зелёным цветом, медиана - коричневым, биссектриса - синим.\n\
Размер самого большого угла между биссектрисой и медианой в треугольнике будет выведен в информационном сообщении."))

menu.add_cascade(label = "Информация", menu = menu_inf)


# Функция даёт вставить только +,- и цифры
def checker(key):
    # Создаётся список с названиями окошек ввода
    butt = [x1, y1]
    # Проходимся по всем 5-и окошкам
    for j in range(len(butt)):
        try:
            int(butt[j].get())
        except:
            # Считывае позицию курсора в этом окошке
            ind = butt[j].index(tk.INSERT)
            # Если позиция изменилась по сравнению с предыдущей и она не равна 0
            if ind != 0:
                # Если символ не +,- или цифра
                if not (butt[j].get()[ind - 1]).isdigit() and butt[j].get()[ind - 1] not in "+-":
                    # Удаляем невалидный символ из поля ввода
                    a = butt[j].get()
                    a = a[:ind - 1] + a[ind:]
                    butt[j].delete(0, tk.END)
                    butt[j].insert(0, a)
                    mb.showerror('Ошибка!', "Можно вводить только вещественные числа.")


# Реагирует на нажатие клавиш и вызывает функцию checker
window.bind('<Key>', checker)

# реакция на закрытие окна
def on_closing():
    if mb.askokcancel("Выход", "Вы уверены что хотите выйти из приложения?"):
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)

# Функция для обработки события прокрутки колеса мыши
def scroll(event):
    if event.delta > 0:
        zoom_in()
    else:
        zoom_out()
# Функция для обработки события нажатия клавиш клавиатуры
def key_press(event):
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


