import pygame;
from board import Board;

def setUpGame():
    grey = (128, 128, 128)
    black = (0, 0, 0)
    white = (255, 255, 255)
    board = Board(435, 435, grey)

    running = True

    board.placePiece(7, 7, "black")

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()

def main(): 
    pygame.init()
    setUpGame()

main()