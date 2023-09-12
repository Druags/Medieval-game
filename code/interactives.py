import pygame

from settings import *
from sprites import GenericObject

from items import Item


def create_interactive(pos, surf, groups, z, size_difference, name, player):
    if 'runestone' in name:
        Runestone(pos, surf, groups, z, size_difference, name, player)
    elif 'portal' in name:
        Portal(pos, surf, groups, z, size_difference, name, player)
    elif 'ladder' in name:
        Ladder(pos, surf, groups, z, size_difference, name, player)
    elif 'door' in name:
        Door(pos, surf, groups, z, size_difference, name, player)
    elif 'chest' in name:
        Chest(pos, surf, groups, z, size_difference, name, player)
    elif 'arch' in name:
        Arch(pos, surf, groups, z, size_difference, name, player)


class Interactive(GenericObject):
    def __init__(self, pos, surf, groups, z, size_difference, name, player):
        super().__init__(pos, surf, groups, z, size_difference)
        self.name = name
        self.mouse_interaction = False if 'arch' in name or 'ladder' in name else True
        self.player = player
        self.active = False if 'arch' in name or 'ladder' in name else True

        self.interaction_hitbox = self.hitbox.inflate((20 * size_difference[0], 20 * size_difference[1]))
        self.is_hovered = False

    def clicked(self):
        pass

    def hovered(self, ):
        pass


class Runestone(Interactive):
    def __init__(self, pos, surf, groups, z, size_difference, name, player):
        super().__init__(pos, surf, groups, z, size_difference, name, player)
        self.hitbox = pygame.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, 50)
        self.hitbox.bottom = self.rect.bottom
        self.item = Item(self.player)


    def clicked(self):
        print(1)


class Portal(Interactive):
    def __init__(self, pos, surf, groups, z, size_difference, name, player):
        super().__init__(pos, surf, groups, z, size_difference, name, player)
        self.hitbox = self.hitbox.inflate((-60 * size_difference[0], -50 * size_difference[1]))
        self.z = LAYERS['Ground']


class Ladder(Interactive):
    def __init__(self, pos, surf, groups, z, size_difference, name, player):
        super().__init__(pos, surf, groups, z, size_difference, name, player)
        self.z = LAYERS['Interactive']


class Door(Interactive):
    def __init__(self, pos, surf, groups, z, size_difference, name, player):
        super().__init__(pos, surf, groups, z, size_difference, name, player)
        closed_door = self.resize_surf(surf)
        opened_door = self.resize_surf(pygame.image.load('../data/objects/open_door.png'))
        self.z = LAYERS['Ground']
        self.surfaces = [closed_door, opened_door]
        self.current_surf = 0
        self.image = self.surfaces[self.current_surf]

    def clicked(self):
        self.change_surf()

    def change_surf(self):
        if self.current_surf == 0:
            self.current_surf = 1
        else:
            self.current_surf = 0
        self.active = not self.active
        self.image = self.surfaces[self.current_surf]


class Chest(Interactive):
    def __init__(self, pos, surf, groups, z, size_difference, name, player):
        super().__init__(pos, surf, groups, z, size_difference, name, player)
        opened_chest = self.resize_surf(surf)
        closed_chest = self.resize_surf(pygame.image.load('../data/objects/open_chest.png'))
        self.surfaces = [opened_chest, closed_chest]
        self.current_surf = 0
        self.image = self.surfaces[self.current_surf]

    def clicked(self):
        self.change_surf()

    def change_surf(self):
        if self.current_surf == 0:
            self.current_surf = 1
        else:
            self.current_surf = 0
        self.image = self.surfaces[self.current_surf]


class Arch(Interactive):
    def __init__(self, pos, surf, groups, z, size_difference, name, player):
        super().__init__(pos, surf, groups, z, size_difference, name, player)
