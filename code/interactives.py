import math
import random

import pygame

from settings import *
from sprites import GenericObject

from items import Item


def create_interactive(obj, groups, z, size_difference, player, special_group):
    if 'runestone' in obj.name:
        Runestone(pos=(obj.x, obj.y), surf=obj.image, groups=groups, z=z, size_difference=size_difference,
                  name=obj.name,
                  player=player,
                  content=obj.content)
    elif 'portal' in obj.name:
        Portal(pos=(obj.x, obj.y), surf=obj.image, groups=groups, z=z, size_difference=size_difference, name=obj.name,
               player=player,
               portals=special_group)
    elif 'ladder' in obj.name:
        Ladder(pos=(obj.x, obj.y), surf=obj.image, groups=groups, z=z, size_difference=size_difference, name=obj.name,
               player=player)
    elif 'door' in obj.name:
        Door(pos=(obj.x, obj.y), surf=obj.image, groups=groups, z=z, size_difference=size_difference, name=obj.name,
             player=player)
    elif 'chest' in obj.name:
        Chest(pos=(obj.x, obj.y), surf=obj.image, groups=groups, z=z, size_difference=size_difference, name=obj.name,
              player=player)
    elif 'arch' in obj.name:
        Arch(pos=(obj.x, obj.y), surf=obj.image, groups=groups, z=z, size_difference=size_difference, name=obj.name,
             player=player)


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
    def __init__(self, pos, surf, groups, z, size_difference, name, player, content):
        super().__init__(pos, surf, groups, z, size_difference, name, player)
        self.hitbox = pygame.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, 50)
        self.hitbox.bottom = self.rect.bottom
        self.item = Item(self.player)
        self.text = content
        self.content = None

    def set_content(self, one_letter_width, space_width, text_rows_page, text_width, font):
        content_len = len(self.text) * one_letter_width
        text_rows_content = math.ceil(content_len / WINDOW_WIDTH)
        num_of_pages = math.ceil(text_rows_content / text_rows_page)
        content_lst = []
        for page in range(num_of_pages):
            page = []
            for x in range(text_rows_page):
                part = self.text[0:text_width]
                last_space = part.rfind(' ')
                part = part[0: last_space]
                self.text = self.text[last_space + 1:]
                to_fill = (WINDOW_WIDTH - len(part) * one_letter_width) // space_width

                page.append(part.center(int(text_width + to_fill), ' '))

            content_lst.append(page)
        self.content = [[font.render(row, False, 'black') for row in part] for part in content_lst]

    def clicked(self):
        return self.content


class Portal(Interactive):
    def __init__(self, pos, surf, groups, z, size_difference, name, player, portals):

        super().__init__(pos, surf, groups+[portals], z, size_difference, name, player)

        self.hitbox = self.hitbox.inflate((-60 * size_difference[0], -50 * size_difference[1]))
        self.z = LAYERS['Interactive']
        self.portals_coords = [portal.pos for portal in self.groups()[2].sprites()]

    def clicked(self):

        if self.name == 'portal_enter':
            pos = self.groups()[2].sprites()[1].pos
            self.player.pos = pygame.math.Vector2(pos[0] + self.size[0], pos[1] + self.size[1]*2)
        else:
            pos = self.groups()[2].sprites()[0].pos
            self.player.pos = pygame.math.Vector2(pos[0] + self.size[0], pos[1] + self.size[1]*2)
        # print(self.portals_coords)


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
