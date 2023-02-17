
import esper
import tkinter as tk

class Engine(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__()
        self.geometry("800x600")
        self.canvas = tk.Canvas(self, width=800, height=600, bg="black")
        self.world = esper.World()
        self.canvas.pack()
        self.name = "world"
        self.player = None
        if "world" in kwargs:
            self.name = kwargs["world"]
        elif "player" in kwargs:
            self.player = kwargs["player"]

        
        self.title("Alchemist: " + self.name)

    def mainloop(self):
        self.world.process()
        super().mainloop()

