import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z='Main'):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS[z]


class Tree(Generic):
    def __init__(self, pos, surf, groups, z, size_difference):
        
        size = surf.get_size()
        surf = pygame.transform.scale(surf, (size[0]*size_difference[0], size[1]*size_difference[1]))
        pos = [pos[i]*size_difference[i] for i in range(2)]
        super().__init__(pos, surf, groups)
