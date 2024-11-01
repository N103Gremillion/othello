import pygame;
from board import Board;
from player import Player;

grey = (128, 128, 128)
black = (0, 0, 0)
white = (255, 255, 255)

class Game:

    def __init__(self):
        self.board = Board(435, 490, grey)
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.curPlayer = self.player1
    
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
        piecePlaced = self.board.placePieceUsingPosition(x, y, self.curPlayer.playerNumber)

        if (piecePlaced == True):
            self.determinePlayerTurn()

    def determinePlayerTurn(self):
        if self.curPlayer.playerNumber == 1:
            self.curPlayer = self.player2
        else:
            self.curPlayer = self.player1
