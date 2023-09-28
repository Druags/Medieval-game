import math

import pygame
from itertools import cycle

from timer import Timer
from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, window, x, y, width, height, click_action, group, color='white'):
        super().__init__(group)
        self.window = window
        self.rect = pygame.Rect((x, y), (width, height))
        self.interaction_hitbox = self.rect.copy()
        self.border = self.rect.inflate(2, 2)
        self.color = color

        self.actions = {'close': self.close_window,
                        'next': self.next_page,
                        'prev': self.prev_page}
        self.click_action = self.actions[click_action]

    def clicked(self):
        self.click_action()

    def close_window(self):
        self.window.change_status()
        self.window.cur_page = 0
        self.window.interface.change_inter()

    def next_page(self):
        self.window.cur_page += 1 if self.window.cur_page < self.window.num_of_pages - 1 else 0

    def prev_page(self):
        self.window.cur_page -= 1 if self.window.cur_page > 0 else 0

    def hovered(self, ):
        pass


class Window:
    def __init__(self, interface):
        self.active = False
        self.interface = interface

        self.display_surf = pygame.display.get_surface()

        self.x = (SCREEN_WIDTH - WINDOW_WIDTH) // 2
        self.y = (SCREEN_HEIGHT - WINDOW_HEIGHT) // 2
        self.window = pygame.Rect(self.x, self.y, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.border = self.window.inflate(2, 2)

        self.font_height = 25
        self.font = pygame.font.Font('../font/DiaryOfAn8BitMage-lYDD.ttf', self.font_height)
        self.one_letter_width = self.font.render('a', False, 'black').get_size()[0]
        self.space_width = self.font.render(' ', False, 'black').get_size()[0]
        self.text_width = self.window.width // self.one_letter_width
        self.line_spacing = 10
        self.margin_top = 10
        self.margin_left = 10

        self.cur_page = 0

        self.interactive_group = WindowGroup()
        self.setup()

        self.text_rows_page = (int(WINDOW_HEIGHT) - self.margin_top) // (self.font_height + self.line_spacing) - 2
        self.content = None

    def setup(self):
        Button(window=self,
               x=self.window.right + 15,
               y=self.window.top,
               width=30,
               height=30,
               click_action='close',
               group=self.interactive_group)
        Button(window=self,
               x=self.window.left + self.window.width * 0.25,
               y=self.window.top + self.window.height * 0.90,
               width=self.window.width * 0.10,
               height=self.window.height * 0.05,
               click_action='prev',
               group=self.interactive_group)
        Button(window=self,
               x=self.window.left + self.window.width * 0.65,
               y=self.window.top + self.window.height * 0.90,
               width=self.window.width * 0.10,
               height=self.window.height * 0.05,
               click_action='next',
               group=self.interactive_group)

    def change_status(self):
        self.active = not self.active

    def display_content(self):

        pygame.draw.rect(self.display_surf, 'white', self.window)
        pygame.draw.rect(self.display_surf, 'black', self.border, 2, 2)
        self.interactive_group.custom_draw()
        for i, row in enumerate(self.content[self.cur_page]):
            self.display_surf.blit(row,
                                   (self.window.x + self.margin_left,
                                    self.window.y + self.margin_top + i * (self.font_height + self.line_spacing)))

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.change_status()

    def update(self):

        self.input()
        if self.active:
            self.display_content()
            self.input()


class WindowGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for item in self.sprites():
            pygame.draw.rect(self.display_surface, item.color, item.interaction_hitbox)
            pygame.draw.rect(self.display_surface, 'black', item.border, 3, 2)


class UserInterface:
    def __init__(self, interactive, offset, player):
        self.window = Window(self)

        self.cur_interactive = interactive

        self.interactives = cycle([self.window.interactive_group, interactive])

        self.player = player
        self.hovered_sprite = None

        self.offset = offset
        self.mouse = pygame.mouse.get_pos()
        self.cursor_visible = False

        self.display_surface = pygame.display.get_surface()

        self.timers = {'click': Timer(400)}

        self.setup()

    def setup(self):
        for interactive_item in self.cur_interactive:
            if hasattr(interactive_item, 'set_content'):
                interactive_item.set_content(
                    one_letter_width=self.window.one_letter_width,
                    space_width=self.window.space_width,
                    text_rows_page=self.window.text_rows_page,
                    text_width=self.window.text_width,
                    font=self.window.font)
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

    def click(self, item):
        content = item.clicked()
        if content:
            self.window.content = content
            self.window.num_of_pages = len(content)
            self.window.change_status()
            self.change_inter()

    def check_hover(self, item):
        return item.interaction_hitbox.collidepoint(self.mouse) and \
               item.interaction_hitbox.colliderect(self.player) and \
               item.mouse_interaction or self.window.active and item.interaction_hitbox.collidepoint(self.mouse)

    def hover(self):
        if self.hovered_sprite is None:
            for inter_item in self.cur_interactive:
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
        self.cursor_visible = pygame.mouse.get_visible()
        pygame.mouse.set_visible(not self.cursor_visible)

    def hover_cursor(self):
        size = self.text.get_size()
        self.text_rect.center = pygame.mouse.get_pos()
        text_x = self.text_rect.topleft[0] + (self.text_rect.width - size[0]) // 2
        text_y = self.text_rect.topleft[1] + (self.text_rect.height - size[1]) // 2

        self.display_surface.blit(self.shape_surf, self.text_rect)

        pygame.draw.rect(self.display_surface, '#6f4641', self.text_rect.inflate(2, 2), 2, 4)

        self.display_surface.blit(self.text, (text_x, text_y))

    def input(self):
        self.mouse = pygame.mouse.get_pos()
        if not self.window.active:
            self.mouse = (self.mouse[0] + self.offset.x, self.mouse[1] + self.offset.y)
        else:
            self.mouse = pygame.mouse.get_pos()

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
        self.update_timers()
        self.window.update()
        self.input()
        if self.cursor_visible:
            self.hover_cursor()
