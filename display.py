import pygame
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, GAME_NAME, BACKGROUND


# Display Window
class Display:
    """Class that handles display"""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        self.WIDTH = DISPLAY_WIDTH
        self.HEIGHT = DISPLAY_HEIGHT
        self.surface = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.clock = pygame.time.Clock()
        self.__background = pygame.image.load(BACKGROUND)
        self.__background = pygame.transform.scale(
            self.__background, [DISPLAY_WIDTH, DISPLAY_HEIGHT]
        )

    def get_background(self):
        """Returns background."""
        return self.__background
