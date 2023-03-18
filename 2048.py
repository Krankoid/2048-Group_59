import random

# makes an empty board and sets running to true to start the game loop
board = [[0] * 4 for _ in range(4)]
running = True

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
    board = new_board

# merges like tiles by checking if the tile is equal to the tile to the right
def merge(board):
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j+1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j+1] = 0

# reverseBoards the board to mimic the right direction
def reverseBoard(board):
    new_board = []
    for i in range(4):
        new_board.append([])
        for j in range(4):
            new_board[i].append(board[i][3 - j])
    board = new_board

# transposeBoards the board to mimic the up and down directions
def transposeBoard(board):
    new_board = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            new_board[i][j] = board[j][i]
    board = new_board

# adds a random 2 or 4 tile to the board
def addRandomTile(board):
    row = random.randint(0, 3)
    col = random.randint(0, 3)
    while board[row][col] != 0:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
    board[row][col] = 2 if random.randint(1, 10) > 1 else 4

# move functions
def left(board):
    pushLeft(board)
    merge(board)
    pushLeft(board)
    addRandomTile(board)
    printBoard(board)

def right(board):
    reverseBoard(board)
    pushLeft(board)
    merge(board)
    pushLeft(board)
    reverseBoard(board)
    addRandomTile(board)
    printBoard(board)

def up(board):
    transposeBoard(board)
    pushLeft(board)
    merge(board)
    pushLeft(board)
    transposeBoard(board)
    addRandomTile(board)
    printBoard(board)
    end_game(board)

def down(board):
    transposeBoard(board)
    reverseBoard(board)
    pushLeft(board)
    merge(board)
    pushLeft(board)
    reverseBoard(board)
    transposeBoard(board)
    addRandomTile(board)
    printBoard(board)


def horizontal_move_possible(board):
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j+1]:
                return True
    return False

def vertical_move_possible(board):
    for i in range(3):
        for j in range(4):
            if board[i][j] == board[i+1][j]:
                return True
    return False

def end_game(board):
    if any(2048 in row for row in board):
        print("You win!")
        return True
    elif not any (0 in row for row in board) and not horizontal_move_possible(board) and not vertical_move_possible(board):
        print("You lose!")
        return True

initialize_game(board)
printBoard(board)
while running:
    if end_game(board):
        break
    print("Enter a move: left, right, up, down")
    move = input()
    match move:
        case "left":
            left(board)
        case "right":
            right(board)
        case "up":
            up(board)
        case "down":
            down(board)
        case "quit":
            running = False
    

    