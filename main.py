## Alchemist: a 2D game with a sophisticated chemistry engine

## import modules
import os
import pyglet
from pyglet import app
from pyglet.window import Window

## create main window

def main():
    window = Window(1280, 780, caption="Alchemist")
    batch = pyglet.graphics.Batch()

    lil_dude = pyglet.resource.image("assets/player_sprites/LIL_DUDE.png")
    lil_dude.anchor_x = lil_dude.width // 2
    lil_dude.anchor_y = lil_dude.height // 2

    walk = []
    for spr in os.listdir("assets/player_sprites/walk"):
        if spr.endswith(".png"):
            walk.append(pyglet.resource.image("assets/player_sprites/walk/" + spr))
    walk_animation = pyglet.image.Animation.from_image_sequence(walk, 0.1, True)
    sprite = pyglet.sprite.Sprite(walk_animation, x=500, y=500, batch=batch)

    @window.event
    def on_draw():
        window.clear();
        batch.draw();
    app.run()


if __name__ == "__main__":
    main()

