import pygame
from itertools import cycle

from timer import Timer
from settings import *
from transition import Transition


class Button(pygame.sprite.Sprite):
    def __init__(self, window, pos, size, click_action, group, color='white'):
        super().__init__(group)
        self.window = window
        self.interaction_hitbox = pygame.Rect(pos, size)
        self.border = self.interaction_hitbox.inflate(2, 2)
        self.color = color

        self.actions = {'close': self.close_window,
                        'next': self.next_page,
                        'prev': self.prev_page}
        self.click_action = self.actions[click_action]

    def clicked(self):
        self.click_action()

    def close_window(self):
        self.window.switch_status()
        self.window.cur_page = 0
        self.window.interface.change_interactive_group()

    def next_page(self):
        self.window.cur_page += 1 if self.window.cur_page < self.window.num_of_pages - 1 else 0

    def prev_page(self):
        self.window.cur_page -= 1 if self.window.cur_page > 0 else 0

    def is_hovered(self, mouse_position):
        return self.window.is_active and self.interaction_hitbox.collidepoint(mouse_position)


class Window:
    def __init__(self, interface):
        self.is_active = False
        self.interface = interface

        self.display_surf = pygame.display.get_surface()

        self.x = (SCREEN_WIDTH - WINDOW_WIDTH) // 2
        self.y = (SCREEN_HEIGHT - WINDOW_HEIGHT) // 2
        self.rect = pygame.Rect(self.x, self.y, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.border = self.rect.inflate(2, 2)

        self.interactive_group = WindowGroup()
        self.text_setup()
        self.buttons_setup()

        self.cur_page = 0
        self.content = None

    def text_setup(self):
        self.font_height = 25
        self.font = pygame.font.Font('../font/DiaryOfAn8BitMage-lYDD.ttf', self.font_height)
        self.one_letter_width = self.font.render('a', False, 'black').get_size()[0]
        self.space_width = self.font.render(' ', False, 'black').get_size()[0]
        self.text_width = self.rect.width // self.one_letter_width
        self.line_spacing = 10
        self.margin_top = 10
        self.margin_left = 10
        self.text_rows_in_one_page = (int(WINDOW_HEIGHT) - self.margin_top) // (
                self.font_height + self.line_spacing) - 2

    def buttons_setup(self):
        Button(window=self,
               pos=(self.rect.right + 15, self.rect.top),
               size=(30, 30),
               click_action='close',
               group=self.interactive_group)
        Button(window=self,
               pos=(self.rect.left + self.rect.width * 0.25, self.rect.top + self.rect.height * 0.90),
               size=(self.rect.width * 0.10, self.rect.height * 0.05),
               click_action='prev',
               group=self.interactive_group)
        Button(window=self,
               pos=(self.rect.left + self.rect.width * 0.65, self.rect.top + self.rect.height * 0.90),
               size=(self.rect.width * 0.10, self.rect.height * 0.05),
               click_action='next',
               group=self.interactive_group)

    def switch_status(self):
        self.is_active = not self.is_active

    def set_content(self, content):
        self.content = content
        self.num_of_pages = len(content)

    def draw_window(self):
        pygame.draw.rect(self.display_surf, 'white', self.rect)
        pygame.draw.rect(self.display_surf, 'black', self.border, 2, 2)

    def draw_content(self):
        for i, row in enumerate(self.content[self.cur_page]):
            self.display_surf.blit(row,
                                   (self.rect.x + self.margin_left,
                                    self.rect.y + self.margin_top + i * (self.font_height + self.line_spacing)))

    def update(self):
        if self.is_active:
            self.draw_window()
            self.interactive_group.custom_draw()
            self.draw_content()


class WindowGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for item in self.sprites():
            pygame.draw.rect(self.display_surface, item.color, item.interaction_hitbox)
            pygame.draw.rect(self.display_surface, 'black', item.border, 3, 2)


