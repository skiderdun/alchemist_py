
## World Object
# The World object is the main object of the game. It contains all the
# information about the game world, including the player, the map, the
# items, the monsters, and the game state. The World object is responsible
# for updating the game state, and for drawing the game world to the
# screen.


import debug
import render as r

import esper   # Entity-Component-System


world = esper.World()


## player entity
player = world.create_entity()
## player sprite component
player_sprite = r.SpriteComponent("assets/Tiles/LIL_DUDE.png")
world.add_component(player, player_sprite)
world.add_processor(r.RendererSystem(world))



## main loop
while True:
    world.process()
    r.main_window.update()
