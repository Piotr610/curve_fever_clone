import random

from constants import *
from entity import Entity

color = [BLUE, RED, GREEN, WHITE, YELLOW, VIOLET, AQUA]


class PowerUp(Entity):
    def __init__(self, surface):
        self.point = (random.randint(50, (DISPLAY_WIDTH-50)), random.randint(50, (DISPLAY_HEIGHT-50)))
        self.type = random.randint(0, 6)
        self.surface = surface
        self.color = color[self.type]
        self.__track = None
        self.players = None

    def do_sth(self, p):
        """
        Does something after being 'taken'.
        :param Player p: player who has 'taken' the powerup
        """
        if self.type == 0:
            self.__track.fill(BLACK)

        elif self.type == 1:
            for player in self.players:
                if player is not p:
                    player.set_speed((player.get_speed() + 5))

        elif self.type == 2:
            for player in self.players:
                if player is not p:
                    player.set_turn((player.get_turn() / 1.8))

        elif self.type == 3:
            p.ghost = True
            for player in self.players:
                if player is not p:
                    player.ghost = False

        elif self.type == 4:
            for player in self.players:
                if player is not p:
                    if player.size < 15:
                        player.size *= 1.7

        elif self.type == 5:
            if p.keys_reversed:
                p.keys.reverse()
                p.keys_reversed = False
            for player in self.players:
                if player is not p:
                    player.keys.reverse()
                    player.keys_reversed = not player.keys_reversed

        elif self.type == 6:
            for player in self.players:
                if player is not p:
                    player.wall = False

    def set_track(self, track):
        """
        Sets 'track' surface.
        :param track: surface with track drawn on it
        """
        self.__track = track

    def set_players(self, players):
        """
        Sets players.
        :param list players: list of players
        """
        self.players = players

    def __generate_type_and_color(self):
        """Generates powerup's type and color"""
        self.type = random.randint(0, 6)
        self.color = color[self.type]

    def reset(self):
        """Resets powerup"""
        self.__generate_type_and_color()
        self.point = (random.randint(50, (DISPLAY_WIDTH - 50)), random.randint(50, (DISPLAY_HEIGHT - 50)))

    def draw(self):
        """Draws powerup"""
        pygame.draw.circle(self.surface, self.color, self.point, POWERUP_SIZE)
