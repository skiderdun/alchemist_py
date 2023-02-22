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

    def sense_quarum(self, x: int, y: int) -> int:
        return sum([self.grid[x-1, y-1], self.grid[x, y-1], self.grid[x+1, y-1],
                    self.grid[x-1, y], self.grid[x+1, y],
                    self.grid[x-1, y+1], self.grid[x, y+1], self.grid[x+1, y+1]])

    def get_alive_cells(self) -> npt.NDArray[np.int8]:
        return np.array(np.where(self.grid == 1)).T

    def get_neighbor_indices(self) -> npt.NDArray[np.int8]:
        alive_cells = self.get_alive_cells()
        neighbor_indices = np.array(
            [
            [alive_cells[:, 0]-1, alive_cells[:, 1]-1],
            [alive_cells[:, 0], alive_cells[:, 1]-1],
            [alive_cells[:, 0]+1, alive_cells[:, 1]-1],
            [alive_cells[:, 0]-1, alive_cells[:, 1]],
            [alive_cells[:, 0]+1, alive_cells[:, 1]],
            [alive_cells[:, 0]-1, alive_cells[:, 1]+1],
            [alive_cells[:, 0], alive_cells[:, 1]+1],
            [alive_cells[:, 0]+1, alive_cells[:, 1]+1]
            ]
        ).T
        return neighbor_indices

    def apply_rules(self) -> npt.NDArray[np.int8]:
        neighbor_indices = self.get_neighbor_indices()
        neighbor_indices = neighbor_indices.reshape(-1, 2)
        neighbor_indices = np.unique(neighbor_indices, axis=0)
        neighbor_indices = neighbor_indices[
            (neighbor_indices[:, 0] >= 0) &
            (neighbor_indices[:, 0] < self.grid.shape[0]) &
            (neighbor_indices[:, 1] >= 0) &
            (neighbor_indices[:, 1] < self.grid.shape[1])
        ]
        neighbor_counts = np.zeros(self.grid.shape, dtype=np.int8)
        for i in range(neighbor_indices.shape[0]):
            neighbor_counts[neighbor_indices[i, 0], neighbor_indices[i, 1]] = \
                self.sense_quarum(neighbor_indices[i, 0], neighbor_indices[i, 1])
        return np.where(
            (neighbor_counts == 3) |
            (neighbor_counts == 2) & (self.grid == 1),
            1, 0
        )
    
    def run(self, n: int) -> None:
        for i in range(n):
            self.grid = self.apply_rules()



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
