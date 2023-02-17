
import esper
import tkinter as tk
import keyboard as kb

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
        self.x_pos = 0
        self.y_pos = 0

        # Kewarg processing
        if "world" in kwargs:
            self.name = kwargs["world"]
        elif "player" in kwargs:
            self.player = kwargs["player"]

        ## add test sprite
        self.sprite = tk.PhotoImage(file="assets/Tiles/LIL_DUDE.png")

        # add processors
        self.world.add_processor(self.Position(self.x_pos, self.y_pos, self.canvas, self.canvas.create_image(self.x_pos, self.y_pos, image=self.sprite)))

    def update(self):
        self.world.process()
        self.title("Alchemist: " + self.name)
        self.canvas.update()
        self.canvas.delete("all")
        
    def mainloop(self):
        while True:
            self.update()
    
    class Position(esper.Processor):
        def __init__(self, x_pos, y_pos, canvas, sprite):
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.canvas = canvas
            self.sprite = sprite
            
        def process(self):    
            right = kb.is_pressed("a")
            left = kb.is_pressed("d")
            up = kb.is_pressed("w")
            down = kb.is_pressed("s")
            if right:
                self.x_pos += 1
            elif left:
                self.x_pos -= 1
            elif up:
                self.y_pos -= 1
            elif down:
                self.y_pos += 1
            
