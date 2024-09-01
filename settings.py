class Settings:
    """Class that handles settings"""

    def __init__(self):
        self.__number_of_players = 2
        self.__game_mode = True

    def get_number(self):
        """Returns number of players."""
        return self.__number_of_players

    def set_number(self, number):
        """
        Sets number of players.
        :param int number: number of players
        """
        self.__number_of_players = number

    def get_mode(self):
        """Returns set game mode."""
        return self.__game_mode

    def set_mode(self, mode):
        """
        Sets game mode.
        :param bool mode: True if enabled powerups, False otherwise
        """
        self.__game_mode = mode
