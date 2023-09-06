import pygame
from itertools import cycle

from timer import Timer
from settings import *


class Button:
    def __init__(self, x, y, width, height):
        self.interaction_hitbox = pygame.Rect(x, y, width, height)


class Window:
    def __init__(self):
        self.active = False

        self.display_surf = pygame.display.get_surface()

        self.x = SCREEN_WIDTH - WINDOW_WIDTH * 1.5
        self.y = SCREEN_HEIGHT - WINDOW_HEIGHT * 1.25
        self.window = pygame.Rect(self.x, self.y, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.exit_button = Button(self.x + WINDOW_WIDTH + 15, self.y, 30, 30)
        self.interactive = [self.exit_button]

    def change_status(self):
        self.active = not self.active

    def get_content(self, content):
        self.content = content

    def display_content(self):
        pygame.draw.rect(self.display_surf, 'white', self.window)
        pygame.draw.rect(self.display_surf, 'white', self.exit_button.interaction_hitbox)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.change_status()

        buttons = pygame.mouse.get_pressed()
        if buttons[0] and self.exit_button.interaction_hitbox.collidepoint(pygame.mouse.get_pos()):
            self.change_status()

    def update(self):
        self.input()
        if self.active:
            self.display_content()
            self.input()


class UserInterface:
    def __init__(self, interactive, offset, player):
        self.window = Window()

        self.interactive = interactive
        self.player = player
        self.hovered_sprite = None

        self.offset = offset
        self.mouse = pygame.mouse.get_pos()
        self.visible = False

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

    def click(self, item):
        # for inter_item in self.interactive:
        #     if inter_item.rect.collidepoint(self.offset_mouse):
        if not self.window.active:
            self.window.get_content(item.item)

    def check_hover(self, item):
        print(self.offset_mouse, item.interaction_hitbox)
        return item.interaction_hitbox.collidepoint(self.offset_mouse) and \
               item.interaction_hitbox.colliderect(self.player) and \
               item.mouse_interaction

    def hover(self):
        if self.hovered_sprite is None:
            for inter_item in self.interactive:
                if self.check_hover(inter_item):
                    self.hovered_sprite = inter_item
                    self.hovered_sprite.hovered()
                    self.change_cursor()
                    break
        elif not self.check_hover(self.hovered_sprite):
            self.hovered_sprite.hovered()
            self.change_cursor()
            self.hovered_sprite = None

    def change_cursor(self):
        self.visible = pygame.mouse.get_visible()
        pygame.mouse.set_visible(not self.visible)

    def hover_cursor(self):
        size = self.text.get_size()
        self.text_rect.center = self.mouse
        text_x = self.text_rect.topleft[0] + (self.text_rect.width - size[0]) // 2
        text_y = self.text_rect.topleft[1] + (self.text_rect.height - size[1]) // 2
        self.display_surface.blit(self.shape_surf, self.text_rect)
        pygame.draw.rect(self.display_surface, '#6f4641', self.text_rect.inflate(2, 2), 2, 4)
        self.display_surface.blit(self.text, (text_x, text_y))

    def input(self):
        self.mouse = pygame.mouse.get_pos()
        self.offset_mouse = (self.mouse[0] + self.offset.x, self.mouse[1] + self.offset.y)
        buttons = pygame.mouse.get_pressed()
        # click
        if buttons[0] and not self.timers['click'].active:
            if self.hovered_sprite:
                self.click(self.hovered_sprite)
            self.timers['click'].activate()
        # hover
        self.hover()

    def update_timers(self):
        for timer in self.timers:
            self.timers[timer].update()

    def update(self):
        print(self.interactive)
        self.update_timers()

        self.input()

        self.window.update()
        if self.visible:
            self.hover_cursor()
