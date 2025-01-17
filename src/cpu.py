import inspect
import logging
from typing import Type

import instructions
from src.memory import Memory4KB
from src.register import Register
from src.rom import ROM
from src.screen import Screen
from src.stack import Stack16

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')
logger = logging.getLogger()


class CPU:
    INSTRUCTIONS: list[Type[instructions.Instruction]] = [
        obj for name, obj in inspect.getmembers(instructions, inspect.isclass) if
        obj.__module__ == "instructions" and issubclass(obj, instructions.Instruction) and obj.nibble1 is not None
    ]

    def __init__(self, screen: Screen):
        logging.info(f"Load instructions{', '.join([cls.__name__ for cls in self.INSTRUCTIONS])}")
        self.memory: Memory4KB = Memory4KB()
        self.stack: Stack16 = Stack16()
        self.register: Register = Register()
        self.instruction_mapper = {instruction.nibble1: instruction for instruction in self.INSTRUCTIONS}
        self.screen = screen

    def load_rom(self, rom: ROM):
        logging.info("Load rom in memory")
        for i, byte in enumerate(rom.data):
            self.memory.memory[0x200 + i] = byte
        self.register.pc = 0x200

    def fetch_instructions(self):
        pc = self.register.pc
        byte1 = self.memory.memory[pc]
        byte2 = self.memory.memory[pc + 1]
        instruction = (byte1 << 8) | byte2
        self.register.pc += 2
        return instruction

    def execute_instruction(self):
        opcode = self.fetch_instructions()
        if opcode < 0x100:
            opcode = (opcode << 8)
        instruction = (opcode & 0xF000) >> 12
        instruction_class = self.instruction_mapper.get(hex(instruction))
        if instruction_class:
            return instruction_class(self, opcode).execute()
        raise ValueError(f"Instruction {hex(opcode)} not found")
