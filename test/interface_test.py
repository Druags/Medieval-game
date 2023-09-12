import pygame
from itertools import cycle

from code.settings import *
from code.timer import Timer
from interactive_test import Interactive


class Button(Interactive):
    def __init__(self, group, x, y, width, height):
        super().__init__(group)
        self.rect = pygame.Rect(x, y, width, height)
        self.interactive_rect = self.rect.copy()


class Window:
    def __init__(self):
        self.active = False

        self.display_surf = pygame.display.get_surface()
        self.group = pygame.sprite.Group()
        self.x = SCREEN_WIDTH - WINDOW_WIDTH * 1.5
        self.y = SCREEN_HEIGHT - WINDOW_HEIGHT * 1.25
        self.window = pygame.Rect(self.x, self.y, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.exit_button = Button(self.group, self.window.topright[0] + 15, self.window.topright[1], 30, 30)
        self.interactive = [self.exit_button]

    def change_status(self):
        self.active = not self.active

    def get_content(self, content):
        self.content = content

    def display_content(self):
        pygame.draw.rect(self.display_surf, 'white', self.window)
        pygame.draw.rect(self.display_surf, 'white', self.exit_button.interactive_rect)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.change_status()

    def update(self):
        self.input()
        print(self.exit_button.rect)
        if self.active:
            self.display_content()
            self.input()


class UserInterface:
    def __init__(self, interactive, player):
        self.cur_interactive = interactive
        self.window = Window()
        self.interactives = cycle([self.window.interactive, interactive])

        self.player = player
        self.hovered_sprite = None
        self.mouse = pygame.mouse.get_pos()
        self.cursor_visible = False
        self.display_surface = pygame.display.get_surface()

        self.timers = {'click': Timer(400)}

        self.setup()

    def setup(self):
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 25)
        self.text = self.font.render('Interact', False, '#dadbdf')
        self.text_rect = self.text.get_rect().inflate(10, 10)
        self.shape_surf = pygame.Surface(self.text_rect.size, pygame.SRCALPHA)
        self.shape_surf.set_alpha(128)
        self.shape_surf.fill('#292f3d')

    def change_inter(self):
        self.cur_interactive = next(self.interactives)
        self.hovered_sprite.hovered()
        self.change_cursor()
        self.hovered_sprite = None

    def click(self):
        for interactive in self.cur_interactive:
            if interactive.rect.collidepoint(self.mouse):
                interactive.clicked()
                self.window.change_status()
                self.change_inter()

    def check_hover(self, sprite):
        return sprite.interactive_rect.collidepoint(self.mouse)

    def hover(self):
        if self.hovered_sprite is None:
            for interactive in self.cur_interactive:
                if self.check_hover(interactive):
                    self.hovered_sprite = interactive
                    self.hovered_sprite.hovered()
                    self.change_cursor()
                    break
        elif not self.check_hover(self.hovered_sprite):
            self.hovered_sprite.hovered()
            self.change_cursor()
            self.hovered_sprite = None

    def change_cursor(self):
        self.cursor_visible = pygame.mouse.get_visible()
        pygame.mouse.set_visible(not self.cursor_visible)

    def draw(self):
        size = self.text.get_size()
        self.text_rect.center = self.mouse
        text_x = self.text_rect.topleft[0] + (self.text_rect.width - size[0]) // 2
        text_y = self.text_rect.topleft[1] + (self.text_rect.height - size[1]) // 2
        self.display_surface.blit(self.shape_surf, self.text_rect)
        pygame.draw.rect(self.display_surface, '#6f4641', self.text_rect.inflate(2, 2), 2, 4)

        self.display_surface.blit(self.text, (text_x, text_y))

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
        self.window.update()
        print(self.cur_interactive)
        if self.cursor_visible:
            self.draw()
        self.input()
