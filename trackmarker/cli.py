import os.path as op
import glob as gb
import cmd
import readline


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
                    err(f'Invalid numer of arguments: required {min_num}'
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
        return gb.glob(op.join(path, '*'))
    else:
        return gb.glob(path + '*')


def _parse_args(arg):
    """Split all the string arg into a list of args."""
    return arg.split()


class MainCMD(cmd.Cmd):
    """Main trackl editor CLI.

    Import object files (music or sounds) and tracks.
    """

    intro = ('Welcome to trackmarker.\n'
             'Type help or ? to list commands.')
    prompt = '> '

    def __init__(self):
        # Set readline (not available on windows)
        readline.set_completer_delims(' \t\n')

        # Init parent
        super().__init__()
