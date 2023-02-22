import pyglet
pyglet.options['debug_gl'] = False
import numpy as np
import numpy.typing as npt

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

# Performace notes:
# - use of functions rather than dict for lookup
# - use of numpy arrays for grid
# - abstract rules and neighbors to allow for different rulesets and neighbor counts
# - abstraction also allows for greater speed (no need to check for neighbors that don't exist)
# - use list comprehension for grid updates

############################################
#
#
#   Cell: Optimized for speed
#
#
############################################

class Biome():
    def __init__(self, grid: npt.NDArray[np.int8]):
        self.grid = grid

    def run(self, generations: int):
        for i in range(generations):
            self.grid = self._update(self.grid)
        
    def _update(self, grid: npt.NDArray[np.int8]) -> npt.NDArray[np.int8]:
        
        if np.sum(grid) == 0:
            return grid

        # get indices of all non-zero elements
        indices = np.argwhere(grid == 1)
   
        # get the surrounding indices
        surrounding_indices = np.array([indices + np.array([i, j]) for i in range(-1, 2) for j in range(-1, 2) if indices.shape[0] != 0])

        # colapse the array
        surrounding_indices = surrounding_indices.reshape(-1, 2)
      
        # remove the indices that are out of bounds
        surrounding_indices = surrounding_indices[(surrounding_indices[:, 0] >= 0) 
                                                & (surrounding_indices[:, 0] < grid.shape[0])
                                                & (surrounding_indices[:, 1] >= 0) 
                                                & (surrounding_indices[:, 1] < grid.shape[1])]

        # remove the indices that are the same as the original indices
        surrounding_indices = surrounding_indices[(surrounding_indices[:, 0] != indices[:, 0]) | (surrounding_indices[:, 1] != indices[:, 1])]

        # for each surrounding index that occures three times, set the biome to 1 
        for i in np.unique(surrounding_indices, axis=0):
            if np.sum(np.all(surrounding_indices == i, axis=1)) == 3:
                grid[i[0], i[1]] = 1
        
        # set indices that are not surrounded by 2 or 3 cells to 0
        for i in np.unique(indices, axis=0):
            if np.sum(np.all(surrounding_indices == i, axis=1)) not in [2, 3]:
                grid[i[0], i[1]] = 0

############################################
#
#
#   Main
#
#
############################################

def main():

    # create the window
    window = pyglet.window.Window(width=800, height=600, caption='Alchemy', resizable=True)
    batch = pyglet.graphics.Batch()

    # create the grid
    grid = np.zeros((100, 100), dtype=np.int8)

    # add a glider to center of grid
    grid[50, 50] = 1
    grid[51, 51] = 1
    grid[51, 52] = 1
    grid[50, 52] = 1
    grid[49, 52] = 1
    

    # create the biome
    biome = Biome(grid)

    # create the sprites
    green = pyglet.image.SolidColorImagePattern((0, 255, 0, 255)).create_image(10, 10)
    red = pyglet.image.SolidColorImagePattern((255, 0, 0, 255)).create_image(10, 10)
    
    sprites = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 1:
                sprites.append(pyglet.sprite.Sprite(green, x=i*10, y=j*10, batch=batch))
            else:
                sprites.append(pyglet.sprite.Sprite(red, x=i*10, y=j*10, batch=batch))
    
    # update the sprites
    def update(dt):
        biome.run(1)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[i, j] == 1:
                    sprites[i*grid.shape[0]+j].image = green
                else:
                    sprites[i*grid.shape[0]+j].image = red

    # draw the grid
    @window.event
    def on_draw():
        window.clear()
        batch.draw()

    # run the game
    pyglet.clock.schedule_interval(update, 1/5.0)
    pyglet.app.run()

if __name__ == '__main__':
    main()
