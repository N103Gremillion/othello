import pygame
from game import Game
from menu import Menu

# entry point
def main(): 
    pygame.init()
    pygame.font.init()
    game = Game()
    game.startGame()
main()