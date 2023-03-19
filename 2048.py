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

# move functions
def left(board, score):
    board_copy = [row[:] for row in board]
    board = pushLeft(board)
    board, score = merge(board, score)
    board = pushLeft(board)
    isValid = board_copy != board and horizontal_move_possible(board)
    addRandomTile(board)
    # printBoard(board)
    
    #print(score)
    #isValid= horizontal_move_possible(board)
    #end_game(board)
    return board, score, isValid

def right(board, score):
    board_copy = [row[:] for row in board]
    board = reverseBoard(board)
    board = pushLeft(board)
    board, score = merge(board, score)
    board = pushLeft(board)
    board = reverseBoard(board)
    isValid = board_copy != board
    addRandomTile(board)
    # printBoard(board)
    
    #print(score)
    #end_game(board)
    return board, score, isValid

def up(board, score):
    board_copy = [row[:] for row in board]

    board = transposeBoard(board)
    board = pushLeft(board)
    board, score = merge(board, score)
    board = pushLeft(board)
    board = transposeBoard(board)
    isValid = board_copy != board 
 
    
    addRandomTile(board)
    # printBoard(board)  
    #print(score)
    #end_game(board)
    return board, score, isValid


def down(board, score):
    board_copy = [row[:] for row in board]
    board = transposeBoard(board)
    board = reverseBoard(board)
    board = pushLeft(board)
    board, score = merge(mergeBoard, score)
    board = pushLeft(mergeBoard)
    board = reverseBoard(board)
    board = transposeBoard(board)
    addRandomTile(board)
    # printBoard(board)

    #print(score)
    #end_game(board)
    return board, score, isValid

def randomMove(board):
    moveMade = False
    move_order = [right, up, down, left]
    while not moveMade and len(move_order) > 0:
        move_index = random.randint(0, len(move_order)-1)
        move = move_order[move_index]
        valid = validMove(board, move)
        if valid:
            score += scoreChange
            return move, True
        move_order.pop(move_index)
    return move_order[0], False

def horizontal_move_possible(board):
    for i in range(4):
        for j in range(3):
            if board[i][j] != 0 and board[i][j] == board[i][j+1]:
                return True
    return False

def vertical_move_possible(board):
    for i in range(3):
        for j in range(4):
            if board[i][j] != 0 and board[i][j] == board[i+1][j]:
                return True
    return False

def end_game(board):
    if any(2048 in row for row in board):
        print("You win!")
        return True
    elif not any (0 in row for row in board) and not horizontal_move_possible(board) and not vertical_move_possible(board):
        print("You lose!")
        return True
    
def validMove(board, move):
    newBoard = board.copy()
    newBoard, _, _ = move(board, 0)

    if board != newBoard:
        return True
    else:
        return False

# ######## AI ##########
def aiMove(board, searchesPerMove, searchLength, currentScore):
    firstMoves = [down, left, up, right]
    scores = [currentScore] * 4

    for i in range(4):
        firstMove = firstMoves[i]
        firstBoard, firstScore, firstValid = firstMove(board, 0)

        if firstValid:
            firstBoard = addRandomTile(firstBoard)
            scores[i] += firstScore
        else:
            continue
        for m in range(searchesPerMove):
            mNr = 1
            searchBoard = board.copy()
            valid = True

            while valid and mNr < searchLength:
                
                move, valid = randomMove(board)
                if valid:
                    newBoard, scoreChange, _ = move(board, 0)
                    searchBoard = newBoard
                    scores[i] += scoreChange

                    searchBoard = addRandomTile(searchBoard)
                    mNr +=1

    bestMoveIndex = scores.index(max(scores))
    bestMove = firstMoves[bestMoveIndex]
    print("Best move found by AI: " + bestMove.__name__)
    boardFinal, finalScore, validPos  = bestMove(board, currentScore)
    return boardFinal, finalScore, validPos

########### GAME LOGIC ###########

print("Do you want to play or watch the AI play? [p/a]")
choice = input()


initialize_game(board)
printBoard(board)
score = 0
if choice == "p":
    while running:
        if end_game(board):
            break
        print()
        print("Enter a move: l, r, u, d")
        move = input()
        
        match move:
            #make a move and store results
            case "l":
                valid = validMove(board, left)
                if (valid): 
                    #make move here (left)
                    newBoard, scoreChange, _ = left(board, score)
                    board = newBoard
                    score += scoreChange
                else:
                    print("not valid move")
                    #not valid here
            case "r":
                valid, scoreChange = validMove(board, right)

                newBoard,scoreChange, isValid = right(board, score)
            case "u":
                valid, scoreChange = validMove(board, up)

                newBoard, scoreChange, isValid = up(board, score)
            case "d":
                valid, scoreChange = validMove(board, down)
                
                newBoard, scoreChange, isValid = down(board, score)
            case "quit":
                running = False


if choice == "a":
    while running:
        if end_game(board):
            break
        print()
        
        board, score, validPos = aiMove(board, 20, 30, score)

        printBoard(board)
        print()
        print("\nScore:"+ str(score))

        if (not validPos): 
            running = False
            print("AI game over")
            
        # match move:
        #     case "l":
        #         board, score, isValid = left(board, score)
        #     case "r":
        #         board,score, isValid = right(board, score)
        #     case "u":
        #         board, score, isValid = up(board, score)
        #     case "d":
        #         board, score, isValid = down(board, score)
        #     case "quit":
                
        