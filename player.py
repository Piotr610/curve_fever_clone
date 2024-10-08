import asyncio
import math
import random
from threading import Thread

import pygame

from constants import (
    BLACK,
    CIRCLE_SIZE,
    DEFAULT_SPEED,
    DEFAULT_TURN,
    DISPLAY_HEIGHT,
    DISPLAY_WIDTH,
    POWERUP_COOLDOWN,
    POWERUP_SIZE,
)
from entity import Entity


class Player(Entity):
    """Class that handles players"""

    def __init__(self, color, surface, keys):
        self.__color = color
        self.pos_new = list(
            (
                random.randint(50, (DISPLAY_WIDTH - 100)),
                random.randint(50, (DISPLAY_HEIGHT - 100)),
            )
        )
        self.pos_old = self.pos_new[:]
        self.speed = DEFAULT_SPEED
        self.__angle = random.randint(0, 359)
        self.__track = None
        self.surface = surface
        self.game_over = False
        self.keys = keys
        self.__turn = DEFAULT_TURN
        self.ghost = False
        self.size = CIRCLE_SIZE
        self.keys_reversed = False
        self.wall = True
        self.gap = False

    def get_color(self):
        """Returns color of the player."""
        return self.__color

    def set_track(self, track):
        """
        Sets 'track' surface.
        :param track: surface with track drawn on it
        """
        self.__track = track

    def set_speed(self, speed):
        """Sets speed for the player."""
        self.speed = speed

    def get_speed(self):
        """Returns speed of the player."""
        return self.speed

    def set_turn(self, turn):
        """Sets turn which the player is able to do."""
        self.__turn = turn

    def get_turn(self):
        """Returns turn which the player is able to do."""
        return self.__turn

    async def make_gaps(self):
        self.gap = True
        await asyncio.sleep(0.2)
        self.gap = False

    def handle_gaps(self):
        asyncio.run(self.make_gaps())

    def draw(self):
        """Draws a track of the player, drawing a line between its old and new position."""
        if self.pos_new != self.pos_old and not self.ghost and not self.gap:
            pygame.draw.line(
                self.__track,
                self.__color,
                self.pos_new,
                self.pos_old,
                int(self.size * 2.2),
            )
        self.pos_old = self.pos_new[:]

        if not random.randint(0, 30):
            Thread(target=self.handle_gaps).start()

        self.surface.blit(self.__track, (0, 0))

    def __collision(self, sum_dx, sum_dy, powerups):
        """Handles collisions and checks if the player has lost."""
        if (
            0 <= (self.pos_new[0] + int(sum_dx)) < DISPLAY_WIDTH
            and 0 <= (self.pos_new[1] + int(sum_dy)) < DISPLAY_HEIGHT
        ):
            color = self.__track.get_at(
                (self.pos_new[0] + int(sum_dx), self.pos_new[1] + int(sum_dy))
            )

            if color != BLACK and not self.ghost and not self.gap:
                print("sum_dx,sum_dy:", int(sum_dx), int(sum_dy))
                self.speed = 0
                self.game_over = True
            for powerup in powerups:
                if abs(powerup.point[0] - self.pos_new[0] - int(sum_dx)) < (
                    POWERUP_SIZE + self.size
                ) and abs(powerup.point[1] - self.pos_new[1] - int(sum_dy)) < (
                    POWERUP_SIZE + self.size
                ):
                    Thread(
                        target=powerup.do_sth,
                        args=(self, POWERUP_COOLDOWN, powerup.type),
                    ).start()
                    powerup.reset()

        elif (
            0 > (self.pos_new[0] + int(sum_dx))
            or (self.pos_new[0] + int(sum_dx)) >= DISPLAY_WIDTH
        ) and self.wall:
            self.pos_new[0] -= DISPLAY_WIDTH
            self.pos_new[0] = abs(self.pos_new[0])
            self.pos_old = self.pos_new

        elif (
            0 > (self.pos_new[1] + int(sum_dy))
            or (self.pos_new[1] + int(sum_dy)) >= DISPLAY_HEIGHT
        ) and self.wall:
            self.pos_new[1] -= DISPLAY_HEIGHT
            self.pos_new[1] = abs(self.pos_new[1])
            self.pos_old = self.pos_new
        else:
            self.speed = 0
            self.game_over = True

        return self.game_over

    def steer(self, powerup):
        """
        Handles steering over the player and calculates movement.
        :param powerup: powerup to check if it was 'taken' by the player
        """

        keys = pygame.key.get_pressed()

        if keys[self.keys[0]]:
            self.__angle -= self.__turn
        if keys[self.keys[1]]:
            self.__angle += self.__turn

        if self.__angle >= 360:
            self.__angle -= 360
        elif self.__angle < 0:
            self.__angle += 360

        move_x = self.speed * (math.cos(math.radians(self.__angle)))
        move_y = self.speed * (math.sin(math.radians(self.__angle)))

        max_xy = max((abs(move_x), abs(move_y)))

        dx = move_x / max_xy
        dy = move_y / max_xy

        sum_dx = dx
        sum_dy = dy

        for _ in range(int(max_xy) - 1):
            sum_dx += dx
            sum_dy += dy

        self.game_over = self.__collision(sum_dx, sum_dy, powerup)

        self.pos_new[0] += int(move_x)
        self.pos_new[1] += int(move_y)

        return self.game_over

    def reset(self):
        """Resets players properties."""
        self.speed = DEFAULT_SPEED
        self.wall = True
        if self.keys_reversed:
            self.keys.reverse()
            self.keys_reversed = False
        self.ghost = False
        self.gap = False
        self.size = CIRCLE_SIZE
        self.__turn = DEFAULT_TURN
        self.__angle = random.randint(0, 359)
        self.pos_new = list(
            (
                random.randint(50, (DISPLAY_WIDTH - 100)),
                random.randint(50, (DISPLAY_HEIGHT - 100)),
            )
        )
        self.pos_old = self.pos_new[:]
        self.game_over = False
