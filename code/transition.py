import pygame
from settings import *


class Transition:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.active = False
        self.dark = False

        # оверлей
        self.image = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 255
        self.speed = -6

    def change_act_status(self):
        self.active = not self.active

    def play(self):
        self.color += self.speed
        if self.color <= 0:
            self.speed *= -1
            self.color = 0
            self.dark = True

        if self.color > 255:
            self.color = 255
            self.speed *= -1
            self.dark = False
            self.change_act_status()

        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(self.image, (0,0), special_flags=pygame.BLEND_RGBA_MULT)