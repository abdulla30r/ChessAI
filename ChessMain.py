"""
This is our main driver file. It will be responsible for holding user input and display the current GameState Object
"""

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8  # dimension of chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animation
IMAGES = {}

'''
Initialise a global dictionary of images. This will be called exactly once in the main.
'''


def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        # images loading with scaling
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

    # Note: we can access an image by saying 'IMAGES['WP']'


'''
The main driver of our code. This will handle user input and updating the graphics
'''


def main():
    p.init()
    p.display.set_caption("Chess with AI")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock().tick(60)
    screen.fill(p.Color("white"))

    gs = ChessEngine.GameState()

    validMoves = gs.getValidMoves()
    moveMade = False    # flag variable for when a move is made

    loadImages()  # only do this once. before the while loop

    running = True
    sqSelected = ()  # no squared selected initially. keep track of the last click of user. (tuple: (row,col))
    playerClicks = []  # keep track of player clicks (two tuple: ((6,4),(4,4))
    while running:  # game started
        for event in p.event.get():
            if event.type == p.QUIT:  # cross clicked
                running = False  # quit game

            # mouse click
            elif event.type == p.MOUSEBUTTONDOWN:  # left or right click of mouse
                location = p.mouse.get_pos()  # (x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sqSelected == (row, col):  # user clicked the same square twice
                    sqSelected = ()  # deselecting user click
                    playerClicks = []  # clear user clicks

                else:  # valid click
                    sqSelected = (row, col)  # selecting user click
                    playerClicks.append(sqSelected)  # append for both first and second click

                if len(playerClicks) == 2:  # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())

                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            # print(move.pieceMoved)
                            gs.makeMove(move)
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                            txtMove = "White's turn" if gs.whiteToMove else "Black's turn"
                            print(txtMove)
                    if not moveMade:
                        playerClicks = [sqSelected]

            # undo move
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:  # undo when z is pressed
                    gs.undoMove()
                    moveMade = True

            if moveMade:
                validMoves = gs.getValidMoves()
                moveMade = False

            # UI
            drawGameState(screen, gs)
            p.display.flip()


'''
Responsible for all the graphics within a current game state
'''


def drawGameState(screen, gs):
    drawBoard(screen)  # draw square on boards

    # add in piece highlighting and move suggestions
    drawPieces(screen, gs.board)


'''
Draw the squares on the board. The top left corner is always light.
'''


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


main()
