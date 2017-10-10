"""
Author: Floyd Kots ~ github.com/floydkots
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
# do not change their names.
NTRIALS = 10000    # Number of trials to run
SCORE_CURRENT = 3.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    Plays a game on the given board, starting with the
    given player.
    """
    empty_squares = board.get_empty_squares()
    random.shuffle(empty_squares)
    for row, col in empty_squares:
        if not board.check_win():
            board.move(row, col, player)
            player = provided.switch_player(player)
    

def mc_update_scores(scores, board, player):
    """
    Scores the completed board and updates the scores grid.
    """
    game = board.check_win()
    other = provided.switch_player(player)
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if game == provided.DRAW:
                scores[row][col] += 0
            elif game is player:
                if board.square(row, col) is player:
                    scores[row][col] += SCORE_CURRENT
                elif board.square(row, col) is other:
                    scores[row][col] -= SCORE_OTHER
                else:
                    scores[row][col] += 0
            elif game is other:
                if board.square(row, col) is other:
                    scores[row][col] += SCORE_OTHER
                elif board.square(row, col) is player:
                    scores[row][col] -= SCORE_CURRENT
                else:
                    scores[row][col] += 0
            else:
                scores[row][col] += 0
    
    

def get_best_move(board, scores):
    """
    Finds and returns the best move
    """
    
    empty_squares = board.get_empty_squares()
#    print "BOARD"
#    print board
#    print "SCORES"
#    for one, two, three in scores:
#        print "% 4.1f" % one, "% 4.1f" % two, "% 4.1f" % three
#
#    print "EMPTY SQUARES", empty_squares
    if empty_squares:
        tops = []
        top = scores[empty_squares[0][0]][empty_squares[0][1]]
        for row, col in empty_squares:
            if scores[row][col] >= top:
                top = scores[row][col]
        for row, col in empty_squares:
            if scores[row][col] == top:
                tops.append((row, col))
#        print "TOPS", tops
#        print top
#        print len(tops)
        best_move = random.choice(tops)
#        print "BEST MOVE", best_move
        return best_move
    return None
        

def mc_move(board, player, trials):
    """
    Uses Monte Carlo simulation to return a move for the
    machine player
    """
    best_moves = {}
    temp_board = board.clone()
    scores = [[0] * temp_board.get_dim() for _ in range(temp_board.get_dim())]
    for _ in range(trials):
        mc_trial(temp_board, player)
        mc_update_scores(scores, temp_board, player)
        best_move = get_best_move(board, scores)
        if best_move in best_moves.keys():
            best_moves[best_move] += 1
        else:
            best_moves[best_move] = 0
    bests = best_moves.items()
    bests.sort(key=lambda x: x[1])
    return bests[-1][0]
        
        
    


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
#print get_best_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO], [provided.PLAYERO, provided.PLAYERX, provided.PLAYERX], [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]), [[3, 2, 5], [8, 2, 8], [4, 0, 2]])
#print get_best_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.EMPTY, provided.EMPTY]]), [[-3, 6, -2], [8, 0, -3], [3, -2, -4]])
#print mc_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]), provided.PLAYERX, NTRIALS) 