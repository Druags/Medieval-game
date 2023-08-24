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

    def update_status(self):
        self.hitbox_status = not self.hitbox_status


# Спрайты на основе объектов
class GenericObject(Generic):
    def __init__(self, pos, surf, groups, z, size_difference):
        self.size = surf.get_size()
        self.size_difference = size_difference
        surf = self.resize_surf(surf)
        pos = [pos[i] * size_difference[i] for i in range(2)]
        super().__init__(pos, surf, groups, z)

    def resize_surf(self, surf):
        return pygame.transform.scale(surf,
                                      (self.size[0] * self.size_difference[0], self.size[1] * self.size_difference[1]))


class Decoration(GenericObject):
    def __init__(self, pos, surf, groups, z, size_difference):
        super().__init__(pos, surf, groups, z, size_difference)
        self.hitbox = None


class Tree(GenericObject):
    def __init__(self, pos, surf, groups, z, size_difference):
        super().__init__(pos, surf, groups, z, size_difference)
        self.hitbox = self.hitbox.inflate((-200, -250))
        self.hitbox.top += 125


class Interactive(GenericObject):
    def __init__(self, pos, surf, groups, z, size_difference, name):
        super().__init__(pos, surf, groups, z, size_difference)
        self.name = name
        self.active = False if any([name in self.name for name in ['arch', 'ladder']]) else True

        if 'runestone' in self.name:
            self.hitbox = pygame.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, 50)
            self.hitbox.bottom = self.rect.bottom
        elif 'portal' in self.name:
            self.hitbox = self.hitbox.inflate((-60*size_difference[0], -50*size_difference[1]))
            self.z = LAYERS['Ground']
        elif 'ladder' in self.name:
            self.z = LAYERS['Interactive']
        elif 'door' in self.name:
            closed_door = self.resize_surf(surf)
            opened_door = self.resize_surf(pygame.image.load('../data/objects/open_door.png'))
            self.z = LAYERS['Ground']
            self.surfaces = [closed_door, opened_door]
            self.current_surf = 0
            self.image = self.surfaces[self.current_surf]

        self.interaction_hitbox = self.hitbox.inflate((20*size_difference[0], 20*size_difference[1]))

    def change_surf(self):
        if self.current_surf == 0:
            self.current_surf = 1
        else:
            self.current_surf = 0
        if 'door' in self.name:
            self.hitbox_status = not self.hitbox_status

        self.image = self.surfaces[self.current_surf]


class Building(GenericObject):
    def __init__(self, pos, surf, groups, z, size_difference):
        super().__init__(pos, surf, groups, z, size_difference)
        self.hitbox = pygame.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, 50)
        self.hitbox.bottom = self.rect.bottom


# Спрайты на основе тайлов
class Wall(Generic):
    def __init__(self, pos, surf, groups, size_difference, wall_type):
        size = surf.get_size()
        surf = pygame.transform.scale(surf, (size[0] * size_difference[0], size[1] * size_difference[1]))
        pos = [pos[i] * size_difference[i] * TILE_SIZE for i in range(2)]
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
    def __init__(self, pos, surf,  groups, z, size_difference):
        size = surf.get_size()
        surf = pygame.transform.scale(surf, (size[0] * size_difference[0], size[1] * size_difference[1]))
        pos = [pos[i] * size_difference[i]*TILE_SIZE for i in range(2)]
        super().__init__(pos, surf, groups, z)

