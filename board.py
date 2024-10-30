import pygame;

class Board: 

    def __init__(self, boardWidth, boardHeight, color):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.screen = pygame.display.set_mode ([boardWidth, boardHeight])
        pygame.display.flip()