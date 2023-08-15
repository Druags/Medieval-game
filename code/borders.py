import pygame
from settings import *


class Border(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, size_difference):
        super().__init__(groups)
        self.pos = [pos[i] * size_difference[i] for i in range(2)]
        self.size = [size[i] * size_difference[i] for i in range(2)]
        self.rect = pygame.Rect(*self.pos, *self.size)
        self.hitbox = self.rect.copy()
        self.hitbox_status = True

    def update_status(self):
        self.hitbox_status = not self.hitbox_status

