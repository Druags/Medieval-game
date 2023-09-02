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


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = pygame.Rect(20, 20, 30, 30)
        self.direction = pygame.math.Vector2()
        self.current_color = 'green'

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def move(self):
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y

    def update(self):
        self.input()
        self.move()


class UserInterface:
    def __init__(self, interactive, player):
        self.interactive = interactive
        self.player = player
        self.hovered_sprite = None
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
            if interactive.rect.collidepoint(self.mouse):
                interactive.clicked()

    def check_hover(self, sprite):
        return sprite.interactive_rect.collidepoint(self.mouse) and sprite.interactive_rect.colliderect(self.player)

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
        if self.visible:
            self.draw()
        self.input()


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.group = CustomGroup()
        self.player = Player(self.group)

        self.setup()

    def setup(self):
        self.objects = [Interactive(self.group) for _ in range(5)]
        self.interface = UserInterface(self.objects, self.player)

    def run(self, dt):
        self.display_surface.fill('black')

        self.group.custom_draw()
        self.group.update()
        self.interface.update()


class CustomGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for item in self.sprites():
            if hasattr(item, 'interactive_rect'):
                pygame.draw.rect(self.display_surface, 'white', item.interactive_rect)
            pygame.draw.rect(self.display_surface, item.current_color, item.rect)
