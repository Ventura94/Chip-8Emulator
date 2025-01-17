from src.exceptions.memory import MemoryException
from src.singleton import Singleton


class Memory4KB(Singleton):
    def __init__(self):
        self.size = 4 * 1024
        self.memory = bytearray(self.size)

    def read(self, address):
        if 0 <= address < self.size:
            return self.memory[address]
        else:
            raise MemoryException("Dirección fuera de rango")

    def write(self, address, value):
        if 0 <= address < self.size:
            if 0 <= value <= 255:
                self.memory[address] = value
            else:
                raise MemoryException("El valor debe estar entre 0 y 255")
        else:
            raise MemoryException("Dirección fuera de rango")
