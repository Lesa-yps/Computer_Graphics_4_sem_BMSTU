import math as m
# формулы, по которым пользователь может строить плоскость


def func1(x: float, z: float) -> float:
    return m.sin(x) * m.cos(z)


def func2(x: float, z: float) -> float:
    return x**2 / 2 + z**2 / 3 - 5


def func3(x: float, z: float) -> float:
    return m.sin(x) + z


def func4(x: float, z: float) -> float:
    return m.sqrt(x**2 + z**2)


list_of_func = [(func1, "y = sin(x) * cos(z)"), (func2, "y = x**2 / 2 + z**2 / 3 - 5"),
                (func3, "y = sin(x) + z"), (func4, "y = sqrt(x^2 + z^2)")]
