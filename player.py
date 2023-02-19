## player entity, components, and processors

from dataclasses import dataclass as component
import esper
import tkinter as tk
import keyboard as kb
import os

 v

# import player sprites
dirs = os.listdir("assets/player_sprites")
sprites = {}
for i in dirs:
    sprites[i] = tk.PhotoImage(file="assets/player_sprites/" + i)

# entities
@component
class player:
    pass

# components
@component
class position:
    x: int
    y: int

@component
class sprite:
    image: tk.PhotoImage

# processors

class move(esper.Processor):
    def __init__(self, canvas):
        self.canvas = canvas
        super().__init__()
    def process(self):
        for ent, (pos, sprite) in self.world.get_components(position, sprite):
            if kb.is_pressed("w"):
                pos.y -= 1
            if kb.is_pressed("a"):
                pos.x -= 1
            if kb.is_pressed("s"):
                pos.y += 1
            if kb.is_pressed("d"):
                pos.x += 1

class animate(esper.Processor):
    def __init__(self, canvas):
        self.canvas = canvas
        super().__init__()
    def process(self):
        for ent, (pos, sprite) in self.world.get_components(position, sprite):
            self.canvas.create_image(pos.x, pos.y, image=sprite.image)
