import os.path as op
import glob as gb
import cmd
import readline
import json

import pyglet


def err(string):
    """Print an error message."""
    print('*** %s' % string)


def require_params(min_num, max_num=None):
    """Return a decorator which checks for argument count
    Basically checks the number of passed arguments is in the range
    [min_num, max_num].
    If one argument is passed(min_num), an exact match will be required.
    """
    if max_num is None:     # Set max equal to min if not set
        max_num = min_num

    def decorator(function):
        """Decorator that checks for argument count."""

        def wrapper(self, arg):
            """Internal wrapper to encapsulate the original function."""
            args = arg.split()

            nonlocal min_num, max_num

            # Check for argument count
            if not (min_num <= len(args) <= max_num):
                if min_num == max_num:
                    err(f'Invalid numer of arguments: required {min_num} '
                        f'given {len(args)}')
                else:
                    err('Invalid number of arguments: required min '
                        f'{min_num}, max {max_num}, given {len(args)}')
                return False
            return function(self, arg)

        # Set proper docstring(based on the original function)
        wrapper.__doc__ = function.__doc__

        return wrapper
    return decorator


def _complete_path(path):
    """Autocompletion function for paths."""
    if op.isdir(path):
        ret = gb.glob(op.join(path, '*'))
    else:
        ret = gb.glob(path + '*')

    return tuple(p.replace('\\', '/') for p in ret)


def _parse_args(arg):
    """Split all the string arg into a list of args."""
    return arg.split()


class MainCMD(cmd.Cmd):
    """Main trackl editor CLI.

    Import track files (music or sounds) and markers.
    """

    intro = ('Welcome to trackmarker.\n'
             'Type help or ? to list commands.')
    prompt = '> '

    _track = None
    _track_file = None
    _loaded_file = None

    def __init__(self, window):
        # Set readline (not available on windows)
        readline.set_completer_delims(' \t\n')

        # Associated window
        self._window = window
        self._markers = {}

        # Init parent
        super().__init__()

    def do_quit(self, arg):
        """Exit the program."""
        print('Have a nice day.')
        self._window.action_queue.put((self._window.close,))
        return True

    def do_EOF(self, arg):
        """Exit the program."""
        return self.do_quit(arg)

    @require_params(1)
    def do_ogg(self, arg):
        """Select the current music track in memory."""
        arg = _parse_args(arg)[0]

        try:
            self._track = pyglet.media.StaticSource(pyglet.media.load(arg))
        except Exception as e:
            err(str(e))
            return

        self._track_file = arg

    @require_params(0, 1)
    def do_save(self, arg):
        """Save the current marker dictionary on file.

        If a parameter is given, use it as path for a new file.
        If no parameter is given, try saving in the last loaded/saved
        file.
        """
        args = _parse_args(arg)

        # Save to new location
        if args:
            try:
                with open(args[0], 'w') as file:
                    json.dump(self._markers, file)
            except IOError as e:
                err(str(e))
                return

            self._loaded_file = args[0]
        else:
            # Try saving in the last loaded/saved file
            if self._loaded_file is None:
                err('No file currently loaded, specify a filename.')
            else:
                try:
                    with open(self._loaded_file, 'w') as file:
                        json.dump(self._markers, file)
                except Exception as e:
                    err(str(e))

    @require_params(1)
    def do_load(self, arg):
        """Load from file the current markers.

        This will override the data currently in memory, if any.
        """
        arg = _parse_args(arg)[0]

        try:
            with open(arg) as file:
                self._markers = json.load(file)
        except Exception as e:
            err(str(e))
            return

        self._loaded_file = arg

    def do_show(self, arg):
        """Show current loaded data (music track and markers).

        If parameters are specified, only marker channels with those
        names will be shown.
        """
        args = _parse_args(arg)

        # Show currently loaded files
        playing = '(playing)' if self._window.player.playing else ''
        print(f'Ogg track: {self._track_file} {playing}')
        print(f'Markers file: {self._loaded_file}')

        print('Markers:')
        # Show markers
        # All markers if no argument is given
        if not args:
            print(self._markers)
        else:
            for a in args:
                if a in self._markers:
                    print(f'{a}: {self._markers[a]}')
                else:
                    err(f'Could not find marker {a}')

    @require_params(1)
    def do_add(self, arg):
        """Add a marker channel, specifying its name."""
        arg = _parse_args(arg)[0]

        if arg in self._markers:
            err(f'Channel {arg} already exists.')
            return

        self._markers[arg] = []

    @require_params(1)
    def do_del(self, arg):
        """Delete a marker channel, specifying its name."""
        arg = _parse_args(arg)[0]

        if arg not in self._markers:
            err(f'Channel {arg} doesn\'t exist.')
            return

        del self._markers[arg]

    @require_params(0, 1)
    def do_rec(self, arg):
        """Start/stop recording on a channel (this start the track).

        Only one channel at a time is supported. If used while the track
        is playing, the track will be stopped.
        """
        args = _parse_args(arg)

        if self._track is None:
            err('No track loaded, please load one with "ogg filename"')
            return

        if args:
            if self._window.player.playing:
                # Stop playback
                self._window.action_queue.put((self._window.stop_playback,))
            else:
                # Set marker channel
                self.do_add(args[0])

                def play():
                    self._window.channel = self._markers[args[0]]
                    # Track playback
                    self._window.player = self._track.play()

                self._window.action_queue.put((play,))
        else:
            if self._window.player.playing:
                # Stop playback
                self._window.action_queue.put((self._window.stop_playback,))
            else:
                err('Specify a channel name to record to.')

    # Autocompletion
    def complete_ogg(self, text, line, start_idx, end_idx):
        """Autocompletion for the ogg command."""
        return _complete_path(text)

    def complete_save(self, text, line, start_idx, end_idx):
        """Autocompletion for the save command."""
        return _complete_path(text)

    def complete_load(self, text, line, start_idx, end_idx):
        """Autocompletion for the load command."""
        return _complete_path(text)
