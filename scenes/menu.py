import pygame
import settings
from scene import Scene


class Menu(Scene):
    def __init__(self, game):
        super().__init__(game)

        # make text for the options menu
        self.text_options = self.make_text(
            text="options",
            color=(255, 255, 255),
            fontSize=30,
            stroke=True,
            strokeColor=(255, 100, 100),
            strokeThickness=2,
        )

        self.text_quit = self.make_text(
            text="quit",
            color=(200, 200, 200),
            fontSize=30,
            stroke=True,
            strokeColor=(255, 100, 200),
            strokeThickness=2,
        )

    def update(self):
        if pygame.K_ESCAPE in self.game.just_pressed:
            self.game.quit = True

    def draw(self):
        # draw a circle in the middle of the screen
        self.blit_centered(self.text_options, self.screen, (0.5, 0.1))
        self.blit_centered(self.text_quit, self.screen, (0.5, 0.8))
