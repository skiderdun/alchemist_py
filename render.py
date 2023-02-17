## renderer system
## 1. render the scene

import tkinter as tk
from dataclasses import dataclass as component
import esper

@component
class SpriteComponent:
    def __init__(self, image):
        self.image = image

class RendererSystem(esper.Processor):
    def __init__(self, canvas):
        self.canvas = canvas

    def process(self):
        for ent, sprite in self.world.get_component(SpriteComponent):
            img = tk.PhotoImage(file=sprite.image)
            tk.Canvas.create_image(0, 0, anchor=tk.NW, image=img)