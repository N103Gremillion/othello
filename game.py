import pygame;
from board import Board;
from player import Player;

grey = (128, 128, 128)
black = (0, 0, 0)
white = (255, 255, 255)

class Game:

    def __init__(self):
        self.board = Board(435, 485, grey)
        self.player1 = Player
        self.player2 = Player
    
    def startGame(self):

        running = True

        while running:

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.handleClick()
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
    
    def handleClick(self):
        pos = pygame.mouse.get_pos()
        x, y = pos
        self.board.placePieceUsingPosition(x, y)
