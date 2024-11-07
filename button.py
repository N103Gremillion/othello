import pygame

black = (0, 0, 0)

class Button:

    def __init__(self, text, x, y, width, height, color):
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text = self.font.render(text, False, black)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def drawButton(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, (self.x + (self.width / 3), self.y + (self.height / 4)))
        pygame.display.update()
