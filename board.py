import math
import pygame;

"""
Note: for this class a 2 on the grid is white(p2) & 1 is black(p1) and a 0 is (empty)
"""

# rgb colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 139)
yellow = (255, 255, 0)
grey = (128, 128, 128)
radius = 25

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
        # this is a 2d array
        self.grid = []
        # start board with intial valid positions for black
        self.validMoves = [(4, 6), (3, 5), (5, 3), (6, 4)]
        self.playerScoreFont = pygame.font.SysFont('Comic Sans MS', 30)
        self.currentTurnFont = pygame.font.SysFont('Comit Sans MS', 45)
        self.player1text = self.playerScoreFont.render("Player 1: 0", False, black)
        self.player2text = self.playerScoreFont.render("Player 2: 0", False, white)
        self.currentTurnText = self.currentTurnFont.render("Player 1's Turn", False, black)
        self.drawBoard(color)
        self.initalizeGrid()
        self.drawStartingPieces()
        self.highlightStartingValidMoves()

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
        verticalLineHeight = 440

        # draw divider line that divides header from board
        self.screen.fill(color)
        dividerLine = pygame.Rect(dividerLinePos.x, dividerLinePos.y, horizontalLineWidth, horizontalLineHeight)
        pygame.draw.rect(self.screen, blue, dividerLine)
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
            pygame.draw.rect(self.screen, blue, curHorizontalLine)
            pygame.draw.rect(self.screen, blue, curVerticalLine)
            pygame.display.update()

            # update line positions
            horizontalLinePos.y += 55
            verticalLinePos.x += 55

    def drawStartingPieces(self):
        self.drawPiece(4, 4, 1)
        self.drawPiece(4, 5, 2)
        self.drawPiece(5, 4, 2)
        self.drawPiece(5, 5, 1)

    def highlightStartingValidMoves(self):
        for i in range(len(self.validMoves)):
            x, y = self.validMoves[i]
            self.highlightSquare(x, y)
        
    def initalizeGrid(self):
        # initalize as -1 to represent null
        for i in range(8):
            row = []
            for j in range(8):
                row.append(0)
            self.grid.append(row)

    def drawPiece(self, xIndex, yIndex, colorNumber):
        # Error checking
        if (xIndex < 1 or xIndex > 8 or yIndex < 1 or yIndex > 8):
            print("You idiot these are out of bounds!!!")
        
        # add the circle
        if (self.grid[xIndex - 1][yIndex - 1] != 0):
            return
        
        # add either 0 "for white" or 1 "for black"
        position = self.positionMapForPieces[xIndex, yIndex]

        if (colorNumber == 2):
            self.grid[xIndex - 1][yIndex - 1] = 2
            pygame.draw.circle(self.screen, white, position, radius)
            pygame.display.flip()
        elif (colorNumber == 1):
            self.grid[xIndex - 1][yIndex - 1] = 1
            pygame.draw.circle(self.screen, black, position, radius)
            pygame.display.flip()
        else:
            print("Not a valid color dummy!!")

    def clearPreviousValidMoves(self, positionPlace):
        
        for i in range(len(self.validMoves)):
            if self.validMoves[i] != positionPlace:
                x, y = self.validMoves[i]
                position = self.positionMapForPieces[x, y]
                pygame.draw.circle(self.screen, grey, position, radius)
                pygame.display.flip()
    
    def highlightValidPositions(self):
        
        for i in range(len(self.validMoves)):
            x, y = self.validMoves[i]
            self.highlightSquare(x, y)
            
    def updateScoreText(self, player, score):
        
        if player.lower() == "player1":
            self.player1text = self.playerScoreFont.render(f"Player 1: {score}", False, black)
            self.screen.blit(self.player1text, (0, 0))
        elif player.lower() == "player2":
            self.player2text = self.playerScoreFont.render(f"Player 2: {score}", False, white)
            self.screen.blit(self.player2text, (0, 25))
        
        pygame.display.update()
        
    def updateCurrentTurnText(self, playerNumber):

        self.screen.fill(grey, (160, 10, 300, 40))
        
        if playerNumber == 1:
            self.currentTurnText = self.currentTurnFont.render(f"Player 1's Turn", True, black)
        elif playerNumber == 2:
            self.currentTurnText = self.currentTurnFont.render(f"Player 2's Turn", True, white)
            
        self.screen.blit(self.currentTurnText, (160, 10))
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
    
    def placePieceUsingPosition(self, x, y, playerNumber):

        # get the corect indexs using math
        xIndex = math.floor(x / 55) + 1
        yIndex = math.floor(y / 55)
        indexPosition = (xIndex, yIndex)
        
        if xIndex < 1 or xIndex > 8 or yIndex < 1 or yIndex > 8:
            return False

        if playerNumber == 1 and indexPosition in self.validMoves:
            self.drawPiece(xIndex, yIndex, 1)
            return True
    
        elif (playerNumber == 2 and indexPosition in self.validMoves):
            self.drawPiece(xIndex, yIndex, 2)
            return True

        # when a position is not valid
        else:
            return False
        
    def getIndeciesWithPosition(self, x, y):
        # get the corect indexs using math
        xIndex = math.floor(x / 55) + 1
        yIndex = math.floor(y / 55)
        indexPosition = (xIndex, yIndex)
        
        return indexPosition
    
    def fillSandwichedLine(self, directions, color, xIndex, yIndex):
        white = 2
        black = 1
        
        print("trying to fill sandwiched lines")
        print()
        if (color == "black"):
            numToFill = white
            fillingWith = black
        else:
            numToFill = black
            fillingWith = white
        
        for dx, dy in directions:
            newX = xIndex - dx
            newY = yIndex - dy
            
            while (0 <= newX < len(self.grid) and 0 <= newY < len(self.grid[0]) and self.grid[newX][newY] == numToFill):
                print("filling Piece")
                self.grid[newX][newY] = fillingWith
                self.drawPiece(xIndex, yIndex, fillingWith)
                newX -= dx
                newY -= dy
                
        
    # returns true if there is a valid postion aka (highlighting a square)
    def highlightSquare(self, xIndex, yIndex):
        
        if xIndex < 1 or xIndex > 8 or yIndex < 1 or yIndex > 8:
            return False

        # I use a hollow circle to highlight
        position = self.positionMapForPieces[xIndex, yIndex]
        pygame.draw.circle(self.screen, yellow, position, radius, 1)
        pygame.display.flip()
        
    def printGrid(self):

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                print(self.grid[i][j], end='')
            print("")
    


