import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.pos = pygame.math.Vector2(pos)
        self.image = pygame.image.load('../data/objects/small_box.png')
        self.rect = self.image.get_rect(center=self.pos)
        self.line_of_sight = self.rect.copy().inflate((SCREEN_WIDTH*2, SCREEN_HEIGHT*2))

        self.z = LAYERS['Main']

        self.direction = pygame.math.Vector2()
        self.speed = 200

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

    def move(self, dt):
        # нормализация вектора
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * dt * self.speed
        self.pos.y += self.direction.y * dt * self.speed

        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.line_of_sight.center = (round(self.pos.x), round(self.pos.y))

    def update(self, dt):
        self.input()
        self.move(dt)
