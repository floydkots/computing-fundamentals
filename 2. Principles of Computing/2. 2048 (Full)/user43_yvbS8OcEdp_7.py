"""
Clone of 2048 game.
"""
import random
import poc_2048_gui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def sum_tiles(line):
    """
    Sums adjacent tiles of equal value
    """
    for index, _ in enumerate(line):
        if index + 1 < len(line) and line[index] == line[index+1]:
            line[index] += line[index + 1]
            line[index + 1] = 0
    return line

def slide_tiles(line):
    """
    Slides tiles to the left
    """
    slid = []
    for tile in line:
        if tile:
            slid.append(tile)
    slid += [0 for _ in range(len(line) - len(slid))]
    return slid

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """ 
    return slide_tiles(sum_tiles(slide_tiles(line)))



class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        self._initial_tiles = self._get_initial_tiles()
        
        
    def _get_initial_tiles(self):
        """
        Compute the indices of the initial tiles in the 4 directions
        """
        _up = [(0, col) for col in range(self.get_grid_width())]
        _down = [(self.get_grid_height() - 1, col) for col in range(self.get_grid_width())]
        _left = [(row, 0) for row in range(self.get_grid_height())]
        _right = [(col, self.get_grid_width() - 1) for col in range(self.get_grid_height())]
        return {UP: _up, DOWN: _down, LEFT: _left, RIGHT: _right}
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0] * self.get_grid_width() for _ in range(self.get_grid_height())]
        for _ in range(2):
            self.new_tile()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        
        return "\n".join(str(line) for line in self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        if direction == 1 or direction == 2:
            steps = self.get_grid_height()
        elif direction == 3 or direction == 4:
            steps = self.get_grid_width()
            
        offset = OFFSETS[direction]
        changed = False
        
        for initial_tile in self._initial_tiles[direction]:
            line = self.get_line(initial_tile, offset, steps)
            merged = merge(line)
            if self.set_line(initial_tile, offset, steps, merged):
                changed = True
        if changed:
            self.new_tile()
            
    def traversal_points(self, initial, offset, steps):
        """
        Get list of points to be traversed
        """
        points = []
        for step in range(steps):
            row = initial[0] + step * offset[0]
            col = initial[1] + step * offset[1] 
            points.append((row, col))
        return points
            
    def get_line(self, initial, offset, steps):
        """
        Gets the values of the tiles in a line
        """
        temp_list = []
        for point in self.traversal_points(initial, offset, steps):
            temp_list.append(self.get_tile(point[0], point[1]))
        return temp_list
                         
                         
    def set_line(self, initial, offset, steps, values):
        """
        Sets the values of tiles in a line
        """
        changed = False
        for index, point in enumerate(self.traversal_points(initial, offset, steps)):
            if self.get_tile(point[0], point[1]) != values[index]:
                changed = True
            self.set_tile(point[0], point[1], values[index]) 
        return changed

    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        values = [2] * 9 + [4] * 1
        done = False
        while not done:
            row = random.randint(0, self.get_grid_height() - 1)
            col = random.randint(0, self.get_grid_width() - 1)
            if not self._grid[row][col]:
                self._grid[row][col] = random.choice(values)
                done = True

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

    

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
