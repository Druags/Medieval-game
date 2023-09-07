import random
from itertools import cycle

import pygame

from code.settings import *


class Interactive(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = pygame.Rect(random.randint(100, SCREEN_WIDTH - 100),
                                random.randint(100, SCREEN_HEIGHT - 100),
                                100,
                                100)
        self.interactive_rect = self.rect.copy().inflate(60, 60)

        self.color_active = cycle(['red', 'gray'])
        self.color_hover = cycle(['blue', 'gray'])
        self.current_color = 'gray'
        self.is_hovered = False

    def change_color(self, type):
        if type == 'click':
            self.current_color = next(self.color_active)
        elif type == 'hover':
            self.current_color = next(self.color_hover)

    def clicked(self):
        self.change_color('click')

    def hovered(self, ):
        self.change_color('hover')