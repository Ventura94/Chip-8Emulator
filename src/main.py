import pygame

from src.cpu import CPU
from src.rom import ROM
from src.screen import Screen


def main():
    rom = ROM("https://github.com/kripod/chip8-roms/raw/refs/heads/master/games/Pong%20(1%20player).ch8")
    screen = Screen()
    cpu = CPU(screen)
    cpu.load_rom(rom)
    screen.update()
    running = True
    while cpu.register.pc < 0x1000 and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        cpu.execute_instruction()


if __name__ == '__main__':
    main()
