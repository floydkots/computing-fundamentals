"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player, moves=()):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    win = board.check_win()
    if win:
        return SCORES.get(win), (-1, -1)

    empty_squares = board.get_empty_squares()
    for row, col in empty_squares:
        next_board = board.clone()
        next_board.move(row, col, player)
        next_player = provided.switch_player(player)
        move = mm_move(next_board, next_player, [])
        current_score = move[0]
        current_move = (current_score, (row, col))
        if current_score == 1 and player is provided.PLAYERX:
            return current_move
        else:
            moves = list(moves)
            moves.append(current_move)

    assert len(moves) == len(empty_squares)
    best_move = max(moves) if player == provided.PLAYERX else min(moves)
    del moves[:]
    return best_move
    

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)


import poc_simpletest

def test_mm_move():
    ts = poc_simpletest.TestSuite()
    X = provided.PLAYERX
    O = provided.PLAYERO
    _ = provided.EMPTY
    
    state_1 = [[O, X, X],
               [O, X, _],
               [O, O, X]]
    board = provided.TTTBoard(len(state_1), False, state_1)
    ts.run_test(mm_move(board, X), (-1, (-1, -1)), "mm_move")
    
    state_2 = [[O, X, X],
               [O, X, O],
               [_, O, X]]
    board = provided.TTTBoard(len(state_2), False, state_2)
    ts.run_test(mm_move(board, X), (1, (2, 0)), "mm_move")
    
    state_3 = [[O, X, _],
               [O, X, _],
               [X, O, X]]
    board = provided.TTTBoard(len(state_3), False, state_3)
    ts.run_test(mm_move(board, O), (0, (0, 2)), "mm_move")
    
    state_4 = [[O, X, _],
               [O, X, _],
               [_, O, X]]
    board = provided.TTTBoard(len(state_4), False, state_4)
    ts.run_test(mm_move(board, X), (0, (2, 0)), "mm_move")
    
    ts.report_results()
    
test_mm_move()