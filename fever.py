import asyncio

import pygame

import game
from constants import (
    ABOUT_FONT_SIZE,
    BLACK,
    BLUE,
    DISPLAY_HEIGHT,
    DISPLAY_WIDTH,
    GREEN,
    MENU_FPS,
    RED,
    YELLOW,
)
from menu import text_objects
from powerUp import PowerUp


def message_display(text, surface, font_size, color):
    """
    Displays text in the middle of the screen
    :param str text: text to display
    :param surface: surface for the text to be displayed on
    :param font_size: font size of the text
    :param color: color of the text
    """
    large_text = pygame.font.Font(None, font_size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))
    surface.blit(text_surf, text_rect)


class Fever:
    """Class that handles gameplay"""

    def __init__(self, surface, display, settings):
        self.__surface = surface
        self.track = pygame.Surface(self.__surface.get_size())
        self.__game_over_values = list((False, False, False, False))
        self.powerup = None
        self.players = None
        self.after_game_over = False
        self.game_over_screen = True
        self.display = display
        self.settings = settings
        # self.__powerup_active = True

    def set_players(self, players):
        """
        Sets players and sets "track" surface for them.
        :param list players: list of players
        """
        self.players = players
        for player in self.players:
            player.set_track(self.track)

    def __game_over(self):
        """Handles game over event and displays who's the winner."""
        self.game_over_screen = True
        click = (0, 0, 0)
        if len(self.players) == 2:
            self.__game_over_values[2] = True
            self.__game_over_values[3] = True
        elif len(self.players) == 3:
            self.__game_over_values[3] = True
        if (
            self.__game_over_values[0]
            and self.__game_over_values[1]
            and self.__game_over_values[2]
            or self.__game_over_values[0]
            and self.__game_over_values[2]
            and self.__game_over_values[3]
            or self.__game_over_values[1]
            and self.__game_over_values[2]
            and self.__game_over_values[3]
            or self.__game_over_values[0]
            and self.__game_over_values[1]
            and self.__game_over_values[3]
        ):
            while self.game_over_screen:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.game_over_screen = False
                    if click[0] == 1 or click[2] == 1:
                        self.game_over_screen = False
                    if event.type == pygame.QUIT:
                        game.stop_threads = True
                        pygame.quit()
                        quit()

                if len(self.players) == 2:
                    if self.__game_over_values[1]:
                        message_display(
                            "Player red won", self.__surface, ABOUT_FONT_SIZE, RED
                        )
                    elif self.__game_over_values[0]:
                        message_display(
                            "Player green won", self.__surface, ABOUT_FONT_SIZE, GREEN
                        )

                elif len(self.players) == 3:
                    if self.__game_over_values[0] and self.__game_over_values[1]:
                        message_display(
                            "Player blue won", self.__surface, ABOUT_FONT_SIZE, BLUE
                        )
                    elif self.__game_over_values[0] and self.__game_over_values[2]:
                        message_display(
                            "Player green won", self.__surface, ABOUT_FONT_SIZE, GREEN
                        )
                    elif self.__game_over_values[1] and self.__game_over_values[2]:
                        message_display(
                            "Player red won", self.__surface, ABOUT_FONT_SIZE, RED
                        )

                elif len(self.players) == 4:
                    if (
                        self.__game_over_values[0]
                        and self.__game_over_values[1]
                        and self.__game_over_values[3]
                    ):
                        message_display(
                            "Player blue won", self.__surface, ABOUT_FONT_SIZE, BLUE
                        )
                    elif (
                        self.__game_over_values[0]
                        and self.__game_over_values[2]
                        and self.__game_over_values[3]
                    ):
                        message_display(
                            "Player green won", self.__surface, ABOUT_FONT_SIZE, GREEN
                        )
                    elif (
                        self.__game_over_values[1]
                        and self.__game_over_values[2]
                        and self.__game_over_values[3]
                    ):
                        message_display(
                            "Player red won", self.__surface, ABOUT_FONT_SIZE, RED
                        )
                    elif (
                        self.__game_over_values[0]
                        and self.__game_over_values[1]
                        and self.__game_over_values[2]
                    ):
                        message_display(
                            "Player yellow won", self.__surface, ABOUT_FONT_SIZE, YELLOW
                        )

                click = pygame.mouse.get_pressed()
                pygame.display.update()
                self.display.clock.tick(MENU_FPS)

            for player in self.players:
                player.reset()

            self.__game_over_values = list((False, False, False, False))
            self.track.fill(BLACK)
            self.powerup.clear()
            self.after_game_over = True

    def spawn_powerup(self):
        asyncio.run(self.spawn_powerup_async())

    async def spawn_powerup_async(self):
        while not game.stop_threads and self.settings.get_mode():
            await asyncio.sleep(8)
            powerup = PowerUp(self.__surface)
            powerup.set_players(self.players)
            powerup.set_track(self.track)
            self.powerup.append(powerup)

    def play(self):
        """Handles gameplay."""
        i = 0

        for player in self.players:
            if not self.__game_over_values[i]:
                self.__game_over_values[i] = player.steer(self.powerup)
            i += 1

        if (
            self.__game_over_values[0]
            or self.__game_over_values[1]
            or self.__game_over_values[2]
            or self.__game_over_values[3]
        ):
            self.__game_over()

        for player in self.players:
            player.draw()

        for player in self.players:
            pygame.draw.circle(
                player.surface, player.get_color(), player.pos_new, int(player.size)
            )

        for powerup in self.powerup:
            powerup.draw()
