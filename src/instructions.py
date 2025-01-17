import logging
import random
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')
logger = logging.getLogger()


class Instruction(ABC):
    nibble1 = None

    def __init__(self, cpu, opcode: int):
        logging.info(f"Run instruction {self.nibble1} with opcode {opcode}")
        self.cpu = cpu
        self.opcode = opcode

    @abstractmethod
    def execute(self):
        pass


class LD_Vx_byte(Instruction):
    nibble1 = hex(0x6)

    def execute(self):
        nibble2 = (self.opcode & 0x0F00) >> 8
        byte = self.opcode & 0x00FF
        self.cpu.register.v[nibble2] = byte


class LD_I_addr(Instruction):
    nibble1 = hex(0xA)

    def execute(self):
        address = self.opcode & 0x0FFF
        self.cpu.register.i = address


class DRW_Vx_Vy_nibble(Instruction):
    nibble1 = hex(0xD)

    def execute(self):
        x = self.cpu.register.v[(self.opcode & 0x0F00) >> 8]
        y = self.cpu.register.v[(self.opcode & 0x00F0) >> 4]
        height = self.opcode & 0x000F
        collision = 0
        for row in range(height):
            sprite_byte = self.cpu.memory.memory[self.cpu.register.i + row]
            for col in range(8):
                pixel = (sprite_byte >> (7 - col)) & 0x1
                if self.cpu.screen.draw_pixel(x + col, y + row, pixel):
                    collision = 1
        self.cpu.register.v[0xF] = collision
        self.cpu.screen.update()


class CALL_subroutine_2(Instruction):
    nibble1 = hex(0x2)

    def execute(self):
        address = self.opcode & 0x0FFF
        self.cpu.register.sp -= 1
        self.cpu.memory.memory[self.cpu.register.sp] = self.cpu.register.pc & 0xFF
        self.cpu.register.pc = address


class LD_BCD_Vx(Instruction):
    nibble1 = hex(0xF)

    def execute(self):
        x = self.opcode & 0x0F
        value = self.cpu.register.v[x]
        hundreds = value // 100
        tens = (value // 10) % 10
        ones = value % 10
        self.cpu.memory.memory[self.cpu.register.i] = hundreds
        self.cpu.memory.memory[self.cpu.register.i + 1] = tens
        self.cpu.memory.memory[self.cpu.register.i + 2] = ones


class ADD_Vx_byte(Instruction):
    nibble1 = hex(0x7)

    def execute(self):
        x = (self.opcode & 0x0F00) >> 8
        byte = self.opcode & 0x00FF
        self.cpu.register.v[x] += byte
        self.cpu.register.v[x] &= 0xFF


class RET(Instruction):
    nibble1 = hex(0xe)

    def execute(self):
        self.cpu.register.sp += 1
        return_address = self.cpu.memory.memory[self.cpu.register.sp]
        self.cpu.register.pc = return_address


class NOOP(Instruction):
    nibble1 = hex(0x0)

    def execute(self):
        logging.info("Executing NOOP (no operation), skipping to the next instruction.")


class CALL_subroutine_1(Instruction):
    nibble1 = hex(0x1)

    def execute(self):
        address = self.opcode & 0x0FFF
        self.cpu.register.sp -= 1
        self.cpu.memory.memory[self.cpu.register.sp] = self.cpu.register.pc
        self.cpu.register.pc = address


class RND_Vx_byte(Instruction):
    nibble1 = hex(0xC)

    def execute(self):
        x = (self.opcode & 0x0F00) >> 8
        kk = self.opcode & 0x00FF
        random_number = random.randint(0, 255)
        self.cpu.register.v[x] = random_number & kk


class SE_Vx_byte(Instruction):
    nibble1 = hex(0x3)

    def execute(self):
        x = (self.opcode & 0x0F00) >> 8
        kk = self.opcode & 0x00FF
        if self.cpu.register.v[x] == kk:
            self.cpu.register.pc += 2
