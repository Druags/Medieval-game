import pygame, sys
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('My game')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.font = pygame.font.Font(None, 32)

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick() / 1000
            self.level.run(dt)
            if DEBUG:
                fps = self.font.render(f'FPS: {int(self.clock.get_fps())}', True, 'green')
                self.screen.blit(fps, (0, 0))
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()