
import esper
import tkinter as tk
import keyboard as kb
from dataclasses import dataclass as component
import math

class Engine(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__()
        self.geometry("800x600")
        self.canvas = tk.Canvas(self, width=800, height=600, bg="black")
        self.world = esper.World()
        self.canvas.pack()
        self.name = "world"
        self.player = None
        self.title("Alchemist: " + self.name)

        # Kewarg processing
        if "world" in kwargs:
            self.name = kwargs["world"]
        elif "player" in kwargs:
            self.player = kwargs["player"]

        # add entities
        self.player = self.world.create_entity(self.player)
        
        # new components
        @component
        class Position(object):
            x: float = 100
            y: float = 100

        ## add test sprite
        self.sprite = tk.PhotoImage(file="assets/Tiles/LIL_DUDE.png")

        # add processors
        self.world.add_processor(self.PlayerPosition(Position, self.canvas, self.sprite))
        
    def update(self):
        self.world.process()
        self.title("Alchemist: " + self.name)
        self.canvas.update()
        self.canvas.delete("all")
        
    def mainloop(self):
        while True:
            self.update()
    
    class PlayerPosition(esper.Processor):
        def __init__(self, position , canvas, sprite):
            self.x = position.x
            self.y = position.y
            self.canvas = canvas
            self.sprite = sprite
            
        def process(self):    
            right = kb.is_pressed("a")
            left = kb.is_pressed("d")
            up = kb.is_pressed("w")
            down = kb.is_pressed("s")
            if right:
                self.x -= 1
            elif left:
                self.x += 1
            elif up:
                self.y -= 1
            elif down:
                self.y += 1
            self.canvas.create_image(self.x, self.y, image=self.sprite)
