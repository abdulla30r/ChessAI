"""
This class is responsible for storing all the information about current state of the chess game. It will also be
responsible for determining valid moves at the current state. It will also keep a move log.
"""


class GameState():
    def __init__(self):
        # board is an 8*8 2d list . each element has 2 character.
        # first character means color. 2nd character piece name.
        # for example: bQ = black Queen
        # "--" represents empty space with no piece

        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["--", "--", "--", "--", "--", "--", "--", "--", ],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.moveFunction = {'p': self.getPawnMoves, 'R': self.getRookeMoves, 'N': self.getKnightMoves,
                             'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves, }

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.stallMate = False

    '''
    move a piece using move parameter. this will not work for pawn promotion, castling, en-passant
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"  # make blank in source
        self.board[move.endRow][move.endCol] = move.pieceMoved  # put piece in destination
        self.moveLog.append(move)  # log the move, so we can see history or undo move
        self.whiteToMove = not self.whiteToMove  # swap players

        # keep tracking of king in case of check
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

    '''
      undo the last move
    '''
    def undoMove(self):
        if len(self.moveLog) > 0:  # make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # swap players

            # keep tracking of king in case of check
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

    def getValidMoves(self):
        # 1. generate all possible moves
        moves = self.getAllPossibleMoves()
        # 2. for each move, make them
        for i in range(len(moves) - 1, -1, -1):     # when removing from a list fo backward through that list
            self.makeMove(moves[i])
            # 3. generate all opponent's move
            # 4. for each of your opponent's move, see if they attack your king.
            # 3 and 4
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            # 5. if they attack your king, then it's invalid move.
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.stallMate = True
        else:
            self.checkMate = False
            self.stallMate = False

        return moves

    '''
    Determine if the current player is in check
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # determine if the enemy attack r,c
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove     # switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of cols
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r, c, moves)  # calls the appropriate move function based on piece
        return moves

    '''
    Get all the pawn moves at row,col and add these moves to the list
    gonna refactor this part of code later
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves

            # 1 square pawn advance
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))

                # 2 square pawn advance
                if (self.board[r - 2][c] == "--") and (r == 6):
                    moves.append(Move((r, c), (r - 2, c), self.board))

            # capture left corner
            if (c > 0) and (self.board[r - 1][c - 1][0] == "b"):
                moves.append(Move((r, c), (r - 1, c - 1), self.board))

            # capture right corner
            if (c < 7) and (self.board[r - 1][c + 1][0] == "b"):
                moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # black pawn moves
            # 1 square pawn advance
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))

                # 2 square pawn advance
                if (self.board[r + 2][c] == "--") and (r == 1):
                    moves.append(Move((r, c), (r + 2, c), self.board))

            # capture left corner
            if (c > 0) and (self.board[r + 1][c - 1][0] == "w"):
                moves.append(Move((r, c), (r + 1, c - 1), self.board))

            # capture right corner
            if (c < 7) and (self.board[r + 1][c + 1][0] == "w"):
                moves.append(Move((r, c), (r + 1, c + 1), self.board))

            # add pawn promotion later

    '''
    4 direction ei jete pare
    loop for each direction:
       left=>
           loop for each cell
               first cell=> check piece and take decision
               adjacent cell theke count shuru hobe. adjacent invalid hole ar samne jete parbena
               so loop break
    this is common for both rooke and bishop. only difference one goes straight another diagonal.
    so after deciding direction just use this function.
    '''

    def getCommonMoves(self, directions, r, c, moves):
        enemyColor = "b" if self.whiteToMove else "w"  # defining enemy color
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:
                    break

    def getRookeMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        self.getCommonMoves(directions, r, c, moves)

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # 4 diagonal
        self.getCommonMoves(directions, r, c, moves)

    def getKingAndKnightMoves(self, directions, r, c, moves):
        allyColor = "w" if self.whiteToMove else "b"
        for m in directions:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getKnightMoves(self, r, c, moves):
        directions = ((2, -1), (2, 1), (-2, 1), (-2, -1), (1, -2), (1, 2), (-1, -2), (-1, 2))
        self.getKingAndKnightMoves(directions, r, c, moves)

    def getKingMoves(self, r, c, moves):
        directions = ((0, -1), (0, 1), (1, 0), (-1, 0), (-1, -1), (1, 1), (1, -1), (-1, 1))
        self.getKingAndKnightMoves(directions, r, c, moves)

    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookeMoves(r, c, moves)


class Move():
    # maps keys to value
    # key : value
    # normally chess e vertical e 0-7 numbering kora. starting from white.
    # horizontal e a-h. called files. our board orders are not same. hence, mapping.
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}  # mapping dictionary
    rowsToRanks = {v: k for k, v in ranksToRows.items()}  # reverse a dictionary

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}  # mapping dictionary
    colsToFiles = {v: k for k, v in filesToCols.items()}  # reverse a dictionary

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    # source Destination of current move. example : d2d4
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
