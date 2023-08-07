import pygame
from pytmx.util_pygame import load_pygame

from settings import *
from player import Player
from sprites import Generic, Tree


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()

        self.player = Player((200, 200), self.all_sprites)
        self.setup()

    def setup(self):
        tmx_data = load_pygame('../data/game_map.tmx')

        # first_layer = tmx_data.layers[0]
        # for tile in first_layer.tiles():
        #     self.display_surface.blit(tile[2], (tile[0] * TILE_SIZE, tile[1] * TILE_SIZE))
        Generic(
            pos=(0, 0),
            surf=pygame.image.load('../data/game_map.png'),
            groups=self.all_sprites,
            z='Ground'
        )
        self.all_sprites.world_size = self.all_sprites.sprites()[1].image.get_size()
        world_width = self.all_sprites.world_size[0]
        world_height = self.all_sprites.world_size[1]

        size_difference = (world_width//(tmx_data.width*TILE_SIZE), world_height//(tmx_data.height*TILE_SIZE))

        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(pos=(obj.x, obj.y),
                 surf=obj.image,
                 groups=self.all_sprites,
                 z='Main',
                 size_difference=size_difference)

    def run(self, dt):
        self.display_surface.fill('black')
        self.player.update(dt)
        self.all_sprites.custom_draw(self.player)


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
        offset_text = self.font.render(f'{self.offset}', True, 'green')
        self.display_surface.blit(offset_text, (10, 10))
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset

                    self.display_surface.blit(sprite.image, offset_rect)
                    if DEBUG:
                        # if sprite.z == 'Ground':
                        #     offset_text = self.font.render(f'{offset_rect.center}', True, 'green')
                        #     self.display_surface.blit(offset_text, (10, 10))
                        if isinstance(sprite, Player):
                            text = self.font.render(f'{player.rect.center}', True, 'green')
                            self.display_surface.blit(text, offset_rect)
                        pygame.draw.rect(self.display_surface, 'red', offset_rect, 2)
