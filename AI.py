import Game
from math import sqrt, log


# ######## AI ##########
def aiMove(board, rSims, searchLength):
    # List of possible first moves
    moves = [Game.down, Game.left, Game.up, Game.right]
    scores = [0] * 4
    totalRan = 0

    for i in range(4):
        # get next move in list
        currentMove = moves[i]
        # checks if move is valid before moving foreward
        if (Game.validMove(board, currentMove)):
            currentBoard, scores[i] = currentMove(board, 0)
            currentBoard = Game.addRandomTile(currentBoard)
            totalRan += 1
        else:
            continue
        # loops however many times specifies to run simluations
        for simulation in range(rSims):
            
            mNr = 1
            searchBoard = currentBoard.copy()
            valid = True
            # loop as long as there's a possible move, and the seach length hasn't been reached
            while valid and mNr < searchLength:
                
                #gets a random move, if possible
                move, valid = Game.randomMove(searchBoard)
                # if a move is found, play it and advance the board
                if valid:
                    searchBoard, scores[i] = move(searchBoard, scores[i])
                    searchBoard = Game.addRandomTile(searchBoard)

                    mNr +=1
        
    # calculates the UCB of each branch
    bestUCB = 0
    foundMove = False
    bestMove = Game.down
    totalRan *= rSims
    for i in range(4):
        if Game.validMove(board, moves[i]):
            UCB = ( scores[i] / rSims ) + sqrt((2 * log(totalRan)) /  rSims)
            if UCB >= bestUCB:
                foundMove = True
                bestMove = moves[i]
                bestUCB = UCB
    #return best move & if one was found
    print("Best move found by AI: " + bestMove.__name__)
    return bestMove, foundMove