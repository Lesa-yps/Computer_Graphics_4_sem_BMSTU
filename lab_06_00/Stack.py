# стек

class Stack:
    def __init__(self):
        self._stack = []

    def push(self, elem):
        self._stack.append(elem)

    def pop(self):
        if not self.is_empty():
            return self._stack.pop()
        return None

    def is_empty(self):
        return len(self._stack) == 0
