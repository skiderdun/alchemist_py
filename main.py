## Alchemist: a 2D game with a sophisticated chemistry engine

import debug
import tkinter as tk
from engine import Engine

## create main window

def main():
    world = Engine()
    world.mainloop()

if __name__ == "__main__":
    main()

