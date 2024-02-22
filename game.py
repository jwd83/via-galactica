import os
import pygame
import settings
from scene import Scene
import scenes


class Game:
    def __init__(self):
        # set the quit flag to false at the start
        self.quit = False
        self.pressed = []
        self.just_pressed = []
        self.__sfx = {}
        self.volume_music = 100
        self.volume_effects = 100
        self.winner = None

        # initialize pygame
        pygame.init()
        pygame.mixer.init()

        # load our sound effects
        # for sound in settings.SFX_LIST:
        #     self.__sfx[sound] = pygame.mixer.Sound("assets/" + sound)

        # load all sounds in assets/sounds as sound effects
        for sound in os.listdir("assets/sounds"):
            load_sound = False
            if (
                sound.endswith(".wav")
                or sound.endswith(".ogg")
                or sound.endswith(".mp3")
            ):
                load_sound = True

            if load_sound:
                sound_name = sound.split(".")[0]
                self.__sfx[sound_name] = pygame.mixer.Sound("assets/sounds/" + sound)

        # create a window
        self.screen = pygame.display.set_mode(
            settings.RESOLUTION, pygame.FULLSCREEN | pygame.SCALED
        )
        pygame.display.set_caption(settings.TITLE)

        # create a pygame clock to limit the game to 60 fps
        self.clock = pygame.time.Clock()

        # create a stack for scenes to be updated and drawn
        # and add the title scene to the stack
        self.scene = []  # type: list[Scene]
        self.scenes = settings.SCENE_LIST
        self.scene.append(self.load_scene(settings.SCENE_START))

        # create variables to handle scene changes
        self.scene_replace = None
        self.scene_push = None
        self.scene_pop = None

    def run(self):
        self.debug_scene = scenes.Debug(self)

        while not self.quit:
            # handle events and input
            self.get_events_and_input()

            # set all scenes to inactive except the top scene in the stack
            for scene in self.scene:
                scene.active = False
            self.scene[-1].active = True

            # process update for the top scene in the stack
            self.scene[-1].update()

            # draw all scenes in the stack from bottom to top
            for scene in self.scene:
                scene.draw()

            # draw the debug panel
            if settings.DEBUG:
                self.debug_scene.update()
                self.debug_scene.draw()

            # update the display
            pygame.display.flip()

            # process scene change requests (if any)
            self.change_scenes()

            # limit the game to 60 fps
            self.clock.tick(settings.FPS)

    def get_events_and_input(self):
        # get input
        self.pressed = pygame.key.get_pressed()
        self.just_pressed = []

        # get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN:
                self.just_pressed.append(event.key)

        # check for escape key to quit
        if pygame.K_ESCAPE in self.just_pressed:
            self.scene_pop = True
            # self.quit = True

        # check for F11 to toggle the debug setting
        if pygame.K_F11 in self.just_pressed:
            settings.DEBUG = not settings.DEBUG

    def change_scenes(self):
        # check for scene changes
        if self.scene_replace is not None:
            if self.scene_replace in self.scenes:
                self.scene = []
                self.scene.append(self.load_scene(self.scene_replace))
            self.scene_replace = None

        elif self.scene_push is not None:
            if self.scene_push in self.scenes:
                self.scene.append(self.load_scene(self.scene_push))
            self.scene_push = None

        elif self.scene_pop is not None:
            if len(self.scene) > 1:
                # if scene pop was given an integer, pop that many scenes
                # otherwise, pop only one scene
                if isinstance(self.scene_pop, int):
                    for _ in range(self.scene_pop):
                        self.scene.pop()
                else:
                    self.scene.pop()
            else:
                print("WARNING: Cannot pop last scene! Exiting!")
                self.quit = True
            self.scene_pop = None

    def load_scene(self, scene: str):
        print("load_scene: " + scene)
        if scene in self.scenes:
            # use an eval to return the scene based on the scene string
            return eval("scenes." + scene + "(self)")
        else:
            return scenes.Title(self)

    # from the pygame tutorial:
    # https://www.pygame.org/docs/tut/tom_games3.html
    def load_png(self, name):
        """Load image and return image object"""
        fullname = os.path.join("assets/images", name)
        try:
            image = pygame.image.load(fullname)
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except FileNotFoundError:
            print(f"Cannot load image: {fullname}")
            raise SystemExit
        return image, image.get_rect()

    def make_text(
        self,
        text,
        color,
        fontSize,
        font=None,
        stroke=False,
        strokeColor=(0, 0, 0),
        strokeThickness=1,
    ):
        if font is None:
            font = "assets/fonts/" + settings.FONT

        # if we aren't stroking return the text directly
        if not stroke:
            return pygame.font.Font(font, fontSize).render(text, 1, color)

        # if we are stroking, render the text with the stroke
        # first render the text without the stroke

        # create a version of the text in the stroke color and blit it to the surface
        surf_text = pygame.font.Font(font, fontSize).render(text, 1, color)
        surf_text_stroke = pygame.font.Font(font, fontSize).render(text, 1, strokeColor)

        # create a transparent surface to draw the text and stroke on
        size = (
            surf_text.get_width() + strokeThickness * 3,
            surf_text.get_height() + strokeThickness * 3,
        )
        surface = self.make_transparent_surface(size)

        # blit the stroke text to the surface
        for i in range(strokeThickness * 2 + 1):
            for j in range(strokeThickness * 2 + 1):
                surface.blit(surf_text_stroke, (i, j))

        # blit the text on top of the stroke
        surface.blit(surf_text, (strokeThickness, strokeThickness))

        # return the surface
        return surface

    def make_transparent_surface(self, size):
        return pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()

    def blit_centered(self, source, target, position=(0.5, 0.5)):
        """
        This function places a given surface at a specified position on the target surface.

        Parameters:
        source (pygame.Surface): The source surface to be placed. This is a pygame Surface object, which can be
        created using pygame.font.Font.render() method.

        target (pygame.Surface): The target surface on which the surface is to be placed. This could be
        the game screen or any other surface.

        position (tuple): A tuple of two values between 0 and 1, representing the relative position
        on the target surface where the surface should be placed. The values correspond to the horizontal
        and vertical position respectively. For example, a position of (0.5, 0.5) will place the text dead
        center on the target surface.


        """
        source_position = source.get_rect()
        source_position.centerx = target.get_rect().centerx * position[0] * 2
        source_position.centery = target.get_rect().centery * position[1] * 2
        target.blit(source, source_position)

    def play_sound(self, sound):
        # set the volume of the sound based on the settings
        self.__sfx[sound].set_volume(self.volume_effects / 100)

        pygame.mixer.Sound.play(self.__sfx[sound])
