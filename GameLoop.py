import Game
import AI

########### GAME LOOP ###########

# makes an empty board and sets running to true to start the game loop
board = [[0] * 4 for _ in range(4)]
running = True

print("Do you want to play or watch the AI play? [p/a]")
choice = input()

# initializes the game
Game.initialize_game(board)
Game.printBoard(board)
score = 0

#player game loop
if choice == "p":
    while running:

        print()
        print("Enter a move: l, r, u, d")
        move = input()
                
        #find and store the choosen move
        match move:
            case "l":
                move = Game.left
                
            case "r":
                move = Game.right
            
            case "u":
                move = Game.up

            case "d":
                move = Game.down

            case "quit":
                running = False
            
            case default:
                print("please enter a valid move")
                continue
        
        # check if game is valid, if so perform the move
        valid = Game.validMove(board, move)
        if (valid): 
            newBoard, score = move(board, score)
            newBoard = Game.addRandomTile(newBoard)
            board = newBoard
            Game.printBoard(board)
            # checks if the goal is reached
            if 2048 in board:
                print("you win!")
                running = False
        else:
            print("not valid move")
            # not valid here


if choice == "a":
    while running:
        move, valid = AI.aiMove(board, 50, 50)

        # checks if the AI found a valid move in the board
        if not valid:
            running = False
            print("AI game over")
        # makes the move if a valid one was found
        else:
            newBoard, score = move(board, score)
            board = newBoard
            board = Game.addRandomTile(board)

            Game.printBoard(board)
            print()
            print("\nScore:"+ str(score))
            # checks if the goal is reached
            if 2048 in board:
                print("you win!")
                running = False

    print()        
        
        