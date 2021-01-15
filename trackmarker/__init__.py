"""A tool for music timestamps.

Load music tracks, and create a file populated with markers. Markers
are timestamps, and are divided into named channels.

The exported markers file (a json) can be used in games and other
software to map actions to specific moments in the song.
"""

import pyglet
import threading
from . import cli

window = None
batch = None


class TrackWindow(pyglet.window.Window):
    """A window used for user input (to add markers)."""
    channel = None
    track_file = None
    _track = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = pyglet.media.Player()
        self._play = False

    def play_later(self):
        self._play = True

    def on_draw(self):
        batch.draw()

    def on_key_press(self, symbol, mods):
        """"""
        if symbol == pyglet.window.key.SPACE:
            # Create a mark
            self.channel.append(self.player.time)


def main():
    global window, batch
    window = TrackWindow()
    batch = pyglet.graphics.Batch()

    rect = pyglet.shapes.Rectangle(0, 0, window.width, window.height,
                                   batch=batch,
                                   color=(0xff, 0xff, 0xff))
    rect.visible = False

    # Init CLI
    cmd = cli.MainCMD(window)
    threading.Thread(target=cmd.cmdloop).start()

    # Init window
    pyglet.clock.schedule(lambda dt: None)
    pyglet.app.run()
