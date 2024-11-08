import pygame;
from board import Board;
from menu import Menu;
from player import Player;

grey = (128, 128, 128)
black = (0, 0, 0)
white = (255, 255, 255)
searchDepth = 2

class Game:

    def __init__(self):
        # by default it is pvp
        self.alphaBeta = False
        self.gameMode = "pVp"
        self.curScreen = "board"
        self.menu = Menu(435, 490)
        self.board = Board(435, 490)
        self.player1 = Player(1, "black")
        self.player2 = Player(2, "white")
        self.curPlayer = self.player1
        self.board.draw()
    
    def startGame(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.handleBoardClick()
                    self.handleMenuClick()
                if event.type == pygame.KEYDOWN:
                    self.handleKeyPress(event.key)
                if event.type == pygame.QUIT:
                    running = False

            # checking if in a mode where an ai is playing
            if (self.gameMode == "aiVsAi"):
                self.handleAiMove()
            elif (self.gameMode == "pVsAi"):
                self.handleAiMove()
        pygame.quit()

    def handleAiMove(self):
        if self.gameMode == "aiVsAi" or (self.gameMode == "pVsAi" and self.curPlayer == self.player1):
            return

        

    def miniMax(self, board, depth, maximizingNode):
        print("miniMax")

    # recursively explores a move to the depth at the top of the class
    def recursiveMiniMax(self, board, depth, maximizingNode):
        if depth == 0 or not self.getValidPlacementsForClone(board):
            return self.evaluateGrid(board.grid)
        
        print("recursive call")

    # this returns a value that essentialy is the overall score of the game negative for p2 and positive for p1
    def evaluateGrid(self, grid):
        score = 0

        for row in grid:
            for val in row:
                if (val == self.player1.playerNumber):
                    score += 1
                elif (val == self.player2.playerNumber):
                    score -= 1
        return score
    
    # this clones the array that stores the state of the board
    def cloneGrid(self):
        newBoard = []
        for i in range(len(self.board.grid)):
            curRow = []
            for j in range(len(self.board.grid[0])):
                curRow.append(self.board.grid[i][j])
            newBoard.append(curRow)
        return newBoard

    def openMenu(self):
        self.curScreen = "menu"
        self.menu.drawMenu()

    def closeMenu(self):    
        self.curScreen = "board"
        self.board.drawBoard(grey)
        self.board.drawCurBoard()
        self.board.highlightValidPositions()

    def handleMenuClick(self):
        if (self.curScreen == "board" or self.gameMode == "aiVsAi" or self.gameMode == "pVsAi" and self.curPlayer == "white"):
            return

        pos = pygame.mouse.get_pos()
        x, y = pos
        
        if (125 <= x <= 325):
            # p vs p button
            if (50 <= y <= 100):
                self.closeMenu()
                self.gameMode = "pVp"
            # p vs a button
            elif (150 <= y <= 200):
                self.closeMenu()
                self.gameMode = "pVsAi"
            # a vs a button
            elif (250 <= y <= 300):
                self.closeMenu()
                self.gameMode = "aiVsAi"
            # Exit button
            elif (350 <= y <= 400):
                self.closeMenu()

    def handleKeyPress(self, key):
        if (key == pygame.K_ESCAPE):
            if (self.curScreen == "menu"):
                self.closeMenu()
                
            elif (self.curScreen == "board"):
                self.openMenu()

    def handleBoardClick(self):
        if (self.curScreen == "menu"):
            return
                
        pos = pygame.mouse.get_pos()
        x, y = pos
        piecePlaced = self.board.placePieceUsingPosition(x, y, self.curPlayer.playerNumber)

        if piecePlaced:
            
            positionPlace = self.board.getIndeciesWithPosition(x, y)
            self.updateBoard(positionPlace)
            self.renderBoard(positionPlace)
            # Switch to the other player after AI move
            self.curPlayer = self.player1 if self.curPlayer == self.player2 else self.player2
            self.board.updateCurrentTurnText(self.curPlayer.playerNumber)

    def updateBoard(self, postion):
        x, y = postion
        self.board.updateGrid(self.curPlayer.playerNumber, x, y)
        self.board.validMoves = self.getValidPlacements()
        self.tallyScore()
    
    def renderBoard(self, position):
        x, y = position
        self.board.clearBoardVisuals()
        self.board.drawCurBoard()
        self.board.updateCurrentTurnText(self.curPlayer.playerNumber)
        self.board.highlightValidPositions()
        self.board.renderNewScores(self.player1.score, self.player2.score)

    def tallyScore(self):
        self.player1.score = 0
        self.player2.score = 0
        grid = self.board.grid

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                # P1 of black
                if (grid[i][j] == 1):
                    self.player1.score += 10
                elif (grid[i][j] == 2):
                    self.player2.score += 10

    def getValidPlacementsForClone(self, board):
        p1 = 1
        p2 = 2
        grid = board.grid
        curPlayer = self.curPlayer
        validIndexes = []
        
        # get previous players turn and to try and search for oposing player positions | reminder: p1 = black = 1 on grid / p2 = white = 2 on grid
        if curPlayer.playerNumber == 1:
            curPlayer = self.player2
        else:
            curPlayer = self.player1
        
        # search for the valid positions for curPlayer
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                curNum = grid[row][col]
                if (curNum == 0 and self.isIndexPlacable(row, col, grid, curPlayer.playerNumber)):
                    validIndexes.append((row + 1, col + 1))

        return validIndexes

    def getValidPlacements(self):
        
        # player nums and current state of the board | validIndexes is a list of tuples for valid move indexes
        self.directionsFilledWithPlacement = []
        
        p1 = 1
        p2 = 2
        grid = self.board.grid
        curPlayer = self.curPlayer
        validIndexes = []
        
        # get previous players turn and to try and search for oposing player positions | reminder: p1 = black = 1 on grid / p2 = white = 2 on grid
        if curPlayer.playerNumber == 1:
            curPlayer = self.player2
        else:
            curPlayer = self.player1
        
        # search for the valid positions for curPlayer
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                curNum = grid[row][col]
                if (curNum == 0 and self.isIndexPlacable(row, col, grid, curPlayer.playerNumber)):
                    validIndexes.append((row + 1, col + 1))

        return validIndexes

    def isIndexPlacable(self, x, y, grid, colorChecking):
        empty = 0
        black = 1
        white = 2
        
        if grid[x][y] != empty:
            return False
        
        # Set opponent's color
        opponentColor = black if colorChecking == white else white

        # Directions to check around the placement
        directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        isPlaceable = False

        for dx, dy in directions:
            newX, newY = x + dx, y + dy
            
            # Check bounds
            if 0 <= newX < 8 and 0 <= newY < 8:
                if grid[newX][newY] == opponentColor:
                    if self.checkForSandwich(grid, opponentColor, (dx, dy), newX, newY):
                        # Only set isPlaceable to True after confirming the sandwich
                        isPlaceable = True

        return isPlaceable

    def checkForSandwich(self, grid, colorBeingSandwiched, direction, x, y):
        empty = 0
        black = 1
        white = 2

        # Determine closing color
        closingColor = black if colorBeingSandwiched == white else white

        dx, dy = direction
        newX, newY = x + dx, y + dy

        # Check the line in the specified direction
        while 0 <= newX < 8 and 0 <= newY < 8:
            if grid[newX][newY] == empty:
                return False
            if grid[newX][newY] == closingColor:
                # A closing color was found // sandwich confirmed in this direction
                return True
            
            # Move further in the current direction
            newX += dx
            newY += dy
        
        return False
                
        
        