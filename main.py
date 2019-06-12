from constants import *
from display import Display
from fever import Fever
from game import Game
from menu import GameMenu
from powerUp import PowerUp
from settings import Settings

# Set up
myDisplay = Display()
mySettings = Settings()
myMenu = GameMenu(myDisplay, mySettings)
myPowerup = PowerUp(myDisplay.surface)
myFever = Fever(myDisplay.surface, myPowerup, myDisplay)
myPowerup.set_track(myFever.track)
myGame = Game(myMenu, myDisplay, myFever, mySettings, myPowerup)
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


