import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z='Main'):
        super().__init__(groups)
        self.image = surf
        self.pos = pos
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS[z]
        self.hitbox = self.rect.copy()
        self.hitbox_status = True

    def switch_status(self):
        self.hitbox_status = not self.hitbox_status


# Спрайты на основе объектов
class GenericObject(Generic):
    def __init__(self, pos, surf, groups, z):
        super().__init__(pos, surf, groups, z)


class Decoration(GenericObject):
    def __init__(self, pos, surf, groups, z):
        super().__init__(pos, surf, groups, z, )
        self.hitbox = None


class Tree(GenericObject):
    def __init__(self, pos, surf, groups, z):
        super().__init__(pos, surf, groups, z)
        self.hitbox = self.hitbox.inflate((-200, -250))
        self.hitbox.top += 125


class Building(GenericObject):
    def __init__(self, pos, surf, groups, z):
        super().__init__(pos, surf, groups, z)
        self.hitbox = pygame.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, 50)
        self.hitbox.bottom = self.rect.bottom


# Спрайты на основе тайлов
class Wall(Generic):
    def __init__(self, pos, surf, groups, wall_type):
        super().__init__(pos, surf, groups)
        self.wall_type = wall_type
        if self.wall_type == 'back':
            self.z = LAYERS['Walls_back']
            self.hitbox = None
        elif self.wall_type == 'front':
            self.z = LAYERS['Walls_front']
        elif self.wall_type == 'front_second_floor':
            self.z = LAYERS['Second_floor']


class Roof(Generic):
    def __init__(self, pos, surf,  groups, z):
        super().__init__(pos, surf, groups, z)

