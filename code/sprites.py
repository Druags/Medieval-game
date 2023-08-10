import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z='Main'):
        super().__init__(groups)

        self.image = surf
        self.pos = pos
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS[z]


# Спрайты на основе объектов
class GenericObject(Generic):
    def __init__(self, pos, surf, groups, z, size_difference):
        size = surf.get_size()
        surf = pygame.transform.scale(surf, (size[0] * size_difference[0], size[1] * size_difference[1]))
        pos = [pos[i] * size_difference[i] for i in range(2)]
        super().__init__(pos, surf, groups, z)


class Tree(GenericObject):
    def __init__(self, pos, surf, groups, z, size_difference):
        super().__init__(pos, surf, groups, z, size_difference)


class Interactive(GenericObject):
    def __init__(self, pos, surf, groups, z, size_difference, name):
        super().__init__(pos, surf, groups, z, size_difference)
        self.name = name
        self.active = False if any([name in self.name for name in ['arch', 'ladder']]) else True


class Building(GenericObject):
    def __init__(self, pos, surf, groups, z, size_difference):
        super().__init__(pos, surf, groups, z, size_difference)


# Спрайты на основе тайлов
class Wall(Generic):
    def __init__(self, pos, surf, groups, z, size_difference, wall_type):
        size = surf.get_size()
        surf = pygame.transform.scale(surf, (size[0] * size_difference[0], size[1] * size_difference[1]))
        pos = [pos[i] * size_difference[i] * TILE_SIZE for i in range(2)]
        super().__init__(pos, surf, groups, z)
        self.wall_type = wall_type


class Roof(Generic):
    def __init__(self, pos, surf,  groups, z, size_difference):
        size = surf.get_size()
        surf = pygame.transform.scale(surf, (size[0] * size_difference[0], size[1] * size_difference[1]))
        pos = [pos[i] * size_difference[i]*TILE_SIZE for i in range(2)]
        super().__init__(pos, surf, groups, z)

