import pygame
from settings import *


class HoverInteractive:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render('Interact', True, 'black', 'white')

    def draw(self, coordinate):
        print(coordinate)
        size = self.text.get_size()
        x = coordinate[0] - size[0] // 2
        y = coordinate[1] - size[1] * 2.5
        self.display_surface.blit(self.text, (x, y))
