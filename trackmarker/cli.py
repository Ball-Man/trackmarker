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

    _loaded_track = None
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
        self._window.close()
        return True

    def do_EOF(self, arg):
        """Exit the program."""
        return self.do_quit(arg)

    @require_params(1)
    def do_ogg(self, arg):
        """Select the current music track in memory."""
        arg = _parse_args(arg)[0]

        try:
            self._loaded_track = pyglet.resource.media(arg, False)
        except Exception as e:
            err(str(e))

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
                except IOError as e:
                    err(str(e))

    # Autocompletion
    def complete_ogg(self, text, line, start_idx, end_idx):
        """Autocompletion for the ogg command."""
        return _complete_path(text)
