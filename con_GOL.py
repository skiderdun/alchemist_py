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

############################################
#
#
#   The Species Class
#
#
############################################

# The Species class is a framework for creating objects.
# All objects are governed by a Species.
# Species are collections of components assigned to an ID.
# the species of any object can be determined by its ID.
# the properties of any object can be determined by its components.
# and its components can be determined by its species.
# The components include:
#  - properties such as color, enthalpy, entropy, etc.
#  - rules that govern the behavior of the object an how it interacts with other objects.

class Species:
    '''A Species is a collection of components assigned to an ID.
    The species of any object can be determined by its ID.
    The properties of any object can be determined by its components.
    And its components can be determined by its species.
    The components include:
        - properties such as color, enthalpy, entropy, etc.
        - rules that govern the behavior of the object an how it interacts with other objects.
    requires:
        id: int
            The ID of the Species.
        components: list
            A list of components that make up the Species.
        '''
    def __init__(self, id: int, components: list):
        self.id = id
        self.components = components


############################################
#
#
#   The Biome Class
#
#
############################################

# The Biome class is the foundation of the alchemy system.
# each object is governed by a Biome.
# the state of the Biome determines the state of the object.
class Biome:
    '''A Biome is a collection of rules that can be applied to a grid of cells.
    The rules are applied to each cell in the grid and the result is a new grid.
    The rules are applied in a loop until the grid is stable.
    Repeating the process will result in a new grid.
    requires:
        obj: int
            The object that the Biome is for.
        seed: numpy.ndarray
            The seed for the Biome.
        rules: list
            A list of rules that can be applied to the grid.
        size: int = 100
            The size of the grid.
        scale: int = 8
            The scale of the grid.
        '''
    def __init__(self, species: int, seed: npt.ArrayLike, rules: list, size: int = 100, scale: int = 8):
        self.species = species
        self.seed = seed
        self.rules = rules
        self.size = size
        self.scale = scale
        self.grid = np.zeros((size, size), dtype=np.uint8)
        
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if self.seed.shape[0] > x and self.seed.shape[1] > y:
                    self.grid[x,y] = self.seed[x,y]
                else:
                    self.grid[x,y] = 0
    def update(self):
        '''Update the grid.'''
        # create a copy of the grid
        new_grid = np.copy(self.grid)
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                # count the neighbours
                neighbours = 0
                for i in range(-1,2):
                    for j in range(-1,2):
                        if i == 0 and j == 0:
                            continue
                        if x+i < 0 or x+i >= self.grid.shape[0] or y+j < 0 or y+j >= self.grid.shape[1]:
                            continue
                        if self.grid[x+i,y+j] == 1 or self.grid[x+i,y+j] == 2:
                            neighbours += 1
                # apply the rules
                for rule in self.rules:
                    new_grid[x,y] = rule(self.grid[x,y], neighbours)

        return new_grid


############################################
#
#
#   Main
#
#
############################################

def main():
    # The rules are functions that are applied to the grid.
    # The rules are applied to each cell in the grid.
    # rule 1: Any live cell with fewer than two live neighbours dies, as if caused by under-population.
    rule_1 = lambda cell, neighbours: 0 if cell == 1 and neighbours < 2 else cell
    # rule 2: Any live cell with two or three live neighbours lives on to the next generation.
    rule_2 = lambda cell, neighbours: 1 if cell == 1 and (neighbours == 2 or neighbours == 3) else cell
    # rule 3: Any live cell with more than three live neighbours dies, as if by overcrowding.
    rule_3 = lambda cell, neighbours: 0 if cell == 1 and neighbours > 3 else cell
    # rule 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    rule_4 = lambda cell, neighbours: 1 if cell == 0 and neighbours == 3 else cell

    # test array: 
    test_seed = np.random.randint(0, 2, size=(5, 5))

    test = Biome(0, test_seed, [rule_1, rule_2, rule_3,rule_4], size=100, scale=8)


    # create a window
    window = pyglet.window.Window(width=800, height=800)
    batch = pyglet.graphics.Batch()

    # create a grid of squares
    squares = []
    for x in range(test.grid.shape[0]):
        for y in range(test.grid.shape[1]):
            squares.append(pyglet.shapes.Rectangle(x*test.scale, y*test.scale, test.scale, test.scale, color=(55, 55, 255), batch=batch))

    # update the grid
    def update(dt):
        test.grid = test.update()
        for x in range(test.grid.shape[0]):
            for y in range(test.grid.shape[1]):
                if test.grid[x,y] == 0:
                    squares[x+y*test.grid.shape[0]].color = (55, 55, 255)
                else:
                    squares[x+y*test.grid.shape[0]].color = (255, 55, 55)

    # draw the grid
    @window.event
    def on_draw():
        window.clear()
        batch.draw()

    # run the game
    pyglet.clock.schedule_interval(update, 1/10.0)
    pyglet.app.run()

if __name__ == '__main__':
    main()
