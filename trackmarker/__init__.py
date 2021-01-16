"""A tool for music timestamps.

Load music tracks, and create a file populated with markers. Markers
are timestamps, and are divided into named channels.

The exported markers file (a json) can be used in games and other
software to map actions to specific moments in the song.
"""

import pyglet
import threading
import queue
import bisect
from . import cli

window = None
batch = None
rect = None
playback_rect = None
cmd = None


class TrackWindow(pyglet.window.Window):
    """A window used for user input (to add markers)."""
    channel = None
    track_file = None
    _track = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Queue of actions destinated to the main thread
        # (pyglet stuff basically)
        # An action is a triple: function, args, kwargs
        self.action_queue = queue.Queue()

        self._player = pyglet.media.Player()
        self._marker_index = 0

    def on_update(self, dt):
        if self.player.playing and self.channel is not None \
           and len(self.channel) > self._marker_index \
           and self._player.time >= self.channel[self._marker_index]:
            # Do not overlap
            if not rect.visible:
                playback_rect.visible = True
                pyglet.clock.schedule_once(
                    lambda dt: setattr(playback_rect, 'visible', False),
                    0.1)
            self._marker_index += 1

        while self.action_queue.qsize() > 0:
            action = self.action_queue.get()
            action[0](*action[1] if len(action) > 1 else [],
                      **action[2] if len(action) > 2 else {})

    def on_draw(self):
        window.clear()
        batch.draw()

    def on_key_press(self, symbol, mods):
        """"""
        if symbol == pyglet.window.key.SPACE and self.player.playing:
            # Create a mark
            bisect.insort(self.channel, self.player.time)
            rect.visible = True

        elif symbol == pyglet.window.key.P:
            if self.player.playing:
                self.player.pause()
            else:
                self.player.play()

    def on_key_release(self, symbol, mods):
        if symbol == pyglet.window.key.SPACE:
            rect.visible = False

    def on_close(self):
        """Terminate the whole program."""
        pass

    def stop_playback(self):
        """Stop current playback."""
        self.player.pause()

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._marker_index = 0
        self._player = value


def main():
    global window, batch, rect, playback_rect
    window = TrackWindow(vsync=False)
    batch = pyglet.graphics.Batch()

    rect = pyglet.shapes.Rectangle(0, 0, window.width, window.height,
                                   batch=batch,
                                   color=(0xdd, 0xdd, 0xdd))

    playback_rect = pyglet.shapes.Rectangle(0, 0, window.width, window.height,
                                            batch=batch,
                                            color=(0x05, 0x05, 0xbb))

    rect.visible = False
    playback_rect.visible = False

    # Init CLI
    cmd = cli.MainCMD(window)
    cli_thread = threading.Thread(target=cmd.cmdloop)
    cli_thread.start()

    # Init window
    pyglet.clock.schedule(window.on_update)
    pyglet.app.run()

    cli_thread.join()
