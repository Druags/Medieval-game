import pygame
from settings import *

from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, interactive_sprites, borders):
        super().__init__(group)
        self.pos = pygame.math.Vector2(pos)
        self.image = pygame.image.load('../data/objects/small_box.png')
        self.rect = self.image.get_rect(center=self.pos)

        self.hitbox = self.rect.copy().inflate(0, -20)
        self.hitbox_active = True

        self.collision_sprites = collision_sprites
        self.interactive_sprites = interactive_sprites
        self.borders = borders

        self.z = LAYERS['Main']

        self.direction = pygame.math.Vector2()
        self.speed = 200

        self.offset = None
        self.line_of_sight = self.rect.copy().inflate((SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2))

        self.current_floor = 0

        self.active_item = None

        self.timers = {
            'ladder_timer': Timer(1000),
            'input_timer': Timer(200)
        }

    def input(self):
        keys = pygame.key.get_pressed()
        if DEBUG:
            if keys[pygame.K_SPACE] and not self.timers['input_timer'].is_active:
                self.hitbox_active = not self.hitbox_active
                self.timers['input_timer'].activate()

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

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

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

    def collide_ladders(self, sprite):
        if self.direction.y == -1 and sprite.rect.collidepoint(self.rect.midbottom):
            self.z = LAYERS['Second_floor']
            self.current_floor = 1
        elif self.direction.y == 1 and sprite.rect.collidepoint(self.rect.midtop):
            self.z = LAYERS['Main']
            self.current_floor = 0

    def collision_check(self, direction):
        if self.hitbox_active:
            for sprite in self.interactive_sprites.sprites():

                if sprite.name == 'ladder' and self.rect.colliderect(sprite.hitbox):
                    self.collide_ladders(sprite)
                elif self.rect.colliderect(sprite.hitbox) and sprite.is_active:
                    self.collide(sprite, direction)
            for sprite in self.collision_sprites.sprites():
                if hasattr(sprite, 'hitbox') and sprite.hitbox and sprite.hitbox_status:
                    self.collide(sprite, direction)

            for sprite in self.borders.sprites():
                if sprite.floor == self.current_floor:
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
        self.update_timers()
        self.move(dt)
