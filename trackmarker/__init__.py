import pyglet

window = None
batch = None

track_dict = {}


def on_draw():
    batch.draw()


def on_key_press(symbol, mods):
    """"""
    pass


def main():
    global window, batch
    window = pyglet.window.Window()
    batch = pyglet.graphics.Batch()

    rect = pyglet.shapes.Rectangle(0, 0, window.width, window.height,
                                   batch=batch,
                                   color=(0xff, 0xff, 0xff))
    rect.visible = False

    window.set_handlers(on_draw, on_key_press)

    pyglet.app.run()
