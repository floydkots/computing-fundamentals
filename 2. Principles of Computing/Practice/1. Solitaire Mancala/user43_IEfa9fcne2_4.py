"""
Floyd Kots ~ github.com/floydkots

Student facing implementation of solitaire version of Mancala - Tchoukaillon

Goal: Move as many seeds from given houses into the store

In GUI, you make ask computer AI to make move or click to attempt a legal move
"""


class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """
    
    def __init__(self):
        """
        Create Mancala game with empty store and no houses
        """
        self._board = [0]
    
    def set_board(self, configuration):
        """
        Take the list configuration of initial number of seeds for given houses
        house zero corresponds to the store and is on right
        houses are number in ascending order from right to left
        """
        self._board = list(configuration)
    
    def __str__(self):
        """
        Return string representation for Mancala board
        """
        board = list(self._board)
        board.reverse()
        return str(board)
    
    def get_num_seeds(self, house_num):
        """
        Return the number of seeds in given house on board
        """
        return self._board[house_num]

    def is_game_won(self):
        """
        Check to see if all houses but house zero are empty
        """
        for house_num in range(1, len(self._board)):
            if self.get_num_seeds(house_num) > 0:
                return False
        return True
    
    def is_legal_move(self, house_num):
        """
        Check whether a given move is legal
        """
        return house_num > 0 and self.get_num_seeds(house_num) == house_num 

    
    def apply_move(self, house_num):
        """
        Move all of the stones from house to lower/left houses
        Last seed must be played in the store (house zero)
        """
        if self.is_legal_move(house_num):
            seeds = self.get_num_seeds(house_num)
            self._board[seeds] = 0
            while seeds > 0:
                seeds -= 1
                self._board[seeds] += 1
        return self

    def choose_move(self):
        """
        Return the house for the next shortest legal move
        Shortest means legal move from house closest to store
        Note that using a longer legal move would make smaller illegal
        If no legal move, return house zero
        """
        for house_num in range(1, len(self._board)):
            if self.is_legal_move(house_num):
                return house_num
        return 0
    
    def plan_moves(self):
        """
        Return a sequence (list) of legal moves based on the following heuristic: 
        After each move, move the seeds in the house closest to the store 
        when given a choice of legal moves
        Not used in GUI version, only for machine testing
        """
        moves = []
        temp_board = list(self._board)
        temp_game = SolitaireMancala()
        temp_game.set_board(temp_board)
        while temp_game.choose_move():
            moves.append(temp_game.choose_move())
            temp_game.apply_move(temp_game.choose_move())
        return moves
 


# Create tests to check the correctness of your code

def test_mancala():
    """
    Test code for Solitaire Mancala
    """
    
    my_game = SolitaireMancala()
    print "Testing init - Computed:", my_game, "Expected: [0]"
    
    config1 = [0, 0, 1, 1, 3, 5, 0]    
    my_game.set_board(config1)   
    
    print "Testing set_board - Computed:", str(my_game), "Expected:", str([0, 5, 3, 1, 1, 0, 0])
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(1), "Expected:", config1[1]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(3), "Expected:", config1[3]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(5), "Expected:", config1[5]
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(5), "Expected:", True
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(0), "Expected:", False
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(2), "Expected:", False
    print "Testing apply_move - Computed:", my_game.apply_move(5), "Expected:", str([0, 0, 4, 2, 2, 1, 1])
    print "Testing apply_move - Computed:", my_game.apply_move(1), "Expected:", str([0, 0, 4, 2, 2, 0, 2])
    print "Testing apply_move - Computed:", my_game.apply_move(2), "Expected:", str([0, 0, 4, 2, 0, 1, 3])
    print "Testing apply_move - Computed:", my_game.apply_move(2), "Expected:", str([0, 0, 4, 2, 0, 1, 3])
    print "Testing choose_move - Computed:", my_game.choose_move(), "Expected:", 1
    print "Testing apply_move - Computed:", my_game.apply_move(1), "Expected:", str([0, 0, 4, 2, 0, 0, 4])
    print "Testing choose_move - Computed:", my_game.choose_move(), "Expected:", 4
    print "Testing apply_move - Computed:", my_game.apply_move(4), "Expected:", str([0, 0, 0, 3, 1, 1, 5])
    print "Testing apply_move - Computed:", my_game.apply_move(3), "Expected:", str([0, 0, 0, 0, 2, 2, 6])
    print "Testing apply_move - Computed:", my_game.apply_move(2), "Expected:", str([0, 0, 0, 0, 0, 3, 7])
    print "Testing choose_move - Computed:", my_game.choose_move(), "Expected:", 0

    config2 = [0, 1, 0, 0, 0, 0, 0]    
    my_game.set_board(config2) 
    print "\n\n"
    print "Testing is_game_won - Computed:", my_game.is_game_won(), "Expected:", False
    print "Testing choose_move - Computed:", my_game.choose_move(), "Expected", 1
    print "Testing apply_move - Computed:", my_game.apply_move(1), "Expected", str([0, 0, 0, 0, 0, 0, 1])
    print "Testing is_game_won - Computed:", my_game.is_game_won(), "Expected:", True
    
    config2 = [0, 1, 0, 0, 0, 0, 0]    
    my_game.set_board(config2) 
    print "\n\n"
    print "Testing plan_moves - Computed:", my_game.plan_moves(), "Expected:", str([1])
    
    config1 = [0, 0, 1, 1, 3, 5, 0]    
    my_game.set_board(config1)  
    print "\n\n"
    print "Testing plan_moves - Computed:", my_game.plan_moves(), "Expected:", str([5, 1, 2, 1, 4, 1, 3, 1, 2, 1])
    
    
test_mancala()


# Import GUI code once you feel your code is correct
import poc_mancala_gui
poc_mancala_gui.run_gui(SolitaireMancala())
