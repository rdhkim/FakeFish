"""
This is our main driver file.
It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8 #dimension of chess board (8x8)
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #animations later on
IMAGES = {}

"""
Initialize a global dictionary of images.
This wlil be called exactly once in the main.
"""

def loadImages():
    pieces = ["bB", "bK", "bN", "bP", "bQ", "bR", "wB", "wK", "wN", "wP", "wQ", "wR"]
    for piece in pieces:
        IMAGES[piece] = p.transform.smoothscale(p.image.load("images/" + piece + ".png").convert_alpha(), (SQ_SIZE, SQ_SIZE))
        # we can now retrieve images by key search in our dictonary 'IMAGES["wP"]'

"""
Main driver for our code
Handle user input and updating graphics
"""

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made

    loadImages() #only do this once, before the while loop
    running = True
    sqSelected = () # no Square is selected, keep track of last click of user (tuple (row, col))
    playerClicks = [] # keeps track of player clicks (two tuples: [(6,4), (4, 4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) position of mouse
                col = location[0]//SQ_SIZE 
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #user clicked same square twice
                    sqSelected = () # deselect
                    playerClick = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #append for both first and second clicks
                if len(playerClicks) == 2: # after second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    # print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () # reset user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            # Key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when Z is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs) 
        clock.tick(MAX_FPS) 
        p.display.flip() 

"""
Responsible for all the graphics within a current game state.
"""

def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on the board
    #add piece highlighting or move suggestions
    drawPieces(screen, gs.board) #draw pieces on top of those squares

"""
Draw the squares on the board. The top left square is always light
"""

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
Draw the pieces on the board using the current GameState.board
"""

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