class UserInterface:
    def __init__(self, interactive_items, offset, player):
        self.window = Window(self)
        self.screen_transition = Transition()
        self.player = player
        self.screen_offset = offset
        self.mouse_position = pygame.mouse.get_pos()
        self.cursor_visibility = False
        self.display_surface = pygame.display.get_surface()
        self.timers = {'click': Timer(400)}
        self.setup_sprites(interactive_items)
        self.setup()

    def setup_sprites(self, interactive_items):
        self.current_interactive_group = interactive_items
        self.all_interactive_groups = cycle([self.window.interactive_group, interactive_items])
        self.hovered_sprite = None
        self.clicked_sprite = None

    def setup(self):
        for interactive_item in self.current_interactive_group:
            if hasattr(interactive_item, 'set_content'):
                interactive_item.set_content(
                    one_letter_width=self.window.one_letter_width,
                    space_width=self.window.space_width,
                    text_rows_page=self.window.text_rows_in_one_page,
                    text_width=self.window.text_width,
                    font=self.window.font)
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 25)
        self.text = self.font.render('Interact', False, '#dadbdf')
        self.text_size = self.text.get_size()
        self.text_rect = self.text.get_rect().inflate(10, 10)
        self.shape_surf = pygame.Surface(self.text_rect.size, pygame.SRCALPHA)
        self.shape_surf.set_alpha(128)
        self.shape_surf.fill('#292f3d')

    def change_interactive_group(self):
        self.current_interactive_group = next(self.all_interactive_groups)

    def click(self, item):
        content = item.clicked()
        if content == 'teleport':
            self.screen_transition.change_act_status()
            self.clicked_sprite = item
        elif content:
            self.window.set_content(content)
            self.window.switch_status()
            self.change_interactive_group()
            self.switch_cursor_visibility()
            self.hovered_sprite = None

    def hover(self):
        if self.hovered_sprite is None:
            for item in self.current_interactive_group:
                if item.is_hovered(self.mouse_position):
                    self.hovered_sprite = item
                    self.switch_cursor_visibility()
                    break
        elif not self.hovered_sprite.is_hovered(self.mouse_position):
            self.switch_cursor_visibility()
            self.hovered_sprite = None

    def switch_cursor_visibility(self):
        self.cursor_visibility = pygame.mouse.get_visible()
        pygame.mouse.set_visible(not self.cursor_visibility)

    def draw_cursor_in_hover_status(self):
        self.text_rect.center = pygame.mouse.get_pos()
        text_x = self.text_rect.topleft[0] + (self.text_rect.width - self.text_size[0]) // 2
        text_y = self.text_rect.topleft[1] + (self.text_rect.height - self.text_size[1]) // 2
        self.display_surface.blit(self.shape_surf, self.text_rect)
        pygame.draw.rect(self.display_surface, '#6f4641', self.text_rect.inflate(2, 2), 2, 4)
        self.display_surface.blit(self.text, (text_x, text_y))

    def is_able_to_click(self):
        return not self.timers['click'].is_active and self.hovered_sprite

    def input(self):
        keys = pygame.key.get_pressed()
        self.mouse_position = pygame.mouse.get_pos()
        if not self.window.is_active:
            self.mouse_position = (self.mouse_position[0] + self.screen_offset.x,
                                   self.mouse_position[1] + self.screen_offset.y)
        else:
            if keys[pygame.K_ESCAPE]:
                self.window.switch_status()
                self.change_interactive_group()

        buttons = pygame.mouse.get_pressed()
        if buttons[0] and self.is_able_to_click():
            self.click(self.hovered_sprite)
            self.timers['click'].activate()
        self.hover()

    def update_timers(self):
        for timer in self.timers:
            self.timers[timer].update()

    def update(self):  # TODO работа transition сделана неуклюже и громоздко, постараться исправить
        if not self.screen_transition.active:
            self.update_timers()
            self.window.update()
            self.input()
            if self.cursor_visibility:
                self.draw_cursor_in_hover_status()
        else:
            self.screen_transition.play()
            if self.screen_transition.dark:
                self.clicked_sprite.teleport()
                self.screen_transition.dark = False
