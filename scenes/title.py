import scene
import pygame
import settings


class Title(scene.Scene):
    def __init__(self, game):
        super().__init__(game)
        # make text of the game
        self.text_via = self.game.make_text(
            text="via",
            color=(255, 0, 255),
            fontSize=180,
            stroke=True,
            strokeColor=(255, 255, 255),
            strokeThickness=3,
        )
        self.text_galactica = self.game.make_text(
            text="GALACTICA",
            color=(100, 100, 255),
            fontSize=60,
            stroke=True,
            strokeColor=(255, 255, 255),
            strokeThickness=2,
        )

        self.text_press_enter = self.game.make_text(
            text="press enter to start",
            color=(255, 255, 255),
            fontSize=30,
            stroke=True,
            strokeColor=(255, 0, 0),
            strokeThickness=2,
        )

        # load the title_ship.png image
        self.img_ship, self.img_ship_rect = self.game.load_png("title_ship.png")

        # resize to 1/4 of the original size
        self.img_ship = pygame.transform.scale(
            self.img_ship,
            (
                int(self.img_ship_rect.width / 4),
                int(self.img_ship_rect.height / 4),
            ),
        )

        # update the rect
        self.img_ship_rect = self.img_ship.get_rect()

    def update(self):
        # if escape was pressed quit the game
        if pygame.K_ESCAPE in self.game.just_pressed:
            self.game.quit = True

    def draw(self):
        progress = self.constrain(self.elapsed() / 1, 0, 1)

        # draw the ship coming in from the top right
        self.img_ship_rect.topleft = (
            settings.RESOLUTION[0] - self.img_ship_rect.width * progress,
            -self.img_ship_rect.height + self.img_ship_rect.height * progress,
        )
        self.screen.blit(self.img_ship, self.img_ship_rect)

        self.game.blit_centered(
            source=self.text_galactica,
            target=self.screen,
            position=(0.5, progress * 0.45),
        )
        self.game.blit_centered(
            source=self.text_via, target=self.screen, position=(progress * 0.5, 0.2)
        )

        if progress >= 1:

            self.game.blit_centered(
                source=self.text_press_enter, target=self.screen, position=(0.5, 0.7)
            )
