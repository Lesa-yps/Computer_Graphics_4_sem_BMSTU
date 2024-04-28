# тестируем мой стек
from Stack import Stack

# пуст ли стек?
# is_empty


def test_is_empty() -> None:
    my_stack = Stack()
    # стек новый пустой
    assert my_stack.is_empty()
    # добавили 1 элемент -> стек не пустой
    my_stack.push(1)
    assert not my_stack.is_empty()
    # достали единственный элемент -> стек снова пуст
    my_stack.pop()
    assert my_stack.is_empty()

# как кладём и берём элементы
# push и pop


def test_push_pop() -> None:
    my_stack = Stack()
    for i in range(3):
        my_stack.push(i)
    # проверка, что достаём в обратном порядке от того как положили
    for i in range(2, 0, -1):
        assert my_stack.pop() == i
