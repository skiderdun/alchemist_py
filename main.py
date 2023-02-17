## Alchemist: a 2D game with a sophisticated chemistry engine

import debug
import tkinter as tk
import world

## print LIL_DUDE.png to screen

def main():
    main_window = tk.Tk()
    main_window.title("Alchemist")
    main_window.geometry("800x600")
    
    canvas = tk.Canvas(main_window, width=800, height=600)
    canvas.pack()

    # draw LIL_DUDE.png to screen
    img = tk.PhotoImage(file="assets/Tiles/LIL_DUDE.png")
    canvas.create_image(0, 0, anchor=tk.NW, image=img)

    main_window.mainloop()

if __name__ == "__main__":
    main()

