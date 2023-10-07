import pygame
from settings import *


class Border(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, floor):
        super().__init__(groups)
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(*self.pos, *self.size)
        self.hitbox = self.rect.copy()
        self.hitbox_status = True
        self.floor = floor

    def activate_hitbox(self):
        self.hitbox_status = True

    def deactivate_hitbox(self):
        self.hitbox_status = False
