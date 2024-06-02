from Draw import draw_line_algo_DDA, clean_all
import Const as c


# умножаем точку-массив на матрицу для трансформации и зум, тем самым применяя масштабирование и поворот (+ смещение к центру холста)
def transform_point(cnv, arr_point, transform_matrix, scale_coef):
    arr_point += [1]
    res_arr_point = list()
    for i in range(c.MATRIX_SIZE):
        summ = 0
        for j in range(c.MATRIX_SIZE):
            summ += arr_point[j] * transform_matrix[j][i]
        res_arr_point.append(summ * scale_coef)
    res_arr_point[c.X_PART] += cnv.winfo_width() // 2
    res_arr_point[c.Y_PART] += cnv.winfo_height() // 2
    return res_arr_point[:3]

# подпрограмма обработки бокового ребра ("заштопывает" края)


def rib_process(cnv, func, x, z, Zstep, transform_matrix, color_plane, scale_coef):
    point1 = transform_point(
        cnv, [x, func(x, z), z], transform_matrix, scale_coef)
    point2 = transform_point(
        cnv, [x, func(x, z + Zstep), z + Zstep], transform_matrix, scale_coef)
    cnv.create_line(point1[c.X_PART], point1[c.Y_PART], point2[c.X_PART],
                    point2[c.Y_PART], fill=color_plane, tag="plane")


# вычисление функции на каждой плоскости z = const, начиная с ближайшей  к наблюдателю плоскости Zmax
def floating_horizon_const_z(cnv, func, Y_up_horizon, Y_down_horizon, x_param, z, transform_matrix, color_plane, scale_coef):
    Xmin, Xmax, Xstep = x_param
    point_before = None
    # Для каждой точки на кривой, лежащей в плоскости z = const
    x = Xmin
    while x <= Xmax:
        y = func(x, z)
        # умножаем точку-массив на матрицу для трансформации и зум, тем самым применяя масштабирование и поворот
        point_now = transform_point(
            cnv, [x, y, z], transform_matrix, scale_coef)
        if point_before:
            # рисует линию попиксельно
            draw_line_algo_DDA(cnv, Y_up_horizon, Y_down_horizon,
                               point_before, point_now, color_plane, "plane")
        point_before = point_now
        x += Xstep

# распаковка интервала


def unpack_params(params):
    Xmin, Xcount, Xmax = params
    if Xmin > Xmax:
        Xmin, Xmax = Xmax, Xmin
    Xstep = (Xmax - Xmin) / Xcount
    return Xmin, Xmax, Xstep

# алгоритм плавающего горизонта


def floating_horizon(cnv, func, x_params, z_params, transform_matrix, color_plane, scale_coef) -> None:
    # Очистка старой отрисовки
    clean_all(cnv)
    Xmin, Xmax, Xstep = unpack_params(x_params)
    Zmin, Zmax, Zstep = unpack_params(z_params)
    # массив, содержащий ординаты верхнего горизонта
    Y_up_horizon = [0 for _ in range(max(Xmax, cnv.winfo_width()) + 1)]
    # массив, содержащий ординаты нижнего горизонта
    Y_down_horizon = [cnv.winfo_height()
                      for _ in range(max(Xmax, cnv.winfo_width()) + 1)]
    # вычисление функции на каждой плоскости z = const, начиная с ближайшей  к наблюдателю плоскости Zmax
    z = Zmin
    while z <= Zmax:
        # обрабатывается левое боковое ребро
        rib_process(cnv, func, Xmin, z, Zstep,
                    transform_matrix, color_plane, scale_coef)
        # вычисление функции на текущей плоскости z = const
        floating_horizon_const_z(cnv, func, Y_up_horizon, Y_down_horizon, (
            Xmin, Xmax, Xstep), z, transform_matrix, color_plane, scale_coef)
        # обрабатывается правое боковое ребро
        rib_process(cnv, func, Xmax, z, Zstep,
                    transform_matrix, color_plane, scale_coef)
        z += Zstep
