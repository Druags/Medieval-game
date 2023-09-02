import pygame

from settings import *
from sprites import GenericObject
from items import Item


class Interactive(GenericObject):
    def __init__(self, pos, surf, groups, z, size_difference, name, player):
        super().__init__(pos, surf, groups, z, size_difference)
        self.name = name
        self.active = False if any([name in self.name for name in ['arch', 'ladder']]) else True
        self.player = player
        if 'runestone' in self.name:
            self.hitbox = pygame.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, 50)
            self.hitbox.bottom = self.rect.bottom
            self.item = Item(self.player)
        elif 'portal' in self.name:
            self.hitbox = self.hitbox.inflate((-60 * size_difference[0], -50 * size_difference[1]))
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
        elif 'chest' in self.name:
            opened_chest = self.resize_surf(surf)
            closed_chest = self.resize_surf(pygame.image.load('../data/objects/open_chest.png'))
            self.surfaces = [opened_chest, closed_chest]
            self.current_surf = 0
            self.image = self.surfaces[self.current_surf]

        self.interaction_hitbox = self.hitbox.inflate((20 * size_difference[0], 20 * size_difference[1]))
        # self.color_active = cycle(['red', 'gray'])
        # self.color_hover = cycle(['blue', 'gray'])
        # self.current_color = 'gray'
        self.is_hovered = False

    # def change_color(self, type):
    #     if type == 'click':
    #         self.current_color = next(self.color_active)
    #     elif type == 'hover':
    #         self.current_color = next(self.color_hover)

    def clicked(self):
        # self.change_color('click')
        pass

    def hovered(self, ):
        # self.change_color('hover')
        pass

    def change_surf(self):

        if self.current_surf == 0:
            self.current_surf = 1
        else:
            self.current_surf = 0
        if 'door' in self.name:
            self.hitbox_status = not self.hitbox_status

        self.image = self.surfaces[self.current_surf]

    def click(self):
        if hasattr(self, 'current_surf'):
            self.change_surf()
        if hasattr(self, 'item'):
            self.player.overlay.change_status()
            self.item.change_status()
