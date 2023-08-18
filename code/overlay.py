import pygame
from settings import *


class HoverInteractive:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render('Interact', True, 'black', 'white')
        self.text_rect = self.text.get_rect()
        self.drawing = False
        self.sprite_hovered = None

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        size = self.text.get_size()
        x = mouse_pos[0] - size[0] // 2
        y = mouse_pos[1]
        self.text_rect.topleft = (x, y)
        self.display_surface.blit(self.text, self.text_rect)

    def update(self):
        if self.drawing:
            self.draw()
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)