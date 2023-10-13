import math
import pygame
from itertools import cycle

from settings import *
from sprites import GenericObject


def create_interactive(pos, surf, name, groups, z, player, content=None, special_group=None):
    if 'runestone' in name:
        Runestone(pos=pos, surf=surf, groups=groups, z=z,
                  name=name, player=player, content=content)
    elif 'portal' in name:
        Portal(pos=pos, surf=surf, groups=groups, z=z,
               name=name, player=player, portals=special_group)
    elif 'ladder' in name:
        Ladder(pos=pos, surf=surf, groups=groups, z=z,
               name=name, player=player, )
    elif 'door' in name:
        Door(pos=pos, surf=surf, groups=groups, z=z,
             name=name, player=player, )
    elif 'chest' in name:
        Chest(pos=pos, surf=surf, groups=groups, z=z,
              name=name, player=player, )
    elif 'arch' in name:
        Arch(pos=pos, surf=surf, groups=groups, z=z,
             name=name, player=player, )
    elif 'statue' in name:
        Statue(pos=pos, surf=surf, groups=groups, z=z,
               name=name, player=player, )


class Interactive(GenericObject):
    def __init__(self, pos, surf, groups, z, name, player):
        super().__init__(pos, surf, groups, z)
        self.name = name
        self.player = player
        self.is_interactive = self.choose_activity_by_type(name)
        self.is_collidable = True
        self.size = surf.get_size()
        self.interaction_hitbox = self.hitbox.inflate((20, 20))

    def choose_activity_by_type(self, name):
        return False if 'arch' in name or 'ladder' in name else True

    def clicked(self):
        pass

    def is_hovered(self, mouse_position):
        return self.is_interactive and \
               self.interaction_hitbox.collidepoint(mouse_position) and \
               self.interaction_hitbox.colliderect(self.player)


class Statue(Interactive):
    def __init__(self, pos, surf, groups, z, name, player, content=None):
        super().__init__(pos, surf, groups, z, name, player)
        self.hitbox = pygame.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, 50)
        self.hitbox.bottom = self.rect.bottom
        self.text = content
        self.content = None


class Runestone(Interactive):
    def __init__(self, pos, surf, groups, z, name, player, content):
        super().__init__(pos, surf, groups, z, name, player)
        self.hitbox = pygame.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, 50)
        self.hitbox.bottom = self.rect.bottom

        self.interaction_hitbox = self.hitbox.inflate((self.hitbox.width * 1.3, self.hitbox.height * 1.3))
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
    def __init__(self, pos, surf, groups, z, name, player, portals):
        super().__init__(pos, surf, groups + [portals], z, name, player)
        self.hitbox = self.rect.inflate((-self.size[0] * 0.8, -self.size[1] * 0.8))
        self.interaction_hitbox = self.hitbox.inflate((self.hitbox.width * 1.3, self.hitbox.height * 1.3))
        self.z = LAYERS['Interactive']
        self.portals_coords = [portal.pos for portal in self.groups()[2].sprites()]

    def teleport(self):  # TODO механика телепорта и создания группы телепортов неудобна, нужно исправить
        if self.name == 'portal_enter':
            pos = self.groups()[2].sprites()[1].interaction_hitbox.midbottom
            self.player.pos = pygame.math.Vector2(pos)
        else:
            pos = self.groups()[2].sprites()[0].interaction_hitbox.midbottom
            self.player.pos = pygame.math.Vector2(pos)

    def clicked(self):
        return 'teleport'


class Ladder(Interactive):
    def __init__(self, pos, surf, groups, z, name, player):
        super().__init__(pos, surf, groups, z, name, player)
        self.z = LAYERS['Interactive']
        self.is_collidable = False
        self.interaction_hitbox = None


class Door(Interactive):
    def __init__(self, pos, surf, groups, z, name, player):
        super().__init__(pos, surf, groups, z, name, player)
        closed_door = surf
        opened_door = pygame.transform.scale(pygame.image.load('../data/objects/open_door.png'),
                                             closed_door.get_size())
        self.z = LAYERS['Decorations']
        self.images = cycle([opened_door, closed_door])
        self.image = closed_door

        self.hitbox.top += 50
        self.hitbox = self.hitbox.inflate((0,-80))
        self.interaction_hitbox = self.hitbox.inflate((30, 50))

    def clicked(self):
        self.change_surf()

    def change_surf(self):
        self.image = next(self.images)
        self.is_collidable = not self.is_collidable


class Chest(Interactive):
    def __init__(self, pos, surf, groups, z, name, player):
        super().__init__(pos, surf, groups, z, name, player)
        opened_chest = surf
        closed_chest = pygame.transform.scale(pygame.image.load('../data/objects/open_chest.png'),
                                              opened_chest.get_size())
        self.images = cycle([opened_chest, closed_chest])
        self.image = surf

    def clicked(self):
        self.change_surf()

    def change_surf(self):
        self.image = next(self.images)


class Arch(Interactive):
    def __init__(self, pos, surf, groups, z, name, player):
        super().__init__(pos, surf, groups, z, name, player)
        self.is_collidable = False
        self.z = LAYERS['Decorations']+1
        self.interaction_hitbox = None
