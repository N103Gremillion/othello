import math
import pygame;

"""
Note: for this class a 0 on the grid is white & 1 is black and a -1 is (empty)
"""

black = (0, 0, 0)
white = (255, 255, 255)

class Board: 

    # maps indexes to circle (pieces) postions on the board
    positionMapForPieces = {}
    # maps indexes to rect positions the value is (topLeft(x, y), bottomRight(x, y)) uses tuple of tuples as value ((x, y), (x, y))
    positionMapForHighlighting = {}

    def __init__(self, boardWidth, boardHeight, color):

        pygame.display.set_mode ([boardWidth, boardHeight])

        # setup of game display and grid
        self.setupMaps()
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.screen = pygame.display.get_surface()
        self.grid = []
        self.playerScoreFont = pygame.font.SysFont('Comic Sans MS', 30)
        self.currentTurnFont = pygame.font.SysFont('Comit Sans MS', 45)
        self.player1text = self.playerScoreFont.render("Player 1: 0", False, black)
        self.player2text = self.playerScoreFont.render("Player 2: 0", False, white)
        self.currentTurnText = self.currentTurnFont.render("Player 1's Turn", False, black)
        self.drawBoard(color)
        self.initalizeGrid()
        self.drawStartingPieces()

        pygame.display.flip()

    def drawBoard(self, color):
        
        # setup inital values for lines
        dividerLinePos = pygame.Vector2(0, 50)
        horizontalLinePos = pygame.Vector2(0, 105)
        verticalLinePos = pygame.Vector2(50, 50)

        # setup temporary constants
        horizontalLineWidth = 435
        horizontalLineHeight = 5
        verticalLineWidth = 5
        verticalLineHeight = 435

        # draw divider line that divides header from board
        self.screen.fill(color)
        dividerLine = pygame.Rect(dividerLinePos.x, dividerLinePos.y, horizontalLineWidth, horizontalLineHeight)
        pygame.draw.rect(self.screen, black, dividerLine)
        pygame.display.update()

        # draw player scores
        self.screen.blit(self.player1text, (0, 0))
        self.screen.blit(self.player2text, (0, 25))
        self.screen.blit(self.currentTurnText, (160, 10))

        # loop over and draw the initial vertical and horizontal lines on the board
        for i in range(7):

            horizontalX = horizontalLinePos.x
            horizontalY = horizontalLinePos.y
            verticalX = verticalLinePos.x
            verticalY = verticalLinePos.y

            curHorizontalLine = pygame.Rect(horizontalX, horizontalY, horizontalLineWidth, horizontalLineHeight)
            curVerticalLine = pygame.Rect(verticalX, verticalY, verticalLineWidth, verticalLineHeight)
            pygame.draw.rect(self.screen, black, curHorizontalLine)
            pygame.draw.rect(self.screen, black, curVerticalLine)
            pygame.display.update()

            # update line positions
            horizontalLinePos.y += 55
            verticalLinePos.x += 55

    def drawStartingPieces(self):
        self.drawPiece(4, 4, "black")
        self.drawPiece(4, 5, "white")
        self.drawPiece(5, 4, "white")
        self.drawPiece(5, 5, "black")

    def initalizeGrid(self):
        # initalize as -1 to represent null
        for i in range(64):
            row = []
            for j in range(64):
                row.append(-1)
            self.grid.append(row)

    def drawPiece(self, xIndex, yIndex, colorString):
        # Error checking
        if (xIndex < 1 or xIndex > 8 or yIndex < 1 or yIndex > 8):
            print("You idiot these are out of bounds!!!")
        
        # add the circle
        if (self.grid[xIndex][yIndex] != -1):
            return
        
        # add either 0 "for white" or 1 "for black"
        white = (255, 255, 255)
        black = (0, 0, 0)
        radius = 25
        position = self.positionMapForPieces[xIndex, yIndex]

        if (colorString.lower() == "white"):
            self.grid[xIndex][yIndex] = 0
            pygame.draw.circle(self.screen, white, position, radius)
            pygame.display.flip()
        elif (colorString.lower() == "black"):
            self.grid[xIndex][yIndex] = 1
            pygame.draw.circle(self.screen, black, position, radius)
            pygame.display.flip()
        else:
            print("Not a valid color dummy!!")

    def updateScoreText(self, player, score):
        
        if player.lower() == "player1":
            self.player1text = self.playerScoreFont.render(f"Player 1: {score}", False, black)
            self.screen.blit(self.player1text, (0, 0))
        elif player.lower() == "player2":
            self.player2text = self.playerScoreFont.render(f"Player 2: {score}", False, white)
            self.screen.blit(self.player2text, (0, 25))
        
        pygame.display.update()
        
    def updateCurrentTurnText(self, player):

        if player.lower() == "player1":
            self.currentTurnText = self.currentTurnFont.render(f"Player 1's Turn", False, black)
            self.screen.blit(self.currentTurnFont, (160, 10))
        elif player.lower() == "player2":
            self.currentTurnText = self.currentTurnFont.render(f"Player 2's Turn", False, white)
            self.screen.blit(self.currentTurnFont, (160, 10))
        
        pygame.display.update()

    def setupMaps(self):
        # map indeces in the board to the corresponding positions

        curXPosition = 25
        curYPosition = 80 
        
        # loop over and fill the map
        for i in range(8):
            for (j) in range(8):
                # these represent the bounds of the square at that location on the board
                topLeft = (curXPosition - 25, curYPosition - 25)
                bottomRight = (curXPosition + 25, curYPosition + 25)

                self.positionMapForPieces[j + 1, i + 1] = [curXPosition, curYPosition]
                self.positionMapForHighlighting[j + 1, i + 1] = [topLeft, bottomRight]
                curXPosition += 55

            curXPosition = 25
            curYPosition += 55
    
    def placePieceUsingPosition(self, x, y):

        # get the corect indexs using math
        xIndex = math.floor(x / 55) + 1
        yIndex = math.floor(y / 55)
        self.drawPiece(xIndex, yIndex, "black")

    


