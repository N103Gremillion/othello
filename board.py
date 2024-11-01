import pygame;

"""
Note: for this class a 0 on the grid is white & 1 is black and a -1 is (empty)
"""

black = (0, 0, 0)
white = (255, 255, 255)

class Board: 

    # maps indexes to postions on the board
    positionMap = {}

    def __init__(self, boardWidth, boardHeight, color):

        pygame.display.set_mode ([boardWidth, boardHeight])

        # setup of game display and grid
        self.setupPositionMap()
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
        self.drawPiece(3, 3, "black")
        self.drawPiece(3, 4, "white")
        self.drawPiece(4, 3, "white")
        self.drawPiece(4, 4, "black")

    def initalizeGrid(self):
        # initalize as -1 to represent null
        for i in range(64):
            row = []
            for j in range(64):
                row.append(-1)
            self.grid.append(row)

    def drawPiece(self, x, y, colorString):
        # Error checking
        if (x < 1 or x > 8 or y < 1 or y > 8):
            print("You idiot these are out of bounds!!!")
        
        # add the circle
        if (self.grid[x][y] != -1):
            return
        
        # add either 0 "for white" or 1 "for black"
        white = (255, 255, 255)
        black = (0, 0, 0)
        radius = 25
        position = self.positionMap[x, y]

        if (colorString.lower() == "white"):
            self.grid[x][y] = 0
            pygame.draw.circle(self.screen, white, position, radius)
            pygame.display.flip()
        elif (colorString.lower() == "black"):
            self.grid[x][y] = 1
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

    def setupPositionMap(self):
        # map indeces in the board to the corresponding positions
        curXPosition = 25
        curYPosition = 80 
        
        # loop over and fill the map
        for i in range(8):
            for (j) in range(8):
                self.positionMap[j, i] = [curXPosition, curYPosition]
                curXPosition += 55
            curXPosition = 25
            curYPosition += 55

