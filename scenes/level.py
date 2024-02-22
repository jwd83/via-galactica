import pygame
import settings
from scene import Scene


class Level(Scene):
    def __init__(self, game):
        super().__init__(game)

    def update(self):
        pass

    def draw(self):
        # draw a circle in the middle of the screen
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            (settings.RESOLUTION[0] // 2, settings.RESOLUTION[1] // 2),
            50,
        )
