# стартовое создание домика
def build_start_house():
    house = dict()
    house["center"] = (0, 0)
    house["grass"] = [(-150, 80), (150, 80)]
    house["rect"] = [(-100, 80), (-100, -20), (100, -20), (100, 80)]
    house["roof"] = [(-120, -20), (-100, -80), (100, -80), (120, -20)]
    house["wind"] = {"center": (50, 20), "radius": 20}
    house["wind_frame"] = [(30, 20), (50, 0), (70, 20), (50, 40)]
    house["door"] = [(-80, 80), (-80, 0), (-20, 0), (-20, 80)]
    house["door_handle"] = [(-35, 50), (-35, 30), (-25, 30), (-25, 50)]
    return house

# рисует ломаную прямую по массиву кортежей-точек
def draw_polyline(cnv, arr_turple, color, width_line, is_closed = True):
    coords = [coord for point in arr_turple for coord in point] + [arr_turple[0][0], arr_turple[0][1]]
    cnv.create_line(coords, fill=color, tags="line", width=width_line)

# рисует овал
def draw_oval(cnv, points, width_line, color):
    x_min = min([i[0] for i in points])
    y_min = min([i[1] for i in points])
    x_max = max([i[0] for i in points])
    y_max = max([i[1] for i in points])
    cnv.create_oval(x_min, y_min, x_max, y_max, outline = color, tags="line", width=width_line)


# отрисовка домика
def draw_house(cnv, house):
    width_line = 2
    draw_polyline(cnv, house["grass"], "green", width_line)
    draw_polyline(cnv, house["rect"], "blue", width_line)
    draw_polyline(cnv, house["roof"], "blue", width_line)
    draw_oval(cnv, house["wind_frame"], width_line, "red")
    cnv.create_line(house["wind_frame"][0][0], house["wind_frame"][0][1], house["wind_frame"][2][0], house["wind_frame"][2][1], fill="red", tags="line", width=width_line)
    cnv.create_line(house["wind_frame"][1][0], house["wind_frame"][1][1], house["wind_frame"][3][0], house["wind_frame"][3][1], fill="red", tags="line", width=width_line)
    draw_polyline(cnv, house["door"], "brown", width_line)
    cnv.create_line(house["door"][0][0], house["door"][0][1], house["door"][2][0], house["door"][2][1], fill="brown", tags="line", width=width_line)
    cnv.create_line(house["door"][1][0], house["door"][1][1], house["door"][3][0], house["door"][3][1], fill="brown", tags="line", width=width_line)
    draw_polyline(cnv, house["door_handle"], "brown", width_line)
