import pygame
from button import Button

blue = (0, 0, 125)
grey = (128, 128, 128)

class Menu:

    def __init__(self, menuWidth, menuHeight):
        pygame.display.set_mode ([menuWidth, menuHeight])
        self.menuWidth = menuWidth
        self.menuHeight = menuHeight
        self.screen = pygame.display.get_surface()
        self.PlayerVsPlayerButton = Button("P vs P", 125, 50, 200, 50, grey)
        self.PlayerVsAiButton = Button("P vs A", 125, 150, 200, 50, grey)
        self.AiVsAiButton = Button("A vs A", 125, 250, 200, 50, grey)
        self.ExitButton = Button("Exit", 125, 350, 200, 50, grey)
        self.drawMenu()
    
    def drawMenu(self):
        self.screen.fill(blue)

        # draw buttons
        self.PlayerVsPlayerButton.drawButton(self.screen)
        self.PlayerVsAiButton.drawButton(self.screen)
        self.AiVsAiButton.drawButton(self.screen)
        self.ExitButton.drawButton(self.screen)

