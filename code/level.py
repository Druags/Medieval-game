import pygame
from pytmx.util_pygame import load_pygame

from settings import *
from player import Player


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.setup()
        self.player = Player()

    def setup(self):
        tmx_data = load_pygame('../data/game_map.tmx')
        first_layer = tmx_data.layers[0]

        for tile in first_layer.tiles():
            self.display_surface.blit(tile[2], (tile[0]*TILE_SIZE, tile[1]*TILE_SIZE))

    def run(self, dt):
        self.player.update(dt)

        pygame.draw.rect(self.display_surface, 'red', pygame.Rect(self.player.pos.x, self.player.pos.y, 20, 20))
