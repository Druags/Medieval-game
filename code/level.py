import pygame
from pytmx.util_pygame import load_pygame

from settings import *
from player import Player
from sprites import Generic, Tree, Wall, Building, Roof, Decoration
from interactives import create_interactive
from borders import Border
from items import Item
from interface import UserInterface


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.interactive_sprites = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()

        self.player = Player((700, 1600), self.all_sprites, self.collision_sprites, self.interactive_sprites,
                             self.borders)


        self.setup()
        self.interface = UserInterface(self.interactive_sprites, self.all_sprites.offset, self.player)

    def setup(self):
        tmx_data = load_pygame('../data/game_map.tmx')
        Generic(
            pos=(0, 0),
            surf=pygame.image.load('../data/game_map.png'),
            groups=self.all_sprites,
            z='Ground'
        )
        self.all_sprites.world_size = self.all_sprites.sprites()[1].image.get_size()
        self.all_sprites.world_size = (1920, 2560)

        world_width = self.all_sprites.world_size[0]
        world_height = self.all_sprites.world_size[1]

        size_difference = (world_width // (tmx_data.width * TILE_SIZE), world_height // (tmx_data.height * TILE_SIZE))

        for x, y, surf in tmx_data.get_layer_by_name('Walls_front').tiles():
            Wall(pos=(x, y),
                 surf=surf,
                 groups=[self.all_sprites, self.collision_sprites],
                 size_difference=size_difference,
                 wall_type='front')
        for x, y, surf in tmx_data.get_layer_by_name('Walls_back').tiles():
            Wall(pos=(x, y),
                 surf=surf,
                 groups=[self.all_sprites, self.collision_sprites],
                 size_difference=size_difference,
                 wall_type='back')
        for x, y, surf in tmx_data.get_layer_by_name('Walls_front_second_floor').tiles():
            Wall(pos=(x, y),
                 surf=surf,
                 groups=[self.all_sprites, self.collision_sprites],
                 size_difference=size_difference,
                 wall_type='front_second_floor')
        for x, y, surf in tmx_data.get_layer_by_name('Roof_1').tiles():
            Roof(pos=(x, y),
                 surf=surf,
                 groups=self.all_sprites,
                 z='Walls_back',
                 size_difference=size_difference)
        for x, y, surf in tmx_data.get_layer_by_name('Roof_2').tiles():
            Roof(pos=(x, y),
                 surf=surf,
                 groups=self.all_sprites,
                 z='Second_floor_roof',
                 size_difference=size_difference)
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(pos=(obj.x, obj.y),
                 surf=obj.image,
                 groups=[self.all_sprites, self.collision_sprites],
                 z='Trees',
                 size_difference=size_difference)

        for obj in tmx_data.get_layer_by_name('Interactive_objects'):
            create_interactive(obj=obj,
                               groups=[self.all_sprites, self.interactive_sprites],
                               z='Main',
                               size_difference=size_difference,
                               player=self.player)
        for obj in tmx_data.get_layer_by_name('Interactive_objects_second_floor'):
            create_interactive(obj=obj,
                               groups=[self.all_sprites, self.interactive_sprites],
                               z='Second_floor',
                               size_difference=size_difference,
                               player=self.player)
        for obj in tmx_data.get_layer_by_name('Buildings'):
            Building(pos=(obj.x, obj.y),
                     surf=obj.image,
                     groups=[self.all_sprites, self.collision_sprites],
                     z='Second_floor_buildings',
                     size_difference=size_difference)
        for layer in ['Stones', 'Small_plants']:
            for obj in tmx_data.get_layer_by_name(layer):
                Decoration(pos=(obj.x, obj.y),
                           surf=obj.image,
                           groups=[self.all_sprites],
                           z='Decorations',
                           size_difference=size_difference)
        for obj in tmx_data.get_layer_by_name('Borders_first_floor'):
            Border(pos=(round(obj.x), round(obj.y)),
                   size=(round(obj.width), round(obj.height)),
                   groups=[self.borders],
                   size_difference=size_difference,
                   floor=0
                   )
        for obj in tmx_data.get_layer_by_name('Borders_second_floor'):
            Border(pos=(round(obj.x), round(obj.y)),
                   size=(round(obj.width), round(obj.height)),
                   groups=[self.borders],
                   size_difference=size_difference,
                   floor=1
                   )

    def run(self, dt):
        self.all_sprites.custom_draw(self.player)
        if not self.interface.window.active:
            self.player.update(dt)
        self.interface.update()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.world_size = None
        self.font = pygame.font.Font(None, 32)

    def border_camera(self, player):
        if player.rect.left < SCREEN_WIDTH // 2:
            self.offset.x = 0
        elif player.rect.right > self.world_size[0] - SCREEN_WIDTH // 2:
            pass
        else:
            self.offset.x = player.pos.x - SCREEN_WIDTH // 2

        if player.rect.top < SCREEN_HEIGHT // 2:
            self.offset.y = 0
        elif player.rect.bottom > self.world_size[1] - SCREEN_HEIGHT // 2:
            self.offset.y = self.world_size[1] - SCREEN_HEIGHT
        else:
            self.offset.y = player.pos.y - SCREEN_HEIGHT // 2

    def custom_draw(self, player):
        self.border_camera(player)
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.rect.colliderect(player.line_of_sight) and sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    if isinstance(sprite, Player):
                        offset_rect.top -= 10
                    copy_sight = player.line_of_sight.copy()
                    copy_sight.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    if DEBUG:
                        if hasattr(sprite, 'hitbox') and sprite.hitbox:
                            hitbox_copy = sprite.hitbox.copy()
                            hitbox_copy.center -= self.offset

                            if isinstance(sprite, Player):
                                rect_offset = sprite.rect.copy()
                                rect_offset.center -= self.offset

                                text = self.font.render(f'{player.rect.center}', True, 'green')
                                offset_rect.centery -= text.get_size()[1] + 10
                                offset_rect.centerx -= text.get_size()[0] // 2 - offset_rect.width // 2
                                self.display_surface.blit(text, offset_rect)

                            pygame.draw.rect(self.display_surface, 'red', hitbox_copy, 2)
                        # pygame.draw.rect(self.display_surface, 'red', offset_rect, 2)
