import pygame;

"""
Note: for this class a 0 on the grid is white & 1 is black
"""
class Board: 

    # maps indexes to postions on the board
    positionMap = {}

    def __init__(self, boardWidth, boardHeight, color):

        self.setupPositionMap()
        pygame.display.set_mode ([boardWidth, boardHeight])
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.screen = pygame.display.get_surface()
        self.grid = []
        self.drawBoard(color)
        self.initalizeGrid()
        pygame.display.flip()

    def drawBoard(self, color):
        
        # setup inital values for lines
        horizontalLinePos = pygame.Vector2(0, 50)
        verticalLinePos = pygame.Vector2(50, 0)

        # setup temporary constants
        horizontalLineWidth = 435
        horizontalLineHeight = 5
        verticalLineWidth = 5
        verticalLineHeight = 435
        black = (0, 0, 0)

        self.screen.fill(color)
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

    def initalizeGrid(self):
        # initalize as -1 to represent null
        for i in range(64):
            row = []
            for j in range(64):
                row.append(-1)
            self.grid.append(row)

    def placePiece(self, x, y, colorString):
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

    def setupPositionMap(self):
        # map indeces in the board to the corresponding positions
        curXPosition = 25
        curYPosition = 25 
        
        # loop over and fill the map
        for i in range(8):
            for (j) in range(8):
                self.positionMap[j, i] = [curXPosition, curYPosition]
                curXPosition += 55
            curXPosition = 25
            curYPosition += 55

