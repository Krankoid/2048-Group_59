import random

# prints the board after each move
def printBoard(board):
    for i in range(4):
        print()
        for j in range(4):
            print(board[i][j], end = " ")

#  adds two random 2-tiles to the board
def initialize_game(board):
    row = random.randint(0, 3)
    col = random.randint(0, 3)
    board[row][col] = 2
    while(board[row][col] != 0):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
    board[row][col] = 2

# moves all tiles to the left by checking if 0. We move them left 
# because we can transposeBoard or reverseBoard the board to mimic different directions
def pushLeft(board):
    new_board = [[0] * 4 for _ in range(4)]
    for i in range(4):
        fill_position = 0
        for j in range(4):
            if board[i][j] != 0:
                new_board[i][fill_position] = board[i][j]
                fill_position += 1
    return new_board

# merges like tiles by checking if the tile is equal to the tile to the right
def merge(board, score):
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j+1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j+1] = 0
                score += board[i][j]
    return board, score

# reverseBoards the board to mimic the right direction
def reverseBoard(board):
    new_board = []
    for i in range(4):
        new_board.append([])
        for j in range(4):
            new_board[i].append(board[i][3 - j])
    return new_board

# transposeBoards the board to mimic the up and down directions
def transposeBoard(board):
    new_board = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            new_board[i][j] = board[j][i]
    return new_board

# adds a random 2 or 4 tile to the board
def addRandomTile(board):
    row = random.randint(0, 3)
    col = random.randint(0, 3)
    while board[row][col] != 0:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
    board[row][col] = 2 if random.randint(1, 10) > 1 else 4
    return board

# move functions
def left(board, score):
    board = pushLeft(board)
    board, score = merge(board, score)
    board = pushLeft(board)

    return board, score

def right(board, score):
    board = reverseBoard(board)
    board = pushLeft(board)
    board, score = merge(board, score)
    board = pushLeft(board)
    board = reverseBoard(board)

    return board, score

def up(board, score):
    board = transposeBoard(board)
    board = pushLeft(board)
    board, score = merge(board, score)
    board = pushLeft(board)
    board = transposeBoard(board)
    
    return board, score

def down(board, score):
    board = transposeBoard(board)
    board = reverseBoard(board)
    board = pushLeft(board)
    board, score = merge(board, score)
    board = pushLeft(board)
    board = reverseBoard(board)
    board = transposeBoard(board)

    return board, score

# selects a random move, from the list of possible moves (is one is possible)
def randomMove(board):
    moveMade = False
    move_order = [down, left, up, right]
    while not moveMade and len(move_order) > 0:
        move_index = random.randint(0, len(move_order)-1)
        move = move_order[move_index]
        valid = validMove(board, move)
        if valid:
            return move, True
        move_order.pop(move_index)
    return None, False

#checks if a move has any impact on the board (is valid)
def validMove(board, move):
    newBoard, _ = move(board, 0)

    if board != newBoard:
        return True
    else:
        return False