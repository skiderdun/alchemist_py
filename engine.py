
import esper
import tkinter as tk

class Engine(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alchemist")
        self.geometry("800x600")
        self.canvas = tk.Canvas(self, width=800, height=600, bg="black", border=0, borderwidth=0)
        self.canvas.pack()
        self.world = esper.World()
        self.player = self.world.create_entity()

    def mainloop(self):
        self.world.process()
        super().mainloop()
