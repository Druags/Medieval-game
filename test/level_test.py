import pygame

from interface_test import UserInterface

from interactive_test import Interactive


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
