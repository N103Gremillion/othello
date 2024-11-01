import pygame;
from game import Game;

def main(): 
    pygame.init()
    pygame.font.init()
    game = Game()
    game.startGame()

main()