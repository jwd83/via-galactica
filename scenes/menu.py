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
            fontSize=40,
            stroke=True,
            strokeColor=(0, 0, 0),
            strokeThickness=2,
        )

        self.text_quit = self.make_text(
            text="quit",
            color=(200, 200, 200),
            fontSize=40,
            stroke=True,
            strokeColor=(0, 0, 0),
            strokeThickness=2,
        )

        self.img_cursor, _ = self.load_png("cursor-4x7.png")

        self.play_sound("click")

    def update(self):
        if pygame.K_ESCAPE in self.game.just_pressed:
            self.game.quit = True

    def draw(self):
        self.draw_box(
            (100, 50), (settings.RESOLUTION[0] - 200, settings.RESOLUTION[1] - 100)
        )
        if self.elapsed() > self.box_delay:

            self.blit_centered(self.text_options, self.screen, (0.5, 0.2))
            self.blit_centered(self.text_quit, self.screen, (0.5, 0.8))
            self.screen.blit(self.img_cursor, (0, 0))
