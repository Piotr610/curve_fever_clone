from display import Display
from fever import Fever
from game import Game
from menu import GameMenu
from settings import Settings

import pygame

# Set up
myDisplay = Display()
mySettings = Settings()
myMenu = GameMenu(myDisplay, mySettings)
# myPowerup = PowerUp(myDisplay.surface)
myFever = Fever(myDisplay.surface, myDisplay, mySettings)
# myPowerup.set_track(myFever.track)
myGame = Game(myMenu, myDisplay, myFever, mySettings)
running = True

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    myGame.run()

# Quit the game
pygame.quit()
quit()
