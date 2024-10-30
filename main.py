import pygame;
from board import Board;

def setUpGame():
    color = (255, 255, 255)
    board = Board(400, 400, color)

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

def main(): 
    setUpGame()

main()