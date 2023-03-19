import random
import math

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
    return board

# move functions
def left(board, score):
    board = pushLeft(board)
    board, score = merge(board, score)
    board = pushLeft(board)
    # addRandomTile(board)
    # printBoard(board)
    
    #print(score)
    #isValid= horizontal_move_possible(board)
    #end_game(board)
    return board, score

def right(board, score):
    board = reverseBoard(board)
    board = pushLeft(board)
    board, score = merge(board, score)
    board = pushLeft(board)
    board = reverseBoard(board)
    # addRandomTile(board)
    # printBoard(board)
    
    #print(score)
    #end_game(board)
    return board, score

def up(board, score):
    board = transposeBoard(board)
    board = pushLeft(board)
    board, score = merge(board, score)
    board = pushLeft(board)
    board = transposeBoard(board)
 
    
    # addRandomTile(board)
    # printBoard(board)  
    #print(score)
    #end_game(board)
    return board, score


def down(board, score):
    board = transposeBoard(board)
    board = reverseBoard(board)
    board = pushLeft(board)
    board, score = merge(board, score)
    board = pushLeft(board)
    board = reverseBoard(board)
    board = transposeBoard(board)
    # addRandomTile(board)
    # printBoard(board)
    
    #print(score)
    #end_game(board)
    return board, score

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

    print("no valid move found")
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
    newBoard, _ = move(board, 0)

    if board != newBoard:
        return True
    else:
        return False


# ######## AI ##########
def aiMove(board, rSims, searchLength):
    moves = [down, left, up, right]
    scores = [0] * 4
    nRan = [0] * 4

    for i in range(4):
        currentMove = moves[i]
        if (validMove(board, currentMove)):
            currentBoard, scores[i] = currentMove(board, 0)
            currentBoard = addRandomTile(currentBoard)
        else:
            continue
            
        for simulation in range(rSims):
            mNr = 1
            searchBoard = currentBoard.copy()
            valid = True

            while valid and mNr < searchLength:

                move, valid = randomMove(board)
                
                if valid:
                    newBoard, scores[i] = move(board, 0)
                    searchBoard = newBoard

                    searchBoard = addRandomTile(searchBoard)
                    mNr +=1
            
            nRan[i] += mNr
        
        

                

    nTotal = sum(nRan)
    bestUCB = 0
    foundMove = False
    for i in range(4):
        UCB = ( scores[i] / rSims ) + math.sqrt((2 * math.log(nTotal)) /  rSims)
        if UCB > bestUCB and validMove(board, moves[i]):
            foundMove = True
            bestMove = moves[i]
            bestUCB = UCB

    print("Best move found by AI: " + bestMove.__name__)
    return bestMove, foundMove
    #boardFinal, finalScore  = bestMove(board, currentScore)
    #return boardFinal, finalScore, (validMove(board, currentMove))

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
        
        
        print("AI recommends:" )
        aiMove(board, 20, 30)
        
        match move:
            #make a move and store results
            case "l":
                move = left
                
            case "r":
                move = right
            
            case "u":
                move = up

            case "d":
                move = down

            case "quit":
                running = False
            
            case default:
                print("please enter a valid move")
                continue
        

        valid = validMove(board, move)

        if (valid): 
            newBoard, score = move(board, score)
            board = newBoard
            board = addRandomTile(board)
            printBoard(board)
        else:
            print("not valid move")
            #not valid here


if choice == "a":
    while running:
        if end_game(board):
            break
        print()
        
        move, valid = aiMove(board, 100, 50)

        if not valid:
            running = False
            print("AI game over")
        else:
            newBoard, score = move(board, score)
            board = newBoard
            board = addRandomTile(board)


            printBoard(board)
            print()
            print("\nScore:"+ str(score))

        
            
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
                
        