from constants import *
from player import Player


class Game:
    """Class that handles the game"""
    def __init__(self, menu, display, fever, settings, powerup):
        self.__menu = menu
        self.__display = display
        self.__fever = fever
        self.__settings = settings
        self.__powerup = powerup
        self.__intro = True

    def __play(self):
        """Creates player objects and sets up the game."""
        playing = True
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

        self.__powerup.set_players(players)
        self.__fever.set_players(players)
        self.__fever.set_powerups(self.__settings.get_mode())

        # Game loop
        while playing and not self.__fever.after_game_over:
            self.__fever.after_game_over = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        playing = False
            self.__fever.play()
            pygame.display.update()
            self.__display.clock.tick(FPS)

    def run(self):
        """Starts intro and then handles the menu and gameplay."""
        if self.__intro:
            self.__menu.game_intro()
            self.__intro = False
        self.__menu.game_menu()
        self.__play()
