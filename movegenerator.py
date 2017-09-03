import argparse, json

alpha_to_index_mapping = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7
}
index_to_alpha_mapping = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h"
}


def getColAndRow(pos):
    """Takes a chess oriented position and returns its matrix equivalent"""
    pos = pos.strip().lower()
    stringcol, stringrow = pos
    row = int(stringrow) - 1
    col = alpha_to_index_mapping[stringcol]
    return col, row

def getPos(col, row):
    return "".join([index_to_alpha_mapping[col], str(row + 1)])

def checkcol_and_addmove(dy, dx, chessBoard, moves, direction_done, direction, color='W'):
    piece = chessBoard[dy][dx]
    if piece is not '0':
        if piece[0] is not color:
            moves.append((dy, dx))
        direction_done[direction] = True
    else:
        moves.append((dy, dx))
    return moves

def getmovesKnight(pos, chessBoard, color='W'):
    """Takes position of the knight, the chess board, and piece type and returns all position positions of that knight
    on the specified chess board"""
    col, row = getColAndRow(pos)
    moves = []
    deltas = [(-2, -1), (-2, +1), (+2, -1), (+2, +1), (-1, -2), (-1, +2), (+1, -2), (+1, +2)]
    for delta in deltas:
        move = (col + delta[0], row + delta[1])
        if move[0] < 0 or move[1] < 0:
            continue

        piece = chessBoard[move[0]][move[1]]
        if piece[0] is color:
            continue
        moves.append(move)

    possiblemoves = ["".join([index_to_alpha_mapping[i[0]], str(i[1] + 1)]) for i in moves]
    return possiblemoves

def getmovesRook(pos, chessBoard, color='W'):
    col, row = getColAndRow(pos)
    moves = []
    for j in range(1, 8 - col):
        piece = chessBoard[col + j][row]
        if piece is not '0':
            if piece[0] is not color:
                moves.append((col + j, row))
            break
        else:
            moves.append((col + j, row))

    for j in range(col):
        piece = chessBoard[col - (j + 1)][row]
        if piece is not '0':
            if piece[0] is 'B':
                moves.append((col - (j + 1), row))
            break
        else:
            moves.append((col - (j + 1), row))

    for i in range(1, 8 - row):
        piece = chessBoard[col][row + i]
        if piece is not '0':
            if piece[0] is 'B':
                moves.append((col, row + i))
            break
        else:
            moves.append((col, row + i))

    for i in range(row):
        piece = chessBoard[col][row - (i + 1)]
        if piece is not '0':
            if piece[0] is 'B':
                moves.append((col, row - (i + 1)))
            break
        else:
            moves.append((col, row - (i + 1)))

    possiblemoves = [getPos(i[0], i[1]) for i in moves]
    return possiblemoves

def getmovesKing(pos, chessBoard, color='W'):
    """Takes position of the knight and the chess board and returns all position positions of that knight
        on the specified chess board"""
    col, row = getColAndRow(pos)
    moves = []
    deltas = [(0, 1), (1, 1), (1, 0), (0, -1), (-1, -1), (-1, 0), (1, -1), (-1, 1)]
    for delta in deltas:
        move = (col + delta[0], row + delta[1])
        if move[0] < 0 or move[1] < 0:
            continue

        piece = chessBoard[move[0]][move[1]]
        if piece[0] is color:
            continue
        moves.append(move)

    possiblemoves = [getPos(i[0], i[1]) for i in moves]
    return possiblemoves

def getmovesPawn(pos, chessBoard, color='W'):
    """Takes position of the knight and the chess board and returns all position positions of that knight
            on the specified chess board"""
    col, row = getColAndRow(pos)
    moves = []
    deltas = []
    if color is 'W':
        deltas = [1,2]
    else:
        deltas = [-1, -2]

    piece = chessBoard[col][row + deltas[0]]
    if piece is '0':
        moves.append((col, row + deltas[0]))
        #account for starting pawn position
        piece = chessBoard[col][row + deltas[1]]
        if row is 1 and piece is '0':
            moves.append((col, row + deltas[1]))

    #check for killing positions
    if color is 'W':
        delta_kill = [(-1, 1), (1, 1)]
    else:
        delta_kill = [(-1, -1),(1, -1)]

    for delta in delta_kill:
        move = (col + delta[0], row + delta[1])
        if move[0] < 0 or move[1] < 0:
            continue

        piece = chessBoard[move[0]][move[1]]
        if piece[0] is color or piece is '0':
            continue
        moves.append(move)

    possiblemoves = [getPos(i[0], i[1]) for i in moves]
    return possiblemoves

