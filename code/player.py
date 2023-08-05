import pygame
from settings import *


class Player:
    def __init__(self):
        self.pos = pygame.math.Vector2()
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
        # print(self.direction.x, self.direction.y)
        # нормализация вектора
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        print(self.direction.x * dt * self.speed)
        self.pos.x += self.direction.x * dt * self.speed

        self.pos.y += self.direction.y * dt * self.speed
        # print(self.rect.center)

    def update(self, dt):
        self.input()
        self.move(dt)
