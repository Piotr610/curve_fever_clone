class Settings:
    def __init__(self):
        self.__number_of_players = 2
        self.__game_mode = True

    def get_number(self):
        return self.__number_of_players

    def set_number(self, number):
        self.__number_of_players = number

    def get_mode(self):
        return self.__game_mode

    def set_mode(self, mode):
        self.__game_mode = mode
