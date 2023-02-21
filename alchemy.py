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

# create a function to check the neighbors of a cell via list comprehension
def quarum_sense(grid: npt.NDArray[np.int8], x: int, y: int) -> int:
    return sum([grid[x-1, y-1], grid[x, y-1], grid[x+1, y-1],
                grid[x-1, y], grid[x+1, y],
                grid[x-1, y+1], grid[x, y+1], grid[x+1, y+1]])

# create function to apply the rules via list comprehension
def update_biome(grid: npt.NDArray[np.int8]) -> npt.NDArray[np.int8]:
    return np.array(
        [
        [
        1 if quarum_sense(grid, x, y)
        in [2, 3] else 0
        for x in range(1, grid.shape[0]-1)
        ]
        for y in range(1, grid.shape[1]-1)
        ]
    )



############################################
#
#
#   Main
#
#
############################################

def main():

    # test array: 
    test_seed = np.random.randint(0, 2, size=(10, 10))

    test = Biome(1, test_seed, Cell(test_seed).update, size=800, scale=8)


    # create a window
    window = pyglet.window.Window(width=800, height=800)
    batch = pyglet.graphics.Batch()

    # create a grid of squares
    squares = []
    for x in range(test.grid.shape[0]):
        for y in range(test.grid.shape[1]):
            squares.append(pyglet.shapes.Rectangle(x*test.scale, y*test.scale, test.scale, test.scale, color=(153, 184, 152), batch=batch))

    # update the grid
    def update(dt):
        test.grid = test.update()
        for x in range(test.grid.shape[0]):
            for y in range(test.grid.shape[1]):
                if test.grid[x,y] == 0:
                    squares[x+y*test.grid.shape[0]].color = (153, 184, 152)
                else:
                    squares[x+y*test.grid.shape[0]].color = (254, 206, 171)

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
