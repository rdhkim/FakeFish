"""
This class is responsible for storing all the information about the current state of a chess game.
It will also be responsible for determining valid moves at the current state.
It will also keep a move log.
"""
class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.moveFunction = {
                'P': self.getPawnMoves,
                'R': self.getRookMoves,
                'N': self.getKnightMoves,
                'B': self.getBishopMoves,
                'Q': self.getQueenMoves,
                'K': self.getKingMoves
                }    
        self.whiteToMove = True
        self.moveLog = []
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

    """
    Takes a move as a parameter and executes it 
    This will not work for castling, pawn promotion, and en-passant
    """ 
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove # swap players
        # update the king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    """
    Undo the last move made
    """
    def undoMove(self):
        if len(self.moveLog) != 0: # makes sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # switch turns back
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    """
    All moves considering checks
    """
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endrow, moves[1].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()
        
        return moves
                        
        # #naive algorithm 
        # # 1) generate all possible moves
        # moves = self.getAllPossibleMoves()
        # # 2) for each move, make the move
        # for i in range(len(moves)-1, -1, -1): # when removing from a list go backwards through the list
        #     self.makeMove(moves[i])
        #     #print(moves[i].pieceMoved)
        #     #print(moves[i].getChessNotation())
        #     # 3) generate all opponent's moves
        #     # 4) for each of your oponent's moves, see if they attack your king
        #     self.whiteToMove = not self.whiteToMove
        #     if self.inCheck():
        #         print(moves[i].pieceMoved)
        #         print(moves[i].pieceCaptured)
        #         #print(moves[i].pieceMoved + moves[i].pieceCaptured + str(moves[i].moveID))
        #         #print(moves[i].getChessNotation())
        #         moves.remove(moves[i]) # 5) if they do attack your king, not a valid move
        #     self.whiteToMove = not self.whiteToMove
        #     self.undoMove()
        # return moves

    """
    Determine if the current player is in check
    """
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        
    """
    Determine if the enemy can attack the square r, c
    """
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # switches to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: # square is under attack
                print("under atk " + move.getChessNotation())
                return True
        return False

    """
    All moves without considering checks
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): # number of rows
            for c in range(len(self.board[r])): # number of cols in given row
                turn = self.board[r][c][0] # checks color of piece (first value of the square "w" or "b")
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove): # need to check whose turn it is to generate valid moves accordingly
                    piece = self.board[r][c][1] # type of piece (pawn, rook, bishop, etc); denoted by "p", "R", "B", etc
                    if piece != '-':
                        self.moveFunction[piece](r, c, moves) # calls the appropriate move functoin based on piece type
        return moves    

    """
    Get all the pawn moves for the pawn located at row, col and add these moves to the lsit
    """
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove and self.board[r][c][0] == 'w': # wite pawn move
            if self.board[r-1][c] == "--": # 1 square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # 2 square move is possible
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:    # captures to left
                if self.board[r-1][c-1][0] == "b": # enemy piece avaliable to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: # captures to right
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        
        elif not self.whiteToMove and self.board[r][c][0] == 'b': # black to move
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))

    """
    Get all the rook moves for the rook located at row, col and add these moves to the list
    """
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, len(self.board)):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board[endRow]):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #friendly piece invalid
                        break
                else: #off board
                    break

    def getKnightMoves(self, r, c, moves):
        directions = ((-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)) 
        allyColor = "w" if self.whiteToMove else "b"
        for d in directions:
                endRow = r + d[0]
                endCol = c + d[1]
                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board[endRow]):
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # 4 diagonals
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, len(self.board)):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board[endRow]):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
 
    def getQueenMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, len(self.board)):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board[endRow]):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1)) 
        allyColor = "w" if self.whiteToMove else "b"
        for i in kingMoves:
            endRow = r + i[0]
            endCol = c + i[1]
            if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board[endRow]):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: 
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () # reset possible pin
            for i in range(1,8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == (): #1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # # 5 possibilites here in this complex conditions
                        # 1.) orthogonally away from king and piece is a rook 
                        # 2.) diagonally away from king and piece is a bishop 
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen 
                        # 5.) any direction 1 square away and piece is a king (this is necessary to prevent a king move to a square controlled by another king) 
                        if (0 <= j <= 3 and type == "R") or \
                                (4 <= j <= 7 and type == "B") or \
                                (i == 1 and type == "P" and ((enemyColor == "w" and 6 <= j <= 7) or (enemyColor == "b" and 4 <= j <= 5))) or \
                                (type == "Q") or (i == 1 and type == "K"):
                                if possiblePin == ():
                                    inCheck = True
                                    checks.append((endRow, endCol, d[0], d[1]))
                                    break
                                else:
                                    pins.append(possiblePin)
                                    break
                        else:
                            break
        directions = ((-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)) 
        for d in directions:
                endRow = startRow + d[0]
                endCol = startCol + d[1]
                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board[endRow]):
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == enemyColor and endPiece[1] == 'N':
                        inCheck = True
                        checks.append((endRow, endCol, d[0], d[1]))
        return inCheck, pins, checks


class Move(): 
    # maps keys to values
    # key : value
    ranksToRows = { "1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = { "a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol] 
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.board = board
        self.moveID = self.startRow * 1000 + self.startCol * 1000 + self.endRow * 10 + self.endCol
    
    """
    Override the equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.pieceMoved +  self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


