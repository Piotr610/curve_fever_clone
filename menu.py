from constants import *


color = [BLUE, RED, GREEN, WHITE, YELLOW, VIOLET, AQUA]


def text_objects(text, font, color):
    """
    Sets up text format and returns it
    :param str text: text to format
    :param font: Font
    :param color: Color of text
    """
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def button(text, x, y, w, h, ic, ac, surface):
    """
    Creates button and returns False if clicked and True if not clicked
    :param str text: text to display on the button
    :param int x: x parameter of button's localization
    :param int y: y parameter of button's localization
    :param int w: width of the button
    :param int h: height of the button
    :param ic: inactive color of the button
    :param ac: active color of the button
    :param surface: surface for the button to be displayed on
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(surface, ac, (x, y, w, h))
        if click[0] == 1:
            return False
    else:
        pygame.draw.rect(surface, ic, (x, y, w, h))

    small_text = pygame.font.Font(None, BUTTON_FONT_SIZE)
    text_surf, text_rect = text_objects(text, small_text, BLACK)
    text_rect.center = ((x+(w/2)), (y+(h/2)))
    surface.blit(text_surf, text_rect)
    return True


def message_display(text, surface, font_size, color, localization):
    """
    Displays text on screen.
    :param str text: text to display
    :param surface: surface for the text to be displayed on
    :param font_size: font size of the text
    :param color: color of the text
    :param localization: localization of the text
    """
    large_text = pygame.font.Font(None, font_size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = localization
    surface.blit(text_surf, text_rect)


class GameMenu:
    """Class that handles game menu"""
    def __init__(self, game_display, settings):
        self.__gameDisplay = game_display
        self.__settings = settings

    def game_intro(self):
        """Game intro screen."""
        intro = True
        while intro:
            click = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or click[0] == 1 or click[2] == 1:
                    intro = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.__gameDisplay.surface.blit(self.__gameDisplay.get_background(), [0, 0])
            message_display(GAME_NAME, self.__gameDisplay.surface, INTRO_FONT_SIZE, GAME_NAME_COLOR,
                            ((self.__gameDisplay.WIDTH / 2), (self.__gameDisplay.HEIGHT / 6)))
            message_display(PRESS_KEY, self.__gameDisplay.surface, int(INTRO_FONT_SIZE/2), PRESS_KEY_COLOR,
                            ((self.__gameDisplay.WIDTH / 2), (self.__gameDisplay.HEIGHT / 1.3)))
            pygame.display.update()
            self.__gameDisplay.clock.tick(MENU_FPS)

    def game_menu(self):
        """Game menu screen with buttons handling player actions."""
        not_playing = True
        about = False
        settings = False
        quit_st = False

        while not_playing:
            if about:
                self.game_about()
            if settings:
                self.game_settings()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or quit_st:
                    pygame.quit()
                    quit()
            self.__gameDisplay.surface.blit(self.__gameDisplay.get_background(), [0, 0])
            not_playing = button(PLAY, int((DISPLAY_WIDTH / 2) - 100),
                   int(DISPLAY_HEIGHT / 8), 200, 100, GREEN, LIGHT_GREEN, self.__gameDisplay.surface)
            settings = not button(SETTINGS, ((DISPLAY_WIDTH / 2) - 100),
                   (DISPLAY_HEIGHT / 3), 200, 100, RED, LIGHT_RED, self.__gameDisplay.surface)
            about = not button(ABOUT, ((DISPLAY_WIDTH / 2) - 100),
                   (DISPLAY_HEIGHT / 2), 200, 100, BLUE, LIGHT_BLUE, self.__gameDisplay.surface)
            quit_st = not button(QUIT, ((DISPLAY_WIDTH / 2) - 100),
                   (DISPLAY_HEIGHT / 1.5), 200, 100, WHITE, GRAY, self.__gameDisplay.surface)
            pygame.display.update()
            self.__gameDisplay.clock.tick(MENU_FPS)

    def game_about(self):
        """Screen with name of author and instructions to the game."""
        about = True
        click = (0, 0, 0)
        while about:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        about = False
                if click[0] == 1 or click[2] == 1:
                    about = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                click = pygame.mouse.get_pressed()
            self.__gameDisplay.surface.fill(BLACK)
            message_display(GAME_ABOUT, self.__gameDisplay.surface, ABOUT_FONT_SIZE,
                            GAME_ABOUT_COLOR, ((DISPLAY_WIDTH/2), (DISPLAY_HEIGHT/8)))
            message_display(PLAYER_CONTROLS, self.__gameDisplay.surface, PLAYER_CONTROLS_FONT_SIZE+20,
                            AQUA, ((DISPLAY_WIDTH / 4.5), ((DISPLAY_HEIGHT / 8) + 130)))
            message_display(PLAYER0_CONTROLS, self.__gameDisplay.surface, PLAYER_CONTROLS_FONT_SIZE,
                            RED, ((DISPLAY_WIDTH / 4.5), ((DISPLAY_HEIGHT / 8)+200)))
            message_display(PLAYER1_CONTROLS, self.__gameDisplay.surface, PLAYER_CONTROLS_FONT_SIZE,
                            GREEN, ((DISPLAY_WIDTH / 4.5), ((DISPLAY_HEIGHT / 8)+250)))
            message_display(PLAYER2_CONTROLS, self.__gameDisplay.surface, PLAYER_CONTROLS_FONT_SIZE,
                            BLUE, ((DISPLAY_WIDTH / 4.5), ((DISPLAY_HEIGHT / 8)+300)))
            message_display(PLAYER3_CONTROLS, self.__gameDisplay.surface, PLAYER_CONTROLS_FONT_SIZE,
                            YELLOW, ((DISPLAY_WIDTH / 4.5), ((DISPLAY_HEIGHT / 8)+350)))
            message_display(" - Clears map", self.__gameDisplay.surface, PLAYER_CONTROLS_FONT_SIZE,
                            color[0], ((DISPLAY_WIDTH / 1.35), ((DISPLAY_HEIGHT / 8) + 150)))
            pygame.draw.circle(self.__gameDisplay.surface, color[0], (int((DISPLAY_WIDTH / 1.35)-220),
                                                                int((DISPLAY_HEIGHT / 8) + 150)), POWERUP_SIZE)
            message_display(" - Speeds up enemies", self.__gameDisplay.surface, PLAYER_CONTROLS_FONT_SIZE,
                            color[1], ((DISPLAY_WIDTH / 1.35), ((DISPLAY_HEIGHT / 8) + 200)))
            pygame.draw.circle(self.__gameDisplay.surface, color[1], (int((DISPLAY_WIDTH / 1.35) - 220),
                                                                int((DISPLAY_HEIGHT / 8) + 200)), POWERUP_SIZE)
            message_display(" - Makes enemies' turn bigger", self.__gameDisplay.surface, PLAYER_CONTROLS_FONT_SIZE,
                            color[2], ((DISPLAY_WIDTH / 1.35), ((DISPLAY_HEIGHT / 8) + 250)))
            pygame.draw.circle(self.__gameDisplay.surface, color[2], (int((DISPLAY_WIDTH / 1.35) - 220),
                                                                int((DISPLAY_HEIGHT / 8) + 250)), POWERUP_SIZE)
            message_display(" - Ghost mode", self.__gameDisplay.surface, PLAYER_CONTROLS_FONT_SIZE,
                            color[3], ((DISPLAY_WIDTH / 1.35), ((DISPLAY_HEIGHT / 8) + 300)))
            pygame.draw.circle(self.__gameDisplay.surface, color[3], (int((DISPLAY_WIDTH / 1.35) - 220),
                                                                int((DISPLAY_HEIGHT / 8) + 300)), POWERUP_SIZE)
            message_display(" - Makes enemies bigger", self.__gameDisplay.surface, PLAYER_CONTROLS_FONT_SIZE,
                            color[4], ((DISPLAY_WIDTH / 1.35), ((DISPLAY_HEIGHT / 8) + 350)))
            pygame.draw.circle(self.__gameDisplay.surface, color[4], (int((DISPLAY_WIDTH / 1.35) - 220),
                                                                int((DISPLAY_HEIGHT / 8) + 350)), POWERUP_SIZE)
            message_display(" - Reverses enemies' keys", self.__gameDisplay.surface, PLAYER_CONTROLS_FONT_SIZE,
                            color[5], ((DISPLAY_WIDTH / 1.35), ((DISPLAY_HEIGHT / 8) + 400)))
            pygame.draw.circle(self.__gameDisplay.surface, color[5], (int((DISPLAY_WIDTH / 1.35) - 220),
                                                                int((DISPLAY_HEIGHT / 8) + 400)), POWERUP_SIZE)
            message_display(" - Enemies cannot pass walls", self.__gameDisplay.surface, PLAYER_CONTROLS_FONT_SIZE,
                            color[6], ((DISPLAY_WIDTH / 1.35), ((DISPLAY_HEIGHT / 8) + 450)))
            pygame.draw.circle(self.__gameDisplay.surface, color[6], (int((DISPLAY_WIDTH / 1.35) - 220),
                                                                int((DISPLAY_HEIGHT / 8) + 450)), POWERUP_SIZE)
            pygame.display.update()
            self.__gameDisplay.clock.tick(MENU_FPS)

    def game_settings(self):
        """Screen with settings of the game."""
        settings = True

        while settings:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        settings = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.__gameDisplay.surface.fill(BLACK)

            number_clicked = not button(NUMBER_OF_PLAYERS, ((DISPLAY_WIDTH / 2) - 150),
                   (DISPLAY_HEIGHT / 8), 300, 150, GREEN, LIGHT_GREEN, self.__gameDisplay.surface)
            powerups = not button(GAME_MODE, ((DISPLAY_WIDTH / 2) - 150),
                   (DISPLAY_HEIGHT / 1.7), 300, 150, BLUE, LIGHT_BLUE, self.__gameDisplay.surface)

            if number_clicked:
                if self.__settings.get_number() == 4:
                    self.__settings.set_number(2)
                else:
                    self.__settings.set_number(self.__settings.get_number() + 1)
            if powerups:
                self.__settings.set_mode(not self.__settings.get_mode())

            message_display(str(self.__settings.get_number()), self.__gameDisplay.surface, int(NUMBER_FONT_SIZE / 2), GREEN,
                            ((self.__gameDisplay.WIDTH / 1.3), ((self.__gameDisplay.HEIGHT / 8) + 75)))
            message_display(str(self.__settings.get_mode()), self.__gameDisplay.surface, int(NUMBER_FONT_SIZE / 2), GREEN,
                            ((self.__gameDisplay.WIDTH / 1.3), ((self.__gameDisplay.HEIGHT / 1.7) + 75)))

            pygame.display.update()
            self.__gameDisplay.clock.tick(13)
