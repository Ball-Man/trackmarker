# Trackmarker
A timestamping tool for music, made in Python3.

## What and why
Trackmarker is a (partially) CLI tool, dead simple, that I use to generate json files containing timestamps for music. These timestamps are called *markers* and are divided into named *channels*.

The program let's you play a music file and insert your own markers by simply pressing *spacebar*.
It is then possible to export the json file (called metafile) and load it in any other software to map actions to those timestamps.

I personally use this software to time automated (music based) actions in my game.

## How to run
### By source
First of all, you'll need Python3 (>= 3.7).
Then, install the dependecies:
```bash
pip install -r requirements.txt
```

Finally, run the program:
```bash
python main.py
```

### By installing
Again, you'll need Python3 (>= 3.7).
Install with:
```bash
python setup.py install
```

Then run (from anywhere)
```bash
trackmarker
```

## How to use
The CLI interface will give you some help. Simply type `help` to get a list of available commands and `help example_command` to get help about the `example_command` command.

The basic workflow is:
Load a song you want to map with
```
ogg path/to/file.mp3
```

Then add a channel and record to it with
```
add channel_name

rec
```

Use `rec` a second time to stop the recording.

Once you open the program, you'll have two windows: the console window, and a self opened standard window (opengl window). When recording with `rec`, music will start playing and **the opengl window needs to be focused** for the program to correctly receive input.
When the correct window is in focus and the music is playing press:
 - `P` to pause/resume,
 - directional arrows (left, right) to rollback/fastforward,
 - `spacebar` to place a marker (if correctly received, the window will blink for a moment)

When done, save your metadata file (a simple json format) with
```
save path/to/metadata.json
```

## Overview of the commands
`help` - Get info about other commands<br/>
`ogg` - Load a music file<br/>
`load` - Load a json metafile<br/>
`save` - Save current state to a json metafile<br/>
`rec` - Start/stop recording to a channel<br/>
`add` - Add an empty channel<br/>
`del` - Remove a channel<br/>
`show` - Show current status (loaded music file, metadata file, current channels etc.)<br/>
`quit` - Exit the program (no automatic save)<br/>

## Additional dependencies
All the Python dependecies are listed into `requirements.txt`, but this doesn't mean that there may not be addional ones. Not all audio formats are supported. Stick to mp3 if you are on MS Windows and do not have [ffmpeg](https://www.ffmpeg.org/download.html) added to your `PATH` (for MS Windows, use the shared build).

If you're on \*nix, be sure to have gstreamer or ffmpeg installed (you probably already have them but you don't know it).

When ffmpeg is correctly installed, some of the supported formats are:
 - AU
 - MP2
 - MP3
 - OGG/Vorbis
 - WAV
 - WMA
