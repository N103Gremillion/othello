import pygame;
from board import Board;
from menu import Menu;
from player import Player;

grey = (128, 128, 128)
black = (0, 0, 0)
white = (255, 255, 255)

class Game:

    searchDepth = 3

    def __init__(self):
        # by default it is pvp
        self.stateCounter = 0
        self.debug = False
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

    # clone the current state of board and run minimax on each branch
    def handleAiMove(self):
        if (self.gameMode == "pVsAi" and self.curPlayer == self.player1) or self.gameMode == "Over":
            return
        boardClone = self.board.clone()
        isMaximizing = (self.curPlayer == self.player1)
        bestMove = self.miniMax(boardClone, self.searchDepth - 1, isMaximizing)
        self.board.placeValueInGrid(self.curPlayer.playerNumber, bestMove[0], bestMove[1])
        self.updateBoard(bestMove)
        self.renderBoard(bestMove)

    # interate over branches and call the recursive mininmax
    def miniMax(self, board, depth, isMaximizing):

        bestMove = None
        alpha = -10000
        beta = 10000
        self.stateCounter = 0

        for move in board.validMoves:

            if self.debug:
                print(f"Evaluating move {move}")

            boardClone = board.clone()
            # place move on clone and change colors of appropriate pieces
            boardClone.placeValueInGrid(self.curPlayer.playerNumber, move[0], move[1])
            boardClone.updateGrid(self.curPlayer.playerNumber, move[0], move[1])

            # get value of the current board state 
            moveValue = self.recursiveMiniMax(boardClone, depth - 1, not isMaximizing, alpha, beta, move)
            
            if self.debug:
                print(f"Move {move} has a heuristic value {moveValue}")

            if isMaximizing and moveValue > alpha:
                alpha = moveValue
                bestMove = move
            elif not isMaximizing and moveValue < beta:
                beta = moveValue
                bestMove = move

        print(f"Total game states evaluated: {self.stateCounter}")
        return bestMove

    def recursiveMiniMax(self, board, depth, isMaximizing, alpha, beta, move):

        self.stateCounter += 1

        if depth == 0 or not self.getValidPlacementsForClone(board):
            score = self.evaluateGrid(board.grid)
            if self.debug:
                print(f"Depth {depth} | Move sequence: {move} | Heuristic value: {score}")
            return score

        # for alpha beta pruning
        if self.alphaBeta:
            if isMaximizing:
                bestScore = -10000
                for move in self.getValidPlacementsForClone(board):
                    if self.debug:
                        print(f"Maximizing | Evaluating move {move}")

                    newBoard = board.clone()
                    newBoard.placeValueInGrid(1, move[0], move[1])
                    newBoard.updateGrid(1, move[0], move[1])

                    score = self.recursiveMiniMax(newBoard, depth - 1, False, alpha, beta, move)
                    bestScore = max(bestScore, score)

                    # check if you  found a better alpha value
                    alpha = max(alpha, bestScore)

                    if self.debug:
                        print(f"Maximizing | Move {move} | Best score: {bestScore} | Alpha: {alpha}")

                    # prune when the beta(minimizer value) is already less than or == to the maximizer at the root
                    if beta <= alpha:
                        if self.debug:
                            print(f"Pruning branches where beta ({beta}) <= alpha ({alpha})")
                        break

                return bestScore
            
            else:
                bestScore = 10000
                for move in self.getValidPlacementsForClone(board):
                    if self.debug:
                        print(f"Minimizing | Evaluating move {move}")

                    newBoard = board.clone()
                    newBoard.placeValueInGrid(2, move[0], move[1])
                    newBoard.updateGrid(2, move[0], move[1])

                    score = self.recursiveMiniMax(newBoard, depth - 1, True, alpha, beta, move)
                    bestScore = min(bestScore, score)
                    beta = min(beta, bestScore)

                    if self.debug:
                        print(f"Minimizing | Move {move} | Best score: {bestScore} | Beta: {beta}")

                    if beta <= alpha:
                        if self.debug:
                            print(f"Pruning branches where beta ({beta}) <= alpha ({alpha})")
                        break
                return bestScore
        # if not in alpha beta pruning
        else:
            bestScore = -10000 if isMaximizing else 10000

            # iterate over the "children" potential moves for this node
            for move in self.getValidPlacementsForClone(board):
                if self.debug:
                    print(f"{'Maximizing' if isMaximizing else 'Minimizing'} | Evaluating move {move}")

                playerNum = 1 if isMaximizing else 2

                newBoard = board.clone()
                newBoard.placeValueInGrid(playerNum, move[0], move[1])
                newBoard.updateGrid(playerNum, move[0], move[1])

                # print board if in debugg
                if self.debug:
                    print(f"{'Maximizing' if isMaximizing else 'Minimizing'} | Move {move} grid state:")
                    newBoard.printGrid()

                score = self.recursiveMiniMax(newBoard, depth - 1, not isMaximizing, alpha, beta, move)
                
                if self.debug:
                    print(f"{'Maximizing' if isMaximizing else 'Minimizing'} | Move {move} | Score: {score}")

                if isMaximizing:
                    bestScore = max(bestScore, score)
                    if self.debug:
                        print(f"Maximizing | Move {move} | Updated best score to {bestScore}")
                else:
                    bestScore = min(bestScore, score)
                    if self.debug:
                        print(f"Minimizing | Move {move} | Updated best score to {bestScore}")

            if self.debug:
                print(f"Returning best score {bestScore}")
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
        # Toggle player and check valid moves for the new player
        self.togglePlayer()
        validMovesForCurrentPlayer = self.getValidPlacements()
        if not validMovesForCurrentPlayer:
            # If the current player has no moves, toggle to the other player
            self.togglePlayer()
            validMovesForOtherPlayer = self.getValidPlacements()
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
        # toggling on and off pruning and debugg
        elif (key == pygame.K_d):
            self.debug = not self.debug
            self.board.renderDebugAlpha(self.debug, self.alphaBeta)
        elif (key == pygame.K_p):
            self.alphaBeta = not self.alphaBeta
            self.board.renderDebugAlpha(self.debug, self.alphaBeta)

    def handleBoardClick(self):
        if (self.curScreen == "menu" or self.gameMode == "aiVsAi" or (self.gameMode == "pVsAi" and self.curPlayer == self.player2) or self.gameMode == "over"):
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
        self.gameMode = "over"
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
        self.board.renderDebugAlpha(self.debug, self.alphaBeta)

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

        # Start searching for valid placement
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                curNum = grid[row][col]
                if curNum == 0 and self.isIndexPlacable(row, col, grid, curPlayer.playerNumber):
                    validIndexes.append((row + 1, col + 1))

        # Display found valid indexes
        return validIndexes

    def isIndexPlacable(self, x, y, grid, colorChecking):
        empty = 0
        black = 1
        white = 2
        
        if grid[x][y] != empty:
            return False

        opponentColor = black if colorChecking == white else white
        directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        isPlaceable = False

        # Check each direction for opponent and potential sandwich
        for dx, dy in directions:
            newX, newY = x + dx, y + dy
            if 0 <= newX < 8 and 0 <= newY < 8:
                if grid[newX][newY] == opponentColor:
                    if self.checkForSandwich(grid, opponentColor, (dx, dy), newX, newY):
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
                
