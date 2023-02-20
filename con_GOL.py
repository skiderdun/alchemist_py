import pyglet
pyglet.options['debug_gl'] = False
import numpy as np

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

# create a grid of 0's and 1's
# 0 = dead
# 1 = alive
# 2 = dead but was alive
# 3 = alive but was dead
grid = np.zeros((100,100), dtype=np.uint8)

# create a glider
grid[1,3] = 1
grid[2,1] = 1
grid[2,3] = 1
grid[3,2] = 1
grid[3,3] = 1

# add rules
def rules(grid):
    # create a copy of the grid
    new_grid = np.copy(grid)
    # loop through every cell
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            # count the neighbours
            neighbours = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    if i == 0 and j == 0:
                        continue
                    if x+i < 0 or x+i >= grid.shape[0] or y+j < 0 or y+j >= grid.shape[1]:
                        continue
                    if grid[x+i,y+j] == 1 or grid[x+i,y+j] == 2:
                        neighbours += 1
            # apply the rules
            if grid[x,y] == 1 or grid[x,y] == 2:
                if neighbours < 2 or neighbours > 3:
                    new_grid[x,y] = 2
            else:
                if neighbours == 3:
                    new_grid[x,y] = 3
    # update the grid
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if new_grid[x,y] == 2:
                new_grid[x,y] = 0
            if new_grid[x,y] == 3:
                new_grid[x,y] = 1
    return new_grid

# create a window
window = pyglet.window.Window(width=800, height=800)
batch = pyglet.graphics.Batch()

# create a grid of squares
squares = []

for x in range(grid.shape[0]):
    for y in range(grid.shape[1]):
        squares.append(pyglet.shapes.Rectangle(x*8, y*8, 8, 8, color=(55, 55, 255), batch=batch))

# update the grid
def update(dt):
    global grid
    grid = rules(grid)
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x,y] == 1:
                squares[x*grid.shape[0]+y].color = (255, 255, 255)
            else:
                squares[x*grid.shape[0]+y].color = (55, 55, 255)

# draw the grid
@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.clock.schedule_interval(update, 1/10.0)
pyglet.app.run()