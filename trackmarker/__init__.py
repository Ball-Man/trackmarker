import pyglet
import threading
from . import cli

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

    # Init CLI
    cmd = cli.MainCMD(window)
    threading.Thread(target=cmd.cmdloop).start()

    # Init window
    pyglet.app.run()
