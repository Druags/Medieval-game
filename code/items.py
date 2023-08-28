import pygame
from settings import *


class Item:
    def __init__(self, player):
        self.player = player
        self.active = False
        self.display_surf = pygame.display.get_surface()

        self.width = SCREEN_WIDTH // 2
        self.height = SCREEN_HEIGHT // 1.5
        self.x = SCREEN_WIDTH - self.width * 1.5
        self.y = SCREEN_HEIGHT - self.height * 1.25
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.display_surf, 'white', self.rect)

    def input(self):
        pass

    def update(self):
        if self.active:
            self.draw()
            self.input()
