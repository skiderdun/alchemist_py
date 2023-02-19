
import esper
import tkinter as tk
import keyboard as kb
from dataclasses import dataclass as component
import math

class Engine(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__()
        self.geometry("800x600")
        self.canvas = tk.Canvas(self, width=600, height=800, bg="black", scrollregion=(-1000, -1000, 1000, 1000))
        self.world = esper.World()
        self.canvas.pack(fill=tk.BOTH, expand=True)
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
        

        ## add test sprite
        self.sprite = tk.PhotoImage(file="assets/player_sprites/LIL_DUDE.png")

        # add processors
        
    def update(self):
        self.world.process()
        self.title("Alchemist: " + self.name)
        self.canvas.update()
        self.canvas.delete("all")
        
    def mainloop(self):
        while True:
            self.update()
    

