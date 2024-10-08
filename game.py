from threading import Thread

import pygame

from constants import (
    BLACK,
    BLUE,
    FPS,
    GREEN,
    PLAYER0_KEYS,
    PLAYER1_KEYS,
    PLAYER2_KEYS,
    PLAYER3_KEYS,
    RED,
    YELLOW,
)
from player import Player
from powerUp import PowerUp

stop_threads = False


class Game:
    """Class that handles game"""

    def __init__(self, menu, display, fever, settings):
        self.__menu = menu
        self.__display = display
        self.__fever = fever
        self.__settings = settings
        self.__powerup = [PowerUp(self.__display.surface)]
        self.__intro = True
        self.__fever.powerup = self.__powerup

    def __play(self):
        """Creates player objects and sets up game."""
        playing = True
        global stop_threads
        stop_threads = False
        self.__fever.after_game_over = False
        self.__display.surface.fill(BLACK)

        player0 = Player(RED, self.__display.surface, PLAYER0_KEYS)
        player1 = Player(GREEN, self.__display.surface, PLAYER1_KEYS)
        player2 = Player(BLUE, self.__display.surface, PLAYER2_KEYS)
        player3 = Player(YELLOW, self.__display.surface, PLAYER3_KEYS)

        if self.__settings.get_number() == 3:
            players = [player0, player1, player2]
        elif self.__settings.get_number() == 4:
            players = [player0, player1, player2, player3]
        else:
            players = [player0, player1]

        if not self.__settings.get_mode():
            self.__powerup.clear()

        for powerup in self.__powerup:
            powerup.set_players(players)
            powerup.set_track(self.__fever.track)
        self.__fever.set_players(players)
        # self.__fever.set_powerups(self.__settings.get_mode())

        if self.__settings.get_mode():
            Thread(target=self.__fever.spawn_powerup).start()

        # Game loop
        while playing and not self.__fever.after_game_over:
            self.__fever.after_game_over = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_threads = True
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        playing = False

            self.__fever.play()
            pygame.display.update()
            self.__display.clock.tick(FPS)

        stop_threads = True

    def run(self):
        """Starts intro and then handles menu and gameplay."""
        if self.__intro:
            self.__menu.game_intro()
            self.__intro = False
        self.__menu.game_menu()
        self.__play()
