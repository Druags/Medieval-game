import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, interactive_sprites, borders):
        super().__init__(groups)
        self.pos = pygame.math.Vector2(pos)
        self.image = pygame.image.load('../data/objects/small_box.png')
        self.rect = self.image.get_rect(center=self.pos)
        self.line_of_sight = self.rect.copy().inflate((SCREEN_WIDTH*2, SCREEN_HEIGHT*2))

        self.hitbox = self.rect.copy()
        self.collision_sprites = collision_sprites
        self.interactive_sprites = interactive_sprites
        self.borders = borders

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

    def collide(self, sprite, direction):
        if sprite.hitbox.colliderect(self.hitbox):
            if direction == 'horizontal':
                if self.direction.x > 0:
                    self.hitbox.right = sprite.hitbox.left
                if self.direction.x < 0:
                    self.hitbox.left = sprite.hitbox.right

                self.rect.centerx = self.hitbox.centerx
                self.pos.x = self.hitbox.centerx

            if direction == 'vertical':
                if self.direction.y > 0:
                    self.hitbox.bottom = sprite.hitbox.top
                if self.direction.y < 0:
                    self.hitbox.top = sprite.hitbox.bottom

                self.rect.centery = self.hitbox.centery
                self.pos.y = self.hitbox.centery

    def collision_check(self, direction):
        for sprite in self.interactive_sprites.sprites():
            if sprite.active:
                self.collide(sprite, direction)
            else:
                if sprite.name == 'ladder' and self.hitbox.colliderect(sprite.hitbox):
                    self.z = LAYERS['Second_floor']


        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox') and sprite.hitbox and sprite.hitbox_status:
                self.collide(sprite, direction)

    def move(self, dt):
        # нормализация вектора
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision_check('horizontal')

        # вертикальное перемещение
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision_check('vertical')

        self.line_of_sight.center = (round(self.hitbox.x), round(self.hitbox.y))

    def update(self, dt):
        self.input()
        self.move(dt)
