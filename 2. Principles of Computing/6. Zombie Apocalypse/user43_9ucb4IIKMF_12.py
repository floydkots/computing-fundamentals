"""
Author: Floyd Kots ~ github.com/floydkots
Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)      
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        return (zombie for zombie in self._zombie_list)

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        return (human for human in self._human_list)
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        height = self.get_grid_height()
        width = self.get_grid_width()
        visited = poc_grid.Grid(height, width)
        boundary = poc_queue.Queue()
        distance_field = [[height * width for _ in range(width)]\
                          for _ in range(height)]
        
        
        if entity_type is ZOMBIE:
            for zombie in self.zombies():
                distance_field[zombie[0]][zombie[1]] = 0
                visited.set_full(*zombie)
                boundary.enqueue(tuple(zombie))
        elif entity_type is HUMAN:
            for human in self.humans():
                distance_field[human[0]][human[1]] = 0
                visited.set_full(*human)
                boundary.enqueue(tuple(human))
        
        while len(boundary) > 0:
            entity = boundary.dequeue()
            for row, col in self.four_neighbors(*entity):
                if visited.is_empty(row, col) and self.is_empty(row, col):
                    visited.set_full(row, col)
                    boundary.enqueue((row, col))
                    distance = distance_field[entity[0]][entity[1]] + 1
                    if distance < distance_field[row][col]:
                        if self.is_empty(row, col):
                            distance_field[row][col] = distance
                        else:
                            distance_field[row][col] = height * width                    
        return distance_field        
    
    def distance_tuple(self, entity, distance_field):
        """
        Get the distance and entity in one tuple in the
        form (distance, entity)
        """
        return (distance_field[entity[0]][entity[1]], entity)
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        zdf = zombie_distance_field
        for human in list(self.humans()):
            print human
            neighbors = self.eight_neighbors(*human)
            distances = map(lambda x: (zdf[x[0]][x[1]], x),
                            neighbors)
            distances = filter(lambda x: self.is_empty(*x[1]) and x[0], distances)
            print distances
            best_move = max(distances)[1] if distances else None
            if best_move:
                self._human_list.remove(human)
                self.add_human(*best_move)
            
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        hdf = human_distance_field
        for zombie in list(self.zombies()):
            if hdf[zombie[0]][zombie[1]] == 0:
                continue
            neighbors = self.four_neighbors(*zombie)
            distances = map(lambda x: (hdf[x[0]][x[1]], x),
                            neighbors)
            distances = filter(lambda x: self.is_empty(*x[1]), distances)
            best_move = min(distances)[1] if distances else None
            if best_move:
                self._zombie_list.remove(zombie)
                self.add_zombie(*best_move)

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
