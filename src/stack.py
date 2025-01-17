from queue import LifoQueue


class Stack16:
    def __init__(self):
        self._stack = LifoQueue(maxsize=16)

    def put(self, value):
        self._stack.put(value)

    def pop(self):
        return self._stack.get()
