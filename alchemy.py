import pyglet
pyglet.options['debug_gl'] = False
import numpy as np
import numpy.typing as npt
import cProfile

# Connway's Game of Life
# http://en.wikipedia.org/wiki/Conway's_Game_of_Life

# The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, 
# each of which is in one of two possible states, alive or dead. Every cell interacts with its eight neighbours,
# which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time,
# the following transitions occur:
# Any live cell with fewer than two live neighbours dies, as if caused by under-population.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overcrowding.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

# The initial pattern constitutes the seed of the system.
# The first generation is created by applying the above rules simultaneously to every cell in the seed-births and deaths occur simultaneously,
# and the discrete moment at which this happens is sometimes called a tick (in other words, each generation is a pure function of the preceding one).
# The rules continue to be applied repeatedly to create further generations.

# The Game of Life is Turing complete and can simulate a universal constructor or any other Turing machine.

########################################################################################
#
#
#   The Alchemy System
#
#
########################################################################################


############################################
#
#
#   Cell: A class for creating and storing cells
#
#
############################################
# a cell is a 2d array of 0s and 1s
# it is a premade cellular automata
# each cell is a seed which may be applied to a grid which is applied to a biome
class Cell():
    def __init__(self, grid: npt.NDArray[np.int8]):
        self.grid = grid

    def __repr__(self):
        return str(self.grid)

    def apply(self, grid: npt.NDArray[np.int8], x: int, y: int) -> npt.NDArray[np.int8]:
        """Apply the cell to the grid at the given x and y coordinates"""
        grid[x:x+self.grid.shape[0], y:y+self.grid.shape[1]] = self.grid
        return grid


############################################
#
#
#   Biome: Optimized for speed
#
#
############################################

# the game of life
# https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
# a biome governs an indevidual grid

class Biome():
    def __init__(self, grid: npt.NDArray[np.int8]):
        self.grid = grid
        self.val_grid = np.zeros(grid.shape, dtype=np.int8)

    def __repr__(self):
        return str(self.grid)
    
    def run(self, generations: int):
        for i in range(generations):
            self.grid = self._update(self.grid)
        
    def _update(self, grid: npt.NDArray[np.int8]) -> npt.NDArray[np.int8]:
        
        if np.sum(grid) == 0:
            return grid

        # get indices of all non-zero elements
        indices = np.argwhere(grid == 1)
   
        # get the surrounding indices
        surrounding_indices = np.array([[x + i, y + j] for x, y in indices for i in range(-1, 2) for j in range(-1, 2) if not (i == 0 and j == 0) ])
      
        # remove the indices that are out of bounds
        surrounding_indices = surrounding_indices[(surrounding_indices[:, 0] >= 0) 
                                                & (surrounding_indices[:, 0] < grid.shape[0])
                                                & (surrounding_indices[:, 1] >= 0) 
                                                & (surrounding_indices[:, 1] < grid.shape[1])]

        # for each surrounding index that occures three times, set the biome to 1
        # for each surrounding index that occures three times, set the biome to 1
        for i in np.unique(surrounding_indices, axis=0):
            if np.sum(np.all(surrounding_indices == i, axis=1)) == 3:
                grid[i[0], i[1]] = 1
            elif grid[i[0], i[1]] == 1 and np.sum(np.all(surrounding_indices == i, axis=1)) == 2:
                grid[i[0], i[1]] = 1
            else:
                grid[i[0], i[1]] = 0
        
        return grid
    
    def values(self, grid: npt.NDArray[np.int8]) -> npt.NDArray[np.int8]:
        # get indices of all non-zero elements
        indices = np.argwhere(grid == 1)
   
        # get the surrounding indices
        surrounding_indices = np.array([[x + i, y + j] for x, y in indices for i in range(-1, 2) for j in range(-1, 2) if not (i == 0 and j == 0) ])
      
        # remove the indices that are out of bounds
        surrounding_indices = surrounding_indices[(surrounding_indices[:, 0] >= 0) 
                                                & (surrounding_indices[:, 0] < grid.shape[0])
                                                & (surrounding_indices[:, 1] >= 0) 
                                                & (surrounding_indices[:, 1] < grid.shape[1])]
        
        val_grid = grid.copy()

        for i in np.unique(surrounding_indices, axis=0):
            val_grid[i[0], i[1]] = np.sum(np.all(surrounding_indices == i, axis=1))
        
        return val_grid