def getmovesBishop(pos, chessBoard, color='W'):
    col, row = getColAndRow(pos)
    moves = []
    direction_done = [False for i in range(4)]
    for i in range(1,8):
        #+dy, +dx direction
        dy, dx = col + i, row + i
        if dy < 8 and dx < 8 and not (direction_done[0]):
            moves = checkcol_and_addmove(dy, dx, chessBoard, moves, direction_done, 0, color)

        #-dy, +dx direction
        dy, dx = col - i, row + i
        if dy >= 0 and dx < 8 and not (direction_done[1]):
            moves = checkcol_and_addmove(dy, dx, chessBoard, moves, direction_done, 1, color)

        #+dy, -dx direction
        dy, dx = col + i, row - i
        if dy < 8 and dx >= 0 and not (direction_done[2]):
            moves = checkcol_and_addmove(dy, dx, chessBoard, moves, direction_done, 2, color)

        #-dx, -dy direction
        dy, dx = col - i, row - i
        if dy >= 0 and dx >= 0 and not (direction_done[3]):
            moves = checkcol_and_addmove(dy, dx, chessBoard, moves, direction_done, 3, color)

    possiblemoves = [getPos(i[0], i[1]) for i in moves]
    return possiblemoves

def getmovesQueen(pos, chessBoard, color='W'):
    possiblemoves = getmovesRook(pos, chessBoard, color)
    for move in getmovesBishop(pos, chessBoard, color):
        possiblemoves.append(move)
    return possiblemoves

if __name__ == "__main__":
    Board = [['0'] * 8 for i in range(8)]  # an 8 by 8 board

    """
    *prototype
    User input:
        Take White board conf
        Take Black board conf
        Take Piece to evaluate
        Add check for proper piece placement (especially pawn) 
        
    """
    print("Example: \n WHITE: Rf1, Kg1, Pf2, Ph2, Pg3 \n BLACK: Kb8, Ne8, Pa7, Pb7, Pc7, Ra5 \n PIECE TO MOVE: Rf1 \\"
          "\n K, Q, R, B, N, and P to identify the King, Queen, Rook, Bishop, Knight, and Pawn respectively.")
    print("Enter Board Configuration:")
    white_stringval = input("WHITE: ")
    black_stringval = input("BlACK: ")
    piece_stringval = input("PIECE TO MOVE: ")
    white_vals = [i.rstrip() for i in white_stringval.split(",")]
    for pos in white_vals:
        (col, row) = getColAndRow(pos[-2] + pos[-1])
        Board[col][row] = 'W' + pos[0]
    black_vals = [i.rstrip() for i in white_stringval.split(",")]
    for pos in black_vals:
        (col, row) = getColAndRow(pos[-2] + pos[-1])
        Board[col][row] = 'B' + pos[0]

    piece_type = piece_stringval[0];
    moves = []
    if piece_type is 'K':
        moves = getmovesKing(piece_stringval[1]+piece_stringval[2], Board)
    elif piece_type is 'Q':
        moves = getmovesQueen(piece_stringval[1] + piece_stringval[2], Board)
    elif piece_type is 'N':
        moves = getmovesKnight(piece_stringval[1] + piece_stringval[2], Board)
    elif piece_type is 'B':
        moves = getmovesBishop(piece_stringval[1] + piece_stringval[2], Board)
    elif piece_type is 'R':
        moves = getmovesRook(piece_stringval[1] + piece_stringval[2], Board)
    elif piece_type is 'P':
        moves = getmovesRook(piece_stringval[1] + piece_stringval[2], Board)

    print(moves)
