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

    def drawCurBoard(self):
        
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                
                position = self.positionMapForPieces[i + 1, j + 1]
                
                if (self.grid[i][j] == 1):
                    pygame.draw.circle(self.screen, black, position, radius)
                    pygame.display.flip()
                elif (self.grid[i][j] == 2):
                    pygame.draw.circle(self.screen, white, position, radius)
                    pygame.display.flip()
                    
                    
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

    def drawPiece(self, row, col, colorNumber):
        # Ensure the indices are in bounds and convert row/col to screen coordinates
        if row < 1 or row > 8 or col < 1 or col > 8:
            print("You idiot these are out of bounds!!!")
            return

        if self.grid[row - 1][col - 1] != 0:  # Check using row and col
            return

        # Map to screen position using col as x and row as y
        position = self.positionMapForPieces[col, row]
        self.grid[row - 1][col - 1] = colorNumber  # Assign in grid using row/col

        # Draw the circle based on color
        color = black if colorNumber == 1 else white
        pygame.draw.circle(self.screen, color, position, radius)
        pygame.display.flip()


    def clearBoardVisuals(self):
        
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                position = self.positionMapForPieces[i + 1, j + 1]
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
    
    def updateGrid(self, colorNum, xIndex, yIndex):
        # Define piece identifiers
        white = 2
        black = 1
        gridX = xIndex - 1
        gridY = yIndex - 1

        if colorNum == black:
            colorFilling = white
        else:
            colorFilling = black

        # Test one of the directions
        directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

        for dx, dy in directions: 
            newX = xIndex + dx
            newY = yIndex + dy
            newGridX = gridX + dx
            newGridY = gridY + dy
            gridPositionsToFill = []

            # Only proceed if initial position is within bounds
            while (1 <= newX <= 8 and 1 <= newY <= 8):
                # Check bounds for newGridX and newGridY before accessing grid
                if not (0 <= newGridX < len(self.grid) and 0 <= newGridY < len(self.grid[0])):
                    break  
                
                gridVal = self.grid[newGridX][newGridY]

                if gridVal == colorFilling:
                    gridPositionsToFill.append((newGridX, newGridY))
                elif gridVal == colorNum and len(gridPositionsToFill) > 0:
                    self.updateGridValues(gridPositionsToFill, colorNum)
                    break
                else:
                    break

                # Move to the next position in the direction
                newX += dx
                newY += dy
                newGridX += dx
                newGridY += dy

    def updateGridValues(self, indexesToSwitch, fillerNum):
        for x, y in indexesToSwitch:
            self.grid[x][y] = fillerNum

            
    def fillSandwichedLine(self, directions, color, xIndex, yIndex):
        print(directions)
        white = 2
        black = 1
        
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
                self.grid[newY][newX] = fillingWith
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
    
    def renderNewScores(self, player1Score, player2Score):

        self.screen.fill(grey, (0, 0, 100, 50))
        self.player1text = self.playerScoreFont.render(f"Player 1: {player1Score}", False, black)
        self.player2text = self.playerScoreFont.render(f"Player 2: {player2Score}", False, white)

        self.screen.blit(self.player1text, (0, 0))
        self.screen.blit(self.player2text, (0, 25))
        pygame.display.update()

    def printGrid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                print(f"{self.grid[i][j]}", end=' ')
            print("")  # Newline after each row

    


