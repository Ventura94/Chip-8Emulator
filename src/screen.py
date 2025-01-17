import pygame

from src.singleton import Singleton


class Screen(Singleton):
    def __init__(self, scale=10):
        self.width = 64
        self.height = 32
        self.scale = scale
        self.screen = pygame.display.set_mode((self.width * self.scale, self.height * self.scale))
        pygame.display.set_caption("CHIP-8 Emulator")
        self.pixels = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def clear(self):
        self.pixels = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.update()

    def draw_pixel(self, x, y, value):
        x %= self.width
        y %= self.height
        self.pixels[y][x] ^= value
        return not self.pixels[y][x]

    def update(self):
        self.screen.fill((0, 0, 0))
        for y in range(self.height):
            for x in range(self.width):
                if self.pixels[y][x] == 1:
                    pygame.draw.rect(
                        self.screen,
                        (255, 255, 255),
                        pygame.Rect(
                            x * self.scale,
                            y * self.scale,
                            self.scale,
                            self.scale
                        )
                    )
        pygame.display.flip()
