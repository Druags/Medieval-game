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


class UserInterface:
    def __init__(self, interactive):
        self.interactive = interactive
        self.hovered_sprite = None
        self.mouse = pygame.mouse.get_pos()

        self.timers = {'click': Timer(200)}

    def click(self):
        for interactive in self.interactive:
            if interactive.rect.collidepoint(self.mouse):
                interactive.clicked()

    def hover(self):
        if self.hovered_sprite is None:
            for interactive in self.interactive:
                if interactive.interactive_rect.collidepoint(self.mouse):
                    self.hovered_sprite = interactive
                    self.hovered_sprite.hovered()
                    break
        elif not self.hovered_sprite.interactive_rect.collidepoint(self.mouse):
            self.hovered_sprite.hovered()
            self.hovered_sprite = None

    def input(self):
        self.mouse = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()
        # click
        if buttons[0] and not self.timers['click'].active:
            self.click()
            self.timers['click'].activate()
        # hover
        self.hover()

    def update_timers(self):
        for timer in self.timers:
            self.timers[timer].update()

    def update(self):
        self.update_timers()
        self.input()


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.group = CustomGroup()
        self.setup()

    def setup(self):
        self.objects = [Interactive(self.group) for _ in range(5)]
        self.interface = UserInterface(self.objects)

    def run(self, dt):
        self.interface.update()
        self.group.custom_draw()
        self.group.update()


class CustomGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for item in self.sprites():
            pygame.draw.rect(self.display_surface, 'white', item.interactive_rect)
            pygame.draw.rect(self.display_surface, item.current_color, item.rect)