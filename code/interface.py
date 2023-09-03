import pygame

from timer import Timer
from settings import *


class UserInterface:
    def __init__(self, interactive, offset, player):
        self.interactive = interactive
        self.player = player
        self.hovered_sprite = None

        self.offset = offset
        self.mouse = pygame.mouse.get_pos()
        self.visible = False

        self.display_surface = pygame.display.get_surface()

        self.timers = {'click': Timer(200)}

        self.setup()

    def setup(self):
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 25)
        self.text = self.font.render('Interact', False, '#dadbdf')
        self.text_rect = self.text.get_rect().inflate(10, 10)
        self.shape_surf = pygame.Surface(self.text_rect.size, pygame.SRCALPHA)
        self.shape_surf.set_alpha(128)
        self.shape_surf.fill('#292f3d')

    def click(self):
        for interactive in self.interactive:
            if interactive.rect.collidepoint(self.offset_mouse):
                interactive.clicked()

    def check_hover(self, sprite):
        return sprite.interaction_hitbox.collidepoint(self.offset_mouse) and \
               sprite.interaction_hitbox.colliderect(self.player) and \
               sprite.mouse_interaction

    def hover(self):
        if self.hovered_sprite is None:
            for interactive in self.interactive:
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
        if self.visible:
            self.hover_cursor()

