## renderer system

import tkinter as tk
from dataclasses import dataclass as component
import esper

## main window
main_window = tk.Tk()
main_window.title("Alchemist")
main_window.geometry("800x600")

## canvas
canvas = tk.Canvas(main_window, width=800, height=600)
canvas.pack()


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
            canvas.create_image(0, 0, anchor=tk.NW, image=img)
            