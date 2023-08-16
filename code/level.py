import pygame
from pytmx.util_pygame import load_pygame

from settings import *
from player import Player
from sprites import Generic, Tree, Wall, Interactive, Building, Roof, Decoration
from borders import Border


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.interactive_sprites = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()

        self.player = Player((700, 1600), self.all_sprites, self.collision_sprites, self.interactive_sprites, self.borders)
        self.setup()

    def setup(self):
        tmx_data = load_pygame('../data/game_map.tmx')
        Generic(
            pos=(0, 0),
            surf=pygame.image.load('../data/game_map.png'),
            groups=self.all_sprites,
            z='Ground'
        )
        self.all_sprites.world_size = self.all_sprites.sprites()[1].image.get_size()
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
        for x, y, surf in tmx_data.get_layer_by_name('Roof_1').tiles():
            Roof(pos=(x, y),
                 surf=surf,
                 groups=self.all_sprites,
                 z='Roof',
                 size_difference=size_difference)

        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(pos=(obj.x, obj.y),
                 surf=obj.image,
                 groups=[self.all_sprites, self.collision_sprites],
                 z='Trees',
                 size_difference=size_difference)

        for obj in tmx_data.get_layer_by_name('Interactive_objects'):
            Interactive(pos=(obj.x, obj.y),
                        surf=obj.image,
                        groups=[self.all_sprites, self.interactive_sprites],
                        z='Main',
                        size_difference=size_difference,
                        name=obj.name)
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
        for obj in tmx_data.get_layer_by_name('Borders'):
            Border(pos=(round(obj.x), round(obj.y)),
                   size=(round(obj.width), round(obj.height)),
                   groups=[self.collision_sprites, self.borders],
                   size_difference=size_difference
                   )

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.player.update(dt)


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
                    self.display_surface.blit(sprite.image, offset_rect)

                    if DEBUG:
                        if hasattr(sprite, 'hitbox') and sprite.hitbox:
                            offset_rect = sprite.hitbox.copy()
                            offset_rect.center -= self.offset

                            if isinstance(sprite, Player):
                                sprite.offset = offset_rect
                                text = self.font.render(f'{player.rect.center}', True, 'green')
                                self.display_surface.blit(text, offset_rect)
                                pygame.draw.rect(self.display_surface, 'green', offset_rect, 4)
                            pygame.draw.rect(self.display_surface, 'red', offset_rect, 2)
                        # pygame.draw.rect(self.display_surface, 'red', offset_rect, 2)
