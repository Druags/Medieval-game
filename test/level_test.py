import pygame
import random
from itertools import cycle

from code.settings import *
from timer import Timer


class Interactive(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = pygame.Rect(random.randint(100, SCREEN_WIDTH - 100),
                                random.randint(100, SCREEN_HEIGHT - 100),
                                100,
                                100)
        self.color_active = cycle(['red', 'gray'])
        self.color_passive = 'gray'
        self.color_clicked = 'red'
        self.current_color = self.color_passive

    def change_color(self, type):
        if type == 'click':
            print(self.current_color)
            self.current_color = next(self.color_active)

    def get_clicked(self):

        self.change_color('click')


class UserInterface:
    def __init__(self, interactives):
        self.interactives = interactives

    def click(self, mouse):
        for interactive in self.interactives:
            if interactive.rect.collidepoint(mouse):
                interactive.get_clicked()

    def hover(self, mouse):
        pass


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.group = CustomGroup()
        self.setup()
        self.timers = {'click': Timer(200)}

    def setup(self):
        self.objects = [Interactive(self.group) for _ in range(5)]
        self.interface = UserInterface(self.objects)

    def input(self):
        mouse = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()
        if buttons[0] and not self.timers['click'].active:
            self.interface.click(mouse)
            self.timers['click'].activate()

    def update_timers(self):
        for timer in self.timers:
            self.timers[timer].update()

    def run(self, dt):
        print(self.timers['click'].active)
        self.update_timers()
        self.input()
        self.group.custom_draw()


class CustomGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for item in self.sprites():
            pygame.draw.rect(self.display_surface, item.current_color, item.rect)