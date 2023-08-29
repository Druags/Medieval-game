import pygame
from settings import *


class HoverInteractive:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 25)
        self.text = self.font.render('Interact', False, '#dadbdf')

        self.text_rect = self.text.get_rect().inflate(10, 10)
        self.shape_surf = pygame.Surface(self.text_rect.size, pygame.SRCALPHA)
        self.shape_surf.set_alpha(128)
        self.shape_surf.fill('#292f3d')

        self.drawing = False
        self.sprite_hovered = None

    def change_status(self):
        self.drawing = not self.drawing

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        size = self.text.get_size()
        self.text_rect.center = mouse_pos
        text_x = self.text_rect.topleft[0] + (self.text_rect.width - size[0]) // 2
        text_y = self.text_rect.topleft[1] + (self.text_rect.height - size[1]) // 2
        self.display_surface.blit(self.shape_surf, self.text_rect)
        pygame.draw.rect(self.display_surface, '#6f4641', self.text_rect.inflate(2,2), 2, 4)

        self.display_surface.blit(self.text, (text_x, text_y))

    def update(self):
        if self.drawing:
            self.draw()
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)
