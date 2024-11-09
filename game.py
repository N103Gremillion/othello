import pygame;
from board import Board;
from menu import Menu;
from player import Player;

grey = (128, 128, 128)
black = (0, 0, 0)
white = (255, 255, 255)

class Game:

    searchDepth = 2

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

        pygame.quit()

    def handleAiMove(self):
        if self.gameMode == "aiVsAi" or (self.gameMode == "pVsAi" and self.curPlayer == self.player1):
            return
        
        # clone the previous state of the board
        boardClone = self.board.clone()

        # for the black player we want to find the maxValue and for the white player we want to find the minValue
        isMaximizing = (self.curPlayer == self.player1)

        bestMove = self.miniMax(boardClone, self.searchDepth - 1, isMaximizing)
        self.board.placeValueInGrid(self.curPlayer.playerNumber, bestMove[0], bestMove[1])
        self.updateBoard(bestMove)
        self.renderBoard(bestMove)

    # iterate over all the branches (possible moves) and get the bestMove 
    def miniMax(self, board, depth, isMaximizing):
        bestMove = None
        bestMoveValue = -10000 if isMaximizing else 10000

        for move in board.validMoves:
            boardClone = board.clone()
            boardClone.printGrid()
            boardClone.placeValueInGrid(self.curPlayer.playerNumber, move[0], move[1])
            boardClone.updateGrid(self.curPlayer.playerNumber, move[0], move[1])
            boardClone.printGrid()
            
            moveValue = self.recursiveMiniMax(boardClone, depth - 1, not isMaximizing)

            if isMaximizing and moveValue > bestMoveValue:
                bestMoveValue = moveValue
                bestMove = move
            elif not isMaximizing and moveValue < bestMoveValue:
                bestMoveValue = moveValue
                bestMove = move

        return bestMove

    # recursively explores a move to the depth at the top of the class
    def recursiveMiniMax(self, board, depth, isMaximizing):
        if depth == 0 or not self.getValidPlacementsForClone(board):
            score = self.evaluateGrid(board.grid)
            return score

        if isMaximizing:
            bestScore = -10000
        else:
            bestScore = 10000

        for move in self.getValidPlacementsForClone(board):
            newBoard = board.clone()
            newBoard.placeOnGrid(move[0], move[1], self.curPlayer.playerNumber)

            self.togglePlayer()
            score = self.recursiveMiniMax(newBoard, depth - 1, not isMaximizing)
            self.togglePlayer()

            if isMaximizing:
                bestScore = max(bestScore, score)
                
            else:
                bestScore = min(bestScore, score)
                
        return bestScore

    
    # this returns a value that essentialy is the overall score of the game negative for p2 and positive for p1
    def evaluateGrid(self, grid):
        score = 0

        for row in grid:
            for val in row:
                if (val == self.player1.playerNumber):
                    score += 10
                elif (val == self.player2.playerNumber):
                    score -= 10
        return score

    def determinePlayer(self):
        print("Determining the player")
        # Toggle player and check valid moves for the new player
        self.togglePlayer()
        validMovesForCurrentPlayer = self.getValidPlacements()
        print(validMovesForCurrentPlayer)
        if not validMovesForCurrentPlayer:
            # If the current player has no moves, toggle to the other player
            self.togglePlayer()
            validMovesForOtherPlayer = self.getValidPlacements()
            print(validMovesForOtherPlayer)
            # If neither player has valid moves, end the game
            if not validMovesForOtherPlayer:
                self.endGame()


        
    def togglePlayer(self):
         # Toggle the player
        self.curPlayer = self.player1 if self.curPlayer == self.player2 else self.player2

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
        elif (key == pygame.K_a or key == pygame.K_i):
        # checking if in a mode where an ai is playing
            if (self.gameMode == "aiVsAi"):
                self.handleAiMove()
            elif (self.gameMode == "pVsAi"):
                self.handleAiMove()

    def handleBoardClick(self):
        if (self.curScreen == "menu" or self.gameMode == "aiVsAi" or (self.gameMode == "pVsAi" and self.curPlayer == self.player2)):
            return
                
        pos = pygame.mouse.get_pos()
        x, y = pos
        piecePlaced = self.board.placePieceUsingPosition(x, y, self.curPlayer.playerNumber)

        if piecePlaced:
            
            positionPlace = self.board.getIndeciesWithPosition(x, y)
            self.updateBoard(positionPlace)
            self.renderBoard(positionPlace)

    def endGame(self):
        print("ending the game")
        print(f"player1 has a score of {self.player1.score}")
        print(f"player2 has a score of {self.player2.score}")
        # pygame.quit()
        # exit()

    def updateBoard(self, postion):
        x, y = postion
        self.board.updateGrid(self.curPlayer.playerNumber, x, y)
        self.determinePlayer()
        self.board.validMoves = self.getValidPlacements()
        self.tallyScore()
        self.board.updateCurrentTurnText(self.curPlayer.playerNumber)
    
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
        grid = board.grid
        curPlayer = self.curPlayer
        validIndexes = []
        
        # get previous players turn and to try and search for oposing player positions | reminder: p1 = black = 1 on grid / p2 = white = 2 on grid
        if curPlayer.playerNumber == 1:
            curPlayer = self.player2
        else:
            print("you are white")
            curPlayer = self.player1
        
        # search for the valid positions for curPlayer
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                curNum = grid[row][col]
                if (curNum == 0 and self.isIndexPlacable(row, col, grid, curPlayer.playerNumber)):
                    validIndexes.append((row + 1, col + 1))

        return validIndexes

    def getValidPlacements(self):
        # Initial state of the board and current player
        grid = self.board.grid
        curPlayer = self.curPlayer
        validIndexes = []

        # Start searching for valid placements
        print("Searching for valid placements for", "White" if curPlayer.playerNumber == 2 else "Black")
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                curNum = grid[row][col]
                if curNum == 0 and self.isIndexPlacable(row, col, grid, curPlayer.playerNumber):
                    print(f"Valid move found at ({row + 1}, {col + 1})")
                    validIndexes.append((row + 1, col + 1))

        # Display found valid indexes
        print("Valid placements:", validIndexes)
        self.board.printGrid()
        return validIndexes

    def isIndexPlacable(self, x, y, grid, colorChecking):
        empty = 0
        black = 1
        white = 2
        
        if grid[x][y] != empty:
            print(f"Index ({x}, {y}) is not empty.")
            return False

        opponentColor = black if colorChecking == white else white
        directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        isPlaceable = False

        # Check each direction for opponent and potential sandwich
        for dx, dy in directions:
            newX, newY = x + dx, y + dy
            if 0 <= newX < 8 and 0 <= newY < 8:
                if grid[newX][newY] == opponentColor:
                    print(f"Opponent color at ({newX}, {newY}) in direction ({dx}, {dy})")
                    if self.checkForSandwich(grid, opponentColor, (dx, dy), newX, newY):
                        print(f"Sandwich confirmed in direction ({dx}, {dy}) starting at ({x}, {y})")
                        isPlaceable = True

        if isPlaceable:
            print(f"Placement at ({x}, {y}) is valid for color {colorChecking}")
        else:
            print(f"No valid sandwich found for placement at ({x}, {y})")

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
                
